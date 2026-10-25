# Evidence pack: nrch (seed 0)

- world: `../world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 649s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/world.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/pack_sub --seeds 0 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [-0.9676, 1.0196], min area 6 px

## Measurements
- components: final 6, mean 8.9, max 25; occupancy final 0.23
- tracks: 25; persistent (alive >= 50% of run): 8; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 68.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 1000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 25
- channel total drift (end/start - 1): [0.0, -639.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 63: holes 0, rim-vs-core 0.24, rim-vs-outside 0.83, heterogeneity 0.13; core [0.991, 0.076] rim [0.813, 0.232]
  - track 1 at frame 63: holes 0, rim-vs-core 0.25, rim-vs-outside 0.87, heterogeneity 0.13; core [0.992, 0.095] rim [0.804, 0.262]
  - track 7 at frame 63: holes 0, rim-vs-core 0.33, rim-vs-outside 0.69, heterogeneity 0.14; core [0.984, 0.045] rim [0.741, 0.274]
  - track 13 at frame 63: holes 0, rim-vs-core 0.29, rim-vs-outside 0.79, heterogeneity 0.13; core [0.99, 0.073] rim [0.778, 0.273]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 50 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.972, rim/outside 41 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.97)
  - radial psi: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 17.2, rim/outside 0.961 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.894)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3150, R_eq 21.04): none; #1 (t=3150, R_eq 24.19): none; #7 (t=3150, R_eq 17.51): none; #13 (t=3150, R_eq 20.03): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
