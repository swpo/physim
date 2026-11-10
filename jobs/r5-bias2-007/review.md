# Review of r5-bias2-007 (resubmission of r5-bias2-006; study `bias2`, follow-up arm `B5_ARMS=w`)

r5-bias2-007 is r5-bias2-006 unchanged (same ref, env, run and setup); only the GPU preference order differs (H200 before H100). 006 ended in infra_error before any pod existed (a Lambdalabs stock-out at create). The review of 006 below applies.

Reviewed by the runner Mac before the job started. Code: `round5/bias2` at affd4ecb2.
Compared with r5-bias2-004's code (a3096634c), which was reviewed in full and ran cleanly.

What runs on the pod changed in only four files:
- `c5.py`: the `w` arm's 8 closure configs.
- `cnets.py`: `Lw` / `Nw` map to the L / N encoders via `base_enc`, with
  `train_glob_white` in the training loss only.
- `ctrain.py`: one line (`train_whitening` recorded, `field_shares` for Lw / Nw).
- `job.sh`: probe timeouts, and a ctrain deadline stop (exit 124) is no longer a failure.

Everything else in the diff is local analysis tools (`cextra`, `cinterp`, `cclaims`,
`cpairs_run.sh`, `csummary`, `canalyze`) and committed results. `job.sh` does not run
them, and they make no network or process calls.

Local CPU run of `job.sh` at `B5_TINY=1` with this request's `B5_ARMS`, `B5_PLAN` and
`B5_JOB_HARD_S`: exit 0, FAIL=0 for all three worlds (76 / 66 / 52 halves, 0 unclaimed).
The Lw / Nw configs record `train_whitening: global`.

**Verdict: fine to run. Both points from the 004/005 review are fixed.**

## Checked

- **Encoder dispatch:** `init_enc` and `enc_parts` map `Lw`/`Nw` through `base_enc` before
  branching. The remaining `enc == "L"` tests (`cnets.py:180, 202`) apply only to the
  reconstruction objective, and this arm trains closure only. The frozen Phi keeps
  per-channel whitening (`glob_white` is true only for U), as the notes say. No code
  parses config names in a way that `Lw0_clos_c1` would break.
- **Simulation deadlines:** they are short (vortex 900 s, membrane 300 s, gliders 300 s) but
  fit the measured times: in 004/005, vortex took 250 s, membrane 104 s and gliders 69 s
  for both halves. The 85% early abort would fire within minutes if a pod were much slower.
- **Time:** realistically about 4500 s in total, against `B5_JOB_HARD_S` = 5100 s
  and the runner's kill at 5760 s.
- **Memory:** unchanged from 004/005 (peak 22.6 GB), so an A100 40GB is enough.
- **Fixes from the last review:** every pre-loop probe now runs under `timeout 120`, and a
  hung GPU probe now aborts with exit 3. A ctrain stopped at the cert deadline (exit 124)
  is now reported as a deadline stop, and `train_done.json` is written if missing.

## Info

1. **Worst case, gliders is skipped.** If vortex and membrane both run to their limits
   (each world ends at most about 690 s after its cert deadline), membrane ends at about
   4580 s. Gliders' cert deadline is then clipped to 4400 s, so the world is skipped with
   FAIL=1. Realistically vortex and membrane end well before their limits, and gliders' cert
   deadline is clipped by at most about 100 s.
2. **Exit 137 still counts as a failure.** `timeout -k 10` escalates to SIGKILL 10 s after
   SIGTERM, which gives exit 137, not 124. ctrain installs no SIGTERM handler, so a
   deadline stop should always end with 124. If it ever showed up as 137, it would still
   be reported as a failure.
