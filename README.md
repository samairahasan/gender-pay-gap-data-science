# Gender Pay Gaps Across UK Industries

This project investigates why gender pay gaps vary so widely across UK industries.

It examines whether observable industry characteristics — such as average wages, workforce composition, and sector type — help explain cross-industry differences in reported gender pay gaps.

---

## Research Question
What explains variation in gender pay gaps across UK industries?

In particular, do differences in pay levels, female employment shares, and sectoral characteristics account for observed disparities in industry-level gender pay gaps?

---

## Data
The analysis combines several publicly available UK datasets:

- UK Gender Pay Gap Service: industry-level measures of the hourly gender pay gap  
- ONS / ASHE: average hourly earnings by industry  
- ONS workforce statistics: industry-level employment and female participation rates  

All datasets are harmonised using consistent industry classifications (SIC / sector groupings) to ensure comparability.

---

## Method

The analysis follows a structured data workflow:

**Raw data → Cleaning → Merging → Industry-level aggregation → Analysis**

Company-level observations are aggregated into industry-level averages to allow cross-industry comparison.

The analysis proceeds in two steps:

1. **Descriptive analysis** of gender pay gap variation across industries  
2. **Regression analysis** to examine how industry characteristics relate to the gender pay gap  

The regression framework is explanatory rather than causal, and results are interpreted accordingly.

---

## Empirical Framework

I estimate the following regression model:

PayGap_i = β0 + β1 FemaleShare_i + β2 AvgWage_i + β3 Sector_i + ε_i

Where:
- i indexes industries
- coefficients capture associations, not causal effects

---

## Project Structure

- `data/raw/`: raw datasets from ONS and Gender Pay Gap Service  
- `data/cleaned/`: processed and harmonised industry-level dataset  
- `scripts/`: reproducible Python scripts for cleaning and analysis  
- `output/figures/`: visualisations and regression outputs  
- `blog/`: final data-driven blog post  

---

## Replication

All results are fully reproducible.

To replicate:
1. Run scripts in order inside `/scripts`
2. Execute data cleaning and merging pipeline
3. Generate final industry-level dataset
4. Run analysis script to reproduce figures and regression results

All outputs are generated programmatically from raw data.
