# Review of r5-foundry-001 (study `foundry`)

Reviewed by the runner Mac before the job started. Code: `round5/foundry` at 22134cfd9
(new study code), plus the bundled `vw1`, `integrate`, `spec` and `level0`.
Method: three reviewers (resources and time at compile level; safety and outputs;
correctness), each finding checked by a skeptical second reviewer. All stage functions
were lowered and compiled on CPU at full shapes.

**Verdict: fine to run. No blocker or major findings; three minor points for the next
version.**

## Memory and the 2^31 limit (checked at compile level)

| Stage | Temp memory | Largest array (fraction of 2^31) |
|---|---|---|
| Screen chunk, 128 draws | 9.10 GiB | 268,435,456 (0.125) |
| Certification, 24 worlds | 8.87 GiB | 301,989,888 (0.141) |
| Controls | 2.28 GiB | 79.6M |
| Gliders, screen size | 4.89 GiB | 603,979,776 (0.281) |
| Gliders, cert size | 14.33 GiB | 1,811,939,328 (0.844) |

- **Largest array:** in the cert-size gliders run, the batched scatter indices of the
  Flow-Lenia reintegration (`s32[452984832,4]`), created by XLA's scatter normalisation.
  It is below 2^31, but with only 16% headroom: `N_GLID2` >= 10 would cross it.
- **Peak:** about 19 GiB including cuFFT workspace, against about 30 GiB usable on an
  A100 40GB. The out-of-memory halving should never trigger. It catches compile-time and
  run-time out-of-memory errors, is bounded at 4 attempts, and cannot loop.
- **No captured device constants:** only small numpy tables are captured; data are
  passed as arguments.

## Time

- **Work per unit:** the job is memory-bound. On an A100 40GB: screen chunk about
  24-32 s (so about 64 chunks, all 8192 draws, before 2700 s), certification run
  21-28 s, controls 6-8 s, gliders 58-79 s and 135-185 s, each plus 1-2 min to compile.
- **Expected end:** about 2600-3300 s on `job.sh`'s clock, against the kill at about
  6240 s.
- **Deadlines:** the screen is checked per chunk, certification per run, and controls and
  gliders at stage start. Outputs are written incrementally, so earlier stages survive a
  kill.

## Minor

1. **The cert-size gliders run has no time guard of its own** (`job.py:345-347`). Only
   `el() < T_LATE` gates it, and it is the longest unit. It overruns the kill only if a
   screen chunk takes about 200 s (about 7x slower than estimated). Guard it with
   `el() + ~2.5 x (screen-size gliders seconds) < T_LATE`.
2. **A stage's `job_state` entry is written only when the whole stage returns**
   (`job.py:344, 369-374`). If the cert-size gliders run is killed or raises,
   `ref_gliders.npz` is on disk but `job_state.json` has no `gliders`, `ok` or
   `seconds_total`. `analyze.py:296` then fails with KeyError before writing anything, so
   the screen, certification and controls analysis would also need a hand patch. The data
   files survive.
3. **Certification has no out-of-memory fallback** (`job.py:291, 302`), although its
   memory (8.87 GiB) is the same size class as the screen chunk that does have one. If
   the GPU ever needed the screen's halving, certification would likely fail too.

## Info

4. job.py exits 1 after any recorded error, including a recovered screen OOM and optional
   stages.
5. A fatal error late in the screen discards the selection and certification of every
   finished chunk (`job.py:399`).
6. Fill-in candidates are ranked by 'moved' regardless of type, so they can include
   invalid, point or noisy worlds (`job.py:278`).
7. `member_ticks_per_s_steady` is wrong if the chunk was halved.
8. Writes go straight to their final names, not through a temp file and rename;
   `job_state.json` is rewritten after every screen chunk.

## Safety and outputs (clean)

- **Code:** no network, subprocess, eval or pickle, and no credential reads.
- **Writes:** stay in OUT.
- **GPU requirement:** `FOUNDRY_REQUIRE_GPU=1` is set.
- **Outputs:** under the per-file and per-job limits by construction.
- **Exam material:** none (this is track 1).
