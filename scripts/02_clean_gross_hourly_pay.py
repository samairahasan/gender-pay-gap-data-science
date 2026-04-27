# Generated from: 02_clean_gross_hourly_pay.ipynb
# Converted at: 2026-04-27T17:31:21.520Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

import pandas as pd
import numpy as np
# =============================
# Script: 02_clean_industry_data.py
# Purpose: Clean ASHE hourly pay data to industry (SIC section) level
# =============================
# -----------------------------
# 1. File paths
# -----------------------------
RAW_PATH = "data/raw/02 - gross hourly pay 2024.csv"
OUT_PATH = "data/clean/industry_pay_clean.csv"
# -----------------------------
# 2. Load raw ASHE data
# -----------------------------
df = pd.read_csv(RAW_PATH, header=4)
# -----------------------------
# 3. Strip whitespace from column names
# -----------------------------
df.columns = df.columns.str.strip()
# -----------------------------
# 4. Keep SIC SECTION rows only
# -----------------------------
# SIC sections are single letters A–U
df = df[df["Code"].astype(str).str.match(r'^[A-U]$')]
# -----------------------------
# 5. Keep only relevant variables
# -----------------------------
df = df[["Code", "Mean"]].copy()
df = df.rename(columns={"Code": "sic_section", "Mean": "avg_hourly_pay"})
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