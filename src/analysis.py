"""
Statistical analysis functions for antimicrobial resistance patterns.
"""

import pandas as pd
import numpy as np
from scipy import stats


def compare_resistance_rates(df1, df2, antibiotic_col, result_col, label1='2024', label2='2025'):
    """
    Compare resistance rates between two time periods.

    Parameters:
    -----------
    df1, df2 : pd.DataFrame
        DataFrames for each time period
    antibiotic_col : str
        Column name for antibiotic
    result_col : str
        Column name for test results
    label1, label2 : str
        Labels for the time periods

    Returns:
    --------
    pd.DataFrame
        Comparison of resistance rates
    """
    def calc_rate(df):
        resistant = df[df[result_col] == 'Resistant'].groupby(antibiotic_col).size()
        total = df.groupby(antibiotic_col).size()
        return (resistant / total * 100).fillna(0)

    rates1 = calc_rate(df1)
    rates2 = calc_rate(df2)

    comparison = pd.DataFrame({
        f'{label1}_rate': rates1,
        f'{label2}_rate': rates2,
        'change': rates2 - rates1,
        'pct_change': ((rates2 - rates1) / rates1 * 100).replace([np.inf, -np.inf], np.nan)
    })

    return comparison.sort_values('change', ascending=False)


def analyze_age_resistance(df, age_col, result_col, organism_col=None):
    """
    Analyze resistance patterns by age group.

    Parameters:
    -----------
    df : pd.DataFrame
        AMR data with age information
    age_col : str
        Column name for age or age group
    result_col : str
        Column name for test results
    organism_col : str, optional
        Column name for organism

    Returns:
    --------
    pd.DataFrame
        Resistance rates by age group
    """
    age_analysis = df.groupby(age_col)[result_col].apply(
        lambda x: (x == 'Resistant').sum() / len(x) * 100
    ).sort_index()

    return pd.DataFrame({
        'age_group': age_analysis.index,
        'resistance_rate': age_analysis.values
    })


def calculate_effectiveness_score(df, antibiotic_col, result_col):
    """
    Calculate effectiveness score for each antibiotic.
    Score based on sensitivity rate and sample size.

    Parameters:
    -----------
    df : pd.DataFrame
        AMR data
    antibiotic_col : str
        Column name for antibiotic
    result_col : str
        Column name for test results

    Returns:
    --------
    pd.DataFrame
        Effectiveness scores
    """
    grouped = df.groupby(antibiotic_col)

    results = []
    for antibiotic, group in grouped:
        total = len(group)
        sensitive = (group[result_col] == 'Sensitive').sum()
        resistant = (group[result_col] == 'Resistant').sum()

        sensitivity_rate = (sensitive / total * 100) if total > 0 else 0

        # Effectiveness score: weighted by sample size and sensitivity
        # Higher score = more effective
        effectiveness = sensitivity_rate * np.log1p(total)

        results.append({
            'antibiotic': antibiotic,
            'sensitivity_rate': sensitivity_rate,
            'total_tests': total,
            'effectiveness_score': effectiveness
        })

    return pd.DataFrame(results).sort_values('effectiveness_score', ascending=False)


def identify_first_line_treatments(df, antibiotic_col, result_col,
                                   sensitivity_threshold=80, min_samples=30):
    """
    Identify antibiotics suitable for first-line treatment.

    Parameters:
    -----------
    df : pd.DataFrame
        AMR data
    antibiotic_col : str
        Column name for antibiotic
    result_col : str
        Column name for test results
    sensitivity_threshold : float
        Minimum sensitivity rate (%)
    min_samples : int
        Minimum number of tests required

    Returns:
    --------
    pd.DataFrame
        Recommended first-line antibiotics
    """
    grouped = df.groupby(antibiotic_col)

    recommendations = []
    for antibiotic, group in grouped:
        total = len(group)
        if total < min_samples:
            continue

        sensitive = (group[result_col] == 'Sensitive').sum()
        sensitivity_rate = (sensitive / total * 100)

        if sensitivity_rate >= sensitivity_threshold:
            recommendations.append({
                'antibiotic': antibiotic,
                'sensitivity_rate': sensitivity_rate,
                'total_tests': total,
                'recommendation': 'First-line'
            })

    return pd.DataFrame(recommendations).sort_values('sensitivity_rate', ascending=False)


def gram_classification_analysis(df, organism_col, gram_col, result_col):
    """
    Compare resistance patterns between Gram-positive and Gram-negative bacteria.

    Parameters:
    -----------
    df : pd.DataFrame
        AMR data
    organism_col : str
        Column name for organism
    gram_col : str
        Column name for Gram classification
    result_col : str
        Column name for test results

    Returns:
    --------
    dict
        Analysis results for both groups
    """
    analysis = {}

    for gram_type in df[gram_col].unique():
        if pd.isna(gram_type):
            continue

        subset = df[df[gram_col] == gram_type]
        total = len(subset)
        resistant = (subset[result_col] == 'Resistant').sum()

        analysis[gram_type] = {
            'total_tests': total,
            'resistant_count': resistant,
            'resistance_rate': (resistant / total * 100) if total > 0 else 0
        }

    return analysis
