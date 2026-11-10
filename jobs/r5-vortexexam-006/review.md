# Review of r5-vortexexam-006 (study `vortexexam`, job 3; resubmission of r5-vortexexam-005)

r5-vortexexam-006 differs from 005 only in its cap ($19.60, which covers $6.69/h x 2.9 h) and its ref (f5daa4978). Between the two refs only local tools (`analyse2.py`, `make_summary.py`, `offline_views.py`), `PROGRESS.md` and `results/` changed. `job2.py`, `vxlib.py`, `vxnet.py`, `vxsbi.py` and `prior_B.json` are identical, and job2 imports none of the changed tools. The review of 005 below applies.

Reviewed by the runner Mac before the job started. Code: `round5/vortexexam` at b6de3c6e9.
Compared with job 2's code (84550bc04, r5-vortexexam-003), which was reviewed in full and
ran cleanly. `vw1`, `agentenv` and `vortex_world` are unchanged since then.
Method: one reviewer over the whole delta, with findings checked by a skeptical second
reviewer. Local CPU run: `job2.py --smoke --prior prior_B.json --smoke-names eps,mu,e`
exit 0. Without `--smoke` on CPU it stops at the GPU assert (exit 1) and writes only
`progress.txt`.

**Verdict: the gate is met and the job is fine to run. No blocker, major or minor
findings. The review of job 2 has been acted on.**

## Gate (met)

- **GPU backend:** asserted at `job2.py:272-273`, before `Secret()`, `Runner(H)` and the
  rate stage. `--smoke` is the only bypass.
- **Per-file limit:** `save_npz` flags any file over 19 MiB. The audit deletes
  over-limit files, and anything beyond the 40 MiB total, and flags each deletion. Any
  flagged failure gives a non-zero exit.
- **Sizes at `xl`:** each `design_S` part is about 3.6 MB, `scores.npz` about 4.4 MB,
  everything else smaller. The total is about 22 MB (at most about 32 MB raw). No file
  comes near 19 MiB.

## Secrecy and markers (clean)

- `Secret()` comes from `os.urandom`, and only its commitment is written. The uses of the
  secret are unchanged from job 2.
- Every npz in the smoke output contains `PILOT_NEVER_REUSE_AS_EXAM`, and every JSON
  carries it at the top level, as does every entry of `lab.json`. This acts on job 2's
  marker finding.

## Presets and time

- **Work per preset:** xl 1,735,168; full 1,045,664; mid 773,184; mid2 620,888;
  low 480,016; small 293,504 member-ticks.
- **Choice:** `xl` is chosen from about 264 member-ticks/s, `full` from about 159. The
  H200 (444/s) gets `xl`, about 5400 s end to end; an A100 (169/s) gets `full`.
- **Efficiency:** the claimed 0.96-0.97 matches job 2's log (episodes 0.978, replicates
  0.955, controls 0.98).
- **Deadlines:** every simulated timeline ends inside `--max-hours` (8640 s) and the
  9480 s kill, including `xl` at 0.7 of the benchmark rate.
- **Tensors:** all far below 2^31. The largest is the P0 dataset, about 64 million
  elements. No device constants are captured in jit closures.

## New policies and prior B (checked)

- `lag_mask(3, ...)` keeps lags 0-2 and zeroes the rest. The warm start shapes match
  (P0 `n_in` = 107 = the dedicated datasets'), and the start is the first early-stopping
  candidate.
- The new families come after the original four, so the earlier families' random draws
  are unchanged.
- `prior_B.json` differs from `prior.json` only in names, boxes and selection metadata.
  The chosen set (eps, mu, e) matches job 1's headroom table. `select_prior.py` is not
  run in this job.

## Info

1. On an A100 near 169/s, whether the no-input controls run depends on about 140 s of
   timing (`job2.py:550-552`). The preset sizing assumes the controls run, but the later
   check prices them at 0.8 x rate plus 1500 s. So on `full` at 165-168/s, or on `xl` at
   264-280/s, they are skipped: logged as 'skipped input controls', exit 0. On the H200
   there is a margin of about 2600 s.
