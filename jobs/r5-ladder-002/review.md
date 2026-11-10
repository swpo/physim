# Review of r5-ladder-002 (study `ladder`, resubmission of r5-ladder-001)

Reviewed by the runner Mac before the job started. Code: `round5/ladder` at 28263eb3e.
Only `round5/ladder` changed since r5-ladder-001 (a92093604), which was rejected for
3.6e9-element validation arrays.
Method: two reviewers (size, memory and time at compile level; correctness of the fixes),
each finding checked by a skeptical second reviewer. Local CPU presmoke
(`--smoke --sets 8 --cpu-ok`) passed in 143 s, with the pilot marker on every output
including `progress.txt`.

**Verdict: fine to run. The 2^31 blocker is fixed, and the other review points are
addressed. One minor issue remains.**

## The 2^31 fix, checked at compile level (independently of check_shapes.json)

- Every view (block, object, pop) and every net group was lowered and compiled at the full
  job's shapes:
  - cond and P0u for n = 1, 4 and 8
  - D group 0, batches 0-2, and D group 1, batches 0-1, at 8 nets each
  - the sampler in all three modes
- Largest array in any compiled program: `f32[8,32768,432]` = 113,246,208 elements
  (0.053 of 2^31), in the block view's 8-net training step.
- Block validation chunk: 28,311,552; block sampler: 42,467,328.
- These match `check_elems` exactly. The largest guarded value is 9.5x below its 2^30
  limit, so the guard refuses nothing legitimate at full size.
- Device peak: about 4.3 GB (block 8-net step 4.02 GB temp). That is about 7x headroom
  on an A100 40GB; r5-ladder-001 needed 34.5 GiB here.
- A real block D group-1 training step plus validation at full size ran on CPU: finite,
  peak RSS 5.3 GiB.

## Correctness (checked)

- **Chunked validation:** matches a per-net, per-chunk reference to 3.8e-7, and the old
  `eval_one` to 0.18%. The only difference is the noise draws; with one chunk the result
  is identical. Reversing the order of the nets permutes the outputs exactly, padding rows
  are masked, and a net with no held-out rows returns 0.
- **Failure isolation:** tested with injected failures in a D batch, an object sampler, the
  pop dataset and the block report. The job exits 2, every failure is recorded in
  `info.json` and `progress.txt`, and `scores.npz`, `train_info.json` and
  `prediction.json` are still written for the rest.
- **Time:** about 3.64 million member-ticks (`estimate_ticks`), about 57 minutes of
  simulation at r4-sbi-002's A100 rates. The whole job comes to about 1.75-1.9 h, well
  under the 2.6 h script limit and the kill.

## Minor

1. **The public `run.log` lists the pilot truths without the marker.**
   `run_ladder.py:70-72` writes the PILOT_NEVER_REUSE_AS_EXAM line only into
   `OUT/progress.txt`. But `log()` prints every line to stdout, including line 269
   (`n={n} truths [...]`), and the runner publishes stdout as `jobs/<id>/logs/run.log`.
   Every file in OUT is marked; this log is the one gap. Fix for next time: also print
   the marker line to stdout at startup.

## Info

2. After the script deadline, the rest of the current view still runs: each remaining
   unit gets 250 steps and one validation pass, and scoring and the report have no budget.
   The worst case is about 3-5 minutes past T_END, inside a kill margin of at least about
   230 s (normally 660-840 s).
3. A slow GPU presmoke now aborts the whole job, because a deadline skip fails the smoke
   pass and the full run is chained with `&&`. That is unlikely: the CPU presmoke had about
   5x headroom.
4. One failed D batch removes D(N) at up to 3 budgets for the whole view, and acceptance
   then quietly uses the ridge as D.
5. The first lockstep batch of each D group pays the compile out of its time budget, so
   D(N) nets at the same N can get different step counts across truths.
6. Dataset construction runs outside the per-net `try`.
7. `estimate_ticks` leaves out the scales stage and the n=8 viability-shrink reruns
   (at most about 142 s).

## Secrecy (unchanged and clean)

The bundled exam directories did not change. The secret comes from `os.urandom` and only
its commitment is written. Only `acceptance.py` is imported from the evaluator.
