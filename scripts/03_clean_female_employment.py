# Generated from: 03_clean_female_employment.ipynb
# Converted at: 2026-04-27T17:40:45.035Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

# =====================================================
# Script: 03_clean_female_employment.py
# Purpose: Construct average female employment by SIC section for 2024
# Input: data/raw/03_female_employment_raw_2024.csv
# Output: data/clean/03_female_employment_clean_2024.csv
# =====================================================

import pandas as pd
import numpy as np

# -----------------------------
# 1. Load raw data
# -----------------------------
# ONS tables contain metadata rows, so the header starts at row 7
RAW_PATH = "data/raw/03_female_employment_raw_2024.csv"
OUT_PATH = "data/clean/03_female_employment_clean_2024.csv"

df = pd.read_csv(RAW_PATH, header=6)

# Rename the first column to something usable
df = df.rename(columns={df.columns[0]: "quarter"})

# -----------------------------
# 2. Keep only 2024 data
# -----------------------------
df_2024 = df[df["quarter"].str.contains("2024", na=False)]

# -----------------------------
# 3. Keep SIC section columns only
# -----------------------------
# These correspond to SIC sections used elsewhere in the project
sic_columns = [
    "A", "C", "F", "G", "H", "I", "J", "K", "L",
    "M", "N", "O", "P", "Q"
]

df_2024 = df_2024[sic_columns]

# -----------------------------
# 4. Convert values to numeric
# -----------------------------
# Remove commas and convert to float
for col in df_2024.columns:
    df_2024[col] = (
        df_2024[col]
        .astype(str)
        .str.replace(",", "")
        .astype(float)
    )

# -----------------------------
# 5. Average across 2024 quarters
# -----------------------------
employment_2024 = (
    df_2024
    .mean()
    .reset_index()
    .rename(
        columns={
            "index": "sic_section",
            0: "female_employment_2024"
        }
    )
)

# -----------------------------
# 6. Validation checks
# -----------------------------
assert employment_2024["sic_section"].is_unique, "Duplicate SIC sections detected"
assert employment_2024.shape[0] <= 21, "Too many industries detected"

# -----------------------------
# 7. Save cleaned dataset
# -----------------------------
employment_2024.to_csv(OUT_PATH, index=False)

print("✓ Cleaned female employment data for 2024 saved")
print(employment_2024)