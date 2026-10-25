# Evidence pack: thinfilm-active (seed 5)

- world: `../../../20261025T1915-c24-thinfilm-sighting/world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 200 steps x dt 0.25 = time 4000; grid [128, 128]; wall 96s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1915-c24-thinfilm-sighting/world.py --out collective/contrib/20261025T2055-c23-review-thinfilm/rerun/def --seeds 5 --frames 80 --no-movie`
- segmentation: matter > 0.10 of robust range [0.0423, 4.8398], min area 6 px

## Measurements
- components: final 3, mean 6.7, max 17; occupancy final 0.24
- tracks: 57; persistent (alive >= 50% of run): 3; longest 71 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.39 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 1000, default): splits 15, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 19, merge/split ratio 1.27, nucleations 0
- channel total drift (end/start - 1): [0.0, 3.5886, 1347.5316, 334.6585]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 32 at frame 45: holes 0, rim-vs-core 0.36, rim-vs-outside 0.32, heterogeneity 0.12; core [0.56, 0.947, 0.332, 0.957] rim [0.218, 0.857, 0.347, 0.889]
  - track 52 at frame 57: holes 0, rim-vs-core 0.40, rim-vs-outside 0.31, heterogeneity 0.13; core [0.603, 0.955, 0.283, 0.023] rim [0.217, 0.861, 0.317, 0.075]
  - track 41 at frame 38: holes 0, rim-vs-core 0.41, rim-vs-outside 0.42, heterogeneity 0.14; core [0.701, 0.965, 0.947, 0.64] rim [0.304, 0.899, 0.901, 0.563]
  - track 50 at frame 46: holes 0, rim-vs-core 0.38, rim-vs-outside 0.30, heterogeneity 0.12; core [0.576, 0.954, 0.956, 0.586] rim [0.215, 0.868, 0.89, 0.577]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 42 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.576, rim/outside 5.59 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.352)
  - radial |p| polar order: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.962, rim/outside 2.27 (aggregate of 42 individuals; 1/42 membrane-like individually; rim level 0.878)
  - radial p_x: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.05 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.506)
  - radial p_y: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 1.08 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.512)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #32 (t=2250, R_eq 11.98): none; #52 (t=2850, R_eq 13.15): none; #41 (t=1900, R_eq 14.15): none; #50 (t=2300, R_eq 12.41): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
