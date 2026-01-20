# GitHub Actions (Python-Based Automation)

This approach used GitHub Actions with scheduled cron triggers
to run a Python script every 15 minutes.

## Characteristics
- Fully cloud-based
- No dependency on local machine
- Free-tier GitHub-hosted runners

## Observed Issues
- Skipped cron executions
- Delays of 30–90 minutes
- No SLA for high-frequency schedules

## Execution Details

The GitHub Actions workflow installs dependencies from
`requirements.txt` and executes `update_crypto_sheet.py`
on a scheduled cron trigger.

## Outcome
Suitable for non-critical automation, unreliable for time-sensitive ingestion.
