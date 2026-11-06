# Level 0: Flow-Lenia worlds

The Flow-Lenia law is implemented, checked against the authors' reference code, and the search kept three worlds with several persistent, moving, interacting creatures. The harness blocked writing a report file into the folder, so the report is below.

Mass is conserved to about 1e-14 over 10⁴ steps at 128². Two caveats come first:
- **Motion is slow.** Bodies move 0.05–0.08 px per step, so one crosses its own length in roughly 120–700 steps.
- **Two of the three worlds use smaller kernels than the paper allows.** Their kernel radii are multiplied by 0.3 and 0.7.

## 1. Implementation and checks

`flowlenia.py` holds `step(A, params, t=0) -> A` on a float64 array of shape (C, H, W), periodic box. For C = 2 at 128², h0 has 32768 entries.

- **Affinity.** U_j = Σ h_i G_i(K_i * A_c0(i)) over kernels feeding channel j, by FFT. K = sigmoid(-(D-1)·10)·Σ_q b_q exp(-(D-a_q)²/w_q), with D = |x|/((R+15)·r·R_scale), normalised to sum 1. G = 2 exp(-((u-m)/s)²/2) - 1.
- **Flow.** F_c = (1-α)∇U_c - α∇A_Σ, with α = clip((A_Σ/θ_A)^n, 0, 1), n = 2, θ_A = C. Gradients are periodic Sobel filters.
- **Transport.** Reintegration tracking, σ = 0.65, dd = 5, dt = 0.2. Each cell's mass is split exactly over the 3×3 cells its moved square overlaps.
- **Optional noise**, a pure function of (seed, t):
  - `flow`: adds noise to F; mass is conserved exactly.
  - `additive`: adds zero-mean noise to A, then clips at 0, so mass drifts by the clipped amount.

**Paper vs code.** The paper (eq. 5) and your spec compute α from A_Σ; the authors' code uses each channel's A_c. I default to A_Σ, and `alpha_src="channel"` gives the code's version. For C = 1 they are the same. The kernel formula and parameter priors follow the code. The code pads Sobel with zeros; mine wraps around.

**Checks** (`checks.py`, results in `checks.json`):
- **Agreement with a numpy transliteration of the reference** (kernels, step, roll-based torus transport):
  - kernels: 1e-17
  - full step: 7e-14 (9e-14 with channel α)
  - transport alone under large random flows: 6e-15
- **Mass drift after 10⁴ steps at 128²** (relative): 5.6e-14 (C = 2), 4.3e-14 (C = 1), 1.5e-14 (C = 2 with flow noise). Over the 4000-step world runs it is at most 1.3e-14.
- **Determinism.** Re-runs are bitwise identical, with and without noise. Each saved world regenerates exactly from `init.npz`.
- **Speed** (one core): 1.9–3.9 ms per step at 96², 3.1–7.0 ms at 128². The three worlds run at 4.4–6.6 ms per step.

## 2. Search

I drew 450 rules from the reference priors on a 128² torus for 2000 steps, from 2–10 random noise patches covering about 20% of the box. C was 1–3 and k was 10–20. There were two groups:
- **paper**: radii as sampled.
- **shrunk**: every kernel radius × 0.3–0.7. This is my only deviation from the paper; at paper radii (17–40 px) a 128² box usually holds one body.

Bodies are blurred density components, tracked by overlap, with fusion/fission events, contacts, occupancy and path length counted.

| Outcome | paper (n=113) | shrunk (n=337) |
|---|---|---|
| Localized | 65% | 65% |
| ≥ 3 persistent bodies | 5.3% | 48% |
| Also moving and interacting | 0.9% (1 run) | 3.6% (12 runs) |
| Seas | 0 | 4 |

No run gave NaNs or dissolved. Most rules make static ring or dotted cells, labyrinths, or foams of dots.

I checked sheets of the top 40 and of 40 random runs by eye. I then re-ran 20 picks for 4000 steps on 3 seeds. CPU: about 1.43 h search, 0.41 h confirmation, 0.3 h other, so about 2.2 CPU-hours in total.

## 3. The three worlds (4000 steps each)

"Major" bodies have at least 30% of typical body mass and live at least 100 steps. "Life" is the time between fusion or fission events.

| | A_gliders | B_swarm | C_cells |
|---|---|---|---|
| Rule (search run) | 26: C=2, k=20, radius ×0.3 | 129: C=2, k=10, radius ×0.7 | 28: C=2, k=15, paper priors |
| Bodies, median (range) | 8 (6–8) | 14 (10–18) | 5 (3–7) |
| Body length | 10 px | 13 px | 34 px |
| Speed | 0.084 px/step | 0.050 | 0.079 |
| Life, median / 90th pct (steps) | 520 / 1545 | 250 / 590 | 380 / 2020 |
| Fusions / fissions | 35 / 32 | 94 / 100 | 7 / 7 (31 / 34 at a 2× threshold) |
| 3 seeds | 7–8 bodies, 0.055–0.065 | 10–14, 0.042–0.060 | 4–5, 0.049–0.071 |
| With flow noise (std 0.5) | 8, 0.056 | 13, 0.068 | 5, 0.088 |

What a viewer sees:
- **A_gliders.** About 8 crescents with a dotted cyan rim and an orange band. They glide in straight lines; long-lived ones cover 10 body lengths. Colliding pairs fuse into U-shaped worms that later break back into crescents. Bodies travel 4–5 lengths between events. This world has the cleanest motion and the most stable identities.
- **B_swarm.** A crowded, lively gas of about 14 ring and crescent cells with orange tails. They wander, touch, form bridges, fuse and split. It has the most interaction, but a body lasts only about one body-length of travel between events.
- **C_cells.** The only hit under the paper's own priors. Four to seven large cells, each a cyan membrane around a grainy orange interior, crawl about trailing cyan tethers. They bind through the tethers, fuse, divide, and sometimes shed droplets.

Each world folder holds:
- `params.json`: the rule, how the initial state is generated, and the screen settings
- `init.npz` (A0 and seed) and `state_t4000.npz`
- `video.mp4`: 4000 steps, 512 px, H.264 yuv420p, 1.6–2.9 MB
- `metrics.json`: tracks, events, time series, fragment-robust event counts, threshold sensitivity
- `robustness.json`: the 3 seeds and the noise run
- `sheet.png`, `tracks.png`, `timeseries.png`

`alternates.json` keeps two runners-up: run 441, about 23 ring cells that persist all run but barely drift (0.01 px/step), and run 158, about 20 small cells with C = 3. To reproduce a world, loop `A = flowlenia.step(A, params, t)` from `init.npz`.

## 4. Known limits

- **Slow motion.** Level-1 tasks need horizons of hundreds of steps, or level-1 sampling every 10–50 steps.
- **Event counts depend on the screen.** In B and C, fusions and fissions include brief contacts through thin bridges, tethers and tail fragments; C's fissions go from 7 to 34 when the threshold doubles. The tracker is heuristic. The first-round motion screen counted centroid jumps at fusions as motion; I fixed this before the confirmation runs. The fractions in section 2 come from screens, checked by eye only for 80 runs.
- **No growth or reproduction.** Total mass is fixed and there is no source, so bodies only fuse and split. Expect individuals, motion and interaction, not reproduction. Flow-Lenia gliders are already known, so these worlds are not novel.
- **Not tested:** a resolution change with scaled kernels and flow, or ±10% parameter jitter. With fixed-σ transport, each world is defined on its 128² grid.
- **Radius shrink.** A (×0.3) and B (×0.7) rely on it, outside the paper's ranges.
- **Agent inputs must keep A ≥ 0.** Additive noise clips and breaks exact conservation. Zero-sum inputs fit the conserved mass, but the interface still has to clip or limit input size.
- **Cost.** About 5 ms per step on one core, so 20–30 s per 4000-step rollout. Large rollout datasets will need batching or a GPU port.

Folder size is 33 MB.

Files are in /home/user/evalwork/vecworld/level0/:
- flowlenia.py
- checks.py
- checks.json
- worlds/A_gliders/
- worlds/B_swarm/
- worlds/C_cells/
- worlds/alternates.json
- search/summary.json
- search/sheets/
- confirm/summary.txt