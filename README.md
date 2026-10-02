# Product Feed Consistency Auditor

Checks product feed scan counts for missing identifiers, invalid prices, currency, and feed freshness.

## How it works

`agent.py` applies the explicit rules in `RULES`, returns each failed rule with observed evidence and a review action, and derives status from the findings. It is deterministic, local-only, and uses no network or credentials.

## Run

```bash
python3 agent.py examples/good-input.json
python3 tools/audit-product-feed-consistency-auditor.py examples/good-input.json
```

## Limitations

Uses caller-declared evidence only; it cannot establish that a real-world process is complete or compliant. Human review remains required.
