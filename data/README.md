# Data Directory

## Structure

- `raw/` - Original, unmodified data files
  - `amr_data_2025.xlsx` - Antimicrobial resistance data for 2025
  - Add your 2024 data file here when available

- `processed/` - Cleaned and processed datasets
  - Generated files will be saved here during analysis

## Data Description

The raw data contains antimicrobial susceptibility testing results including:
- Bacterial organisms identified
- Antibiotics tested
- Resistance/sensitivity results
- Patient demographics (age, etc.)
- Temporal information

## Usage Notes

- Never modify files in `raw/` directory
- All processing should save outputs to `processed/` directory
- Large data files are gitignored but raw data is preserved
