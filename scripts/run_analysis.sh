#!/bin/bash
#
# Complete Analysis Pipeline for Antimicrobial Resistance Project
#
# This script runs the full data cleaning and visualization pipeline.
# Author: Rouhat Abdullah
# Date: December 2025
#

set -e  # Exit on error

echo "========================================================================"
echo "  ANTIMICROBIAL RESISTANCE ANALYSIS PIPELINE"
echo "========================================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found."
    exit 1
fi

# Check if required packages are installed
echo "[INFO] Checking dependencies..."
python3 -c "import pandas, numpy, matplotlib, seaborn" 2>/dev/null || {
    echo "[ERROR] Required packages not installed."
    echo "[INFO] Installing dependencies..."
    pip install -r requirements.txt
}

echo "[✓] Dependencies verified"
echo ""

# Run data cleaning pipeline
echo "========================================================================"
echo "STEP 1: DATA CLEANING"
echo "========================================================================"
python3 scripts/01_clean_data.py

if [ $? -eq 0 ]; then
    echo ""
    echo "[✓] Data cleaning completed successfully"
else
    echo "[ERROR] Data cleaning failed"
    exit 1
fi

echo ""

# Generate visualizations
echo "========================================================================"
echo "STEP 2: VISUALIZATION GENERATION"
echo "========================================================================"
python3 scripts/02_generate_visualizations.py

if [ $? -eq 0 ]; then
    echo ""
    echo "[✓] Visualizations generated successfully"
else
    echo "[ERROR] Visualization generation failed"
    exit 1
fi

echo ""
echo "========================================================================"
echo "  PIPELINE COMPLETED SUCCESSFULLY"
echo "========================================================================"
echo ""
echo "Output files:"
echo "  - data/processed/amr_data_2025_cleaned.csv"
echo "  - data/processed/resistance_rates_summary.csv"
echo "  - reports/figures/*.png"
echo ""
echo "Next steps:"
echo "  1. Review cleaned data in data/processed/"
echo "  2. Examine visualizations in reports/figures/"
echo "  3. Run Jupyter notebooks for detailed analysis"
echo ""
