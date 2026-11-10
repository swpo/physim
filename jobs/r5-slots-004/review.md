# Review of r5-slots-004 (study `slots`, full job)

Reviewed by the runner Mac before the job started. Code: `round5/slots` at 7099a0ded.
Compared with the pilot code reviewed at e5d146ef3; the diff covers commits e139c34f3
and 7099a0ded. Method: three reviewers (size and memory at compile level; time and the
review fixes; safety and outputs), each finding checked by a second, skeptical reviewer.
Every jitted function was lowered and compiled with abstract full-size shapes in a CPU
venv with the job's exact versions.

**Verdict: fine to run. The 2^31 blocker from the pilot review is fixed, and every other
point from that review is addressed.**

## The 2^31 fix, checked at compile level

- Largest argument: X per half, 946,864,128 elements (0.44 of 2^31). This is the
  requester's "largest planned 9.47e8".
- Largest tensor inside any function, across all 14 `S5_KEEP` configs: 603,979,776 (0.28
  of 2^31), the rec decoder hidden layer in validation.
- Training chunks: set/self families 138,412,032; rec families 402,653,184.
- Validation now runs one trajectory at a time: the compiled HLO has a while loop over the
  8 validation trajectories around a 300-tick scan. The old
  `f32[4,8,301,32,32,288]` (2.84e9) is gone.
- No embedded constant is larger than 16,384 elements, so device data reach every
  function as arguments.

## Memory and time

- **Device peak:** about 33-35 GiB (10.4 GiB resident data plus up to 24.7 GiB
  training temp, CPU estimate). That fits 80 GB cards (about 59.5 GiB usable) and the
  H200.
- **Training memory is higher than the pilot's:** the 3x3 token layer is now nine K=32
  matmuls instead of one concat and a K=288 matmul, which adds about 4 GiB of training
  temp. So the pilot's 23.8 GB peak and its 9.6 s per 100 steps no longer bound the full
  job exactly.
- **Configs:** about 700-900 s each with compile, encode and objective values. Expect 8-11
  of the 14 to train before 8400 s, in the listed priority order.
- **Latest end of job.sh:** expected 9000-9300 s, worst case about 9780 s (workers are killed
  at 9750 s). The margin to the runner's kill is at least about 600 s.
- **Cost:** worst case about $20.1 on the H200 at $6.69/h, under the $21.80 cap.

## Review fixes (all confirmed)

- **No certification of initial weights:** a config cut before its first accepted
  checkpoint is certified from its last finite validation state. One with no finite
  state is not certified and goes to `train_errors.txt`. Cuts are flagged by
  `checkpoint`, `cut_by_deadline` and `steps_planned` in the train JSON and in each Phi's
  meta.
- **Hard limit for certification workers:** they are killed at `S5_HARD_S` = 9750 s.
- **DONE marker:** `job.sh` touches `lat/DONE` whatever strain's exit code, and strain also
  writes it in `finally`.
- **`claim()` race:** fixed (`getmtime` inside `try/except OSError`).
- **GPU-backend check:** runs before ssim; the only bypass is `S5_ALLOW_CPU=1`.
- **stopcarry:** now effective. On CPU the forward pass is identical but the gradients
  differ (relative squared difference 0.61), so `sam_set_sg` really trains differently
  from `sam_set`.

## Minor

1. **The config still training at `S5_TRAIN_S` loses its objective values.** The training
   loop stops at 8400 s and the latents are encoded and saved. But `objective_values`
   checks the same deadline before each objective (`strain.py:358-361`), so all three are
   written as null in `objval/<name>.json` and `combined.json`. That happens although the
   cert deadline is 700 s later and the heads need about 75-150 s. Expect the last
   trained config (probably about the 9th) to show null objective values.

## Info

2. A `_ws` config cut before its warm-up ends (about step 375) is certified with its
   unchanged initial encoder, copied from `sam_sup`. It is flagged, but read it with care.
3. strain itself has no hard time limit in `job.sh`. It stops by itself at about 8570 s,
   and the workers' kill at 9750 s bounds the run.
4. With 8-11 configs before the deadline, the stopcarry config (`sam_set_sg`, 14th) and
   most warm-start configs will probably not run in this job.
5. **Size guard is a hand-written list:** the 2^31 guard (`fits()`) checks a list of
   shapes, not the compiled program. It would not catch a new large intermediate inside
   a jitted function. Checking `lower(...).as_text()` result types would.
6. Certification throughput depends on the pod's vCPU count, which the request does not
   constrain: 13 workers on a 16-vCPU H200, 23 on a 26-vCPU card.
7. `items/*.npz` is written before its cert JSON, and not atomically.

## Safety and outputs (clean)

- No network, subprocess, eval, pickle or credential reads, and every `np.load` runs
  without `allow_pickle`.
- `job.sh` does not run `sfetch.sh`, `ssummary.py` or `sfigs.py`.
- Imports resolve inside the bundle. The fixed `/home/user/evalwork` prepends are
  harmless on the pod.
- No exam material: only public `A_gliders` parameters and designer seeds are used.
