# Generated from: 01_clean_gender_pay_gap.ipynb
# Converted at: 2026-04-27T17:22:49.791Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

# =====================================================
# Script: 01_clean_gender_pay_gap.py
# Purpose: Clean and aggregate firm-level gender pay gap data to SIC sections
# Input: data/raw/01_gender_pay_gap_raw_2024.csv
# Output: data/clean/01_gender_pay_gap_clean_2024.csv
# =====================================================

import pandas as pd
import numpy as np

# -----------------------------
# 1. Load raw data
# -----------------------------
RAW_PATH = "data/raw/01_gender_pay_gap_raw_2024.csv"
OUT_PATH = "data/clean/01_gender_pay_gap_clean_2024.csv"

df = pd.read_csv(RAW_PATH)

# -----------------------------
# 2. Keep relevant columns
# -----------------------------
df = df[["SicCodes", "DiffMeanHourlyPercent"]].copy()

# Drop rows with missing values
df = df.dropna(subset=["SicCodes", "DiffMeanHourlyPercent"])

# -----------------------------
# 3. Extract primary SIC code
# -----------------------------
def extract_primary_sic(sic_string):
    """
    Takes a SIC string like '62020, 63110' and returns '62'
    """
    primary = str(sic_string).split(",")[0].strip()
    return primary[:2]

df["sic_2digit"] = df["SicCodes"].apply(extract_primary_sic)

# Drop invalid SICs
df = df[df["sic_2digit"].str.isnumeric()]

# -----------------------------
# 4. Map SIC codes to SIC sections
# -----------------------------
def map_sic_section(sic):
    sic = int(sic)
    if 1 <= sic <= 3: 
        return "A"
    elif 5 <= sic <= 9: 
        return "B"
    elif 10 <= sic <= 33: 
        return "C"
    elif 35 <= sic <= 39: 
        return "D"
    elif 41 <= sic <= 43: 
        return "F"
    elif 45 <= sic <= 47: 
        return "G"
    elif 49 <= sic <= 53: 
        return "H"
    elif 55 <= sic <= 56: 
        return "I"
    elif 58 <= sic <= 63: 
        return "J"
    elif 64 <= sic <= 66: 
        return "K"
    elif sic == 68: 
        return "L"
    elif 69 <= sic <= 75: 
        return "M"
    elif 77 <= sic <= 82: 
        return "N"
    elif sic == 84: 
        return "O"
    elif sic == 85: 
        return "P"
    elif 86 <= sic <= 88: 
        return "Q"
    elif 90 <= sic <= 93: 
        return "R"
    elif 94 <= sic <= 96: 
        return "S"
    elif sic in [97, 98]: 
        return "T"
    elif sic == 99: 
        return "U"
    else: 
        return np.nan

df["sic_section"] = df["sic_2digit"].apply(map_sic_section)

df = df.dropna(subset=["sic_section"])

# -----------------------------
# 5. Aggregate to industry level
# -----------------------------
industry_pay_gap = (
    df
    .groupby("sic_section", as_index=False)
    .agg(
        mean_gender_pay_gap=("DiffMeanHourlyPercent", "mean"),
        firm_count=("DiffMeanHourlyPercent", "count")
    )
)

# -----------------------------
# 6. Validation checks
# -----------------------------
assert industry_pay_gap["sic_section"].is_unique
assert industry_pay_gap.shape[0] <= 21

# -----------------------------
# 7. Save clean dataset
# -----------------------------
industry_pay_gap.to_csv(OUT_PATH, index=False)

print("✓ Clean industry-level gender pay gap data saved")
print(industry_pay_gap.head())