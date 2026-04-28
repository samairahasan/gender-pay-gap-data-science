# =====================================================
# Script: 04_merge.py
# Purpose: Merge three cleaned industry-level datasets,
#          validate the merge, and save to CSV and SQLite
# Input:  data/clean/01_gender_pay_gap_clean_2024.csv
#         data/clean/02_gross_hourly_pay_clean_2024.csv
#         data/clean/03_female_employment_clean_2024.csv
# Output: data/clean/04_merged_industry_dataset_2024.csv
#         data/gender_pay_gap.db
# =====================================================

import os
import sqlite3

import pandas as pd

# -----------------------------------------------------
# 1. File paths
# -----------------------------------------------------
PAY_GAP_PATH    = "data/clean/01_gender_pay_gap_clean_2024.csv"
HOURLY_PAY_PATH = "data/clean/02_gross_hourly_pay_clean_2024.csv"
EMPLOYMENT_PATH = "data/clean/03_female_employment_clean_2024.csv"
OUT_CSV         = "data/clean/04_merged_industry_dataset_2024.csv"
OUT_DB          = "data/uk_gender_pay_gap_industry_2024.db"

# -----------------------------------------------------
# 2. Load clean datasets
# -----------------------------------------------------
print("Loading clean datasets...")

try:
    pay_gap    = pd.read_csv(PAY_GAP_PATH)
    hourly_pay = pd.read_csv(HOURLY_PAY_PATH)
    employment = pd.read_csv(EMPLOYMENT_PATH)
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Please ensure all cleaning scripts (01–03) have been run first.")
    raise

print(f"  pay_gap:    {pay_gap.shape[0]} SIC sections")
print(f"  hourly_pay: {hourly_pay.shape[0]} SIC sections")
print(f"  employment: {employment.shape[0]} SIC sections")

# -----------------------------------------------------
# 3. Standardise merge keys
# Strip whitespace and ensure consistent uppercase
# -----------------------------------------------------
for df in [pay_gap, hourly_pay, employment]:
    df["sic_section"] = df["sic_section"].astype(str).str.strip().str.upper()

# Show which SIC sections are in each dataset before merging
print("\nSIC sections in each dataset:")
print(f"  pay_gap:    {sorted(pay_gap['sic_section'].tolist())}")
print(f"  hourly_pay: {sorted(hourly_pay['sic_section'].tolist())}")
print(f"  employment: {sorted(employment['sic_section'].tolist())}")

# -----------------------------------------------------
# 4. Merge datasets using inner join
# Inner join keeps only SIC sections present in ALL
# three datasets — avoids missing values in regression
# -----------------------------------------------------
print("\nMerging datasets (inner join)...")

# Step 1: merge pay gap with hourly pay
merged = pd.merge(
    pay_gap,
    hourly_pay,
    on="sic_section",
    how="inner",
    validate="1:1",
    indicator=True
)
print(f"\nStep 1 — pay gap + hourly pay:")
print(merged["_merge"].value_counts().to_string())
merged = merged.drop(columns=["_merge"])

# Step 2: merge with female employment
merged = pd.merge(
    merged,
    employment,
    on="sic_section",
    how="inner",
    validate="1:1",
    indicator=True
)
print(f"\nStep 2 — + female employment:")
print(merged["_merge"].value_counts().to_string())
merged = merged.drop(columns=["_merge"])

# -----------------------------------------------------
# 5. Post-merge validation
# -----------------------------------------------------
print(f"\nFinal merged dataset:")
print(f"  Industries retained: {merged.shape[0]}")
print(f"  Variables:           {merged.shape[1]}")
print(f"\nSIC sections retained: {sorted(merged['sic_section'].tolist())}")
print(f"\nMissing values after merge:")
print(merged.isnull().sum().to_string())
print(f"\nPreview:")
print(merged.to_string(index=False))

# Check for any unexpected issues
assert merged["sic_section"].is_unique, "Duplicate SIC sections in merged data"
assert merged.shape[0] >= 5, "Too few industries after merge — check inputs"
assert merged.isnull().sum().sum() == 0, "Unexpected missing values after merge"

# -----------------------------------------------------
# 6. Save to CSV
# -----------------------------------------------------
merged.to_csv(OUT_CSV, index=False)
print(f"\n✓ Merged CSV saved to {OUT_CSV}")

# -----------------------------------------------------
# 7. Save to SQLite database
# -----------------------------------------------------
print(f"Saving to SQLite database: {OUT_DB}")

conn = sqlite3.connect(OUT_DB)

# Create table with proper schema and primary key
conn.execute("DROP TABLE IF EXISTS merged_data")
conn.execute("""
    CREATE TABLE merged_data (
        sic_section            TEXT NOT NULL PRIMARY KEY,
        mean_gender_pay_gap    REAL,
        firm_count             INTEGER,
        avg_hourly_pay         REAL,
        female_employment_2024 REAL
    )
""")

merged.to_sql("merged_data", conn, if_exists="replace", index=False)

# Verify with a SQL query
result = pd.read_sql("""
    SELECT sic_section,
           ROUND(mean_gender_pay_gap, 2)    AS mean_gender_pay_gap,
           ROUND(avg_hourly_pay, 2)         AS avg_hourly_pay,
           ROUND(female_employment_2024, 1) AS female_employment_2024
    FROM merged_data
    ORDER BY mean_gender_pay_gap DESC
""", conn)

print("\nSQL verification — industries ranked by gender pay gap:")
print(result.to_string(index=False))

conn.close()
print(f"\n✓ SQLite database saved to {OUT_DB}")
print("\n✓ Merge complete — ready for analysis in 05_analyse.py")