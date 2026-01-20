# Phase 1.2: Data Cleaning Rules & Decisions

## Purpose

This document defines the **explicit data cleaning and preparation rules**
applied to the raw crypto ingestion dataset.

The goal is to make the data **analytically usable, explainable, and auditable**
without masking or fabricating real-world ingestion issues.

No transformations are performed without justification.

---

## Input Dataset

Source file: 00_foundation_crypto_ingestion/data_samples/Crypto_Data.xlsx

Characteristics of the raw dataset:
- Generated via automated ingestion pipelines
- Contains real-world operational issues
- Optimized for human-readable alerts, not analytics

---

## Dataset Grain

**Logical grain of the dataset:**
(Coin, Updated At)

- Each row represents one snapshot of a coin at a specific ingestion time
- Multiple coins per timestamp are expected
- Repeated timestamps across different coins are valid

---

## Timestamp Handling Rules

### Source Column
Updated At

### Observations
- Stored as text/string
- Format: `YYYY-MM-DD HH:MM:SS`
- Timezone assumed to be **Asia/Kolkata**

### Rules
- Convert `Updated At` into a proper datetime column
- Preserve original text column
- No timezone shifting in Phase 1
- Missing 15-minute intervals will be **detected, not filled**

**Rationale:**  
Filling missing intervals would fabricate data that never existed.

---

## Duplicate Handling Rules

### Definition of Duplicate
A duplicate is defined as: Same Coin + Same Updated At


### Rules
- Exact duplicates will be removed
- Deduplication will keep the first occurrence
- Number of removed duplicates will be logged

**Rationale:**  
Exact duplicates add no analytical value and distort aggregations.

---

## Numeric Field Handling Rules

### Affected Columns
- Current Price
- Market Cap
- 24h Volume
- 24h Change
- Global Rank (string-formatted)

### Observations
- Values stored as text
- Includes currency symbols (`₹`)
- Uses Indian numbering format
- Includes emojis and labels

### Rules
- Original columns will be preserved unchanged
- New numeric columns will be created:
  - `current_price_numeric`
  - `market_cap_numeric`
  - `volume_24h_numeric`
  - `price_change_24h_numeric`
  - `global_rank_numeric`
- Parsing errors will be flagged, not silently dropped

**Rationale:**  
Preserving original text maintains auditability and traceability.

---

## Derived / Categorical Columns

### Columns
- Trend
- Trend Emoji
- ATH Insight
- 24h Range
- Volatility

### Rules
- These columns will **not be recalculated** in Phase 1
- Values will be treated as categorical features
- Original logic remains intact

**Rationale:**  
These fields represent business logic already applied during ingestion.
Re-derivation would introduce inconsistency.

---

## Missing Data Rules

### Rules
- Missing values will NOT be auto-filled
- Missingness will be explicitly identified and quantified
- Missing intervals will be flagged for downstream analytics

**Rationale:**  
Missing data represents operational reality and should remain visible.

---

## Column Naming Rules

### Rules
- Raw columns remain unchanged
- New columns use snake_case
- Suffix `_numeric` used for parsed numeric values
- Suffix `_parsed` used for transformed timestamps if needed

**Rationale:**  
Clear naming avoids confusion between raw and cleaned fields.

---

## Output Datasets

Phase 1 will produce:

1. **Cleaned analytical dataset**
01_data_preparation/outputs/crypto_cleaned_v1.csv

2. **Unmodified raw dataset**
- Remains in Phase 0
- Never overwritten

---

## Audit & Transparency Rules

- All transformations performed in Python
- No manual Excel edits
- All logic documented in notebooks
- Row counts before and after cleaning recorded

---

## Non-Goals of Phase 1

Phase 1 explicitly does NOT:
- Perform forecasting
- Perform anomaly detection
- Create dashboards
- Aggregate metrics
- Impute missing timestamps

These are deferred to later phases.

---

## Summary

Phase 1 prioritizes:
- Transparency over convenience
- Realism over perfection
- Reproducibility over manual fixes

This ensures downstream analytics are **trustworthy and explainable**.
