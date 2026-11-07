# GPU spending ledger (PhySim v2 program)

Approved by the project lead on 7 Nov 2026: up to $1,000 in total for GPU rental on Prime.
Each job states its own cap before it starts, records the wallet balance before and after, and terminates every pod
it created. Spot instances are used only when the job checkpoints.

Access note: these cloud sessions reach pods by SSH tunnelled through the session's HTTPS proxy (HTTP CONNECT to
port 22 is allowed; direct outbound port 22 is refused).

| date | job | session | GPU | hours | cost (USD) | cap (USD) | result |
|---|---|---|---|---|---|---|---|
