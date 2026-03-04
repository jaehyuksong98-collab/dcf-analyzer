DCF Analyzer — Automated Valuation Tool
An automated Discounted Cash Flow (DCF) valuation tool that fetches real-time financial data, runs multi-scenario analysis, and publishes reports to GitHub and Notion via n8n workflow automation.

Features

Automated Data Fetching — Pulls live financial statements from Yahoo Finance using yfinance
Multi-Scenario DCF Model — Calculates intrinsic value under Optimistic, Base, and Pessimistic assumptions
AI-Powered Interpretation — Generates natural language analysis using Google Gemini API
Visualization — Outputs DCF waterfall charts and scenario comparison graphs
Automated Publishing — Sends reports to GitHub and Notion automatically via n8n webhooks


Tech Stack
LayerToolsFinancial ModelingPython, yfinance, pandasAI AnalysisGoogle Gemini APIVisualizationmatplotlibAutomationn8n (webhook → GitHub + Notion)Version ControlGitHubDocumentationNotion

How It Works
python3 main.py
      ↓
Enter ticker (e.g. AAPL)
      ↓
Fetch financial statements (yfinance)
      ↓
Run DCF model (3 scenarios)
      ↓
Generate AI interpretation (Gemini)
      ↓
Save chart + report locally
      ↓
POST to n8n webhook
      ↓
├── GitHub: Auto-commit report to /outputs
└── Notion: Create new page with full report

DCF Model Overview
The model projects Free Cash Flow (FCF) over a 5-year period under three scenarios:
ScenarioGrowth AssumptionOptimisticHigh revenue growth, expanding marginsBaseConsensus estimates, stable marginsPessimisticConservative growth, margin compression
Key inputs: Revenue, Operating Income, D&A, CapEx, Working Capital changes
Discount rate: WACC estimated from market data
Terminal value: Gordon Growth Model

Sample Output
==================================================
  Microsoft Corporation (MSFT)
==================================================
  Current Price:  $392.74
  Scenario       Intrinsic Value        Gap
  ----------------------------------------
  Optimistic          $501.23      +27.6%  Undervalued
  Base                $418.90       +6.7%  Undervalued
  Pessimistic         $331.45      -15.6%  Overvalued
==================================================

Setup
bash# Clone the repo
git clone https://github.com/jaehyuksong98-collab/dcf-analyzer.git
cd dcf-analyzer

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add environment variables
echo "GEMINI_API_KEY=your_key_here" > .env

# Run
python3 main.py

Project Structure
dcf-analyzer/
├── main.py              # Entry point
├── dcf_analyzer.py      # Core DCF calculation logic
├── report_generator.py  # AI report generation (Gemini)
├── visualizer.py        # Chart generation
├── requirements.txt
└── outputs/             # Generated reports and charts

Automation Architecture
Reports are automatically deployed via n8n workflow:

Python script sends POST request to n8n webhook
n8n parses ticker and report data
Simultaneously commits report to GitHub and creates Notion page

This eliminates manual publishing steps and ensures every analysis is version-controlled and documented.

Built as part of a personal finance & automation portfolio project.
