# Review of r6-dialsa2-001 (study `dialsA2`, gliders stress conversion reopened)

Reviewed by the runner Mac as the job started. The code is the eleven request paths at e0df0c07.

Method:
- two reviewers: one checked the run risk on the A100 40GB, the other the correctness against DECLARED.md (3fd4076c5);
- each minor-or-worse finding re-checked by an independent skeptic;
- timings from r6-dialsa-003's measured rates on this card;
- the job's code was not executed on the Mac.

**Verdict: fine to run. 0 blocker, 0 major, 3 minor.**

## Checked

- **Trainers.** run_a2.py calls only a2_lib's scanned trainers: train_nets for the base and D nets, and cv_curves / final_fits through ft_lockstep for the fine-tunes. dialsA's a_nets supplies only constants, datasets, folds and RES, so it did not need to change.
  - One key split per dispatch, then a fold_in per step.
  - The batch sampling and cosine schedule match ladder_net, and the step count is passed as data, so a longer rung does not recompile.
  - Validation runs every 250 steps (base) and every 50 (D), and the trainer raises if the cadence is not a multiple of 50.
  - The fine-tune grid of 10 fits the 40-step dispatch (4 blocks of 10), and every configured step count is a multiple of 40.
- **Base-net ladder.** It is bounded by the rungs (24k, 48k, 96k, 192k) and cannot pass 192k.
  - It stops when a rung meets the rule or when the clock cannot fit the next one; a deadline-stopped rung counts as unmet.
  - N=8 is reserved before each rung, and every rung also stops at T_END.
- **Memory.** Base X is 2.34e8 elements (0.109 of 2^31); step arrays are 8.5e7 to 1.13e8 against check_elems' 2^30. The peak is about 6-8 GB of 40 with the default allocator, and the presmoke runs every full shape.
- **Time.** Most likely about 3.0 h on the script's clock, at most about 3.5 h, against its 3.6 h and the 3.9 h kill, about 17 min later. About $6-6.6.
  - Stage files are written atomically after every stage.
  - Fine-tune steps cost about 30-33 ms, not A's 21.2, because held-out scores run every 10 steps. The guard measures that rate in the presmoke.
- **Outputs.** About 17 files, 10-15 MB; the largest is nets.npz at about 3.4 MB. No names differ only by case.
- **Exit codes:** 1 presmoke failure, 4 speed guard, 2 a failed part, 3 no GPU, 5 fewer than 8 viable truths.
- **Correctness against DECLARED.md.**
  - The items are aimed and regional only, with queries at 8, 12 and 16 ticks. sel and score draw different items from separate exam secrets.
  - Truths 0-7 are round 5's. Truths 8-15 are 48 box draws screened by viability only, under public keys, the same as study A's R19.
  - The three families are as R7 declares; the designed arms are as R6 declares.
  - G*, the best generic repair, is picked on the sel half and scored on score.

## Minor

1. **The speed guard's D(N) projection is about 5-12x too large, so one optional stage that would fit gets cut** (run_a2.py:884-885).
   - The estimate scales the presmoke's D(8) time by the world count, but that time is dominated by compiles and fixed costs. It gives 27-65 min against about 5.3 min actual.
   - With the ladder climbing to 96k, the oversized reserve can cut the 192k rung or N=32 even though both would fit (all stages, 192k included, would end near 206 min).
   - Next time: project D from the measured base rate, or time only the D loop after its first dispatch.
2. **The fine-tune grid widening is capped at 2 rounds in total, not "each at most twice" as R11 says** (run_a2.py:549).
   - A group whose steps double and then gets a smaller rate cannot double its steps again.
   - The pick is then reported as not interior, in NOTES, so nothing is hidden, but the declared grid is not fully reachable.
   - Count each kind separately, or record the 2-round cap in DEVIATIONS.md.
3. **After the clock deadline, the D doubling can retrain for about 50 steps and overwrite the scored Dnet(N)** (run_a2.py:776-784).
   - dstage doubles while the rule is unmet and never checks left(). If D(8) at 1,200 steps is cut by the deadline, the 2,400-step rerun trains about 50 steps per group and replaces Dnet(8), a G* candidate.
   - The effect on the verdict is small, because G* picks on sel. But read Dnet's stopped_early before quoting it.
   - Fix: stop the doubling when a group was stopped early or the clock cannot fit it, and keep the last complete scores.

## Notes

- The base-net ladder will probably climb as far as the clock allows. Under a cosine schedule that anneals to the end, the best step tends to land at the end of any rung, so the "best step at or below 80%" rule may stay unmet through 192k, as in r6-dialsa-003. For later studies, consider a rule a cosine schedule can meet, such as a relative improvement over the last 20%, or continuing from the previous rung's weights.
- Fine-tune stages take about 1.5x the request's estimate (about 30 ms per lockstep step). The guard uses the measured rate, so this only affects the "1.8-3.2 h" expectation.
- The kill margin, incremental writes and outputs are sound.
