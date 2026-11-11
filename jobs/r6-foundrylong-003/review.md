# Review of r6-foundrylong-003 (study `foundrylong`, stage 2, resubmission of 002)

Reviewed by the runner Mac as a delta against r6-foundrylong-002 (919e26ce). Read 002's review (jobs/r6-foundrylong-002/review.md) for everything that is unchanged. The code is at 0777fbfe.

**Verdict: fine to run. 002's blocker is fixed. 2 of 002's 3 minor findings may still apply.**

## The blocker, fixed

- fit_batch now returns timing: the first step (the compile) is timed apart from the steady steps after it (fl_w.py fit_batch). The trace append synchronises each step.
- speed_guard (addendum 4) projects from the steady seconds per step of B fits only. It adds prescreen, predict, respin, FT, D and W+ terms with a 900 s margin. It then sets W's Adam steps for the full pass to whatever fits, between 80 and 200, and exits 4 below 80.
- job_s2.sh reads w_steps from presmoke/shape_test.json and passes --w-steps to the full pass. The step count and the timing records are kept in shape_test.json.

## 002's minor findings

1. **A fit cut by t_max still crashes w_condition at the trace concatenate.** That part of run_fl2.py is unchanged. A cut is now less likely, because the steps are sized to the measured speed, but if it happens that Lab's w_fits / w_info and its W+ are lost. Check info.json and the run log for "stopped at step".
2. **W+ at 4,096 episodes is capped near 0.62 recovery against C16384.** Unchanged: read W+ as a reading only, not against T3's 0.7 bar.
3. **Exit 0 does not mean complete.** make_final.py is new; check that it requires skipped = failed = [] and the fits at the step count shape_test.json chose, before reading T1-T6.

## Notes

- The presmoke still times only 9 steady steps (w_steps 10). That is enough without the compile, but noisy; the 1.1 factor and the 900 s margin absorb it.
- If the guard picks fewer than 200 steps, the fits are shorter than DECLARED's 200. Addendum 4 declares this; report the chosen count with the results.
