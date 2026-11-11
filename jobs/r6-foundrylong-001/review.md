# Review of r6-foundrylong-001 (study `foundrylong`, stage 1)

Reviewed by the runner Mac while the job ran. The code is the four request paths at 065c7bc6.

Method:
- two reviewers: one checked the run risk on the A100 40GB, the other the correctness against DECLARED.md and DEVIATIONS.md addendum 1;
- each minor-or-worse finding re-checked by an independent skeptic;
- timings from the foundry-exam jobs on this card and from round 5's screens;
- the job's code was not executed on the Mac.

**Verdict: fine to run. 0 blocker, 0 major, 2 minor.**

## Checked

- **Device memory.**
  - The C stack: X (8, 16384, 49, 8, 8, 3) is 1.23e9 elements, 0.574 of 2^31; CU and CtU 8.2e8 each; 11.5 GB in all. Every device array is asserted below 2^31.
  - value_and_grad differentiates only the parameters, so no cotangent the size of X is built.
  - P0(1,000), 5.6 GB, is freed before the C stack is built. Even both together, with temporaries, would be about 22 GB.
  - Step arrays: check_elems gives 1.13e8 for C and 8.5e7 for P0, against 2^30.
  - The screen's largest array is 4.03e8 float64 (3.2 GB), and job2.run_arm halves the chunk on failure.
  - shape_test trains the exact C shape 5-8 min in, so an out-of-memory error would cost about $0.25.
- **CPU-side memory.** About 40 GB at peak of about 200 GB. The screen's work files are under $GPUJOB_DIR, not $OUT.
- **Episode constants.** fl_lib sets the constants before fx_net is imported, with an import guard and an assert (fl_lib.py:29-41). fx_lib reads them at call time, and HistoryExam.H = max(queries) = 32. Two H = 16 leftovers in fx_net are not on the job's path.
- **Time.**
  - The screen is about 49.5M member-ticks at an unmeasured A100 rate, estimated at 25k/s: 20-39 min.
  - Simulation is 114M member-ticks at the pilot's 42k/s: 47 min.
  - Nets about 61 min, plus about 10 min of validation and scoring.
  - Total about 2.6-2.9 h on job.sh's clock against its 2.9 h stop and the 3.15 h kill; about $5.4-6.0.
  - The presmoke projection does include the screen and all simulation.
- **Hidden worlds.** The 16 hidden worlds are rebuilt from their labels alone, as TN.draw_theta(2027, i), and inputs/pilot_worlds.json matches r6-foundryexam-005's worlds.json exactly. The larger screen and longer episodes cannot change them.
- **New prior worlds.** They come from seed 2028, so none can coincide with a hidden world.
- **job2.** It is imported, not run.
- **Training driver.** It gives each horizon equal weight and keeps the held-out loss and best parameters per horizon. Scored cells are ordered 8, 16, 32 ticks, and each horizon is answered with its own parameters.
- **Output names.** None differ only by case.

## Minor

1. **Outputs are about 53 MB against the 50 MB git cap, because items.npz is about 19.5 MB, not under 6 MB.**
   - hist is (96, 17, 192) per world x 16 worlds in float32 (run_fl.py:432).
   - The runner adds files to git in the pod's file order and leaves out any that would cross 50 MB, so about 3-4 MB will be in_git false. Which files is arbitrary: the 16 C parameter files that stage 2 reads, params_p0w1000.npz, items.npz, or rarely scores.npz.
   - For this run: check manifest.json's in_git for scores.npz, train_info.json, params_p0w1000.npz, cparams/* and items.npz before running make_summary. Ask the Mac for any file that stayed here.
   - Next time: store hist as float16 or drop it, or the C parameters as float16.
2. **S1a's "robust" reading and the verdict are printed even when declared nets are missing or cut by the deadline** (make_summary.py:197).
   - P0x2 is last in the plan. If it is stopped early, its doubling gain is clipped to 0 and S1a still reads "robust".
   - Fix offline: read train_info.json and info.json. Report S1a as "incomplete" unless P0x2, the second-largest P0 and C4096 are present and not stopped early. Mark S1 incomplete if a declared null candidate or seed is missing or cut.

## Notes

- The screen's rate on an A100 is unmeasured. Only the tail of the plan is at risk: P0x2, then C(1024), P0w64, P0w210 and C(4096), in that order. Cuts start only at a slowdown of about 1.3x.
- The speed guard passes up to 1.25 x the time available, taken while the presmoke is still running.
- The P0 curve (1,000 / 210 / 64 worlds) is nested in the worlds available but not in the worlds each net trains on, and its composition shifts. Say so when reading it as a compute curve.
- There is about a 1-in-4 chance that P0's largest size ends below 1,000 worlds; the code handles that.
- S2's "late gain" measures only part of the last fifth when 80% of a schedule falls between two evaluations.
