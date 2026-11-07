# GPU spending ledger (PhySim v2 program)

Approved by the project lead on 7 Nov 2026: up to $1,000 in total for GPU rental on Prime.
Each job states its own cap before it starts, records the wallet balance before and after, and terminates every pod
it created. Spot instances are used only when the job checkpoints.

Access note (corrected 7 Nov 2026 after the first job): SSH tunnelled through the session's HTTPS proxy does not
work. The proxy answers HTTP CONNECT to port 22 with 200, but the egress proxy re-terminates TLS, so the SSH banner
exchange is reset (tested against github.com:22 and test.rebex.net:22). `/root/.ccr/README.md` lists raw TCP as
"not supported through the proxy (report, do not work around)", and direct outbound port 22 is refused. A GPU job
therefore needs a different access path (for example one that runs over HTTPS, or a session with direct network access)
before it rents a pod.

| date | job | session | GPU | hours | cost (USD) | cap (USD) | result |
|---|---|---|---|---|---|---|---|
| 2026-11-07 | vw1 GPU benchmark (gliders throughput, GPU-vs-CPU agreement, conv training step) | session_01BZceC7G6m7DgM6KpXjnWXj | none (no pod created) | 0 | 0.00 | 15 | blocked at step 1: SSH through the proxy is reset (see access note); no SSH key registered, no pod, nothing to terminate. Wallet 4866.39 before, 4866.29 after (team disk billing, not this job) |
