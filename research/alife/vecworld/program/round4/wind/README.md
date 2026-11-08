# Round 4, study `wind` (track 2): full-size certification of the gliders wind world on one GPU

Builds on `../../track2/wind_recert` (sigma_w = 0.05 kept; objects-view loss under wind unresolved, up to 0.09;
program effect about 0.1 V_best per item, a linear level-1 predictor recovers about a seventh) and
`../../track2/actuation` (the wind channel, `wind.py`, unchanged).

## Design (all sets in one job, one platform)

| set | what | size |
|---|---|---|
| F | free runs at sigma_w = 0.05, the fresh closure layout | 36 trajectories x 300 ticks, test ticks 40/100/160/220, 5 fresh-noise branches x 32 ticks, the tick-40 branches run on to 96 ticks |
| M | the same layout and the same keys at sigma_w = 0 (wind-free) | as F |
| MW | M's test states branched with wind on M's keys (replicate 0 = M's base key and clock) | 36 x 4 states x 6 replicates x 32 ticks |
| F2, M2 | a second, independent F/M pair (objects view only, no learning curve) | as F, M |
| P | the wind_recert program mix (none / blind / aimed / regional, 4-tick programs, 150-700 nats) | 36 trajectories, an episode every 16 ticks (8..280), 9 test episodes per trajectory = 324 items (81 per class), 5 program branches + 3 no-input twins x 16 ticks |

Estimator: `vw1/fresh/closure/scripts/closure_lib.closure_ext` (the checked copy of `integrate/analyze.closure`;
the unmodified function must agree exactly, MLP off) with the VW-0 MLP, the JAX `rmlp` and `patchnet` (coarse) /
`slotnet` (objects) trained on the GPU; learning curves at 1/4, 1/2, all fit trajectories (F, M). For P the
wind_recert input-aware '+u2' predictors and new input-aware nets `patchnet+u` / `slotnet+u` (the declared future
commands as level-1 wind channels; `p4lib.py`); exam effect, true effect from the no-input twins, the share of the true
effect a level-1 predictor recovers, and fair energy scores of residual-pool ensemble forecasts.

Code: `w4.py` (paths, layout, the jax.vmap runner), `check4.py` (vmap runner vs WindWorld's lax.map runner),
`sim4.py`, `clos4.py`, `p4lib.py`, `combine4.py`, `job.sh` (the GPU job), `make_summary4.py`.
Results: `results/` (copied from `origin/gpu-jobs:jobs/<job>/out/`), `results/summary.json` (every number with its
source).

## Results (job r4-wind-002, H100 80GB, 8 Nov 2026; billed $1.86, pod 0.51 h)

Every number below is in `results/summary.json` with its source; the hand-written reading is
`interpretation.json` (also copied into the summary).

| | h = 1 | 2 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|---|
| coarse ceiling F (wind) | 0.991 | 0.966 | 0.847 | 0.496 | 0.175 | 0.066 |
| coarse ceiling M (no wind) | 0.991 | 0.967 | 0.856 | 0.508 | 0.139 | 0.069 |
| coarse F - M (SE) | -0.000 (0.000) | -0.001 (0.001) | -0.009 (0.005) | -0.012 (0.012) | +0.037 (0.019) | -0.002 (0.010) |
| objects ceiling F / M | 0.848 / 0.853 | 0.768 / 0.775 | 0.616 / 0.615 | 0.429 / 0.417 | 0.214 / 0.208 | 0.063 / 0.057 |
| objects F - M, two pairs pooled (SE) | +0.012 (0.016) | +0.006 (0.018) | +0.020 (0.018) | -0.002 (0.019) | -0.004 (0.021) | -0.009 (0.015) |
| oracle cost of the wind, paired (MW), coarse / objects, V_best | 0.044 / 0.028 | 0.025 / 0.028 | 0.012 / 0.034 | 0.010 / 0.043 | 0.017 / 0.039 | 0.034 / 0.039 |

- The closure certificate survives the wind at full size in both views. The objects-view loss left open by
  wind_recert is closed: none (one-sided 95% bound below 0.04 at every horizon).
- Coarse learning curves are not saturated (V_best -26 to -36% from 1/2 to all fit trajectories at h = 1-8);
  objects 2-6%.
- Program mix P: true effect per program item coarse 0.20, 0.22, 0.20, 0.09, 0.08 V_best, objects 0.08, 0.08, 0.09,
  0.06, 0.10. Coarse: the best level-1 predictor is the input-blind patchnet at every horizon; patchnet+u is worse,
  the linear +u2 recovers 12-18% of the effect at h <= 4 on a weaker base. Objects: slotnet+u recovers 44%, 18%, 6%
  at h = 1, 2, 4; 'actions matter' z (energy score, one truth per item) 3.0 / 4.2 at h = 1 with 64 / 128 items,
  4.0 / 5.6 on the aimed+regional half; below 2 at h >= 2.
- GPU float64 runs are not deterministic (same state, same key, one vmap call: 1.2e-7 apart after 3 ticks), so
  common-random-number pairs decorrelate after about 5 ticks on the GPU; record the platform with every truth.
