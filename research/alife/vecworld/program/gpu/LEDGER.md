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
| 2026-11-07 | vw1-bench-001 (gliders throughput, tracker, GPU vs CPU, conv AE step) | Mac runner for session_01BZceC7G6m7DgM6KpXjnWXj | A100 80GB (datacrunch, $2.35/h) | about 0.08 billed | 0.19 | 10 | done: 1,600-1,700 member-ticks/s at B >= 64; see bench/README.md |
| 2026-11-07 | vw1-agree-001 (GPU vs CPU from one shared state) | Mac runner for session_01BZceC7G6m7DgM6KpXjnWXj | A100 80GB (datacrunch, $2.35/h) | about 0.03 billed | 0.08 | 4 | done: rounding floor 1e-14 per substep; divergence about x2,500 per tick; see bench/README.md |
| 2026-11-08 | r4-wind-001/002 (wind world full-size closure, program mix) | Mac runner (round 4 study wind) | H100 80GB (lambdalabs, $4.29/h) | 0.43 | 1.86 | 12 | done; 001 rejected on price ($0) |
| 2026-11-08 | r4-sbi-001/002 (simulate-to-train pilot) | Mac runner (round 4 study sbi) | A100 40GB (lambdalabs, $1.99/h) | 1.80 | 3.64 | 13 | done; 001 provider stock-out ($0) |
| 2026-11-08 | r4-bias-001/002/003 (inductive-bias grid on raw level 0) | Mac runner (round 4 study bias) | A100 80GB / H100 80GB | 2.51 | 7.94 | 16 | done on 003; 001 cancelled (slow gradients), 002 cancelled (out of memory: device data compiled in as constants) |
| 2026-11-10 | r5-bias2-004/005/007 (inductive-bias grid on the membrane and fed-vortex worlds, gliders anchor, whitened-latent follow-up) | Mac runner (round 5 study bias2) | H200 141GB (nebius, bills $6.69/h) x 2, A100 40GB (lambdalabs, $1.99/h) | 2.61 | 10.64 | 35 | done; 001 rejected on price, 002/003 cancelled before start (caps below the H200's billed rate), 006 provider stock-out ($0 each) |
| 2026-11-10 | r5-slots-003/007/008 (slot encoders on raw gliders states: pilot, failed run, main run) | Mac runner (round 5 study slots) | H200 141GB (nebius), A100 40GB (lambdalabs) x 2 | 3.93 | 9.52 | 25 | 003 done (pilot); 007 failed (out of memory from pool fragmentation on the 40 GB card, $1.04); 008 complete with the platform allocator, exit 1 from a table printer only; 001/004/005/006 cancelled before start, 002 stopped by the price guard ($0 each) |
| 2026-11-10 | r5-vortexexam-002/003/006 (fed-vortex exam pilot: throughput, law, headroom; pilots A and B) | Mac runner (round 5 study vortexexam) | H200 141GB (nebius), A100 40GB (lambdalabs) x 2 | 3.06 | 7.32 | 25 | done; 001 cancelled, 004 rejected (request format), 005 stopped by the price guard a tenth of a cent over its cap ($0 billed) |
| 2026-11-10 | r5-ladder-002 (difficulty ladder on the gliders wind world, nine cells) | Mac runner (round 5 study ladder) | A100 40GB (lambdalabs, $1.99/h) | 1.37 | 2.56 | 25 | done; 001 rejected by the runner's code review before any pod (array past 2^31 elements, $0) |
| 2026-11-10 | r5-foundry-001/002 (world foundry v0: screen of 8,192 draws, late-time and enrichment arms) | Mac runner (round 5 study foundry) | H100 80GB (datacrunch, $5.02/h), H200 141GB (nebius) | 0.51 | 2.47 | 25 | done |

Totals after round 5 (from `origin/gpu-jobs:ledger.json`, 10 Nov 2026): $32.51 billed in round 5, $46.27 billed in all, of $1,000 approved.
Lessons of round 5 for requests: the nebius H200 is listed at $5.55/h and bills $6.69/h (the runner now prices offers at the billed rate); size a cap as rate x (max_hours + 0.25), rounded up, plus $0.10; a CPU compile-level memory estimate is not a safe proxy for GPU validation memory; on a 40 GB card a fragmented allocator pool can fail at under 20% use (XLA_PYTHON_CLIENT_ALLOCATOR=platform avoided it); the runner publishes its code review of each job at `jobs/<id>/review.md` on the gpu-jobs branch.
