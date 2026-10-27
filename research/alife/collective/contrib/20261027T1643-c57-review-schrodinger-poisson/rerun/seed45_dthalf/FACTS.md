# Evidence pack: fed-wave-matter (seed 45)

- world: `../../20261027T0949-c55-schrodinger-poisson-negative/world.py`, family `schrodinger-poisson`
- parent: None; mutation: -
- run: 201 frames x 100 steps x dt 0.2 = time 4000; grid [128, 128]; wall 47s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0949-c55-schrodinger-poisson-negative/world.py --out collective/contrib/c57-w17/packC_dthalf --seeds 45 --frames 200 --spf 100 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0002, 4.1838], min area 6 px

## Measurements
- components: final 5, mean 6.3, max 24; occupancy final 0.04
- tracks: 731; persistent (alive >= 50% of run): 0; longest 11 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 3, 2], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 4.8
- replication (lineage window K = 20 frames = time 400, default): splits 159, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 160, merge/split ratio 1.01, nucleations 238
- channel total drift (end/start - 1): [-0.9217, -0.0559, None, 1.0686]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 77 at frame 12: holes 0, rim-vs-core 0.54, rim-vs-outside 0.11, heterogeneity 0.21; core [0.678, 0.19, 0.598, 0.51] rim [0.159, 0.325, 0.549, 0.504]
  - track 532 at frame 129: holes 0, rim-vs-core 0.12, rim-vs-outside 0.15, heterogeneity 0.11; core [0.334, 0.456, 0.447, 0.502] rim [0.227, 0.49, 0.434, 0.479]
  - track 290 at frame 69: holes 0, rim-vs-core 0.23, rim-vs-outside 0.16, heterogeneity 0.12; core [0.364, 0.528, 0.447, 0.732] rim [0.215, 0.565, 0.426, 0.565]
  - track 304 at frame 71: holes 0, rim-vs-core 0.10, rim-vs-outside 0.04, heterogeneity 0.12; core [0.258, 0.528, 0.415, 0.499] rim [0.175, 0.551, 0.405, 0.45]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial density |psi|^2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.503, rim/outside 3.93 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.242)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.64, rim/outside 0.886 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.53)
  - radial potential -V: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 1.22 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.685)
  - radial phase cos: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.903, rim/outside 1.03 (aggregate of 30 individuals; 1/30 membrane-like individually; rim level 0.49)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #77 (t=240, R_eq 5.05): none; #532 (t=2580, R_eq 8.31): none; #290 (t=1380, R_eq 6.72): none; #304 (t=1420, R_eq 4.95): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
