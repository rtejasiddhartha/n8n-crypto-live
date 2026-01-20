# Phase 0: Crypto Data Ingestion & Reliability Exploration

## Objective

The objective of Phase 0 was to generate a **raw crypto market dataset**
by running automated data ingestion jobs every **15 minutes**, using
**only free tools and services**.

Rather than assuming a single solution would work reliably, multiple
automation approaches were tested to understand **real-world operational
behavior**, including failures, delays, and data gaps.

---

## Ingestion Approaches Evaluated

Phase 0 evaluated three different ingestion methods, all serving the same goal:

1. n8n running locally via terminal
2. n8n running locally using Docker
3. GitHub Actions running Python on scheduled cron jobs

Each approach attempted to fetch crypto market data from the same source
and write results to Google Sheets, which were later consolidated.

---

## Script Ownership Clarification

The active ingestion pipeline **GitHub Actions ingestion pipeline** is implemented using GitHub Actions
and executes the Python script located at:

`00_foundation_crypto_ingestion/methods/github_actions/update_crypto_sheet.py`

It is executed exclusively by the GitHub Actions workflow
defined in `.github/workflows/crypto-update.yml`.

n8n-based ingestion approaches do not use this Python script
and instead rely on internal JavaScript logic within n8n workflows.

---

## Why Multiple Approaches Were Required

Using free-tier tooling introduced unavoidable constraints:

- Laptop shutdowns or sleep interruptions
- Terminal session dependency
- Lack of guaranteed 24/7 runtime
- GitHub cron scheduling delays and skipped executions

As a result, **no single ingestion method produced perfectly consistent
15-minute intervals**.

Instead of discarding this behavior, the project intentionally preserves
these inconsistencies to reflect **realistic raw ingestion conditions**.

Exported n8n workflow JSON files are included as evidence of
local and Docker-based experimentation.

---

## Phase 0 Output Dataset

The primary output of this phase is:

- `data_samples/Crypto_Data.xlsx`

This Excel file represents a **merged raw output from multiple ingestion runs**
and is expected to contain:

- Missing 15-minute intervals
- Delayed or irregular timestamps
- Inconsistent execution gaps
- Occasional duplicate rows

These characteristics are **intentional** and are addressed in
**Phase 1: Data Preparation**.

---

## Key Takeaway

> Data reliability is an operational problem, not just a coding problem.
> Phase 0 focuses on understanding how data fails before attempting to fix it.

The file `assets/n8n_ingestion_logical_workflow.png` illustrates the
shared logical workflow used by both local and Docker-based n8n executions.
