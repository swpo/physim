# Statistician's critique of the three dial designs (round 6, `crit_stats`)

11 Nov 2026. Read: the six round-5 `checker` blocks and the three designs. Run: `se_check.py` on the ladder's
per-item scores (`round5/ladder/results/job/n*/scores.npz`; 3 CPU-seconds; `results/se_check.json`, `S` below).
The rest is estimate.

## 1. What the sizes can resolve

Per-truth SD of sigma in round 5: 0.004-0.012 where sigma was near zero, 0.04-0.11 in the population view
(`S` `cells`), 0.15-0.17 on vortex pilot B; 0.65-1.25 times sigma wherever sigma was not zero. I take 0.085-0.17
(0.03-0.06 at eight truths); a design reaching 0.3 should expect the upper figure.

| truths | SE of sigma, truths only | undecided if the true sigma is within this of 0.15 | SE of rho |
|---|---|---|---|
| 4 | 0.04-0.085 | 0.11-0.21 | 0.16-0.38 |
| 8 | 0.03-0.06 | 0.07-0.14 | 0.11-0.27 |
| 12 | 0.025-0.05 | 0.05-0.11 | 0.09-0.22 |
| 16 | 0.02-0.04 | 0.05-0.09 | 0.08-0.19 |

(`S` `design_expectations`: power 0.8, one-sided 90% t bound; rho from the ladder's spread at two episodes.)

- Truths bind, not items: at 48 items, item noise is 10-28% of the between-truth variance.
- Four of the ladder's eight truths give sigma 0.045 to 0.188 in the population view (70 subsets).
- At four clusters the bootstrap SE is 0.87 of the delta-method SE, and "z >= 3" is t on 3 degrees of freedom,
  p 0.03.
- No round-5 error included the training seed. Pilot A's sigma was -0.003 on the pod and 0.045 retrained
  (`vortexexam` checker 11): 0.034 per training, from one pair. C and P0 are single nets shared by all truths, so
  this error does not shrink with truths and no truth bootstrap sees it. With two seeds it is 0.024, the truth SE
  at twelve truths.

## 2. Per design

**defect_gliders.** Stage 1 (4 truths; seeds for P0 and C only) supports its stop rule only at the forecast's
extreme: a true sigma_g of 0 is excluded from 0.15 with probability 0.41-0.95, and rho_g 0.9 against 0.7 is
0.5-1.3 SE. Bar 1's forecast (0.20) needs 16 truths or more. Not fixed: which four truths, the W0 box, the
primary N (32 in section 5, 8 in the failure rule). Bar 1 is on half the items; the full-mix sigma (forecast
0.10) is what compares with round 5. Zero point: the bitwise check is real; "0.018 +- 0.004 within 2 SE" is weak
(a fault degrading P0 and C alike leaves the ratio unchanged; no seed term). RES closing more than 1 shows the
surrogate C is no ceiling; the real C conditions on seven numbers with the 768 points P0 has for four, so rho_g
may measure C's weakness. W0 decides whether the regional push (peak 0.153) triggers: expect two kinds of truth.
*Minimum:* all eight ladder truths at eta 0 and 4 in stage 1 (about $3, inside the cap); three seeds per scored
net; 16 truths before bar 1 is called passed.

**sublevel_second.** The soundest: nested truths, a positive-control arm, G* chosen off the scored half, seeds
on every net. Twelve truths decide gate 1 only if sigma_G is below 0.04-0.10 or above 0.20-0.26; gate 2 is
decidable if its forecast (0.10-0.34) holds. Gate 1's point rule passes a true 0.15 half the time; gate 2 has no
interval. Table 3b's two pilot worlds differ by 0.24 (G) and 0.25 (H): expect the upper SE. Zero point: the
bitwise check is real; check 3 has no baseline and is a first measurement. Not fixed: the hidden set, the ranges
of rho, D_X, a0 (a0 is being tuned on the screen), the size-down rule. Stage 1's truths belong outside the gate
estimate.
*Minimum:* 16 truths at lam 0, 1 and the control, 6 at 0.5 and 0.75 (the same 60 worlds); three seeds; ranges
committed before the job.

**compute_limit.** Its evidence has no hidden worlds: errors are over 8 replicate members at one public
parameter point. "Pooled equals exam-size" compares regressions on 3.5-5.5 and 7 episode equivalents; the
declared budget is 64. Zero point: "0.061 +- 0.048 within 2 se" spans -0.035 to 0.157, the bar included, and
0.061 uses a C the checker showed is no ceiling (0.136 +- 0.054 against the best). r and R change together. Bar
4's denominator is forecast near zero at r = 1/4. C "without limit" has no size; G* is the best of eight recipes
with no selection rule. If the forecast holds (sigma_c about 0.01 and 0.37, SE 0.05), ten truths decide it;
pilot B's means were carried by truths 1 and 6.
*Minimum:* the stop-rule job as a futility test only, with and without those two truths; the zero point as
paired per-truth differences from stored scores; r crossed with R; 16 new truths and three seeds before any pass.

## 3. To declare in advance, all three

1. One primary view, item set, Lab budget and C; every share on the same items.
2. Bars as per-truth contrasts with t: sigma >= 0.15 is mean[L(null) - 0.85 L(C) - 0.15 L(K)] >= 0; rho <= 0.7
   is mean[L(G*) - 0.3 L(P0) - 0.7 L(C)] >= 0, read only if P0 - C exceeds 2 SE. Three outcomes (pass, fail,
   undecided by the one-sided 90% bound); one extension doubling the truths.
3. Three seeds per scored net; SE^2 = SE_truths^2 + SD_seed^2 / seeds.
4. Convergence: best validation step within 80% of the schedule, else the schedule doubles; equal steps for
   conditioned and unconditioned nets (round 5: C at its last evaluations in 9 of 9 cells, D in 47 of 48 nets).
5. C like for like: also C fine-tuned on simulations at the truth, and C given the generic recipes' Lab
   episodes; the best, chosen off the scored items.
6. A real zero test: at zero dial the extended-family C against the public-family C, and G* and H against P0
   and S, paired per truth, tolerance 0.01 of K-to-C, not "within 2 SE".
7. Median and leave-one-truth-out range beside every mean; a pass survives dropping any one truth.
8. The dial as a paired difference from the zero arm on nested truths.
9. The screen prospectively: per-truth gap against per-truth sigma, within one view and family.
