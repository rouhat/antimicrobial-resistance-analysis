#!/usr/bin/env python3
"""
Data Cleaning Pipeline for Antimicrobial Resistance Analysis

This script processes raw antimicrobial susceptibility testing (AST) data,
standardizes resistance categories, and exports cleaned datasets for analysis.

Author: Rouhat Abdullah
Date: December 2025
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from data_processing import categorize_result


def main():
    """Main data cleaning pipeline."""

    print("="*70)
    print("ANTIMICROBIAL RESISTANCE DATA CLEANING PIPELINE")
    print("="*70)

    # Set paths
    raw_data_path = Path('data/raw/amr_data_2025.xlsx')
    processed_dir = Path('data/processed')
    processed_dir.mkdir(exist_ok=True)

    # Load raw data
    print(f"\n[1/5] Loading raw data from {raw_data_path}...")
    df = pd.read_excel(raw_data_path)
    print(f"      Loaded {len(df)} records with {df.shape[1]} columns")

    # Remove system columns
    print("\n[2/5] Removing system metadata columns...")
    system_cols = ['_id', '_uuid', '_submission_time', '_validation_status',
                   '_notes', '_status', '_submitted_by', '__version__', '_tags', '_index']
    df = df.drop(columns=system_cols, errors='ignore')
    print(f"      Retained {df.shape[1]} columns")

    # Identify antibiotic columns
    print("\n[3/5] Identifying antibiotic susceptibility columns...")
    antibiotic_cols = [col for col in df.columns if ' - ' in col or
                      col.startswith('NET_') or col.startswith('MET_')]
    print(f"      Found {len(antibiotic_cols)} antibiotic columns")

    # Standardize resistance categories
    print("\n[4/5] Standardizing resistance categories (R/S/I)...")
    def categorize(result):
        if pd.isna(result):
            return np.nan
        result_str = str(result).upper()
        if 'R' in result_str:
            return 'Resistant'
        elif 'S' in result_str:
            return 'Sensitive'
        elif 'I' in result_str:
            return 'Intermediate'
        return np.nan

    for col in antibiotic_cols:
        df[col + '_Cat'] = df[col].apply(categorize)

    print(f"      Created {len(antibiotic_cols)} categorized columns")

    # Calculate resistance rates
    print("\n[5/5] Calculating resistance rate summary...")
    resistance_data = []

    for col in antibiotic_cols:
        cat_col = col + '_Cat'
        total = df[cat_col].notna().sum()

        if total < 30:  # Minimum sample size
            continue

        resistant = (df[cat_col] == 'Resistant').sum()
        sensitive = (df[cat_col] == 'Sensitive').sum()
        intermediate = (df[cat_col] == 'Intermediate').sum()

        resistance_rate = (resistant / total) * 100
        sensitivity_rate = (sensitive / total) * 100

        ab_name = col.split(' - ')[1] if ' - ' in col else col.replace('_', ' ')

        resistance_data.append({
            'Antibiotic': ab_name,
            'Total_Tests': total,
            'Resistant': resistant,
            'Sensitive': sensitive,
            'Intermediate': intermediate,
            'Resistance_Rate': resistance_rate,
            'Sensitivity_Rate': sensitivity_rate
        })

    resistance_df = pd.DataFrame(resistance_data).sort_values('Resistance_Rate', ascending=False)

    # Export cleaned datasets
    print("\n" + "="*70)
    print("EXPORTING CLEANED DATA")
    print("="*70)

    output_file = processed_dir / 'amr_data_2025_cleaned.csv'
    df.to_csv(output_file, index=False)
    print(f"✓ Cleaned dataset: {output_file}")
    print(f"  Records: {len(df)}")
    print(f"  Columns: {df.shape[1]}")

    summary_file = processed_dir / 'resistance_rates_summary.csv'
    resistance_df.to_csv(summary_file, index=False)
    print(f"\n✓ Resistance summary: {summary_file}")
    print(f"  Antibiotics analyzed: {len(resistance_df)}")

    # Summary statistics
    print("\n" + "="*70)
    print("QUALITY ASSESSMENT")
    print("="*70)

    # Missing data
    missing_pct = (df.isnull().sum().sum() / (len(df) * df.shape[1])) * 100
    print(f"Overall missing data: {missing_pct:.1f}%")

    # Age validation
    valid_ages = df[df['Age (years)'] >= 0]['Age (years)']
    print(f"Valid age records: {len(valid_ages)}/{len(df)} ({len(valid_ages)/len(df)*100:.1f}%)")

    # Sample types
    print(f"\nSample type distribution:")
    for sample_type, count in df['Sample Type'].value_counts().items():
        print(f"  {sample_type}: {count} ({count/len(df)*100:.1f}%)")

    # Organism prevalence
    print(f"\nTop 5 organisms:")
    for org, count in df['Organism Identified'].value_counts().head(5).items():
        print(f"  {org}: {count} ({count/len(df)*100:.1f}%)")

    # Overall resistance
    all_results = []
    for col in antibiotic_cols:
        results = df[col + '_Cat'].dropna()
        all_results.extend(results.tolist())

    overall_dist = pd.Series(all_results).value_counts()
    total_tests = len(all_results)
    overall_resistance = (overall_dist.get('Resistant', 0) / total_tests * 100)

    print(f"\n" + "="*70)
    print(f"OVERALL RESISTANCE RATE: {overall_resistance:.1f}%")
    print("="*70)

    print("\n✓ Data cleaning pipeline completed successfully!")


if __name__ == '__main__':
    main()
