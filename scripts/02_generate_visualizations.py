#!/usr/bin/env python3
"""
Visualization Generation Script for AMR Analysis

Generates publication-quality figures for antimicrobial resistance analysis.

Author: Rouhat Abdullah
Date: December 2025
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Configure plotting
sns.set_style('whitegrid')
sns.set_palette('Set2')
plt.rcParams['figure.dpi'] = 300


def main():
    """Generate all analysis visualizations."""

    print("="*70)
    print("ANTIMICROBIAL RESISTANCE VISUALIZATION GENERATOR")
    print("="*70)

    # Load processed data
    data_dir = Path('data/processed')
    figures_dir = Path('reports/figures')
    figures_dir.mkdir(parents=True, exist_ok=True)

    print("\n[1/4] Loading processed data...")
    df = pd.read_csv(data_dir / 'amr_data_2025_cleaned.csv')
    resistance_df = pd.read_csv(data_dir / 'resistance_rates_summary.csv')
    print(f"      Loaded {len(df)} isolates, {len(resistance_df)} antibiotics")

    # 1. Resistance rates visualization
    print("\n[2/4] Generating resistance rate visualization...")
    top_20 = resistance_df.head(20)

    fig, ax = plt.subplots(figsize=(12, 10))
    colors = ['#d62728' if x >= 80 else '#ff7f0e' if x >= 50 else '#2ca02c'
              for x in top_20['Resistance_Rate']]

    bars = ax.barh(range(len(top_20)), top_20['Resistance_Rate'],
                   color=colors, alpha=0.7)
    ax.set_yticks(range(len(top_20)))
    ax.set_yticklabels(top_20['Antibiotic'])
    ax.set_xlabel('Resistance Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Top 20 Antibiotics by Resistance Rate',
                fontsize=14, fontweight='bold')
    ax.invert_yaxis()

    for i, (rate, n) in enumerate(zip(top_20['Resistance_Rate'],
                                     top_20['Total_Tests'])):
        ax.text(rate + 2, i, f'{rate:.1f}% (n={n})', va='center', fontsize=9)

    ax.axvline(50, color='orange', linestyle='--', alpha=0.5, linewidth=2)
    ax.axvline(80, color='red', linestyle='--', alpha=0.5, linewidth=2)

    plt.tight_layout()
    output_file = figures_dir / 'resistance_rates_top20.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"      ✓ Saved: {output_file}")
    plt.close()

    # 2. Organism distribution
    print("\n[3/4] Generating organism distribution plot...")
    organisms = df['Organism Identified'].value_counts()

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(organisms.index, organisms.values, alpha=0.7, color='steelblue')
    ax.set_xlabel('Number of Isolates', fontsize=12, fontweight='bold')
    ax.set_ylabel('Organism', fontsize=12, fontweight='bold')
    ax.set_title(f'Bacterial Isolate Distribution (n={organisms.sum()})',
                fontsize=14, fontweight='bold')
    ax.invert_yaxis()

    for i, v in enumerate(organisms.values):
        pct = v/organisms.sum()*100
        ax.text(v + 1, i, f'{v} ({pct:.1f}%)', va='center', fontsize=10)

    plt.tight_layout()
    output_file = figures_dir / 'organism_distribution.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"      ✓ Saved: {output_file}")
    plt.close()

    # 3. Best antibiotics (highest sensitivity)
    print("\n[4/4] Generating sensitivity analysis plot...")
    best_abs = resistance_df.sort_values('Sensitivity_Rate', ascending=False).head(15)

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(range(len(best_abs)), best_abs['Sensitivity_Rate'],
                   color='#2ca02c', alpha=0.7)
    ax.set_yticks(range(len(best_abs)))
    ax.set_yticklabels(best_abs['Antibiotic'])
    ax.set_xlabel('Sensitivity Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Most Effective Antibiotics (Highest Sensitivity)',
                fontsize=14, fontweight='bold')
    ax.invert_yaxis()

    for i, (rate, n) in enumerate(zip(best_abs['Sensitivity_Rate'],
                                     best_abs['Total_Tests'])):
        ax.text(rate - 3, i, f'{rate:.1f}%', va='center', ha='right',
               fontsize=9, color='white', fontweight='bold')

    ax.axvline(80, color='darkgreen', linestyle='--', alpha=0.7,
              linewidth=2, label='80% threshold')
    ax.legend(fontsize=10)

    plt.tight_layout()
    output_file = figures_dir / 'highest_sensitivity.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"      ✓ Saved: {output_file}")
    plt.close()

    print("\n" + "="*70)
    print("✓ All visualizations generated successfully!")
    print(f"✓ Figures saved to: {figures_dir}")
    print("="*70)


if __name__ == '__main__':
    main()
