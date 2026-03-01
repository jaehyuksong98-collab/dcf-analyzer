# visualizer.py
# Handles all chart generation for DCF analysis results

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

def visualize_dcf(dcf_result: dict, save_path: str = 'outputs/'):
    """
    Generate two charts:
    1. Intrinsic value by scenario vs current price
    2. Projected FCF over 5 years (base case)
    """
    if dcf_result is None:
        print("No data to visualize.")
        return

    company_name = dcf_result['company_name']
    ticker = dcf_result['ticker']
    current_price = dcf_result['current_price']
    scenarios = dcf_result['scenarios']

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f'{company_name} ({ticker}) — DCF Analysis', 
                 fontsize=14, fontweight='bold')

    # --- Chart 1: Intrinsic Value vs Current Price ---
    labels = list(scenarios.keys())
    values = [scenarios[s]['intrinsic_value'] for s in labels]
    colors = ['#2ecc71', '#3498db', '#e74c3c']  # green, blue, red

    bars = axes[0].bar(labels, values, color=colors, alpha=0.85, width=0.5)
    axes[0].axhline(y=current_price, color='black', linestyle='--',
                    linewidth=2, label=f'Current Price: ${current_price:.2f}')
    axes[0].set_title('Intrinsic Value by Scenario vs Current Price')
    axes[0].set_ylabel('Value per Share ($)')
    axes[0].legend()

    # Add value labels on top of bars
    for bar, val in zip(bars, values):
        axes[0].text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 1,
                     f'${val:.2f}', ha='center', va='bottom', fontweight='bold')

    # --- Chart 2: Projected FCF (Base Case) ---
    base_fcf = scenarios['Base']['projected_fcf']
    years = list(range(1, len(base_fcf) + 1))
    fcf_billions = [f / 1e9 for f in base_fcf]

    axes[1].plot(years, fcf_billions, 'o-', color='#3498db', linewidth=2, markersize=8)
    axes[1].fill_between(years, fcf_billions, alpha=0.2, color='#3498db')
    axes[1].set_title('Projected FCF — Base Case (5 Years)')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('FCF (Billions $)')
    axes[1].set_xticks(years)

    plt.tight_layout()

    # Save chart to outputs folder
    os.makedirs(save_path, exist_ok=True)
    output_file = os.path.join(save_path, f'{ticker}_dcf_analysis.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Chart saved: {output_file}")