# n8n Local (Terminal-Based Execution)

This approach used `n8n start` executed directly from the local terminal
to run a cron-triggered workflow every 15 minutes.

## Characteristics
- Rapid setup and testing
- Cron-based triggers
- API → Google Sheets integration

## Limitations
- Terminal had to remain open
- Laptop sleep or shutdown stopped execution
- No persistence or recovery

## Proof of Implementation

The file `workflow_local_5678.json` is an exported n8n workflow
executed on a local n8n instance (`n8n start`, port 5678).

This workflow was actively used during early experimentation.

## Outcome
Useful for experimentation, but unsuitable for continuous unattended execution.
