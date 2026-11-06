# Check of the fresh VW-1 input runs (key: inputs)

**Verdict.** The runs are genuine VW-1 runs. All twin nulls are exactly 0. The headline numbers recompute exactly from the saved outputs. Nine statements need correcting; they are listed under Corrections, and `summary.json` now carries the corrected numbers.

## Provenance

- **Simulator.** All simulation goes through `aworld.build()` + `MapWorld` and the vw Designer and Ensemble API; nothing simulates with `level0/flowlenia.py` or `lenia_world`. `kick_np`, which copies `flowlenia_jax.kick`, only measures moved matter.
- **Sizes and seeds.** They are as stated: 40 states (seed 7001, world seed 0, 60 ticks); 32 × 43 members × 32 ticks; 81 steering members × 40 ticks; sensitivity states 0–2.
- **Twins and nulls.** Twins share one rollout or step call and the same keys. The null is 0.0 in all 32 visibility states, in steering, and in the 3 finite-difference batches. The autodiff primal equals the rollout bit for bit.
- **Steering re-run.** Identical on every row field.

## My re-runs (core 2, about 14 CPU-min)

- **Visibility, state 13.** Re-ran `visibility.py` end to end (43 members, 194 s). All 19 saved arrays are identical.
- **Test states.** Re-ran `states.py` (40 members, 602 s). The states, tracker memories and level 1 are bit-identical.

## Confirmed by my own estimator (`review/recompute_*.py`)

- **Shift of the mean.** Blind median ≤ 0.0131, worst 0.80, no state ≥ 1. Default-limit programs: median ≤ 0.092 ± 0.020. k32 probe: 0.83 ± 0.12, 10 of 32 states ≥ 1.
- **Random commands.** Moved matter 0.165 ± 0.003; 87% of sites empty, 13% in bodies.
- **Late differences.** Objects: median first tick 23.5, 25 of 32 states. Coarse: 4 of 32.
- **Steering.** 35 of 46 runs; −10.4°, size 20.7°. By strategy 19/24 and 16/22; clean runs 22/23, event runs 13/23.
- **Sensitivity.** 7–72 cells (≤ 0.44%); floor 0.032–0.039; 1.7–9.6% of cells (96–99.6% within 4 px); 1.2–2.1% at 4 ticks. A 0.5 push gives 0.016–0.030 of the oracle variance, 0.07–0.79 of linear.
- **Stride.** The page's "stride applies the input at every substep" is wrong: `stride_level` gates u by (i == 0).

## Corrections

1. **"1 of 32 states exceeds 1 (objects, τ 2–16)".** One state exceeds 1 at each of τ = 2, 4, 8 and 16, but a different one each time (31, 14, 3, 5). The worst is 19.6.
2. **"Toward the side matter was taken from".** This holds only for flank (19/24). Lead takes matter from the rear, so there −n means away from the sink (16/22).
3. **"± 6%".** That is a binomial error; the 46 runs come from 12 targets. Resampling targets gives ± 8%; 10 of 12 targets turn mostly toward −n.
4. **Video "no fusion".** True through tick 22 (mass within 0.5% of the twin). At tick 23, the last frame, the glider fuses into a neighbour (event "fused"). It is last tracked at tick 22.
5. **"188 VJPs".** It is 192.
6. **Finite-difference agreement on the 10 most sensitive cells.** 2e-4 to 3.9e-3 at 1 tick (not "1e-5 to 3e-4"). At 2 ticks 0.02–0.47, against 2.5e-4 to 1.1e-2 overall. "Agree through 2 ticks" holds for typical cells only.
7. **Growth.** 5–100× from 1 to 2 ticks, then 15–230× per tick (not 10–100× and 20–60×).
8. **Most sensitive cells, actual/linear.** 5e-5 to 8e-3 (not "about 1/500").
9. **Minor.**
   - The footprint is 12.6–13.2%.
   - In `sensitivity.png` the finite-difference panel is a 3-state median while the maps are state 0; the caption should say so.
   - `render_steer.log` is stale (it shows 41 frames and 330 KB; the file has 24 frames and 216 KB).

## Media

I opened the poster, frames 1, 12, 22 and 23 of the video, and both PNGs.

- **Steer video.** H.264 yuv420p, 900×364, 24 frames at 4 fps. The panels are as described, with the orange track bending off the grey one. Frame 23 shows the fusion.
- **PNGs.** `visibility.png` matches the JSON (worst values 247 for k32, 19.6 for body ×8); `sensitivity.png` matches the saved maps.

## Edits to `summary.json`

All edits are additions, listed in `checker.edits`; the original is in `review/summary_before_check.json`. Added: `states_ge_1_by_tau`, `n_reached_by_32` (coarse "99" means > 32), the steering clean/event split, the target-resampled SE 0.078, `direction_note`, `video_run.checker_note`, and `c_sensitivity.derived_ranges_over_states`.
