# Data Processing Scripts

Executable scripts for reproducible data cleaning and visualization generation.

## Scripts

### 01_clean_data.py
**Purpose:** Data cleaning and standardization pipeline

**Functions:**
- Loads raw Excel data
- Removes system metadata columns
- Standardizes resistance categories (R/S/I)
- Calculates resistance rate summaries
- Exports cleaned datasets

**Output:**
- `data/processed/amr_data_2025_cleaned.csv`
- `data/processed/resistance_rates_summary.csv`

**Usage:**
```bash
python3 scripts/01_clean_data.py
```

### 02_generate_visualizations.py
**Purpose:** Generate publication-quality figures

**Visualizations Created:**
- Top 20 antibiotics by resistance rate
- Organism distribution
- Highest sensitivity antibiotics

**Output:**
- `reports/figures/resistance_rates_top20.png`
- `reports/figures/organism_distribution.png`
- `reports/figures/highest_sensitivity.png`

**Usage:**
```bash
python3 scripts/02_generate_visualizations.py
```

### run_analysis.sh
**Purpose:** Complete analysis pipeline orchestration

**Workflow:**
1. Validates dependencies
2. Runs data cleaning
3. Generates visualizations
4. Reports completion status

**Usage:**
```bash
./scripts/run_analysis.sh
```

## Requirements

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Pipeline Execution

Run the complete pipeline:
```bash
# Method 1: Use the orchestration script
./scripts/run_analysis.sh

# Method 2: Run scripts individually
python3 scripts/01_clean_data.py
python3 scripts/02_generate_visualizations.py
```

## Notes

- Scripts are idempotent - safe to run multiple times
- All paths are relative to project root
- Scripts include comprehensive logging and error handling
- Designed for reproducibility and automation
