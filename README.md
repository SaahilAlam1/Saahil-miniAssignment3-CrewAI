# CrewAI Business Analysis Crew

## Business Problem
This project analyzes whether a startup should launch a subscription-based healthy meal kit service for young professionals in Bengaluru, India in Q3. The objective is to combine market insights and financial logic into a practical launch recommendation.

## How the 3 Agents Work Together
The crew runs in a sequential pipeline. First, the Market Research Specialist collects customer, trend, and competitor evidence. Second, the Business Financial Analyst uses that research to build assumptions, estimate month-12 outcomes, and evaluate break-even risk. Third, the Strategy Report Writer combines both prior outputs into a founder-facing decision memo with recommendation, KPI dashboard, and a 90-day action plan.

## Challenges and How They Were Solved
- **Challenge:** Ensuring each agent had a clearly distinct function instead of overlapping analysis.
  - **Solution:** I defined role-specific goals and strict task outputs so each handoff is explicit and measurable.
- **Challenge:** Making task dependencies unambiguous for grading.
  - **Solution:** Task 2 is explicitly linked to Task 1 context, and Task 3 depends on both Task 1 and Task 2 outputs.
- **Challenge:** Capturing execution evidence for submission.
  - **Solution:** The script is run with shell redirection so verbose agent traces and final output are saved to `output.txt`.

## One Thing I Would Change with More Time
I would add tools and data sources (for example, web research and spreadsheet-style calculations) so the agents can cite fresher market numbers and produce scenario-based financial models (base, best, worst) with stronger confidence.

## How to Run
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env`, then add your API key (do not commit `.env`):
   ```bash
   cp .env.example .env
   ```
   ```env
   DEEPSEEK_API_KEY=your_key_here
   DEEPSEEK_MODEL=deepseek-chat
   DEEPSEEK_API_BASE=https://api.deepseek.com
   ```
4. Run and capture logs:
   ```bash
   python crew.py > output.txt 2>&1
   ```
