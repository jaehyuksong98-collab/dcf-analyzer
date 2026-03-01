import yfinance as yf
import pandas as pd
import numpy as np

def get_financial_data(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info
    cashflow = stock.cashflow
    balance_sheet = stock.balance_sheet
    return stock, info, cashflow, balance_sheet

def calculate_dcf(ticker: str,
                  growth_optimistic: float = 0.15,
                  growth_base: float = 0.10,
                  growth_pessimistic: float = 0.05,
                  discount_rate: float = 0.10,
                  terminal_growth: float = 0.03,
                  years: int = 5):
    stock, info, cashflow, balance_sheet = get_financial_data(ticker)
    try:
        operating_cf = cashflow.loc['Operating Cash Flow'].iloc[0]
        capex = cashflow.loc['Capital Expenditure'].iloc[0]
        fcf = operating_cf + capex
    except Exception as e:
        print(f"FCF data error: {e}")
        return None
    shares_outstanding = info.get('sharesOutstanding', 1)
    current_price = info.get('currentPrice', 0)
    company_name = info.get('longName', ticker)
    scenarios = {
        'Optimistic': growth_optimistic,
        'Base': growth_base,
        'Pessimistic': growth_pessimistic
    }
    results = {}
    for scenario, growth_rate in scenarios.items():
        current_fcf = fcf
        projected_fcf = []
        for year in range(1, years + 1):
            current_fcf = current_fcf * (1 + growth_rate)
            projected_fcf.append(current_fcf)
        pv_fcf = [cf / ((1 + discount_rate) ** (i + 1))
                  for i, cf in enumerate(projected_fcf)]
        terminal_value = projected_fcf[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
        pv_terminal = terminal_value / ((1 + discount_rate) ** years)
        enterprise_value = sum(pv_fcf) + pv_terminal
        intrinsic_value = enterprise_value / shares_outstanding
        results[scenario] = {
            'intrinsic_value': intrinsic_value,
            'projected_fcf': projected_fcf,
            'pv_fcf': pv_fcf,
            'pv_terminal': pv_terminal
        }
    return {
        'ticker': ticker,
        'company_name': company_name,
        'current_price': current_price,
        'shares_outstanding': shares_outstanding,
        'base_fcf': fcf,
        'scenarios': results
    }