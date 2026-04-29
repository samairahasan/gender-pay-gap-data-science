# =====================================================
# Script: 02_clean_gross_hourly_pay.py
# Purpose: Clean ASHE gross hourly pay data to SIC section (industry) level
# Input: data/raw/02_gross_hourly_pay_raw_2024.csv
# Output: data/clean/02_gross_hourly_pay_clean_2024.csv
# =====================================================

import pandas as pd
import numpy as np

# -----------------------------
# 1. File paths
# -----------------------------
RAW_PATH = "data/raw/02_gross_hourly_pay_raw_2024.csv"
OUT_PATH = "data/clean/02_gross_hourly_pay_clean_2024.csv"

# -----------------------------
# 2. Load raw ASHE data
# -----------------------------
# ONS ASHE tables contain metadata rows, so header starts at row 5
df = pd.read_csv(RAW_PATH, header=4)

# -----------------------------
# 3. Strip whitespace from column names
# -----------------------------
df.columns = df.columns.str.strip()

# -----------------------------
# 4. Keep SIC section rows only
# -----------------------------
# SIC sections are single letters A–U
df = df[df["Code"].astype(str).str.match(r"^[A-U]$")]

# -----------------------------
# 5. Keep only relevant variables
# -----------------------------
df = df[["Code", "Mean"]].copy()
df = df.rename(
    columns={
        "Code": "sic_section",
        "Mean": "avg_hourly_pay"
    }
)

# -----------------------------
# 6. Drop missing or invalid values
# -----------------------------
df["avg_hourly_pay"] = pd.to_numeric(df["avg_hourly_pay"], errors="coerce")
df = df.dropna(subset=["avg_hourly_pay"])

# -----------------------------
# 6b. Drop any remaining duplicates
# -----------------------------
df = df.drop_duplicates(subset=["sic_section"])

# -----------------------------
# 7. Validation checks
# -----------------------------
assert df["sic_section"].is_unique, "SIC sections are not unique"
assert df.shape[0] <= 21, "Too many SIC sections detected"

# -----------------------------
# 8. Save cleaned dataset
# -----------------------------
df.to_csv(OUT_PATH, index=False)

print("✓ Clean industry-level hourly pay data saved")
print(df.sort_values("avg_hourly_pay", ascending=False).head())