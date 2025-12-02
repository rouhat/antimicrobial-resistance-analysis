"""
Visualization utilities for antimicrobial resistance analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def plot_resistance_rates(df, antibiotic_col='antibiotic', rate_col='resistance_rate',
                          top_n=15, title='Antibiotic Resistance Rates'):
    """
    Create a bar plot of resistance rates by antibiotic.

    Parameters:
    -----------
    df : pd.DataFrame
        Data with antibiotics and resistance rates
    antibiotic_col : str
        Column name for antibiotic
    rate_col : str
        Column name for resistance rate
    top_n : int
        Number of top antibiotics to display
    title : str
        Plot title
    """
    # Sort and get top N
    df_sorted = df.nlargest(top_n, rate_col)

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(df_sorted[antibiotic_col], df_sorted[rate_col])

    # Color bars by resistance level
    colors = ['green' if x < 20 else 'yellow' if x < 50 else 'red'
              for x in df_sorted[rate_col]]
    for bar, color in zip(bars, colors):
        bar.set_color(color)
        bar.set_alpha(0.7)

    ax.set_xlabel('Resistance Rate (%)', fontsize=12)
    ax.set_ylabel('Antibiotic', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.invert_yaxis()

    # Add value labels
    for i, v in enumerate(df_sorted[rate_col]):
        ax.text(v + 1, i, f'{v:.1f}%', va='center')

    plt.tight_layout()
    return fig


def plot_organism_resistance(df, organism_col, count_col, top_n=10,
                             title='Multi-Drug Resistant Organisms'):
    """
    Plot organisms by resistance count.

    Parameters:
    -----------
    df : pd.DataFrame
        Data with organisms and resistance counts
    organism_col : str
        Column name for organism
    count_col : str
        Column name for resistance count
    top_n : int
        Number of organisms to display
    title : str
        Plot title
    """
    df_sorted = df.nlargest(top_n, count_col)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.barh(df_sorted[organism_col], df_sorted[count_col], color='coral', alpha=0.7)

    ax.set_xlabel('Number of Resistant Antibiotics', fontsize=12)
    ax.set_ylabel('Organism', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.invert_yaxis()

    # Add value labels
    for i, v in enumerate(df_sorted[count_col]):
        ax.text(v + 0.2, i, str(int(v)), va='center')

    plt.tight_layout()
    return fig


def plot_temporal_comparison(comparison_df, title='Resistance Rate Changes Over Time'):
    """
    Plot temporal changes in resistance rates.

    Parameters:
    -----------
    comparison_df : pd.DataFrame
        Data with resistance rates for different time periods
    title : str
        Plot title
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Plot 1: Side-by-side comparison
    x = np.arange(len(comparison_df))
    width = 0.35

    rate_cols = [col for col in comparison_df.columns if '_rate' in col]
    if len(rate_cols) >= 2:
        ax1.bar(x - width/2, comparison_df[rate_cols[0]], width,
                label=rate_cols[0].replace('_rate', ''), alpha=0.7)
        ax1.bar(x + width/2, comparison_df[rate_cols[1]], width,
                label=rate_cols[1].replace('_rate', ''), alpha=0.7)

        ax1.set_xlabel('Antibiotic', fontsize=12)
        ax1.set_ylabel('Resistance Rate (%)', fontsize=12)
        ax1.set_title('Resistance Rate Comparison', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(comparison_df.index, rotation=45, ha='right')
        ax1.legend()

    # Plot 2: Change in resistance
    if 'change' in comparison_df.columns:
        colors = ['red' if x > 0 else 'green' for x in comparison_df['change']]
        ax2.barh(comparison_df.index, comparison_df['change'], color=colors, alpha=0.7)
        ax2.set_xlabel('Change in Resistance Rate (%)', fontsize=12)
        ax2.set_ylabel('Antibiotic', fontsize=12)
        ax2.set_title('Change in Resistance (Increase = Red)', fontsize=12, fontweight='bold')
        ax2.axvline(x=0, color='black', linestyle='--', linewidth=0.8)

    plt.tight_layout()
    return fig


def plot_age_resistance_trends(df, age_col='age_group', rate_col='resistance_rate',
                               title='Resistance Rate by Age Group'):
    """
    Plot resistance trends across age groups.

    Parameters:
    -----------
    df : pd.DataFrame
        Data with age groups and resistance rates
    age_col : str
        Column name for age group
    rate_col : str
        Column name for resistance rate
    title : str
        Plot title
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df[age_col], df[rate_col], marker='o', linewidth=2, markersize=8, color='steelblue')
    ax.fill_between(range(len(df)), df[rate_col], alpha=0.3)

    ax.set_xlabel('Age Group', fontsize=12)
    ax.set_ylabel('Resistance Rate (%)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Add value labels
    for i, (age, rate) in enumerate(zip(df[age_col], df[rate_col])):
        ax.text(i, rate + 1, f'{rate:.1f}%', ha='center')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig


def plot_heatmap(df, title='Antibiotic Resistance Heatmap', cmap='RdYlGn_r'):
    """
    Create a heatmap of resistance patterns.

    Parameters:
    -----------
    df : pd.DataFrame
        Pivoted data for heatmap (organisms x antibiotics)
    title : str
        Plot title
    cmap : str
        Colormap name
    """
    fig, ax = plt.subplots(figsize=(14, 10))

    sns.heatmap(df, annot=True, fmt='.1f', cmap=cmap, center=50,
                cbar_kws={'label': 'Resistance Rate (%)'}, ax=ax)

    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Antibiotic', fontsize=12)
    ax.set_ylabel('Organism', fontsize=12)

    plt.tight_layout()
    return fig


def save_figure(fig, filename, dpi=300):
    """
    Save figure to reports/figures directory.

    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        Figure to save
    filename : str
        Filename (without path)
    dpi : int
        Resolution
    """
    from pathlib import Path

    output_dir = Path('reports/figures')
    output_dir.mkdir(parents=True, exist_ok=True)

    filepath = output_dir / filename
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    print(f"Figure saved to {filepath}")
