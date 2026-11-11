# Statistician's critique of the dial designs (round 6, `crit_stats`)

11 Nov 2026. Sources: the six round-5 `checker` blocks; `se_check.py`, run on the ladder's per-item scores
(`round5/ladder/results/job/n*/scores.npz`, 3 CPU-seconds; `results/se_check.json`, `S`). The rest is
estimate.

## 1. What the sizes resolve

Per-truth SD of sigma in round 5: 0.004-0.012 in the block and object views, 0.04-0.11 in the population view
(`S` `cells`), 0.15-0.17 on vortex pilot B; where sigma was not zero, 0.65-1.25 times sigma. I take 0.085-0.17
(0.03-0.06 at eight truths).

| truths | SE of sigma | undecided within this of 0.15 | SE of rho |
|---|---|---|---|
| 4 | 0.04-0.085 | 0.11-0.21 | 0.16-0.38 |
| 8 | 0.03-0.06 | 0.07-0.14 | 0.11-0.27 |
| 12 | 0.025-0.05 | 0.05-0.11 | 0.09-0.22 |
| 16 | 0.02-0.04 | 0.05-0.09 | 0.08-0.19 |

(`S` `design_expectations`: truths only; power 0.8, one-sided 90% t bound.)

- Truths bind, not items: at 48 items, item noise is 10-28% of the variance between truths in the 4-parameter
  cells (9-95% over all nine). The designs' item counts suffice.
- Four of the ladder's eight truths give sigma 0.045-0.188 (population view).
- At four truths the bootstrap SE is 0.87 of the delta-method SE, and "z >= 3" is p 0.03 (t, 3 df).
- Training seed (in no round-5 error): pilot A's sigma moved from -0.003 to 0.045 on retraining
  (`vortexexam` checker 11): SD 0.034, one pair. C and P0 are nets shared by all truths, so more truths do not
  shrink it and no truth bootstrap sees it; at two seeds it is 0.024, the lower truth SE at twelve truths.

## 2. Per design

**defect_gliders.** Stage 1 (4 truths; seeds for P0 and C only) supports its stop rule only at the forecast's
extreme: a true sigma_g of 0 is excluded from 0.15 with probability 0.41-0.95; rho_g 0.9 against 0.7 is 0.5-1.3
SE. Bar 1's forecast (0.20) needs 16 truths or more and covers half the items; the full-mix sigma (forecast
0.10) compares with round 5. Not fixed: which four truths, the W0 box, the primary N (32 in section 5,
8 in the failure rule). Zero point: the bitwise check is real; "0.018 +- 0.004 within 2 SE" is weak (a fault
degrading P0 and C alike leaves the ratio unchanged). C conditions on seven numbers with the 768 points P0 has
for four, so rho_g may measure C's weakness. W0 above 0.153 silences the regional push: two kinds of truth.
*Minimum:* all eight ladder truths at eta 0 and 4 in stage 1 (about $3); three seeds per scored net; 16 truths
before bar 1 passes.

**sublevel_second.** The soundest: nested truths, a positive-control arm, G* chosen off the scored half, seeds
on every net. Twelve truths decide gate 1 only if sigma_G is below 0.04-0.10 or above 0.20-0.26. Gate 1's point
rule passes a true 0.15 half the time; gate 2 has no interval. Table 3b's two pilot seeds differ by 0.24 (G) and
0.25 (H): expect the upper SE. Zero point: the bitwise check is real; check 3 has no baseline. Not fixed: the
hidden set, the ranges of rho, D_X, a0 (a0 is being tuned on the screen), the size-down rule.
*Minimum:* 16 truths at lam 0, 1 and the control, 6 at 0.5 and 0.75 (the same 60 worlds); three seeds; ranges
committed before the job.

**compute_limit.** Its evidence has no hidden worlds: errors are over replicate members at two public parameter
points. "Pooled equals exam-size" compares regressions on 3.5-5.5 and 7 episode equivalents; the declared budget
is 64. Zero point: "0.061 +- 0.048 within 2 se" spans -0.035 to 0.157, the bar included, and 0.061 uses a C the
checker showed is no ceiling (0.136 +- 0.054 against the best). G* (best of eight) has no selection rule. If
the forecast holds (sigma_c about 0.01 and 0.37, SE 0.05), ten truths decide it; pilot B's means were carried by
truths 1 and 6.
*Minimum:* the stop-rule job as a futility test only, with and without those two truths; the zero point as
paired per-truth differences from stored scores; r crossed with R; 16 new truths and three seeds before any pass.

## 3. To declare in advance

1. One primary view, item set, Lab budget and C; every share on the same items.
2. Bars as per-truth contrasts with t: sigma >= 0.15 is mean[L(null) - 0.85 L(C) - 0.15 L(K)] >= 0; rho <= 0.7
   is mean[L(G*) - 0.3 L(P0) - 0.7 L(C)] >= 0; ratios read only where the denominator exceeds 2 SE. Outcomes
   pass, fail or undecided by the one-sided 90% bound; one extension doubling the truths.
3. Three seeds per scored net; SE^2 = SE_truths^2 + SD_seed^2 / seeds.
4. Convergence: best validation step within 80% of the schedule, else the schedule doubles; equal steps across
   nets (round 5: C still improving in 9 of 9 cells, D in 47 of 48 nets).
5. C like for like: also C fine-tuned at the truth and C given the generic recipes' Lab episodes; the best,
   chosen off the scored items.
6. A real zero test: at zero dial the extended-family C against the public-family C, and G* and H against P0
   and S, paired per truth, tolerance 0.01 of K-to-C.
7. Median and leave-one-truth-out range beside every mean; the dial as a paired difference on nested truths.
