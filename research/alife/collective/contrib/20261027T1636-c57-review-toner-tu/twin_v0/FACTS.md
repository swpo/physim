# Evidence pack: eating-flocks (seed 41)

- world: `../../20261027T0210-c51-toner-tu-eaters-fronts/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 151 frames x 80 steps x dt 0.25 = time 3000; grid [128, 128]; wall 25s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/world.py --out collective/contrib/c57-w13/twin_v0 --seeds 41 --frames 150 --spf 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.6477], min area 6 px

## Measurements
- components: final 166, mean 145.8, max 166; occupancy final 0.37
- tracks: 366; persistent (alive >= 50% of run): 159; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.18 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [167, 167, 167], H1 [71, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 400, default): splits 138, persistent splits 62 (0 more failed only because the siblings re-merged within K), max generation 3, merges 24, merge/split ratio 0.174, nucleations 2
- channel total drift (end/start - 1): [1.0364, -0.5919, -0.1907, 0.7726]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 63 at frame 77: holes 0, rim-vs-core 0.46, rim-vs-outside 0.38, heterogeneity 0.17; core [0.835, 0.072, 0.849, 0.788] rim [0.475, 0.212, 0.627, 0.675]
  - track 67 at frame 77: holes 0, rim-vs-core 0.48, rim-vs-outside 0.33, heterogeneity 0.16; core [0.807, 0.083, 0.863, 0.217] rim [0.438, 0.223, 0.619, 0.329]
  - track 70 at frame 77: holes 0, rim-vs-core 0.44, rim-vs-outside 0.37, heterogeneity 0.17; core [0.833, 0.069, 0.856, 0.223] rim [0.492, 0.208, 0.638, 0.341]
  - track 304 at frame 91: holes 0, rim-vs-core 0.40, rim-vs-outside 0.36, heterogeneity 0.16; core [0.836, 0.069, 0.861, 0.235] rim [0.514, 0.196, 0.671, 0.3]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 935 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial density rho: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.748, rim/outside 4.42 (aggregate of 935 individuals; 1/935 membrane-like individually; rim level 0.687)
  - radial food c: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 10, rim/outside 0.937 (aggregate of 935 individuals; 0/935 membrane-like individually; rim level 0.333)
  - radial |p|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 3.63 (aggregate of 935 individuals; 18/935 membrane-like individually; rim level 0.782)
  - radial p_x: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1 (aggregate of 935 individuals; 2/935 membrane-like individually; rim level 0.486)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #63 (t=1540, R_eq 3.43): none; #67 (t=1540, R_eq 3.43): none; #70 (t=1540, R_eq 3.48): none; #304 (t=1820, R_eq 3.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
