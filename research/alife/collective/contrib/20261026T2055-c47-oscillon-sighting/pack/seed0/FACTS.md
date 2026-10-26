# Evidence pack: param-oscillon (seed 0)

- world: `../../world.py`, family `parametric-oscillon`
- parent: None; mutation: new class: damped wave field with detuned parametric pumping drawn from a consumed, regrowing energy field
- run: 151 frames x 1000 steps x dt 0.02 = time 3000; grid [128, 128]; wall 618s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2055-c47-oscillon-sighting/world.py --out collective/contrib/20261026T2055-c47-oscillon-sighting/pack --seeds 0 1 --frames 150 --lineage-k 5 --no-movie`
- segmentation: matter > 0.30 of robust range [0.0044, 1.6594], min area 6 px

## Measurements
- components: final 55, mean 72.8, max 158; occupancy final 0.12
- tracks: 410; persistent (alive >= 50% of run): 60; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.52 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [58, 57, 55], H1 [0, 0, 0]
- motion: 38 long-lived tracks moved >= 1 body length; max speed 0.0287/time; max body lengths 2.3
- replication (lineage window K = 5 frames = time 100, --lineage-k): splits 45, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 131, merge/split ratio 2.91, nucleations 0
- channel total drift (end/start - 1): [-0.6998, -0.2332]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 95 at frame 77: holes 0, rim-vs-core 0.37, rim-vs-outside 0.18, heterogeneity 0.13; core [0.767, 0.283] rim [0.408, 0.352]
  - track 153 at frame 77: holes 0, rim-vs-core 0.38, rim-vs-outside 0.15, heterogeneity 0.13; core [0.74, 0.3] rim [0.371, 0.374]
  - track 217 at frame 77: holes 0, rim-vs-core 0.36, rim-vs-outside 0.18, heterogeneity 0.12; core [0.791, 0.26] rim [0.434, 0.324]
  - track 389 at frame 134: holes 0, rim-vs-core 0.23, rim-vs-outside 0.13, heterogeneity 0.09; core [0.603, 0.371] rim [0.379, 0.421]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 411 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial A: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.676, rim/outside 10.9 (aggregate of 411 individuals; 0/411 membrane-like individually; rim level 0.619)
  - radial E: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.46, rim/outside 0.902 (aggregate of 411 individuals; 0/411 membrane-like individually; rim level 0.416)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #95 (t=1540, R_eq 3.34): none; #153 (t=1540, R_eq 3.43): none; #217 (t=1540, R_eq 3.19): none; #389 (t=2680, R_eq 5.23): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
