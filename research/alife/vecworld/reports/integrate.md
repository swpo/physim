I built the first two-level example: the Flow-Lenia gliders world (A_gliders) as level 0, with Phi_coarse and Phi_objects on top, measured for both A_gliders and B_swarm. The main results: Phi_coarse is close to closed only up to about 4 ticks, Phi_objects is legible but its ceiling is limited by tracker events, and inputs within the default constraint are essentially invisible to an agent on average, though a designer-targeted program can steer a glider. Total compute was about 2.6 CPU-hours, never more than 3 processes at once.

# First two-level VW-0 world: Flow-Lenia gliders under two coarse-grainings

## 1. The example

**Level 0.** I used A_gliders as the main world because it has the cleanest motion and the most stable identities. B_swarm is the second world, used as a stress test. I did not use C_cells.
- The state h0 = A has shape (2, 128, 128), so n0 = 32768. The law is `flowlenia.step` with per-cell flow noise of std 0.5, drawn from the VW-0 noise stream.
- Mass per channel drifts by at most 1.9e-14 over 7000 steps.
- One tick is 20 Flow-Lenia steps. Gliders move about 1.6 px per tick, so one crosses its body length in about 8 ticks.
- Burn-in is 50 ticks from the level-0 builder's noise-patch initial state. Replay mode is `initial`.

**Phi_coarse** (n1 = 192, no memory): the 8×8 block means of both channels, plus the block mean of A_sum² (a second moment that says how concentrated a block's matter is).

**Phi_objects** (K = 12 slots × 12 features = 144). The tracking memory m holds a slot-label map plus a slot table, and is a deterministic function of the level-0 history.
- **Features per slot:** presence, mass, channel-1 fraction, the periodic centroid, radius of gyration, a nematic pair (elongation · cos 2θ, elongation · sin 2θ) and velocity in px per tick. Empty slots are all zero.
- **Centroid encoding:** I wrote the centroid as (L/2π)(cos, sin) on each axis. With raw x, y, the wrap-around jumps make the mean over replicates meaningless (an oracle would average 127 and 1 to 64).
- **Bodies:** periodic components of blurred A_sum above the level-0 screen's threshold, with mass ≥ 20.
- **Declared rules:**
  - Matching is greedy by pixel overlap, with a fallback to the nearest predicted position.
  - Fusion: the absorbed slot dies and the survivor gets the mass-weighted mean of the parents' velocities.
  - Fission: the product goes into a free slot and inherits the parent's velocity.
  - Birth takes the lowest free slot. A slot freed this tick is not reused until the next tick.
  - For B, K = 24.

**Inputs.**
- **Actuators:** the 16384 cells, each meaning "matter at a cell". This is one physical type, as the spec's rule 4 requires. Actuating both channels separately would let zero-sum inputs convert one species into the other.
- **Kick κ (physics, not a rejection):** a source cell gives up at most the matter it holds, taken with its own channel composition. The sinks receive exactly what was removed, in the commanded proportions. Each channel's mass is conserved to about 1e-16 and A stays ≥ 0.
- **Default constraint:** k = 8 non-zero coordinates, values in [−1, 1], Σ|a| ≤ 4, zero sum.
  - The bound of 1 is about one body cell: the median occupied cell holds 0.67 of A_sum.
  - The total of 4 moves at most 2 mass units per tick, about 1.4% of a glider's mass of 146.
  - k = 8 allows four source/sink pairs.

**Observation:** hidden permutation, quantum 1e-3.

**API checks.**
- Reset, sparse steps, programs and `InputViolation` all work (`smoke_A_gliders.json`).
- The `Exam` harness runs end to end (`exam_demo.json`).
- `stack` (a 4-number level 2), `concat` (A ⊕ B, k = 16) and `stride` all compose (`compose_demo.json`).
- Identical-noise twins reproduce bit for bit.

## 2. Certificates

**What I changed to make the spec's estimators work at this scale.**
- **Data:** 24 base trajectories of 300 ticks for A (12 for B). 72 test states (36 for B), each with 6 replicate futures (the base continuation plus 5 fresh-noise branches).
- **Error measure:** squared error per coordinate in standardised units, so 1.0 is the unconditional mean. Full log-determinants are impossible at n1 = 144–288 with about 70 states.
- **Fits:** predictors are trained with folds held out by trajectory and scored against the replicates. Standard errors come from a trajectory bootstrap.
- **Designer ensembles:** these have to be single-member, because `Ensemble.normals` draws K × 1.3M normals per tick.
- **Predictor pool:** I added the unconditional mean and a per-coordinate AR(1). Ridge on deltas cannot shrink back to the mean, and without these two the long-horizon ceilings came out negative.

Ceiling c = (V0 − Vbest)/(V0 − Voracle); depth gain g = (Vbest − Voracle)/V0. The oracle is the true simulator run from the true (h0, m).

| | τ = 1 | 2 | 4 | 8 | 16 | 32 ticks |
|---|---|---|---|---|---|---|
| A coarse, c | 0.99 | 0.95 | 0.79 | 0.34 | 0.04 | 0.01 |
| A coarse, g | 0.01 | 0.05 | 0.21 | 0.65 | 0.90 | 0.67 |
| A objects, c | 0.81 | 0.63 | 0.51 | 0.26 | 0.13 | 0.04 |
| A objects, g | 0.18 | 0.36 | 0.46 | 0.66 | 0.61 | 0.34 |
| B coarse, c | 0.96 | 0.84 | 0.48 | 0.05 | 0 | 0 |
| B objects, c | 0.63 | 0.48 | 0.29 | 0.21 | 0.14 | 0.04 |

Bootstrap standard errors are 0.01–0.06.

**How to read the closure numbers.**
- **Noise is weak over short times.** The oracle's error on A coarse is 0.011 at τ = 8.
- **Phi_coarse** is close to closed for τ ≤ 4 ticks and far from closed beyond that, where block means lose where each glider sits inside its block and which way it is heading.
- **Phi_objects** has a gap already at τ = 1. Almost all of it comes from identity events: on presence, mass and composition the best level-1 predictor scores 0.27 against the oracle's 0.00, while on position it scores 0.08 against 0.00. Imminent splits and fusions can be read from h0 but not from the slot summaries.
- **Longer level-1 pasts do not help.** Ridge with 2 lags is best and 8 lags is worse, so the estimators cannot see any level-1 memory at this data size.
- **The coarse gap is overstated.** Its learning curve has not saturated: ridge error at τ = 8 falls 1.14 → 0.93 → 0.73 as training grows from 3 to 6 to 12 trajectories. The objects curve is nearly flat.

**Input visibility (A, 12 states).**
- **Identical-noise twins.**
  - A default single-tick input placed on bodies (k = 8, ±0.5) moves 1.6 mass units.
  - Its level-1 response, relative to the oracle's spread, is 0.13 (objects) and 0.23 (coarse) at τ = 1, below 0.35 up to τ = 8, and about 1.2–1.4 by τ = 32.
  - Random placement, which is what a blind agent does, mostly lands on empty cells and moves a median of 0.17 mass. Its response stays at or below 0.004 (objects) up to τ = 8.
  - Inputs off bodies move only about 1e-5 mass, yet even they reach twin responses near 1 by τ = 32. The level-0 L1 difference grows to about 1400, close to the total mass of about 1420.
  - So the late twin differences are chaotic scrambling, not a reproducible effect.
- **What an agent can actually see.** I ran the same open-loop program under 6 noise realisations, each against its own twin, and measured the shift in the conditional mean.
  - Default inputs, sustained for 1 or 8 ticks, on bodies or at random: the mean shift is at most 0.07 of the oracle spread at every horizon, no state reaches 1, and it is at most 0.03 of the level-1 prediction error.
  - Only a designer probe 20 times over budget (k = 32, value 1, for 8 ticks) reaches 0.3–0.8 at τ = 1–4.
  - B gives the same picture.
- **Can sparse inputs steer a creature?** Yes, when a designer chooses the cells each tick from h0.
  - Setup: 9 isolated gliders, 4 programs each within the default constraint. Matter moves flank to flank, or from the rear to just ahead on one side.
  - Result: 32 of 36 runs turned the same way relative to the commanded side.
    - Median heading change is 20°, with a 6.3 px lateral offset, over a median 15.5-tick window before an identity event. The twin travels about 28 px in that time.
    - Mass is preserved in 83% of runs.
    - The sign is reversed: the glider turns toward the flank matter was taken from, away from where it was deposited.
  - In B the identity windows are too short (median 8.5 ticks) to tell.

**Interestingness** (all 7200 A ticks).
- **A at level 1:** a median of 8 objects (6–9).
  - Speed is 0.081 px per step; bodies are 12.7 px long.
  - Tracks of at least 50 ticks travel a median of 7.6 body lengths, and 98% travel at least 3.
  - There are no births or deaths. Fusions and fissions run at 23 per 100 ticks each. There are 18 encounters per 100 ticks and 65% of them fuse into U-shaped worms, which split again.
  - Median track life is 20 ticks.
- **B:** a median of 14 objects, but slow (0.019 px per step).
  - There are 84 fusions per 100 ticks, track life is 10 ticks, and only 5% of tracks live 50 ticks.
  - The tracker merges rings joined by tails or tethers.
- **Rubric codes for A_gliders at level 1:**
  - **I:** Supported for the gliders. Track identity churns through worm events, but bodies persist through them.
  - **M:** Supported. These are known Flow-Lenia gliders, so novelty is 0.
  - **X:** Weak. Repeatable fusion and fission, but there is no matched ablation and merges roughly equal splits.
  - **B:** present only at level 0. The level-1 slots do not show the cyan rim.
  - **D:** absent; fission without growth is fragmentation.
  - **S:** not met, because the initial state is planted noise patches.
- **Rubric codes for B:** I and M Weak, X present but obscured by the tracker.

## 3. Recommendation

The first world should be **A_gliders with Phi_objects**. It is the legible level the design aims at: individuals, motion and interaction are visible, the ceiling is 0.81 at one tick, and level-0 access gives a real depth gain.

Ship **A_gliders with Phi_coarse as its companion**: the same h0 and the same law, a cleaner closure certificate, and no tracker heuristics. The pair tests whether an agent can tell that both are views of one law. Do not use B as a first world.

## 4. What to fix next

1. **The actuator design.** Inputs within the default constraint barely shift the level-1 mean: at most 0.07 of the oracle spread. Inputs only work when targeted at bodies, closed-loop, and a blind agent with 16384 permuted cells will struggle to learn that. Options: coarser actuators (for example 4×4 patches, about 1000 inputs), a larger per-tick total (16–32), or a declared lower noise level. Re-certify after any change.
2. **Tracker events.** Add hysteresis against fusion and fission flicker and against thin tethers (B). Optionally expose event flags.
3. **Units and scoring.**
   - **The exam's raw squared error is dominated by the mass coordinates (around 150²).** In the exam demo, the designer's kinematic predictor scores only 0.001–0.014 skill over persistence.
   - **Fixes:** normalise the Phi_objects units, standardise the exam error per coordinate, and use slot-matched losses.
4. **Estimator power.** Get more than 100 base trajectories (which needs a batched or GPU Flow-Lenia) and use stronger level-1 predictors, such as convolutional nets on the coarse grid, so the coarse gap stops being only an upper bound. Leak and the Gaussian information gap were not computed.
5. **Level-0 validity** is still untested under a resolution change or ±10% parameter jitter.

## Files

All in `/home/user/evalwork/vecworld/integrate/`:
- **World definition:** `lenia_world.py` (the two `WorldSpec`s, tracker and kick).
- **Runners:** `run_base.py`, `run_branches.py`, `run_inputs.py`, `run_inputs_rep.py`, `run_steer.py`.
- **Analysis:** `analyze.py`, `learning_curve.py`.
- **Demos:** `smoke.py`, `exam_demo.py`, `compose_demo.py`.
- **Rendering:** `render_l1.py`, `prep_render.py`, `make_videos.py`, `plot_certs.py`.
- **`results/`:** `A_gliders_certificates.json`, `B_swarm_certificates.json`, `A_gliders_learning_curve.json`, `certificates.png`, `exam_demo.json`, `compose_demo.json`, `smoke_A_gliders.json`.
- **`videos/`:** `A_gliders_objects.mp4`, `A_gliders_coarse.mp4`, `A_gliders_steer.mp4` (the twin input experiment), `B_swarm_objects.mp4`, `B_swarm_coarse.mp4`, and `A_gliders_poster.png`, `B_swarm_poster.png`. All are H.264 yuv420p, at most 900 px wide and at most 2.8 MB. I looked at both posters and at 3 frames from each video.
- **`data/`** (207 MB in total): the stripped base runs, branches, input and steering runs.
  - **Removed after use:** the level-0 snapshots and frame stacks.
  - **Regenerating:** `run_base.py` reproduces them exactly.
  - **Branching:** the test states saved in the base files are enough to branch from.