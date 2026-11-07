# Check of the actuation probe

**Verdict:** the code does what the report says; all headline numbers reproduce; "wind, not kick" follows. Some claims overreach and three confounds go unstated.

## Checks (core 0, about 5 CPU-minutes plus vw tests)
- **Code read:** the wind enters all 20 substeps before the clip, on an independent noise stream. Programs charge exactly C nats; KA16 sits at the `Admissible` cap; the shift estimator is unbiased.
- **Rerun:** `probe.py` state 10 is bit-identical to the saved record.
- **Independent recompute** from the saved probe records: all effect means and SEs, oracle variances, dV, lateral shifts and kick matter moved are equal.
- **No figures** exist.
- **vw/port:** no port file changed. The new vw modules belong to the `harness` prototype, and actuation does not import them. vw tests: RESULT_PLACEHOLDER.
- **My error:** I truncated `probe_effects.json` (`analyze.main` opens it before dumping), then restored it by re-running `analyze.py`. Same 51,219 bytes, and every block copied into `summary.json` is identical.

## Edits to `summary.json`
1. `viability.design`: "noise-free" → "wind-free (σ_w = 0; flow noise 0.5)" closure trajectories.
2. `member_ticks.check_wind`: 14 → 25.
3. New `checker` block: reproduction notes, 14 sourced corrections and 3 confounds.

Re-running `make_summary.py` would undo all three edits.

## Corrections
- **CPU:** 0.137–0.164 s per member-tick, not 0.147–0.164.
- **Admissible kick at h ≤ 8:** ≤ 0.0065 (coarse) and ≤ 0.0175 (objects). The 0.016 and 0.024 maxima are at h = 16. KA64 objects is 0.015–0.037.
- **"About 87% of nats reach level 1":** that is the best tick (3) at one state, a Gaussian plug-in with 32 keys. Ticks 1–2 give 66–84%. At tick 4 it is 15–19% (1-d) or 64–73% (2-d), when the twins' lateral SD jumps to 2.58 px.
- **"The push sets the effect":**
  - Shown on the coarse view only: 10 states, one push size.
  - Ratios beyond h = 1 are ≥ 1 (up to 1.25, z ≤ 1.8), so the σ_w⁻² budget extrapolation is conservative.
  - On the objects view, h ≥ 4 is unresolved (1.57×).
- **Regional vs aimed:** 0.65–0.73× (coarse, 50 nats) and 0.57–0.62× at 12.5 nats. Log-log slopes of 0.89–1.00 are coarse-only.
- **Objects oracle variance** (3 keys) disagrees with the closure V_oracle by a factor of 0.5–3 at every horizon; coarse matches. Objects budgets are rough throughout.
- **Wind-world V_best ≈ V_best + dV** is an approximation, not a proven lower bound.
- **σ_w = 0.8 "births appear":** one birth in 750 member-ticks. The break rests on speed.
- **"Wind's own drift"** is an interpretation; it was not measured.
- **"3–4 px for h ≤ 4, 7 px for h = 8"** was unsourced. I derived it: it holds for the coarse view at σ_w = 0.05, as displacement by tick 4. The objects view needs 6–8 px.
- **"About 1 GPU-hour at 10³ member-ticks/s":** 50k member-ticks at that rate is about 50 s. The GPU estimate does not follow.

## Unstated confounds
- **One kick design** (open-loop flank transfer). "Kick barely registers" is shown for this design only.
- **Best-case targets:** all 40 are the fastest isolated body. Crowded or slow bodies are untested.
- **The choice of σ_w = 0.05 over 0.1** rests on extrapolated dV (3% vs 14% of V_best at h = 1). The 3-member viability test cannot separate them: 0.1 misses one band by 0.014.

## What stands
Wind, not kick: the capped kick reaches ≤ 0.0065 V_best (coarse, h ≤ 8); aimed wind at 12.5 nats (σ_w = 0.2) reaches 0.15–0.18. The budget scale (115–140 nats at σ_w = 0.05, coarse, h ≤ 4) holds, and the certificates must be recomputed.
