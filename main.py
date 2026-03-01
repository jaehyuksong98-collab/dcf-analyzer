# main.py
# Entry point — type a ticker and the full analysis runs automatically

from dcf_analyzer import calculate_dcf
from visualizer import visualize_dcf
from report_generator import save_report

def main():
    print("=" * 50)
    print("  DCF Analyzer — Automated Valuation Tool")
    print("=" * 50)

    ticker = input("\nEnter company ticker (e.g. AAPL, MSFT, TSLA): ").strip().upper()

    print(f"\nFetching data for {ticker}...")

    # Run DCF calculation
    result = calculate_dcf(ticker)

    if result is None:
        print("Could not retrieve data. Please check the ticker and try again.")
        return

    # Print summary to console
    print(f"\n{'=' * 50}")
    print(f"  {result['company_name']} ({ticker})")
    print(f"{'=' * 50}")
    print(f"  Current Price:  ${result['current_price']:.2f}")
    print(f"  {'Scenario':<12} {'Intrinsic Value':>16} {'Gap':>10}")
    print(f"  {'-' * 40}")

    for scenario, data in result['scenarios'].items():
        iv = data['intrinsic_value']
        gap = ((iv - result['current_price']) / result['current_price']) * 100
        status = "Undervalued" if gap > 0 else "Overvalued"
        print(f"  {scenario:<12} ${iv:>14.2f} {gap:>+8.1f}%  {status}")

    print(f"{'=' * 50}\n")

    # Generate charts
    print("Generating charts...")
    visualize_dcf(result)

    # Generate and save report
    print("Generating report...")
    save_report(result)

    print("\nDone! Check the outputs/ folder for chart and report.")

if __name__ == "__main__":
    main()