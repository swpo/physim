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
2. **12 Nov 2026, 08:10 UTC, after the job ended. r6-dialsa3-001 was cut by the platform; no output file came back.**
   The pod became unreachable over SSH at about 07:50 UTC, during the N = 32 fine-tunes (192 min into the script's
   4.2 h); the runner ended the job as `infra_error` at 07:59 ("pod unreachable over SSH for 10 minutes; collection
   incomplete: transfer exited 255; pods terminated"), billed $7.1364 (`origin/gpu-jobs:jobs/r6-dialsa3-001/status.json`
   [cost], [pods]); the manifest lists no collected file (transfer 0 bytes). Lost: `scores.npz` (per-item scores),
   `info.json`, `train_info.json`, `identification.json`, `nets.npz` and the presmoke files; N = 32 and the eta 1 and 2
   arm never ran. What survives is the runner's heartbeat tails of `progress.txt` in the 19 committed versions of
   `status.json` on the jobs branch (public): the presmoke's stop rule, the guard, the base nets' best steps at 96,000
   and 192,000, the nets' hash, and the job's own first look after N = 8, which `a3_stats.first_look` computed from the
   complete N = 8 scores of all 16 truths with the declared criteria (`a3_stats.criteria`): the verdict, its parts,
   sigma_G, rho_G, the three zero-point pairs, H's recovery and t, and every policy's skill at eta 0 and 4 (rounded to
   3 decimals; the runner's log scrubber replaced keys containing "@" by "<ssh-target>", restored here by their sorted
   order, `summarize_tails.py`). Done instead (nearest thing): the verdict is read from that first look; the standard
   errors, bounds, medians and leave-one-truth-out ranges that DECLARED R4 puts beside every mean cannot be computed
   and are reported as lost, never estimated. **No second job**: the task allows one only within the same $10, which
   leaves $2.86 (billed) and buys at most 1.1 h on this card; the declared required stages took 166 min on the
   script's clock here (presmoke 14, families 27, worlds 15, base-net ladder 84, N = 8 21, D(8) 5), so no declared
   rerun fits; a smaller one would change the declared sizes. The decision goes to the lead (README "Next step").
3. **Same time. The base nets did not meet the training rule at 192,000 steps, the declared maximum (R9).** Best
   validation steps at 192,000: public-form 77,750, 59,750, 39,750; true-form 190,250, 170,000, 178,500 (rule: at most
   153,600); at 96,000 the true-form nets' were 83,750, 96,000, 92,000. As R9 declares, the scored nets are the
   192,000-step ones, reported "not converged by the rule"; the curves survive only in part (the heartbeat tails;
   `results/summary.json` [training]). The true-form nets were still improving (best validation 0.3845-0.3878 against
   the public-form nets' 0.4057-0.4099).
