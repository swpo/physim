# Evidence pack: cgle-gain (seed 1)

- world: `../../world.py`, family `cgle`
- parent: collective/contrib/20261025T0841-c03-cgle-solitons; mutation: the CGLE linear gain becomes a local gain medium g, depleted by |A|^2 and regrowing toward g0
- run: 201 frames x 500 steps x dt 0.01 = time 1000; grid [96, 96]; wall 336s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1530-c43-cgle-gain-sighting/world.py --out collective/contrib/20261026T1530-c43-cgle-gain-sighting/pack/seed1 --seeds 1 --frames 200 --no-movie`
- segmentation: matter > 0.21 of robust range [0.0, 2.3591], min area 6 px

## Measurements
- components: final 1, mean 1.4, max 3; occupancy final 0.07
- tracks: 10; persistent (alive >= 50% of run): 1; longest 109 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.17 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.834/time; max body lengths 12.0
- replication (lineage window K = 20 frames = time 100, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio 1, nucleations 0
- channel total drift (end/start - 1): [-0.8917, 3.1531, -0.1811]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 37: holes 0, rim-vs-core 0.46, rim-vs-outside 0.13, heterogeneity 0.17; core [0.694, 0.375, 0.457] rim [0.263, 0.481, 0.573]
  - track 8 at frame 79: holes 0, rim-vs-core 0.49, rim-vs-outside 0.15, heterogeneity 0.16; core [0.689, 0.088, 0.346] rim [0.258, 0.306, 0.428]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 8 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial |A|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.37, rim/outside 4.49 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.265)
  - radial Re A: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 1.03 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.47)
  - radial g: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.62, rim/outside 0.836 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.563)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=730, R_eq 14.63): none; #4 (t=250, R_eq 14.63): none; #5 (t=185, R_eq 5.41): none; #8 (t=395, R_eq 5.47): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
