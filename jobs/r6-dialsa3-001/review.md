# Review of r6-dialsa3-001 (study `dialsA3`, the zero-point rerun of dialsA2)

Reviewed by the runner Mac before the job started. The code is the twelve request paths at 37035b5c8.

Method:
- three reviewers: run risk on the A100 40GB; correctness against DECLARED.md (3e9026c7b); the delta from dialsA2's run_a2.py;
- a skeptic for every minor-or-worse finding (there were none);
- a final critic who closed the gaps;
- timings from r6-dialsa2-001's measured rates on this card;
- the job's code was not executed on the Mac.

**Verdict: fine to run. 0 blocker, 0 major, 0 minor; notes only.**

Expected: about 3.6 h on the script's clock (presmoke about 16 min, full pass about 197 min). About $7.2 billed; worst case about $9.45. If the declared presmoke stop rule fires: about 17 min, exit 0, about $0.7.

## Checked

- **Memory.** The base-net stack is as stated. X is 6 x 12,288 x 33 x 8 x 8 x 3 = 4.67e8 float32 elements (0.218 of 2^31); CU and CtU are 3.11e8 each; 4.36 GB on the device.
  - Each step gathers 128 rows per net. The largest step intermediate is 8.5e7 elements.
  - Validation is chunked and capped at 1,024 rows. No jit gathers the whole stack.
  - Realistic peak is 8-10 GB of 40. Each rung's stack is freed (train_nets deletes it, and the jit caches are keyed by config, not data).
  - The presmoke runs X, CU and CtU at the full shapes, so an out-of-memory error would end the job in its first minutes.
- **Time.** Built from dialsA2's measured stages:
  - families 26.5 min, worlds 15.5 min;
  - base ladder to 192k 83 min (13.4 ms per step, independent of data size);
  - N = 8 about 20 min, D(8) about 5 min, N = 32 about 33 min, eta 1/2 arm about 12 min, presmoke about 16 min.
  - The total is about 3.5 h against A3_MAX_HOURS 4.2 and the runner's 4.5 h kill. The kill clock includes setup, which leaves about 17.8 min of margin past the script's end.
  - The worst unchecked overrun ends about 8 min past the script's end, inside that margin.
- **Speed guard.** It times steady rates only: the first dispatch is excluded everywhere.
  - D is now projected from the base nets' steady step (23.2 ms per group step against 17.5 measured): 436 s for D(8) against 300 s actual, down from 2,246 s. dialsA2's minor 1 is fixed.
  - Exit 4 would need rates about 2.8x slower than dialsA2's.
- **dialsA2's other two minors.**
  - Widening is now counted per kind, gated by the clock (minor 2).
  - D doubling does not run after a deadline stop, and the last complete scores are kept (minor 3).
- **Shared modules.** a2_lib, a2_stats, dialsA (xlaw, a_nets, a_stats), round5 ladder, round4 sbi, defect_gliders, track2, vw1, integrate, spec and level0 are unchanged since e0df0c07. Every hunk of run_a3.py against run_a2.py was read. No stale names remain, and every key the guard reads exists after the presmoke.
- **Correctness against DECLARED.md.**
  - A3-1: 48 candidates from seed [6631, 4], screened by viability under the public law before any world exists, under public keys. The first 16 viable become the truths; fewer exits 5. The job asserts no overlap with dialsA2's truths. The secret is os.urandom and only its commitment is written.
  - A3-2: the true-form family is 768 at eta 0, 256 at eta 4 and 512 uniform on (0, 4), with its own class array. H_mix is fitted on it.
  - A3-3: the zero point covers the three pairs Ctrue-Cpub, G*-S at N = 8 and H-S at N = 8, each within 0.02 of the K-to-Cpub unit. FAIL holds whatever the zero point if T1 or T2 fails. G* is picked on sel and scored on score. Every input of the verdict is produced.
  - A3-4: the stop rule is r = mean(d) / (mean K - mean Cpub) on the score half, truth 0, eta 0, rung 6,000, with SE from items and seeds. It stops if r > 0.02 + 2 SE.
    - The critic applied it to dialsA2's published presmoke scores and reproduced DECLARED.md's +0.234 +- 0.034 and +0.306 +- 0.072 exactly.
    - It is well defined at presmoke sizes. A NaN fails open, and both paths write their files.
- **Outputs.** About 22 files and 11-15 MB, the largest nets.npz at about 3.2 MB. No names differ only by case. Files are written atomically after each stage. The exit codes match the request.

## Notes

1. **The presmoke stop may well fire, and it is a real signal.** On dialsA2's data, a persistent dialsA2-sized bias stops the job about 20-75% of the time, depending on the presmoke's SE. If A3-2 works, a false stop happens about 1% of the time.
   - Read exit 0 with stopped_by_presmoke_rule.json as the declared UNDECIDED end, not as a fault or a reason to requeue.
   - A go does not show that the zero point holds: the full pass's pair decides that.
   - Report stop_rule.json's r and SE beside the full pass's pair.
2. **The presmoke's example-index array tr is a quarter of the full size** (pad_dataset pads X, CU, CtU and th only). The full pass's 24k rung recompiles once, for tens of seconds. That dispatch is excluded from the step rate, and the array is 31 MB. Next time, pad tr as well, or correct the docstrings.
3. **The D(N) projection now uses the base nets' steady rate rather than the D nets' own** (as the dialsA2 review suggested). It is not recorded in DEVIATIONS.md; add an entry.
4. **R19's "cost of each reference policy in episode equivalents" is not produced by make_summary.py** (inherited from dialsA2). It can be computed after the run from the Lab budgets and info.json.
5. **The eta 1/2 arm's time estimate is about 1.6x too small now that D(8) is realistic.** It matters only on a tight clock. The arm is reported only, and in the expected timeline it starts with about 50 min left.
6. **The per-kind widening path runs only in the full pass** (the presmoke sets ft_widen to 0). Only the CPU smoke test has exercised it; the lookups match widen_decision's return values.
