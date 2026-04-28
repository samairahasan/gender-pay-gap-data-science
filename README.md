# Explaining Gender Pay Gaps Across UK Industries
### Do industry characteristics explain variation in the UK gender pay gap?

---

## Goal

Gender pay gaps persist across the UK labour market but vary substantially across industries. While economy-wide explanations are well documented, less is known about whether **observable industry characteristics** can explain why some sectors exhibit much larger gender pay gaps than others.

The goal of this project is to assess whether differences in **average pay levels**, **female employment**, and **industry sector** help explain cross-industry variation in reported gender pay gaps in the UK.

---

## Solution

I construct an industry-level dataset combining multiple UK administrative data sources and examine whether differences in industry characteristics are systematically associated with gender pay gaps.

The approach proceeds in three steps:

1. Clean and harmonise firm-level and industry-level datasets using consistent SIC section classifications  
2. Aggregate firm-level gender pay gap data to the industry level  
3. Analyse cross-industry variation using descriptive statistics and regression analysis  

The empirical framework is **explanatory rather than causal**, and results are interpreted accordingly.

---

## Details

### Inputs and Outputs

**Inputs**
- Firm-level hourly gender pay gap data from the UK Gender Pay Gap Service (2024)
- Average gross hourly earnings by industry from ONS / ASHE (2024)
- Quarterly female employment by industry from ONS Labour Market Statistics (2024)

**Outputs**
- Harmonised industry-level dataset combining pay gaps, average wages, and female employment
- Descriptive figures illustrating variation in gender pay gaps across industries
- Regression results assessing associations between industry characteristics and pay gaps

---

### Description of the Methodology

The raw gender pay gap data are reported at the firm level and include firms operating across a wide range of industries. To enable cross-industry comparison, firms are first assigned to **SIC sections (A–U)** based on their primary SIC codes. Firm-level observations are then aggregated into industry-level averages.

Industry-level average hourly pay is obtained from the Annual Survey of Hours and Earnings (ASHE). Female employment is constructed by averaging quarterly industry-level employment figures for women across 2024. This measure captures **female employment levels rather than employment shares**, reflecting the overall scale of female participation in each industry.

Gender pay gaps are aggregated using **unweighted averages across reporting firms**, meaning that all firms contribute equally regardless of size. This approach reflects reported firm-level outcomes rather than employment-weighted effects.

The analysis proceeds in two stages. First, descriptive statistics and visualisations are used to document how gender pay gaps vary across industries. Second, regression analysis is used to examine whether industry characteristics—such as pay levels and female employment—are systematically related to the magnitude of gender pay gaps.

---

## Empirical Framework

The following industry-level regression model is estimated:

\[
PayGap_i = \beta_0 + \beta_1 FemaleEmployment_i + \beta_2 AvgWage_i + \beta_3 Sector_i + \varepsilon_i
\]

where:
- \( i \) indexes industries,
- `FemaleEmployment` measures average female employment levels in 2024,
- `AvgWage` captures mean hourly pay,
- coefficients represent **associations rather than causal effects**.

---

## Running Instructions

### Dependencies

The project is implemented in Python. Required packages are listed in the source files via `import` statements.

General setup guidance for Python environments can be found at:
- https://tilburgsciencehub.com  

---

### Running the Code

From the command line or terminal:

1. Navigate to the project directory  
2. Run the scripts sequentially from the `scripts/` directory  
3. Execute the merging and analysis scripts to reproduce results  

All outputs are generated programmatically from raw data with **no manual intervention**.

---

## Generated Files

- Cleaned industry-level datasets: `data/clean/`
- Figures and regression outputs: `output/figures/`
- Final analysis and interpretation: `blog/`

---

## Directory Structure


```txt
├── data
│   ├── clean
│   │   ├── 01_gender_pay_gap_clean_2024.csv
│   │   ├── 02_gross_hourly_pay_clean_2024.csv
│   │   ├── 03_female_employment_clean_2024.csv
│   │   └── 04_merged_industry_dataset_2024.csv
│   ├── raw
│   │   ├── 01_gender_pay_gap_raw_2024.csv
│   │   ├── 02_gross_hourly_pay_raw_2024.csv
│   │   └── 03_female_employment_raw_2024.csv
│   └── uk_gender_pay_gap_industry_2024.db
├── output
│   ├── figures
│   │   ├── pay_gap_by_industry_bar.png
│   │   ├── pay_gap_vs_avg_wage_scatter.png
│   │   ├── pay_gap_vs_female_employment_scatter.png
│   │   ├── regression_coefficients_plot.png
│   └── tables
│       ├── correlation_matrix.csv
│       ├── regression_results.csv
│       └── summary_statistics.csv
├── scripts
│   ├── 01_clean_gender_pay_gap.py
│   ├── 02_clean_gross_hourly_pay.py
│   ├── 03_clean_female_employment.py
│   ├── 04_merge.py
│   └── 05_analysis_and_outputs.py
└── README.md


## Notes on Interpretation

- Results reflect **industry-level aggregation** and mask within-industry heterogeneity  
- Female employment measures capture **levels, not shares**  
- Findings are **descriptive and explanatory**, not causal estimates  

---

## Replication

All results are fully reproducible.

Raw datasets are included for transparency and ease of replication; all analysis uses the cleaned datasets generated by the scripts in this repository.
