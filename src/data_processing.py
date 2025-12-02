"""
Data processing utilities for antimicrobial resistance analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_amr_data(filepath):
    """
    Load antimicrobial resistance data from Excel file.

    Parameters:
    -----------
    filepath : str or Path
        Path to the Excel file

    Returns:
    --------
    pd.DataFrame
        Loaded and initially processed data
    """
    df = pd.read_excel(filepath)
    return df


def clean_data(df):
    """
    Clean and standardize the AMR dataset.

    Parameters:
    -----------
    df : pd.DataFrame
        Raw dataframe

    Returns:
    --------
    pd.DataFrame
        Cleaned dataframe
    """
    # Make a copy to avoid modifying original
    df_clean = df.copy()

    # Remove completely empty rows
    df_clean = df_clean.dropna(how='all')

    # Standardize column names (lowercase, replace spaces with underscores)
    df_clean.columns = df_clean.columns.str.lower().str.replace(' ', '_')

    return df_clean


def categorize_resistance(result):
    """
    Categorize resistance test results.

    Parameters:
    -----------
    result : str
        Resistance test result (R, S, I, etc.)

    Returns:
    --------
    str
        Standardized category
    """
    if pd.isna(result):
        return 'Unknown'

    result = str(result).upper().strip()

    if result in ['R', 'RESISTANT']:
        return 'Resistant'
    elif result in ['S', 'SENSITIVE', 'SUSCEPTIBLE']:
        return 'Sensitive'
    elif result in ['I', 'INTERMEDIATE']:
        return 'Intermediate'
    else:
        return 'Unknown'


def calculate_resistance_rate(df, antibiotic_col, result_col):
    """
    Calculate resistance rate for each antibiotic.

    Parameters:
    -----------
    df : pd.DataFrame
        Data containing antibiotic test results
    antibiotic_col : str
        Column name for antibiotic
    result_col : str
        Column name for test results

    Returns:
    --------
    pd.DataFrame
        Resistance rates by antibiotic
    """
    # Group by antibiotic and count results
    resistance_summary = df.groupby([antibiotic_col, result_col]).size().unstack(fill_value=0)

    # Calculate rates
    if 'Resistant' in resistance_summary.columns:
        total_tests = resistance_summary.sum(axis=1)
        resistance_summary['resistance_rate'] = (
            resistance_summary['Resistant'] / total_tests * 100
        )

    return resistance_summary


def identify_mdr_organisms(df, organism_col, antibiotic_col, result_col, threshold=3):
    """
    Identify multi-drug resistant organisms.

    Parameters:
    -----------
    df : pd.DataFrame
        AMR data
    organism_col : str
        Column name for organism
    antibiotic_col : str
        Column name for antibiotic
    result_col : str
        Column name for test result
    threshold : int
        Minimum number of resistant antibiotics to classify as MDR

    Returns:
    --------
    pd.DataFrame
        Organisms with their resistance counts
    """
    # Filter for resistant results
    resistant_df = df[df[result_col] == 'Resistant']

    # Count resistant antibiotics per organism
    mdr_counts = resistant_df.groupby(organism_col)[antibiotic_col].nunique()

    # Identify MDR organisms
    mdr_organisms = mdr_counts[mdr_counts >= threshold].sort_values(ascending=False)

    return pd.DataFrame({
        'organism': mdr_organisms.index,
        'resistant_antibiotics_count': mdr_organisms.values,
        'mdr_status': ['MDR' if x >= threshold else 'Non-MDR' for x in mdr_organisms.values]
    })
