# =====================================================
# Script: 05_analysis_and_outputs.py
# Purpose: Load merged industry dataset, produce
#          descriptive statistics, visualisations,
#          and OLS regression analysis
# Input:  data/clean/04_merged_industry_dataset_2024.csv
# Output: output/figures/*.png  (4 figures)
#         output/tables/*.csv   (3 tables)
#
# Dependencies: pandas, numpy, matplotlib, statsmodels
# Install via: pip install statsmodels
# =====================================================

import os

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# -----------------------------------------------------
# 1. File paths
# -----------------------------------------------------
MERGED_CSV = "data/clean/04_merged_industry_dataset_2024.csv"

# -----------------------------------------------------
# 2. Create output directories
# -----------------------------------------------------
os.makedirs("output/figures", exist_ok=True)
os.makedirs("output/tables", exist_ok=True)

# -----------------------------------------------------
# 3. Load merged dataset from CSV
# -----------------------------------------------------
print("Loading merged dataset...")

try:
    df = pd.read_csv(MERGED_CSV)
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Please ensure 04_merge.py has been run first.")
    raise

print(f"  Loaded {len(df)} industries")
print(df.to_string(index=False))

# -----------------------------------------------------
# 4. Add industry labels for readable plots
# -----------------------------------------------------
sic_labels = {
    "A": "Agriculture (A)",
    "C": "Manufacturing (C)",
    "F": "Construction (F)",
    "G": "Retail/Wholesale (G)",
    "H": "Transport (H)",
    "I": "Hospitality (I)",
    "J": "Information/Tech (J)",
    "K": "Finance (K)",
    "L": "Real Estate (L)",
    "M": "Professional Services (M)",
    "N": "Admin/Support (N)",
    "O": "Public Admin (O)",
    "P": "Education (P)",
    "Q": "Health/Social Care (Q)",
}
df["industry_label"] = df["sic_section"].map(sic_labels).fillna(
    df["sic_section"]
)

# =====================================================
# TABLE 1: Summary Statistics
# =====================================================
print("\nGenerating Table 1: Summary statistics...")

summary = df[
    ["mean_gender_pay_gap", "avg_hourly_pay", "female_employment_2024"]
].describe().round(2)

summary.index.name = "Statistic"
summary.columns = [
    "Mean Gender Pay Gap (%)",
    "Avg Hourly Pay (£)",
    "Female Employment (thousands)"
]

summary.to_csv("output/tables/summary_statistics.csv")
print(summary.to_string())
print("  Saved: output/tables/summary_statistics.csv")

# =====================================================
# TABLE 2: Correlation Matrix
# =====================================================
print("\nGenerating Table 2: Correlation matrix...")

corr_vars = df[
    ["mean_gender_pay_gap", "avg_hourly_pay", "female_employment_2024"]
].copy()
corr_vars.columns = [
    "Pay Gap (%)", "Avg Hourly Pay (£)", "Female Employment"
]
corr_matrix = corr_vars.corr().round(3)

corr_matrix.to_csv("output/tables/correlation_matrix.csv")
print(corr_matrix.to_string())
print("  Saved: output/tables/correlation_matrix.csv")

# =====================================================
# FIGURE 1: Bar Chart — Gender Pay Gap by Industry
# =====================================================
print("\nGenerating Figure 1: Gender pay gap by industry...")

bar_data = df.sort_values("mean_gender_pay_gap", ascending=True)

fig, ax = plt.subplots(figsize=(10, 7))

colors = [
    "#d73027" if x > 15 else "#fc8d59" if x > 10 else "#91bfdb"
    for x in bar_data["mean_gender_pay_gap"]
]

bars = ax.barh(
    bar_data["industry_label"],
    bar_data["mean_gender_pay_gap"],
    color=colors,
    edgecolor="white",
    height=0.6
)

ax.axvline(x=0, color="black", linewidth=0.8)
ax.set_xlabel("Mean Gender Pay Gap (%)", fontsize=11)
ax.set_title(
    "Figure 1: Mean Gender Pay Gap by Industry (UK, 2024)",
    fontsize=12, fontweight="bold", pad=12
)
ax.grid(axis="x", alpha=0.3)

# Add value labels on bars
for bar, val in zip(bars, bar_data["mean_gender_pay_gap"]):
    ax.text(
        val + 0.2,
        bar.get_y() + bar.get_height() / 2,
        f"{val:.1f}%",
        va="center", fontsize=8
    )

# Legend
high   = mpatches.Patch(color="#d73027", label="Gap > 15%")
medium = mpatches.Patch(color="#fc8d59", label="Gap 10–15%")
low    = mpatches.Patch(color="#91bfdb", label="Gap < 10%")
ax.legend(handles=[high, medium, low], loc="lower right", fontsize=9)

plt.tight_layout()
plt.savefig(
    "output/figures/pay_gap_by_industry_bar.png",
    dpi=150, bbox_inches="tight"
)
plt.close()
print("  Saved: output/figures/pay_gap_by_industry_bar.png")

# =====================================================
# FIGURE 2: Scatter — Pay Gap vs Average Hourly Pay
# =====================================================
print("\nGenerating Figure 2: Pay gap vs average hourly pay...")

fig, ax = plt.subplots(figsize=(9, 6))

ax.scatter(
    df["avg_hourly_pay"],
    df["mean_gender_pay_gap"],
    color="#2c7bb6", s=80, alpha=0.8, edgecolors="white", zorder=3
)

# Label each point with SIC section letter
for _, row in df.iterrows():
    ax.annotate(
        row["sic_section"],
        (row["avg_hourly_pay"], row["mean_gender_pay_gap"]),
        textcoords="offset points", xytext=(6, 3),
        fontsize=9, color="#444444"
    )

# Trend line
z = np.polyfit(df["avg_hourly_pay"], df["mean_gender_pay_gap"], 1)
p = np.poly1d(z)
x_line = np.linspace(
    df["avg_hourly_pay"].min(),
    df["avg_hourly_pay"].max(), 100
)
ax.plot(x_line, p(x_line), "r--", alpha=0.6,
        linewidth=1.5, label="OLS trend line")

# Correlation annotation
corr = df["avg_hourly_pay"].corr(df["mean_gender_pay_gap"])
ax.text(
    0.05, 0.92, f"r = {corr:.3f}",
    transform=ax.transAxes, fontsize=10,
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8)
)

ax.set_xlabel("Average Hourly Pay (£)", fontsize=11)
ax.set_ylabel("Mean Gender Pay Gap (%)", fontsize=11)
ax.set_title(
    "Figure 2: Gender Pay Gap vs Average Hourly Pay by Industry",
    fontsize=12, fontweight="bold"
)
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(
    "output/figures/pay_gap_vs_avg_wage_scatter.png",
    dpi=150, bbox_inches="tight"
)
plt.close()
print("  Saved: output/figures/pay_gap_vs_avg_wage_scatter.png")

# =====================================================
# FIGURE 3: Scatter — Pay Gap vs Female Employment
# =====================================================
print("\nGenerating Figure 3: Pay gap vs female employment...")

fig, ax = plt.subplots(figsize=(9, 6))

ax.scatter(
    df["female_employment_2024"],
    df["mean_gender_pay_gap"],
    color="#1a9641", s=80, alpha=0.8, edgecolors="white", zorder=3
)

for _, row in df.iterrows():
    ax.annotate(
        row["sic_section"],
        (row["female_employment_2024"], row["mean_gender_pay_gap"]),
        textcoords="offset points", xytext=(6, 3),
        fontsize=9, color="#444444"
    )

# Trend line
z = np.polyfit(df["female_employment_2024"], df["mean_gender_pay_gap"], 1)
p = np.poly1d(z)
x_line = np.linspace(
    df["female_employment_2024"].min(),
    df["female_employment_2024"].max(), 100
)
ax.plot(x_line, p(x_line), "r--", alpha=0.6,
        linewidth=1.5, label="OLS trend line")

# Correlation annotation
corr = df["female_employment_2024"].corr(df["mean_gender_pay_gap"])
ax.text(
    0.05, 0.92, f"r = {corr:.3f}",
    transform=ax.transAxes, fontsize=10,
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8)
)

ax.set_xlabel("Female Employment (thousands, 2024 average)", fontsize=11)
ax.set_ylabel("Mean Gender Pay Gap (%)", fontsize=11)
ax.set_title(
    "Figure 3: Gender Pay Gap vs Female Employment by Industry",
    fontsize=12, fontweight="bold"
)
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(
    "output/figures/pay_gap_vs_female_employment_scatter.png",
    dpi=150, bbox_inches="tight"
)
plt.close()
print("  Saved: output/figures/pay_gap_vs_female_employment_scatter.png")

# =====================================================
# OLS REGRESSION
# Model: PayGap_i = b0 + b1*AvgWage_i
#                     + b2*FemaleEmployment_i + e_i
# As specified in README methodology
# =====================================================
print("\nRunning OLS regression...")

# Rename columns to match formula syntax
reg_data = df.rename(columns={
    "mean_gender_pay_gap":    "PayGap",
    "avg_hourly_pay":         "AvgWage",
    "female_employment_2024": "FemaleEmployment"
})

# Model 1: bivariate baseline
model1 = smf.ols("PayGap ~ AvgWage", data=reg_data).fit()

# Model 2: full specification from README
model2 = smf.ols(
    "PayGap ~ AvgWage + FemaleEmployment", data=reg_data
).fit()

print("\nModel 1: PayGap ~ AvgWage")
print(model1.summary())
print("\nModel 2: PayGap ~ AvgWage + FemaleEmployment")
print(model2.summary())

# =====================================================
# TABLE 3: Regression Results
# =====================================================
print("\nGenerating Table 3: Regression results...")

def significance_stars(p):
    if p < 0.01:   return "***"
    elif p < 0.05: return "**"
    elif p < 0.1:  return "*"
    else:          return ""

reg_results = pd.DataFrame({
    "Variable":     model2.params.index,
    "Coefficient":  model2.params.values.round(4),
    "Std_Error":    model2.bse.values.round(4),
    "t_stat":       model2.tvalues.values.round(3),
    "p_value":      model2.pvalues.values.round(3),
    "CI_Lower_95":  model2.conf_int()[0].values.round(4),
    "CI_Upper_95":  model2.conf_int()[1].values.round(4),
})
reg_results["Significance"] = reg_results["p_value"].apply(significance_stars)

reg_results.to_csv("output/tables/regression_results.csv", index=False)
print(reg_results.to_string(index=False))
print(f"\n  R-squared:     {model2.rsquared:.3f}")
print(f"  Adj R-squared: {model2.rsquared_adj:.3f}")
print(f"  N:             {int(model2.nobs)}")
print("  Saved: output/tables/regression_results.csv")

# =====================================================
# FIGURE 4: Regression Coefficient Plot
# =====================================================
print("\nGenerating Figure 4: Regression coefficient plot...")

plot_vars = reg_results[reg_results["Variable"] != "Intercept"].copy()

fig, ax = plt.subplots(figsize=(8, 5))

colors = [
    "#d73027" if p < 0.05 else "#91bfdb"
    for p in plot_vars["p_value"]
]

y_pos = range(len(plot_vars))

ax.barh(
    y_pos,
    plot_vars["Coefficient"],
    xerr=[
        plot_vars["Coefficient"] - plot_vars["CI_Lower_95"],
        plot_vars["CI_Upper_95"] - plot_vars["Coefficient"]
    ],
    color=colors,
    align="center",
    alpha=0.85,
    ecolor="black",
    capsize=6
)

ax.axvline(x=0, color="black", linewidth=1.2)
ax.set_yticks(y_pos)
ax.set_yticklabels(
    ["Avg Hourly Pay (£)", "Female Employment (thousands)"],
    fontsize=10
)
ax.set_xlabel("OLS Coefficient (with 95% CI)", fontsize=11)
ax.set_title(
    f"Figure 4: OLS Regression Coefficients\n"
    f"PayGap ~ AvgWage + FemaleEmployment  "
    f"(R\u00b2 = {model2.rsquared:.3f}, N = {int(model2.nobs)})",
    fontsize=11, fontweight="bold"
)

# Significance stars on bars
for i, (_, row) in enumerate(plot_vars.iterrows()):
    s = significance_stars(row["p_value"])
    if s:
        ax.text(
            row["Coefficient"], i + 0.15, s,
            ha="center", fontsize=12, color="black"
        )

# Legend
sig_patch   = mpatches.Patch(color="#d73027", alpha=0.85, label="p < 0.05")
insig_patch = mpatches.Patch(color="#91bfdb", alpha=0.85, label="p >= 0.05")
ax.legend(handles=[sig_patch, insig_patch], loc="lower right", fontsize=9)
ax.grid(axis="x", alpha=0.3)

plt.tight_layout()
plt.savefig(
    "output/figures/regression_coefficients_plot.png",
    dpi=150, bbox_inches="tight"
)
plt.close()
print("  Saved: output/figures/regression_coefficients_plot.png")

# =====================================================
# Final summary
# =====================================================
print("\n" + "=" * 55)
print("✓ Analysis complete!")
print("=" * 55)
print("\nOutputs saved:")
print("  output/tables/summary_statistics.csv")
print("  output/tables/correlation_matrix.csv")
print("  output/tables/regression_results.csv")
print("  output/figures/pay_gap_by_industry_bar.png")
print("  output/figures/pay_gap_vs_avg_wage_scatter.png")
print("  output/figures/pay_gap_vs_female_employment_scatter.png")
print("  output/figures/regression_coefficients_plot.png")