# Study dialsA3: deviations from the task, the plan and DECLARED.md, written at the time

Each entry: when, what was declared, what was done instead, why. `DECLARED.md` is not edited.

1. **12 Nov 2026, 04:25 UTC, job r6-dialsa3-001 provisioning, no result seen. The runner's review (0 blocker, 0 major,
   0 minor; six notes) and what follows from it.** Nothing in the code changes while the job runs.
   (a) *The D(N) projection of the speed guard* (review note 3). DECLARED A3-8a says the D(N) projection "uses the steady
   D rate". The code (`run_a3.d_seconds`) projects D from the base nets' steady step time, scaled to a lockstep group of
   8 nets and multiplied by 1.3 for validation every 50 steps (23.2 ms per group step against 17.5 measured on this card
   in r6-dialsa2-001, by the review), plus the steady scoring time per world. Why: the presmoke's D stages run 100 steps,
   so their own timing would include the first compilation of the validation function (the bug A3-8a names); the
   review of r6-dialsa2-001 suggested exactly this projection. Effect: D(8) is projected at about 436 s against 300 s
   measured in dialsA2 (the old projection: 2,246 s). It only decides what the clock may cut.
   (b) *The presmoke's index arrays are not padded* (review note 2). DECLARED A3-4 and `pad_dataset`'s docstring say
   every base-net data array has the full pass's shape in the presmoke. The data arrays (X, CU, CtU, th) do; the
   example-index arrays (`tr`, `va`) keep the presmoke's real sizes (`tr` a quarter of the full one), so the full pass's
   first rung compiles the training step once more (tens of seconds, outside the steady step rate the guard uses; the
   index array is 31 MB). No memory risk follows: the large arrays are tested at full size.
   (c) *R19's "cost of each reference policy in episode equivalents"* (review note 4) is not produced by
   `make_summary.py` (as in dialsA2); it is computed after the run from the declared sizes and reported in README.md.
   (d) Review note 1 (the stop rule may fire and is then a real UNDECIDED signal; a "go" does not show the zero point
   holds) agrees with DECLARED A3-4 and A3-11; the presmoke's r and SE are reported beside the full pass's pair.
