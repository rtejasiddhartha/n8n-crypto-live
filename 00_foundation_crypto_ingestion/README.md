# Phase 0: Crypto Data Ingestion & Reliability Exploration

## Background & Motivation

Phase 0 originated from an attempt to build a **24/7 crypto market automation system**
using only **free and open tools**.

The original objective was simple but ambitious:

- Fetch real-time crypto data from the **CoinGecko API**
- Persist data into **Google Sheets** for analytics
- Send alerts to **Telegram**
- Execute automatically every **15 minutes**, without manual intervention

What started as a straightforward automation task quickly evolved into a
**data ingestion and reliability experiment**, exposing important operational
limitations of free-tier tooling.

This phase documents **how the raw dataset was created**, not how it was cleaned.

---

## Ingestion Approaches Evaluated

To achieve the same ingestion goal, **multiple automation approaches** were implemented
and tested:

### 1. n8n – Local Execution (Terminal, Port 5678)
- Executed using `n8n start`
- Cron trigger every 15 minutes
- API fetch → transformation → Google Sheets → Telegram
- Dependent on terminal session and laptop uptime

### 2. n8n – Dockerized Execution (Port 5679)
- n8n executed inside a Docker container with persistent volumes
- Improved stability over terminal-based execution
- Continued running without an open terminal

### 3. GitHub Actions – Python-Based Automation (Active)
- Python script executed via GitHub Actions on a cron schedule
- Fully cloud-based execution using GitHub-hosted runners
- Same ingestion logic implemented using code instead of n8n nodes

All three approaches targeted the **same business logic and data destination**,
but exhibited very different runtime characteristics.

---

## Script Ownership Clarification

The file: 00_foundation_crypto_ingestion/methods/github_actions/update_crypto_sheet.py

belongs **exclusively to the GitHub Actions ingestion pipeline**.

- It is executed by the workflow defined in: .github/workflows/crypto-update.yml
- Dependencies are installed from: 00_foundation_crypto_ingestion/methods/github_actions/requirements.txt

n8n-based ingestion approaches **do not use this Python script** and instead rely on
embedded JavaScript logic inside n8n workflow nodes.

---

## Why Multiple Approaches Were Required

All ingestion methods were implemented using **free-tier tools only**, which introduced
unavoidable constraints:

- Laptop shutdowns or sleep interruptions
- Terminal session dependency (local n8n)
- Lack of guaranteed always-on infrastructure
- GitHub cron scheduling delays and skipped executions

As a result, **no single approach produced perfectly consistent 15-minute intervals**.

Rather than hiding or correcting these issues prematurely, the project intentionally
**preserves these inconsistencies** to reflect how real-world raw ingestion data behaves.

Exported n8n workflow JSON files are included under `methods/` as **verifiable evidence**
of local and Docker-based experimentation.

---

## Phase 0 Output Dataset

The primary output of Phase 0 is: data_samples/Crypto_Data.xlsx

This Excel file represents a **merged raw output** from multiple ingestion pipelines
and is expected to contain:

- Missing 15-minute intervals
- Delayed or irregular timestamps
- Inconsistent execution gaps
- Occasional duplicate or near-duplicate records

These characteristics are **intentional** and form the starting point for
**Phase 1: Data Preparation**.

---

## Logical Workflow Reference

The file: assets/n8n_ingestion_logical_workflow.png

illustrates the **shared logical ingestion workflow** used by both local and
Docker-based n8n executions.  
It represents the business logic independent of runtime environment.

---

## Key Takeaway

> Data reliability is an operational problem, not just a coding problem.  
> Phase 0 focuses on understanding *how data fails* before attempting to fix it.
