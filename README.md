# DCF Analyzer — Automated Valuation Tool

An automated Discounted Cash Flow (DCF) valuation tool that fetches real-time financial data, runs multi-scenario analysis, and publishes reports to GitHub and Notion via n8n workflow automation.

---

## Features

- **Automated Data Fetching** — Pulls live financial statements from Yahoo Finance using `yfinance`
- **Multi-Scenario DCF Model** — Calculates intrinsic value under Optimistic, Base, and Pessimistic assumptions
- **AI-Powered Interpretation** — Generates natural language analysis using Google Gemini API
- **Visualization** — Outputs DCF waterfall charts and scenario comparison graphs
- **Automated Publishing** — Sends reports to GitHub and Notion automatically via n8n webhooks

---

## Tech Stack

| Layer | Tools |
|---|---|
| Financial Modeling | Python, yfinance, pandas |
| AI Analysis | Google Gemini API |
| Visualization | matplotlib |
| Automation | n8n (webhook → GitHub + Notion) |
| Version Control | GitHub |
| Documentation | Notion |

---

## How It Works
```
python3 main.py → Enter ticker → Fetch financial statements → Run DCF (3 scenarios) → AI interpretation → Save locally → POST to n8n webhook → GitHub commit + Notion page
```

---

## DCF Model Overview

| Scenario | Growth Assumption |
|---|---|
| Optimistic | High revenue growth, expanding margins |
| Base | Consensus estimates, stable margins |
| Pessimistic | Conservative growth, margin compression |

- **Key inputs:** Revenue, Operating Income, D&A, CapEx, Working Capital  
- **Discount rate:** WACC estimated from market data  
- **Terminal value:** Gordon Growth Model

---

## Setup
```bash
git clone https://github.com/jaehyuksong98-collab/dcf-analyzer.git
cd dcf-analyzer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_key_here" > .env
python3 main.py
```

---

## Project Structure
```
dcf-analyzer/
├── main.py              # Entry point
├── dcf_analyzer.py      # Core DCF logic
├── report_generator.py  # AI report (Gemini)
├── visualizer.py        # Chart generation
├── requirements.txt
└── outputs/             # Reports and charts
```

---

*Built as part of a personal finance & automation portfolio project.*
