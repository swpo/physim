# Evidence pack: thinfilm-active (seed 5)

- world: `../../../20261025T1915-c24-thinfilm-sighting/world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 400 steps x dt 0.125 (--dt; world META dt 0.25) = time 4000; grid [128, 128]; wall 191s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1915-c24-thinfilm-sighting/world.py --out collective/contrib/20261025T2055-c23-review-thinfilm/rerun/def_dt2 --seeds 5 --frames 80 --spf 400 --dt 0.125 --no-movie`
- segmentation: matter > 0.09 of robust range [0.0428, 4.9465], min area 6 px

## Measurements
- components: final 3, mean 6.8, max 16; occupancy final 0.24
- tracks: 61; persistent (alive >= 50% of run): 3; longest 71 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.41 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 4, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 1000, default): splits 18, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 18, merge/split ratio 1, nucleations 0
- channel total drift (end/start - 1): [0.0, 3.6379, 1332.9851, 367.8465]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 36 at frame 45: holes 0, rim-vs-core 0.35, rim-vs-outside 0.32, heterogeneity 0.13; core [0.559, 0.944, 0.302, 0.947] rim [0.223, 0.862, 0.305, 0.876]
  - track 44 at frame 39: holes 0, rim-vs-core 0.41, rim-vs-outside 0.42, heterogeneity 0.14; core [0.691, 0.966, 0.947, 0.646] rim [0.293, 0.897, 0.899, 0.569]
  - track 54 at frame 58: holes 0, rim-vs-core 0.39, rim-vs-outside 0.31, heterogeneity 0.13; core [0.595, 0.956, 0.303, 0.021] rim [0.217, 0.863, 0.333, 0.073]
  - track 52 at frame 47: holes 0, rim-vs-core 0.38, rim-vs-outside 0.30, heterogeneity 0.12; core [0.573, 0.956, 0.956, 0.598] rim [0.213, 0.869, 0.89, 0.584]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 42 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.597, rim/outside 5.85 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.357)
  - radial |p| polar order: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.967, rim/outside 2.33 (aggregate of 42 individuals; 1/42 membrane-like individually; rim level 0.88)
  - radial p_x: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.06 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.51)
  - radial p_y: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 1.07 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.503)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #36 (t=2250, R_eq 12.05): none; #44 (t=1950, R_eq 14.17): none; #54 (t=2900, R_eq 13.09): none; #52 (t=2350, R_eq 12.48): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.125 only relabels time (world META dt 0.25): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
