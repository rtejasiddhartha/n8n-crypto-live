# Phase 1: Data Preparation & Quality Handling

## Objective

The goal of Phase 1 is to transform a **raw, unreliable ingestion dataset**
into an **analytically usable and explainable dataset**, without masking
or artificially correcting real-world ingestion issues.

This phase focuses on **understanding, documenting, and handling data quality**
rather than modeling or visualization.

---

## Input Dataset

Source: 00_foundation_crypto_ingestion/data_samples/Crypto_Data.xlsx

This dataset was generated via multiple ingestion pipelines and intentionally
contains real-world issues such as missing intervals, execution delays,
and inconsistencies.

---

## Key Activities in This Phase

- Dataset profiling and schema validation
- Timestamp normalization and interval analysis
- Missing interval detection (not blind filling)
- Duplicate and anomaly identification
- Column-level data dictionary creation
- Cleaned dataset generation with auditability

---

## Design Principles

- **No silent fixes** — every transformation is documented
- **Preserve raw truth** — missing data is identified, not hidden
- **Explainability first** — business and technical clarity over aesthetics
- **Separation of layers** — raw vs cleaned data clearly separated

---

## Outputs

This phase produces:
- A documented data dictionary
- One or more cleaned datasets suitable for analytics
- Clear justification for all transformations

These outputs serve as inputs for **Phase 2: Cloud Data Warehousing**.