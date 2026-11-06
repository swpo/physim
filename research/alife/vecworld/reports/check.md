No report file exists in `/home/user/evalwork/vecworld/integrate/`, and I was not allowed to write a corrected copy, so the replacement text is listed below. All values are reproducible from the scripts in `/home/user/evalwork/vecworld_integrate_review/`, each saving a same-named `.json` there; frames are in `frames/`. I used about 3 CPU-minutes.

## Verified

1. **Mass conservation holds.**
   - Level-0 law with the VW-0 noise over 111 ticks (2220 steps): relative drift is at most 7e-15 and A stays ≥ 0.
   - A substep with flow noise of std 200, far past the clip, conserves mass exactly.
   - 400 admissible exact-zero-sum inputs, random and on bodies: per-channel change is at most 2e-13 (about 3e-16 relative), A ≥ 0, and at most 2.0 units move per tick.
2. **h1 comes only from h0 and the declared memory.**
   - `Ensemble.h1` is Phi(h0, m), and m changes only through `memory_update(m, h0_new)`.
   - Replaying the tracker from the h0 history alone gives exactly the same m. The tracker keeps no hidden state and is deterministic, and Phi_coarse ignores m.
   - My own block means agree to 2e-16. My own periodic labelling matches the present-slot masses at 11 of 11 ticks and the centroids to 3e-14 px.
   - `run_base` reproduces `base_000` bit for bit up to t = 61, and one branch replicate reproduces to 2e-16.
3. **Input constraints are enforced, with one exception.**
   - These are all rejected with state, t and ticks unchanged: k = 9, a value of 1.5, Σ|a| = 4.4, a non-zero sum, NaN, an out-of-range index, a string key, a wrongly shaped vector, and a `run()` program whose third entry is bad.
   - **Bug:** the checker allows |Σa| ≤ 1e-9·max(1, Σ|a|), but the kick only takes the mass-conserving branch when |Σa| ≤ 1e-9·Σ|a|. So the command {+0.45, −0.45+9e-10} passes the check and falls into the branch that adds matter. Through the agent API it created 2.37 mass units in 10 ticks, with no bound over an episode, and it changes the channel composition. The exact-zero-sum control changed mass by only 5e-13.
4. **The permutations are real but hide only the index order, not the meaning.**
   - Observations equal the quantised, permuted h1 exactly. Both maps are non-trivial (3 and 1 fixed points) and change with the world seed.
   - From a single 300-tick episode, a blind rule recovers all 12 presence coordinates, the slot of all 144 coordinates, and all 24 centroid pairs. It uses only {0, 1} values, shared zero patterns and constant-norm pairs.
   - For Phi_coarse, every one of the 192 coordinates has its best shared-zero partner in its own block.
   - The public card's `name` (`A_gliders/objects12`, `A_gliders/coarse8`) reveals the creature, the coarse-graining and K.
   - The two companion worlds built with the same world seed share one input permutation.
5. **Closure ceiling, own code (own folds, predictors and λ):** A objects at τ = 1 is 0.815 (report 0.81). A coarse at τ = 4 is 0.793 (report 0.79). The full curves agree within the bootstrap error.
6. **Input visibility, own simulation (12 states, new body cells):** response divided by the oracle spread at τ = 1 is 0.16 for objects and 0.12 for coarse (report 0.13 and 0.23). It is at most 0.28 up to τ = 8 (report: below 0.35). Random placement gives at most 0.004 for objects (report: at most 0.004).
7. **Unit tests:** 37 of 37 pass. They cover the spec only; nothing tests `lenia_world.py`.
8. **Videos match the claims.** All five are H.264 yuv420p, 896–900 px wide and at most 2.79 MB. I looked at both posters and 3 frames of each video:
   - Glyphs follow the bodies.
   - Coarse blocks follow the matter.
   - B's tracker merges tethered rings into large slots.
   - In the steer video the steered glider curves away from its grey twin, and later the whole field diverges.

## Corrections to the report

1. "Phi_coarse close to closed up to about 4 ticks" (summary and §2): change to "for τ ≤ 2 (c ≥ 0.95); c = 0.79 at τ = 4".
2. "Almost all [of the objects τ = 1 gap] comes from identity events": change to "about three quarters".
   - By feature group the best predictor scores 0.27 on identity, 0.21 on shape, 0.29 on velocity and 0.08 on position, against an oracle of at most 0.005.
   - Slots with a tracker event at t+1 are 16% of slot-ticks but carry 75% of the error. Velocity on event-free slots carries another 20%.
3. "No state reaches 1" is false. At τ = 16, 1 of 12 states reaches 1 under each 8-tick default program on Phi_objects. "At most 0.07 at every horizon" is a median over states; say so here and in §4.1.
4. "Designer probe 20 times over budget": change to "8 times the per-tick total (Σ|a| = 32) and 4 times k".
5. "Each channel's mass is conserved to about 1e-16" and "`InputViolation` works": add the zero-sum tolerance bug.
6. Observation: add that the permutation hides only the index order, and that the card name leaks structure.
7. Steering:
   - "9 isolated gliders": 12 were targeted and 3 dropped because their identity broke within 1 tick.
   - "Twin travels about 28 px": it is 29.6 px.
   - "Mass preserved in 83% of runs": that is within 20% of the twin's mass; within 5% it is 75%, and 7 runs changed by 8–150%.
8. "Bootstrap standard errors 0.01–0.06": change to "at most 0.015 for coarse, 0.01–0.06 for objects". They also leave out the choice of the best predictor on the test items.
9. "Ridge with 2 lags is best" is true for coarse only; for objects, AR(1) with no past is best.
10. "Objects learning curve nearly flat": change to "flat for τ ≤ 4, still falling 9–16% at τ ≥ 8".
11. "Designer ensembles have to be single-member": change to "were run single-member". It is a cost choice, about 10 MB of noise per member per tick.
12. Files:
    - "All are H.264…": only the five videos are; the posters are 1080 × 846 PNGs.
    - "data/ (207 MB)": data is 197 MB; the whole folder is 207 MB.
13. "Never more than 3 processes at once" exceeds the 2-process rule.
14. Recommendation: before shipping, fix the tolerance bug and take the map name and K out of the card.

Everything else checked out against the JSON or my own runs: the 1.9e-14 drift, the whole ceiling table, the learning curve (1.14 → 0.93 → 0.73), the interestingness and B statistics, the exam (0.001–0.014), the compose demo, the 0.67 median body cell and the 146 glider mass.

Files are in `/home/user/evalwork/vecworld_integrate_review/`:
- `check_world.py`
- `check_loophole.py`
- `closure_mine.py`
- `inputs_mine.py`
- `blind_typing.py`
- `blind_coarse.py`
- `gap_events.py`
- `frames/`