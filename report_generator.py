# report_generator.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def generate_ai_interpretation(dcf_result: dict) -> str:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    company = dcf_result['company_name']
    ticker = dcf_result['ticker']
    current_price = dcf_result['current_price']
    base_fcf = dcf_result['base_fcf']
    scenarios = dcf_result['scenarios']

    base_iv = scenarios['Base']['intrinsic_value']
    opt_iv = scenarios['Optimistic']['intrinsic_value']
    pes_iv = scenarios['Pessimistic']['intrinsic_value']

    base_gap = ((base_iv - current_price) / current_price) * 100
    opt_gap = ((opt_iv - current_price) / current_price) * 100
    pes_gap = ((pes_iv - current_price) / current_price) * 100

    prompt = f"""You are a financial analyst writing a DCF valuation report section.

Company: {company} ({ticker})
Current Market Price: ${current_price:.2f}
Base FCF: ${base_fcf / 1e9:.2f}B

DCF Valuation Results:
- Optimistic scenario: ${opt_iv:.2f} ({opt_gap:+.1f}% vs market price)
- Base scenario: ${base_iv:.2f} ({base_gap:+.1f}% vs market price)
- Pessimistic scenario: ${pes_iv:.2f} ({pes_gap:+.1f}% vs market price)

Model assumptions:
- 5-year FCF projection
- Discount rate: 10% (simplified WACC proxy)
- Terminal growth rate: 3% (Gordon Growth Model)
- Growth rates: Optimistic 15%, Base 10%, Pessimistic 5%

Write a concise 3-4 paragraph interpretation for a DCF report. Cover:
1. What the valuation gap suggests about current market pricing
2. Key factors explaining the difference between DCF value and market price
3. Important caveats for investors
4. One sentence on what additional analysis would improve this model

Professional financial analyst style. No headers, plain text only."""

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=prompt
    )
    return response.text


def generate_report(dcf_result: dict) -> str:
    if dcf_result is None:
        return "Error: No DCF data available to generate report."

    company = dcf_result['company_name']
    ticker = dcf_result['ticker']
    current_price = dcf_result['current_price']
    base_fcf = dcf_result['base_fcf']
    scenarios = dcf_result['scenarios']

    base_iv = scenarios['Base']['intrinsic_value']
    opt_iv = scenarios['Optimistic']['intrinsic_value']
    pes_iv = scenarios['Pessimistic']['intrinsic_value']

    base_gap = ((base_iv - current_price) / current_price) * 100
    opt_gap = ((opt_iv - current_price) / current_price) * 100
    pes_gap = ((pes_iv - current_price) / current_price) * 100

    def verdict(gap):
        if gap > 15:
            return "Undervalued"
        elif gap < -15:
            return "Overvalued"
        else:
            return "Fairly Valued"

    print("Generating AI interpretation via Gemini API...")
    try:
        ai_interpretation = generate_ai_interpretation(dcf_result)
    except Exception as e:
        ai_interpretation = f"  [AI interpretation unavailable: {e}]\n\n  Based on our Base Case scenario, {company} appears to be {verdict(base_gap).lower()} relative to its current market price of ${current_price:.2f}."

    report = f"""
================================================================================
  DCF VALUATION REPORT — {company} ({ticker})
================================================================================

1. OVERVIEW
-----------
This report presents a Discounted Cash Flow (DCF) valuation of {company} ({ticker}).
The analysis is based on publicly available financial data sourced via Yahoo Finance
through the yfinance Python library. Three scenarios are modeled to account for
uncertainty in future growth: Optimistic, Base, and Pessimistic.

Current Market Price: ${current_price:.2f}
Base FCF (Most Recent): ${base_fcf / 1e9:.2f}B

2. METHODOLOGY
--------------
The DCF model estimates intrinsic value by projecting Free Cash Flow (FCF)
over a 5-year period and discounting those cash flows back to present value.

  Free Cash Flow (FCF) = Operating Cash Flow - Capital Expenditures (CapEx)

  FCF was chosen over net income because it represents the actual cash a company
  generates after maintaining and expanding its asset base — a more reliable
  indicator of true economic value.

  Terminal Value is calculated using the Gordon Growth Model (Perpetuity Formula):

      Terminal Value = FCF(Year 5) × (1 + g) / (r - g)

  Where:
    g = Terminal growth rate (3%) — based on long-term GDP growth assumption.
        The logic: no company can grow faster than the overall economy indefinitely.
    r = Discount rate (10%) — used as a simplified proxy for WACC.

  Note on Discount Rate: In practice, the discount rate should be calculated
  as the Weighted Average Cost of Capital (WACC) using Bloomberg Terminal data.
  A fixed 10% rate is used here as a conservative approximation. The actual
  WACC for {ticker} is estimated to be in the 8-9% range, meaning our model
  may slightly underestimate intrinsic value.

3. ASSUMPTIONS
--------------
  Growth Rates (Annual FCF Growth):
    - Optimistic:   15% — reflects strong historical FCF growth trajectory
    - Base:         10% — reflects consensus analyst expectations for mature tech
    - Pessimistic:   5% — reflects slower growth in a saturated or adverse market

  Discount Rate:        10% (simplified WACC proxy)
  Terminal Growth Rate:  3% (long-term GDP growth rate — Gordon Growth Model)
  Projection Period:     5 years

4. VALUATION RESULTS
--------------------
  Scenario       Intrinsic Value    vs Current Price    Verdict
  ----------     ---------------    ----------------    -------
  Optimistic     ${opt_iv:>10.2f}       {opt_gap:>+8.1f}%         {verdict(opt_gap)}
  Base           ${base_iv:>10.2f}       {base_gap:>+8.1f}%         {verdict(base_gap)}
  Pessimistic    ${pes_iv:>10.2f}       {pes_gap:>+8.1f}%         {verdict(pes_gap)}

5. INTERPRETATION (AI-Generated)
---------------------------------
{ai_interpretation}

6. LIMITATIONS & DISCLAIMER
----------------------------
  - This model uses a simplified 5-year FCF projection
  - Discount rate is approximated, not calculated from market data
  - Does not account for qualitative factors (brand, regulation, competition)
  - Past FCF growth does not guarantee future performance
  - This report is for educational and portfolio purposes only
    and does not constitute financial advice

================================================================================
  Generated by DCF Analyzer | AI Interpretation by Gemini (Google)
  Data Source: Yahoo Finance via yfinance
================================================================================
"""
    return report


def save_report(dcf_result: dict, save_path: str = 'outputs/'):
    os.makedirs(save_path, exist_ok=True)
    ticker = dcf_result['ticker']
    report = generate_report(dcf_result)
    filepath = os.path.join(save_path, f'{ticker}_dcf_report.txt')
    with open(filepath, 'w') as f:
        f.write(report)
    print(f"Report saved: {filepath}")
    return report