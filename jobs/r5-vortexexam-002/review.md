# Review of r5-vortexexam-002 (study `vortexexam`, job 1)

Reviewed by the runner Mac before the job started. Code: `round5/vortexexam` at b7beb6dff
(the r5-vortexexam-001 review). At this request's commit a38a266a6, `job1.py` is
byte-identical and `vxlib.py` only gained functions job1 never calls; `job2.py`,
`vxnet.py` and `vxsbi.py` ship in the bundle but are not run. Method: three reviewers
(safety and exam secrecy, resources and time, correctness), each finding checked by a
second reviewer. Locally, CPU `check_lib.py` PASSED and `job1.py --smoke` passed.

**Verdict: fine to run; exam secrecy clean. The runner watches the first heartbeat for a
CPU fallback.**

## Exam secrecy (clean)

- Nothing reads a secret, a key file or an env var. `vw.secret` and `vw.harness` are not
  imported (checked at runtime).
- Every key comes from the public `make_key` with literal seeds 900, 5101, 5202 and 5203.
- All 13 candidate parameters are explicit `BOX` / `THETA0` literals, and the selection
  coefficients are a literal grid. All of them are written to `info.json`, `scan.json`
  and `law.json`, with `pilot_never_reusable_as_exam: true`.
- Run under `env -i` with no HOME, it wrote only to OUT.

## Major

1. **No GPU-backend check.** `job1.py:113-119` only logs `jax.default_backend()`, and
   `vxlib.py:103` then switches to the CPU `lax.map` path. On a CPU fallback the job spends
   about 22 min on bench, starts the law stage, and is killed before `law.npz` is written,
   publishing CPU numbers as job-1 results. For this run the Mac checks the first
   heartbeat and cancels on CPU. **Job 2 must `assert jax.default_backend() == "gpu"`
   (unless smoke): the runner will not start a job-2 request without it.**

## Minor

2. **Output size.** `scan_branch.npz` (R1b, `job1.py:322-324`) is
   `f32[27,J,2,8,32,2(H/16)^2]`: about 85 MB raw at J=12 and H=128, about 18-36 MB
   compressed. The gpu-jobs branch takes at most 20 MB per file and 50 MB per job.
   Larger files stay on the Mac (`in_git: false` in `manifest.json`) and are sent on
   request. **Job 2 must keep every output file under 20 MB: the runner will not start a
   job-2 request otherwise.**
3. The level-1 'turnover' summary is forced to 0 at every 40th tick, because `summaries()`
   is computed per 40-tick chunk.
4. `bench.json`'s per-row memory is the process-wide running peak, not each row's own peak.
5. When the smallest measured batch is larger than the stage batch, the stage sizers fall
   back to the minimum sample, because the linear extrapolation makes the cost J-independent.

## Info

- Failed bench rows never affect the exit status.
- npz files are not written atomically, and `scan_branch.npz` is rewritten after each
  anchor, so a kill mid-write can leave it truncated.
- The declared prior boxes and the headroom results become public. That is fine if the
  real exam's prior is meant to be declared.
