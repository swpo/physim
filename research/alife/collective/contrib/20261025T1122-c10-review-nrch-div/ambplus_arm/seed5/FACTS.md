# Evidence pack: nrch (seed 5)

- world: `../../../20261025T1017-c08-nrch-no-persistent-division/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 1184s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1017-c08-nrch-no-persistent-division/world.py --out collective/contrib/20261025T1122-c10-review-nrch-div/ambplus_arm/seed5 --seeds 5 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.0745, 1.1127], min area 6 px

## Measurements
- components: final 13, mean 9.7, max 17; occupancy final 0.23
- tracks: 234; persistent (alive >= 50% of run): 0; longest 60 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 13], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.233/time; max body lengths 18.1
- replication (lineage window K = 20 frames = time 1000, default): splits 56, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 38, merge/split ratio 0.679, nucleations 103
- channel total drift (end/start - 1): [0.0, -31.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 159 at frame 88: holes 0, rim-vs-core 0.15, rim-vs-outside 0.58, heterogeneity 0.19; core [0.932, 0.426] rim [0.799, 0.369]
  - track 150 at frame 83: holes 0, rim-vs-core 0.20, rim-vs-outside 0.53, heterogeneity 0.18; core [0.936, 0.407] rim [0.735, 0.391]
  - track 172 at frame 97: holes 0, rim-vs-core 0.23, rim-vs-outside 0.49, heterogeneity 0.18; core [0.943, 0.416] rim [0.715, 0.385]
  - track 171 at frame 91: holes 0, rim-vs-core 0.14, rim-vs-outside 0.53, heterogeneity 0.19; core [0.925, 0.359] rim [0.788, 0.379]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 7.11 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.84)
  - radial psi: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 1.02 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.601)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #159 (t=4400, R_eq 20.84): none; #150 (t=4150, R_eq 20.74): none; #172 (t=4850, R_eq 15.46): none; #171 (t=4550, R_eq 16.81): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
