# Evidence pack: nrch (seed 0)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 922s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/A2s0 --seeds 0 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.0726, 1.1051], min area 6 px

## Measurements
- components: final 8, mean 11.8, max 20; occupancy final 0.23
- tracks: 347; persistent (alive >= 50% of run): 0; longest 46 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 9, 8], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.245/time; max body lengths 17.5
- replication (lineage window K = 20 frames = time 1000, default): splits 61, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 58, merge/split ratio 0.951, nucleations 187
- channel total drift (end/start - 1): [-0.0, -255.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 252 at frame 98: holes 0, rim-vs-core 0.15, rim-vs-outside 0.54, heterogeneity 0.19; core [0.944, 0.404] rim [0.801, 0.428]
  - track 272 at frame 100: holes 0, rim-vs-core 0.26, rim-vs-outside 0.38, heterogeneity 0.18; core [0.917, 0.349] rim [0.662, 0.376]
  - track 274 at frame 100: holes 0, rim-vs-core 0.23, rim-vs-outside 0.47, heterogeneity 0.19; core [0.936, 0.434] rim [0.702, 0.434]
  - track 290 at frame 102: holes 0, rim-vs-core 0.26, rim-vs-outside 0.39, heterogeneity 0.19; core [0.924, 0.322] rim [0.665, 0.367]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 69 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 7.27 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.829)
  - radial psi: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 1.01 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.596)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #252 (t=4900, R_eq 17.82): none; #272 (t=5000, R_eq 13.87): none; #274 (t=5000, R_eq 16.09): none; #290 (t=5100, R_eq 12.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
