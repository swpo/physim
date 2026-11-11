# Review of r6-foundrylong-002 (study `foundrylong`, stage 2)

Reviewed by the runner Mac. The job was stopped by its own speed guard after the presmoke: exit 4, job.sh exit 2, $0.10. This review explains why, and covers the code for the resubmission. The code is the four request paths at 919e26ce.

Method:
- two reviewers: one checked the run risk of the new fit code on the A100 40GB, the other the correctness against DECLARED.md and DEVIATIONS.md addendum 3;
- each finding re-checked by independent skeptics: two for a blocker;
- the job's code was not executed on the Mac.

**Verdict: 1 blocker (the reason 002 stopped), 0 major, 3 minor.** The science is wired as declared, and the run would most likely fit in about 2.2 h once the guard measures steady state.

## Blocker: the speed guard measures compiles and an evaluation, then scales them about 368x

- The SPEED clock starts before fit_batch (run_fl2.py:236) and stops after the post-fit eval_batch (:241-246). In the presmoke this is one group of B = 8 fits and 10 steps (:63).
- That window holds:
  - the first call of vg, the compile of value_and_grad through the rematerialised 16-tick scan (fl_w.py:332);
  - the first call of sp at pool 16, a new shape: the prescreen compiled it at pool 8 (fl_w.py:323, 355);
  - a full 32-episode evaluation and a respin.
- The guard then projects W as seconds / (10 x 8) x 200 x 128 x 1.15 (run_fl2.py:344-346): 368 projected seconds per measured second. The prescreen term is scaled about 64x the same way.
- The guard passes only if those first-call costs come to at most about 5.6 s in total. Stage 1's log on this card shows about 24 s of first-call overhead for a forward-only simulator function, with no compile cache between runs. So a false "too slow" was nearly certain. The run log says: "0.416 s per fit step per fit; projected 4.93 h (W 3.57)".
- The CPU smoke could not catch it, because job_s2.sh passes --full-hours only to the presmoke on the GPU, so the guard always says ok on the CPU.
- **Fix (resubmission):**
  - Measure steady state only: block on the step-1 loss and time steps 2..n.
  - Record eval and respin time separately, per batch.
  - Take the prescreen and predict terms from calls after the first.
  - Raise the presmoke's w_steps to about 30, and log first-call times separately in shape_test.json.
  - Before requesting, feed the guard SPEED/CLOCK values built from stage 1's numbers offline. Confirm it passes at 1.1 s per 8-fit step and fails at about 2.5 s.
- No change to the science (steps, starts, Labs) is needed for time. At the request's own 1.1 s per step the plan comes to about 2.0 h for the full pass and 2.2 h on job_s2's clock, about $4.5.

## Checked

- **Memory.** The fit step peaks at about 6-13 GB. jax.checkpoint wraps a whole tick, so each tick's 4 substeps keep their residuals for 512 trajectories (8 fits x 8 episodes x 2 anchors x 4 members). The largest buffer is 1.34e8 elements (2^27). Eval is about 2 GB, W+ data about 2.9 GB, and the CPU side about 10 GB.
- **Compiles.** Shapes stay the same across worlds, starts and Labs, so vg, ev and sp each compile once per process.
- **Time.** About 67 min for W (128 fits = 16 batches x 200 steps at 1.1 s, plus prescreens, respins and predictions), 12.5 min for FT, about 2 min for D, and about 30 min for W+. The 0.7 h of slack absorbs fit steps up to about 1.9 s. The kill margin is about 14.5 min, and the worst overrun after T_END about 7 min.
- **Science.**
  - W's fit sees only the Lab (labs[c][:32]). The 32 starts are stage-1 training worlds, none of them hidden. Items, futures and the true weights are not touched before the fit; the true weights appear only in the z_true diagnostic, after it.
  - The loss is the 16-tick free forecast scored by the fair energy score, with the gradient only through the forecast.
  - The best 4 starts are chosen on Lab data.
  - Designed episodes spend 12.5 nats in every test tick and are exactly paired with mix episodes.
  - W+ simulates at the fitted weights, not the true ones.
  - All 18 stage-1 parameter files hash identically to r6-foundrylong-001's outputs.

## Minor

1. **A fit batch cut by its time limit crashes w_condition at the trace concatenate** (run_fl2.py:266; fl_w.py:338-343).
   - Traces of different lengths cannot be stacked, so that Lab's w_fits / w_info are lost, its W+ fails, and the cut is never marked. The presmoke cannot hit it, since it has one group and no t_max.
   - Pad traces to w_steps, or keep per-batch medians in a list. Record the steps done per group, mark cuts in SKIPPED, and set WINFO before anything that can raise.
2. **W+ at the C recipe's 4,096 episodes cannot reach T3's 0.7 recovery bar even at the true weights** (run_fl2.py:62, make_summary2.py:62, 87-92).
   - It is stage 1's C(4,096) recipe, and the reference is C(16,384), so recovery is capped near 0.62.
   - State that W+ is a reading only, or run it at 16,384 episodes as declared.
3. **Exit 0 does not mean complete.**
   - In the full pass, parts skipped near the deadline, nets stopped by it and fits cut by t_max all exit 0. Only FAILED gives 1.
   - make_summary2 should require info.json's skipped and failed to be empty, and every fit at 200 steps, before reading T1-T6.

## Notes

- The "1,280 members in flight" bound counts eval trajectories, not the fit's backward footprint. The 6-13 GB is fine on 40 GB but grows about 4x if B and A are raised.
- The scored W is the mean of best-of-{1,3} and best-of-{2,4}, not the single declared best start; the outputs suffice to recompute it.
- Verdict readings: "pass" needs T5 "actions matter", which stage 1 suggests is about 16% likely. T4 compares Labs that differ twofold in nats.
- Fits are not bit-reproducible, because the key comes from os.urandom. A separate fit-only seed (not the noise secret) would fix that.
