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

## Pipeline Attribution & Operational Context

The raw crypto dataset was generated using multiple ingestion pipelines
during distinct time periods. Pipeline attribution was not captured
explicitly at row level during ingestion, but the following operational
timeframes are known with high confidence:

### Ingestion Timeline

- **n8n Local Execution**
  - Period: 2025-07-17 11:30:57 → 2025-08-05 12:00:33
  - Characteristics:
    - Dependent on laptop uptime
    - Terminal-based execution
    - Frequent interruptions due to sleep, shutdowns, and power constraints

- **n8n Dockerized Execution**
  - Period: 2025-08-05 12:30:41 → 2025-08-31 00:00:10
  - Characteristics:
    - Improved stability over terminal execution
    - Required continuous laptop uptime
    - Increased CPU load, heat, and battery drain
    - Eventually discontinued due to hardware constraints

- **GitHub Actions (Python-Based Automation)**
  - Period: 2025-08-31 00:13:19 → 2025-10-04 14:45:03
  - Characteristics:
    - Fully cloud-based execution
    - No local machine dependency
    - Cron scheduling delays and skipped runs observed

### Interpretation Notes

Pipeline attribution is inferred based on execution periods and is treated
as **operational context**, not an absolute guarantee at individual row level.

Observed ingestion gaps and delay severity should be interpreted as a
combination of:
- Pipeline characteristics
- Runtime constraints
- Free-tier scheduling limitations

These factors are intentionally preserved as part of realistic data quality analysis.

## Gap Severity vs Pipeline Insights

A cross-analysis of ingestion gap severity by pipeline reveals clear
operational trade-offs:

- **n8n local execution** shows the highest rate of severe outages (>60 min),
  primarily due to laptop sleep, shutdowns, and power constraints.
- **n8n Docker execution** delivers the most consistent short-interval
  execution (≤15 min), confirming improved reliability through containerization,
  albeit at higher local resource cost.
- **GitHub Actions** removes local hardware dependency but exhibits frequent
  minor delays (15–30 min) and occasional severe gaps, attributable to cron
  scheduling drift and runner availability.

These findings quantitatively validate the architectural evolution decisions
documented in Phase 0.

## Outputs

This phase produces:
- A documented data dictionary
- One or more cleaned datasets suitable for analytics
- Clear justification for all transformations

These outputs serve as inputs for **Phase 2: Cloud Data Warehousing**.