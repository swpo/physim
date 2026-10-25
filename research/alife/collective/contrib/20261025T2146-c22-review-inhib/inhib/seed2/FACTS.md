# Evidence pack: cips-inhib (seed 2)

- world: `../../../../20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 64s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/wip-c22/rev_inh/inhib/seed2 --seeds 2 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.51 of robust range [0.0018, 0.9854], min area 6 px

## Measurements
- components: final 37, mean 28.7, max 42; occupancy final 0.13
- tracks: 47; persistent (alive >= 50% of run): 36; longest 237 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 37, 36], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio n/a, nucleations 43
- channel total drift (end/start - 1): [0.0, -0.5688, 0.3916, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 184: holes 0, rim-vs-core 0.39, rim-vs-outside 0.41, heterogeneity 0.10; core [0.958, 0.928, 0.08, 0.968] rim [0.704, 0.72, 0.26, 0.848]
  - track 1 at frame 184: holes 0, rim-vs-core 0.34, rim-vs-outside 0.40, heterogeneity 0.09; core [0.954, 0.901, 0.168, 0.905] rim [0.732, 0.716, 0.311, 0.803]
  - track 2 at frame 184: holes 0, rim-vs-core 0.36, rim-vs-outside 0.40, heterogeneity 0.10; core [0.954, 0.904, 0.16, 0.907] rim [0.711, 0.708, 0.312, 0.798]
  - track 3 at frame 187: holes 0, rim-vs-core 0.18, rim-vs-outside 0.53, heterogeneity 0.09; core [0.949, 0.885, 0.174, 0.901] rim [0.819, 0.789, 0.245, 0.85]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 193 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.919, rim/outside 24.3 (aggregate of 193 individuals; 0/193 membrane-like individually; rim level 0.902)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 4.13 (aggregate of 193 individuals; 0/193 membrane-like individually; rim level 0.828)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.46, rim/outside 0.69 (aggregate of 193 individuals; 0/193 membrane-like individually; rim level 0.484)
  - radial I: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.928, rim/outside 1.67 (aggregate of 193 individuals; 0/193 membrane-like individually; rim level 0.889)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1840, R_eq 5.14): none; #1 (t=1840, R_eq 4.15): none; #2 (t=1840, R_eq 4.3): none; #3 (t=1870, R_eq 4.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
