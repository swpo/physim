# Check of the fresh closure runs (key `closure`)

Checker: core 0 only, about 8 CPU-minutes. My scripts and outputs are in `../check/`, along with `summary_before_check.json`, the summary as it was before my edits.

## Verified

1. **Only VW-1 produced results.**
   - The simulation uses `RecWorld`: `MapWorld(specs['both'])` plus a read-only tracker-memory record.
   - It calls only `ensemble`, `clone(fresh=True)`, `rollout` and `chunked_rollout`.
   - `analyze.py` imports `lenia_world`/`flowlenia`, but only its numpy estimators and `objects_stats` run.
2. **Sizes and seeds match the metadata and array shapes.**
   - Seeds 301/302, 18 members each, T = 300, test ticks 40/100/160/220.
   - R = 6, 32-tick branches, 96-tick extension.
   - 47,160 member-ticks, float32 only, 59 MB.
3. **Bit-for-bit re-run** (`rerun_sim.py`). I re-simulated sim_A from scratch at the same layouts. Base level 1 and the tracker table for ticks 0–50, and the first 4 ticks of the 90 tick-40 clones, equal `sim_A.npz` exactly.
4. **Null passes** (`sim_probe.json`): same key in one call gives 0, fresh keys give about 2 after one tick. This part has no shared-noise twins. Replicates are independent fresh-noise copies, so the base and clone layouts (B 18 / T 10 vs B 90 / T 4) do not matter.
5. **Analysis end to end** (`e2e_analysis.py`).
   - The unmodified `analyze.closure` reproduces every non-learned V and V_oracle in `closure_objects.json` exactly.
   - Re-training slotnet on fold 0 reproduces the saved errors to 6e-8, which is float32 rounding.
6. **Own code** (`recompute.py`) reproduces:
   - oracle, V0 and persistence, per item;
   - all ceiling curves, the old-set curves, z and the selection check (shifts ≤ 0.002);
   - chaos curves and crossings (42/75 and 27/54 ticks);
   - the τ = 1 shares (10.7/52.8%, 11.0/53.5%, every-tick AR(1) 11.8/68.8% over 83,289 slot-ticks), the per-event errors (0.45 vs 15.0) and velocity 35%;
   - objects statistics: median 7, 23.2/23.0 events per 100 ticks, no births or deaths.
   - SEs agree within 0.003.
7. **The old 16% was sampling.** In the VW-0 data (read only), the 72 test states give 15.7% ± 2.2%, while every tick gives 11.5%.
8. **`closure_check.png` matches the JSON.** No videos were made.

## Corrections (in `summary.json`, listed under `checker.edits`)

1. **Coarse learning curve.** "Fit-to-fit variance" is not shown.
   - The residual net's linear baseline is chosen per horizon on validation. At 16 ticks it is AR(1) with 4 or 9 trajectories and ridge_p2 with 18; at 8 ticks it is AR(1) with 4.
   - Every non-monotone point is that switch.
   - The 9-trajectory fit reaches c = 0.24 at 16 ticks (headline 0.136 ± 0.012).
   - So the 16-tick value is a loose lower bound, and its SE excludes fit and baseline-choice variation. "Most of the ceiling is lost by 16 ticks" still holds.
2. **Validation gains.** patchnet's 21–27% and slotnet's 5–12% hold only at 1–8 ticks. At 16–32 ticks patchnet gains 3–7%; slotnet gains 2–4% at 16 and ≤ 0.6% at 32.
3. **Chaos.** "Neither reaches 1.0 within 96 ticks" is true for coarse (0.98 and still rising) but not established for objects:
   - the curve peaks at 0.996 at 71 ticks;
   - 64% of bootstrap resamples reach 1;
   - the 60–96-tick mean is 0.93 ± 0.025 (the report's "± 0.02" is not in the JSON).
4. **Objects gap.**
   - The quoted ± 15% is the all-replicate SE; the base version's SE is ± 14%.
   - At the same 144 states AR(1) gives 57% ± 14%, which the report omits.
   - "About two thirds" therefore describes AR(1) at every tick; for the best predictor it is about half.
   - Wording is in `objects_gap_tau1.headline_wording`.
5. **The `estimator` string** named only rmlp. It now names patchnet, patchnet_long and slotnet, and says that the SE holds the predictors fixed.
6. **Minor points.**
   - Coarse is also above VW-0 at 1–2 ticks (z = 6 and 8), though only by 0.003–0.014.
   - The objects z at 4 ticks is 1.1, not 1.2.
   - "The 16-tick jump is more data" is mostly supported: ridge_p2 on 18 trajectories gives 0.067 (VW-0 0.042), against 0.126 on 27.
7. **Caveat.** Clone r of member j has identical noise keys in sim_A and sim_B (same world seed and branch counter). The states differ, so the effect is negligible.

## Confirmed unchanged

Headline ceilings and SEs, old-set ceilings, V0/Voracle/Vbest, learning-curve drops, run cost and disk use.
