# Check of the track 2 exam harness v0

An independent check, run on core 1 in about 8 CPU-minutes. Scripts and outputs are in `check/`. The prototype produced no figures.

## What holds

- **The code does what the report says.** The scores, leave-one-out oracle, cell rule, aggregates, program checks, `Lab` refusals and truth branching are all correct.
- **Existing behaviour is unchanged.** No pre-existing `vw` or `port` file was modified, and the vw suite passes 105 tests.
- **The re-run is bit-identical.** Stage A, and world 0 at the small passive budget end to end (Lab through B0–B3 to the 128-item exam), match the saved outputs exactly.
- **The headline numbers recompute.** My own aggregation and bootstrap reproduce every aggregate, gap and standard error in sections 3, 4 and 6 (SEs within 0.001). They also reproduce B3's skill: 0.974 with the fair estimator, 0.645 with v1's.

## Problems

1. **Acceptance check 1 passes.** Under the pooled ratio the report adopts, it passes in world 0 at the small passive budget, with every gap at least 4.5 SE at all three allocations.
   - It passes only because B0 is far below climatology (−0.78) while B1 is not above it (−0.07 ± 0.04).
   - It fails under the equal-weight mean, at the large budgets and at small active.
   - The report's restatement of the check stands; "cannot pass at any single budget" is false.
2. **Check 4 is misdiagnosed.** The prior-mean control already scores 0.83, 0.93 and 0.86 in the three worlds, against B3's 0.94, 0.95 and 0.94.
   - The history closes 0–48% of that small gap, so it does not identify θ "almost as well as 4,000 ticks".
   - B2 does lie between B1 and B3, and more budget does close the gap.
   - Fix: make θ matter more; shorter histories will not help.
3. **The pooled ratio changes what is measured.** It puts 87% of its weight on level 1 at h ≤ 4 and 3% on the h = 16 cells. The prior-mean control scores 0.83 pooled but 0.34 equal-weight. This confounds problem 2, and the recommendation to adopt it needs this caveat.
4. **"Charge = KL exactly" is an identity:** both sides compute ½Σ‖u‖²/σ². The real test is the Monte Carlo likelihood ratio, which passes (|z| ≤ 1.6).
5. **The SE of 10.9 at R = 4 uses the n = 128 cells.** The R = 4 exam's own rule drops h = 16, which gives an SE of 0.014. The 10.9 is also seed-unstable (about 20).
6. **The GPU estimate has a slip.** 200k member-ticks at 10³–10⁴ per second is 0.006–0.06 GPU-hours, not 0.06–0.6. Corrected: **1.3–3.8 GPU-hours per run and 15–37 for the grid** (the report says 1.3–4.3 and 15–45).
7. **Untested claims:**
   - `Lab` and `HistoryExam` on `MapWorld`;
   - "at least 8 truths" (only R = 4 and R = 16 were run);
   - "B1 overfits" (plausible: 96 input regressors on 125 rows).
8. **Minor:** the aimed-item numbers are equal-weight, not pooled. B2 and B2x differ by up to 0.018 per world.

## Edits to `results/summary.json`

All edits are under `headline` and listed in `checker.edits`. They correct the GPU strings, source the 2.5 CPU-hour truth cost, and add the check-1 chains, the pooled weights, θ headroom, the R = 4 SE, `untested_claims` and a `checker` block. Re-running `summarize.py` would undo them.

## Verdict

- **The library and the estimator decision:** sound and reproducible.
- **The aggregate change:** supported, with the weighting caveat.
- **Checks 1 and 4:** need rewording.
- **GPU cost:** still depends on the unmeasured throughput benchmark.
