# Review of r6-foundryexam-004 (study `foundryexam`, follow-up of 003)

Reviewed by the runner Mac as the job started. The code is the four request paths at 1e9acab5.

Method:
- two reviewers: one checked the run risk at the larger sizes, the other the correctness of the changes since r6-foundryexam-003 (96d04d50);
- each minor-or-worse finding re-checked by an independent skeptic;
- timings from 003's measured rates on this card;
- the job's code was not executed on the Mac.

**Verdict: fine to run. 0 blocker, 0 major, 2 minor.** The changes do what the request and DESIGN.md 5c say.

## Checked

- **Memory.**
  - The largest device data set is the 16-net C/Cft/Csm stack: X 4.15e8 elements (1.55 GiB); CU and CtU 3.61 GiB together. Csm is padded to the same size.
  - The batch-128 training step's conv-column array is 2.27e8 elements, under check_elems' 2^30. Residuals and backward temporaries come to about 10 GiB.
  - Peak about 14 GiB of about 39 GiB.
  - N-arm shared sets with 128 neighbours: 8,192 episodes, 0.48 GB.
  - Every device array is asserted below 2^31; the largest is 4.15e8.
  - Nothing is on the device twice: each training call's data is released when it returns.
  - The presmoke shape_test runs the exact C shape on the card first, so an out-of-memory error would end the job in 2-3 min for about $0.10.
- **Time** (003's measured rates):
  - simulation 81.6M member-ticks at about 42k/s (003 measured 16.2 s per chunk, not 47k/s): 32 min;
  - hidden worlds 7 min;
  - shared nets 6.7 min (P) and 5.7 min per N arm;
  - lockstep about 25 min (P) and 19 min per N arm.

  Full pass about 2.1 h; job.sh about 2.2 h, against its 3.0 h limit and the 3.25 h kill. Each arm finishes well inside its deadline: P about 47 of 71 min, N30 38 of 56, N10 38 of 78. Cuts begin only at a uniform slowdown of about 1.45x.
- **Changes.**
  - Sizes, steps and batches are as declared, and every step count divides the 50-step chunk and its eval cadence.
  - Seeds are +1000 at every training call (1000-1331, none equal to 003's), and the noise secret is a fresh draw.
  - The CLOCK fix is correct, and the try per lockstep group keeps finished groups.
  - Csm really is the first 1,024 of each world's 4,096 class-mixed episodes.
  - The speed guard counts both lockstep shapes: 30,000 steps at batch 128 and 16,500 Lab steps, with N arms scaled by 12/16.
  - make_summary keeps the null at 512 and treats Csm as its own family.
- **Outputs.** About 23 MB; the largest file is full/P/items.npz at about 6.5 MB, and gate.json grows to about 0.46 MB. Exit codes are as in 003.

## Minor

1. **The N-arm hidden worlds can differ from 003's, although the request says they are unchanged.**
   - The gate lists candidates as pool worlds, then per arm and centre j in range(nb_train_cand) followed by 1000-1015 (run_fx.py:184-188). Each member's noise is keyed by its global row (fx_lib.py:135).
   - Raising nb_train_cand from 64 to 256 moves every N-arm hidden candidate to a new row, so its gate episodes get new noise.
   - Some of 003's picks sit near the vp16 >= 0.2 bar: N30 centre 1672 j1003 at 0.229 (picked) and j1006 at 0.221. By the reviewer's estimate there is about a 40% chance that N30's hidden set changes by one world.
   - Arm P is unaffected: pool rows come first.
   - For this run: compare the hidden labels in out/full/N30/worlds.json and out/full/N10/worlds.json with 003's before putting 003's and 004's N-arm numbers side by side. Report any difference, and the training-world counts per centre: about 96 of 256 are expected to pass for centre 1672, not 128.
   - Next time: key gate noise by candidate identity (arm, centre, j), not list position, or append new candidates after 003's.
2. **The speed guard is still lenient** (003's minor 1, not changed).
   - It passes up to 1.25 x the time available (run_fx.py:616-618). It times neither validation nor compiles, and counts P0w once although two curve nets train.
   - The 55-min non-net allowance is slightly short: about 57 min, at 003's measured 42k member-ticks/s.
   - At expected speed nothing is cut. If nets run about 1.45x or more slower than 003, the deadlines drop the second seeds, the small-budget curves, P0[16]/P0[64] and possibly Csm, which is the point of 5c.
   - For this run: if presmoke/shape_test.json projects more than about 1.7 h of net time, read SKIPPED and stopped_early before quoting criterion 8, the budget curves or Csm.

## Notes

- Csm's train/validation split is drawn separately from C's: rng.permutation(4096) versus permutation(1024) (fx_net.py:139). About 10% of Csm's training episodes per world, 72-96 of 922, are in C's held-out set. That is harmless for each net's own validation, but a C-versus-Csm comparison on C's validation set would favour Csm slightly.
- Arm P's training simulations, training-world selection and split seed are identical to 003's (run_fx.py:220, 224, 346, 349). Only the net seeds, items and Labs are new. That is useful for a like-for-like comparison of arm P, and worth stating.
