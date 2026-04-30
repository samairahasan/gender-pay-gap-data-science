# Explaining Variation in Gender Pay Gaps Across UK Industries

Do industry characteristics help explain variation in the UK gender pay gap?

## 📖 Blog Post
https://hackmd.io/@samairahasan/H1OjthlRWl
---

## Goal

Gender pay gaps persist across the UK labour market, but vary substantially across industries.

While economy-wide explanations are well documented, less is known about whether observable industry characteristics help explain why some sectors exhibit larger pay gaps than others.

The goal of this project is to assess whether differences in average pay levels, female employment, and industry sector characteristics help explain cross-industry variation in reported gender pay gaps.

---

## Solution

I construct an industry-level dataset combining multiple UK administrative data sources and examine whether industry characteristics are systematically associated with gender pay gaps.

The analysis proceeds in three steps:

1. Clean and harmonise datasets using consistent SIC classifications  
2. Merge industry datasets using validated one-to-one joins and integrity checks  
3. Analyse cross-industry variation using descriptive statistics, visualisation, and OLS regression  

The empirical framework is descriptive and explanatory, rather than causal.

---

## Workflow

The project follows a modular and reproducible pipeline, where each script performs a single function and feeds into the next stage.

---

## Details

### Inputs and Outputs

#### Inputs
- Firm-level gender pay gap data (2024)  
- Average gross hourly pay by industry (2024)  
- Female employment by industry (quarterly 2024)  

#### Outputs
- Harmonised industry-level dataset  
- SQLite database  
- Summary statistics  
- Correlation matrix  
- Regression results  
- Analytical figures  

---

## Description of Methodology

The analytical dataset is constructed in four stages.

### 1. Data Cleaning and Harmonisation

The project uses three cleaning scripts to harmonise SIC classifications across datasets.

This includes:
- Extracting primary firm SIC codes  
- Mapping 2-digit SIC codes into SIC sections  
- Cleaning ONS datasets containing metadata rows  
- Constructing average female employment across 2024 quarters  
- Removing invalid observations and duplicates  
- Ensuring consistent industry definitions across datasets  

**Important note:**  
The ASHE dataset contains grouped SIC categories (“B, D, E” and “R, S, T”) rather than individual SIC letters. These are excluded during cleaning to maintain consistency across datasets. This is a deliberate and transparent design choice.

---

### 2. Industry-Level Aggregation

Gender pay gaps are constructed as simple unweighted averages across reporting firms. This treats each firm equally regardless of size and is acknowledged as a limitation.

---

### 3. Data Integration and Validation

Cleaned datasets are merged using validated one-to-one inner joins.

The merge process includes:
- Standardised SIC keys  
- Post-merge validation checks  
- Missing-value verification  
- Assertion-based integrity checks  
- SQL verification of final dataset  

The SQLite database acts as a structured, queryable intermediate dataset within the analysis pipeline.

Only industries present across all datasets are retained.

---

### 4. Statistical Analysis

Two OLS models are estimated:

Baseline model:  
PayGap_i = β₀ + β₁ AvgWage_i + ε_i  

Full model:  
PayGap_i = β₀ + β₁ AvgWage_i + β₂ FemaleEmployment_i + ε_i  

where:
- PayGap = mean gender pay gap  
- AvgWage = average hourly pay  
- FemaleEmployment = average quarterly employment level  

Scatterplots include fitted linear trend lines using simple polynomial fits for visualisation purposes only (not full regression models with diagnostics).

Interpretation is associational, not causal.

---

## Analytical Outputs

The analysis script produces:

### Tables
- Summary statistics  
- Correlation matrix  
- Regression results (coefficients, standard errors, confidence intervals)  

### Figures
- Gender pay gap by industry bar chart  
- Pay gap vs average hourly pay scatterplot  
- Pay gap vs female employment scatterplot  
- Regression coefficient plot  

---

## Data Sources

All datasets are publicly available:

- Gender Pay Gap Service  
  https://gender-pay-gap.service.gov.uk/Viewing/download  

- ONS ASHE Average Gross Hourly Pay  
  https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/regionbyindustry2digitsicashetable5  

- ONS Female Employment by Industry  
  https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/employmentbyindustryemp13  

Raw data are stored in `data/raw/` and are never modified.

---

## Technical Features

- Automated data cleaning pipeline  
- SIC classification harmonisation  
- Assertion-based data validation  
- Validated one-to-one merges  
- SQLite relational storage  
- OLS regression modelling  
- Automated figure and table generation  
- Fully reproducible workflow  

---

## Running Instructions

### Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

Core packages:
- pandas  
- numpy  
- matplotlib  
- statsmodels  

---

### Running the Code

Run full pipeline:

```bash
python runAll.py
```

Or step-by-step:

```bash
python scripts/01_clean_gender_pay_gap.py
python scripts/02_clean_gross_hourly_pay.py
python scripts/03_clean_female_employment.py
python scripts/04_merge.py
python scripts/05_analysis_and_outputs.py
```

---

## Generated Files

### Data
- `data/clean/04_merged_industry_dataset_2024.csv`  
- `data/uk_gender_pay_gap_industry_2024.db`  

### SQLite Table
- `merged_data`

### Tables
- `output/tables/summary_statistics.csv`  
- `output/tables/correlation_matrix.csv`  
- `output/tables/regression_results.csv`  

### Figures
- `output/figures/pay_gap_by_industry_bar.png`  
- `output/figures/pay_gap_vs_avg_wage_scatter.png`  
- `output/figures/pay_gap_vs_female_employment_scatter.png`  
- `output/figures/regression_coefficients_plot.png`  

---

## Directory Structure

```text
├── data
│   ├── raw
│   ├── clean
│   └── uk_gender_pay_gap_industry_2024.db
├── output
│   ├── figures
│   └── tables
├── scripts
│   ├── 01_clean_gender_pay_gap.py
│   ├── 02_clean_gross_hourly_pay.py
│   ├── 03_clean_female_employment.py
│   ├── 04_merge.py
│   └── 05_analysis_and_outputs.py
├── runAll.py
└── README.md
```

---

## Important Data Notes

- Final sample includes 14 industries  
- Grouped SIC categories in employment data (“B, D, E” and “R, S, T”) are excluded for consistency  
- Female employment is measured as the average quarterly level across 2024  
- Some ONS datasets include metadata rows and require preprocessing, handled automatically in cleaning scripts  

---

## Interpretation Cautions

Given the small cross-sectional sample (n = 14 industries) and two-regressor specification, results are exploratory and should be interpreted as descriptive associations rather than structural or causal estimates.

---

## Future Extensions

- Employment-weighted aggregation  
- Additional controls (firm size, occupation, productivity)  
- Multi-year panel analysis  
- Oaxaca-Blinder decomposition  

---

## Replication

This project is fully reproducible:

- Raw data included  
- All transformations scripted  
- No manual edits  
- Running `runAll.py` reproduces all outputs  
