import os
from datetime import datetime

from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv


def build_agents(llm):
    """Create 3 business analysis agents with distinct roles."""
    market_researcher = Agent(
        role="Market Research Specialist",
        goal=(
            "Identify at least 5 current, evidence-based market insights about "
            "the target customer segment and 3 key competitors for the business case."
        ),
        backstory=(
            "You are a former management consultant who spent 7 years building market "
            "entry briefs for consumer startups. You always prioritize facts, segment "
            "clarity, and concise evidence over generic opinions. You write in a way "
            "that business leaders can act on immediately."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    financial_analyst = Agent(
        role="Business Financial Analyst",
        goal=(
            "Build a practical 12-month financial snapshot with revenue assumptions, "
            "cost drivers, break-even estimate, and 3 quantified risks."
        ),
        backstory=(
            "You are a startup finance advisor with deep experience in unit economics, "
            "pricing, and scenario planning. You focus on transparent assumptions and "
            "simple models that non-finance stakeholders can verify."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    strategy_writer = Agent(
        role="Strategy Report Writer",
        goal=(
            "Deliver a decision-ready strategy memo with clear recommendations, "
            "prioritized actions, and measurable next steps."
        ),
        backstory=(
            "You are a business communications lead who turns complex analysis into "
            "clear executive reports. You connect evidence to decisions and make sure "
            "every recommendation includes rationale and an action owner."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    return market_researcher, financial_analyst, strategy_writer


def build_tasks(market_researcher, financial_analyst, strategy_writer):
    """Create 3 dependent tasks for sequential execution."""
    task_1 = Task(
        description=(
            "{topic}\n\n"
            "Task: Research the market opportunity.\n"
            "Include customer pain points, segment size indicators, demand trends, and "
            "a competitor scan (minimum 3 direct or indirect competitors)."
        ),
        expected_output=(
            "A markdown report with exactly 4 sections:\n"
            "1) Customer Segments\n"
            "2) Market Trends (at least 5 bullet insights)\n"
            "3) Competitor Snapshot (table with name, offering, pricing, strength, weakness)\n"
            "4) Opportunity Gaps"
        ),
        agent=market_researcher,
    )

    task_2 = Task(
        description=(
            "Using the market findings from Task 1, build a compact financial analysis.\n"
            "Estimate revenue assumptions, cost buckets, a simple month-12 outlook, "
            "break-even logic, and key risks with mitigations."
        ),
        expected_output=(
            "A markdown analysis with:\n"
            "- Assumptions table (price, customer count, retention/churn, major costs)\n"
            "- Month-12 revenue and gross margin estimate\n"
            "- Break-even estimate (units or subscribers)\n"
            "- Top 3 financial risks + mitigation actions"
        ),
        agent=financial_analyst,
        context=[task_1],
    )

    task_3 = Task(
        description=(
            "Use Task 1 and Task 2 outputs to produce a final decision memo for the founders.\n"
            "Provide a launch recommendation, rationale, phased action plan, and KPIs."
        ),
        expected_output=(
            "A final strategy memo with exactly these sections:\n"
            "1) Executive Recommendation (Go / No-Go / Conditional Go)\n"
            "2) Why This Decision (evidence from market + financial analysis)\n"
            "3) 90-Day Action Plan (prioritized)\n"
            "4) KPI Dashboard (at least 5 metrics)\n"
            "5) Key Risks and Contingencies"
        ),
        agent=strategy_writer,
        context=[task_1, task_2],
    )

    return [task_1, task_2, task_3]


def main():
    load_dotenv()

    if not os.getenv("DEEPSEEK_API_KEY"):
        raise ValueError(
            "DEEPSEEK_API_KEY not found. Add it to a local .env file before running."
        )

    llm = LLM(
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        base_url=os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )

    agents = build_agents(llm)
    tasks = build_tasks(*agents)

    crew = Crew(
        agents=list(agents),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    print("\n=== CrewAI Business Analysis Run ===")
    print(f"Started at: {datetime.now().isoformat(timespec='seconds')}\n")
    result = crew.kickoff(
        inputs={
            "topic": (
                "A startup is planning to launch a subscription-based healthy meal kit "
                "service for young professionals in Bengaluru, India. The founders need "
                "a business analysis to decide whether to launch in Q3 this year."
            )
        }
    )
    print("\n=== Final Result ===\n")
    print(result)


if __name__ == "__main__":
    main()
