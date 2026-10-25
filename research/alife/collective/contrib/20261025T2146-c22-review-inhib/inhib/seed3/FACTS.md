# Evidence pack: cips-inhib (seed 3)

- world: `../../../../20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 63s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/wip-c22/rev_inh/inhib/seed3 --seeds 3 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.51 of robust range [0.0017, 0.987], min area 6 px

## Measurements
- components: final 35, mean 28.0, max 43; occupancy final 0.13
- tracks: 47; persistent (alive >= 50% of run): 35; longest 240 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 35, 35], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio n/a, nucleations 43
- channel total drift (end/start - 1): [0.0, -0.5721, 0.3941, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 182: holes 0, rim-vs-core 0.35, rim-vs-outside 0.41, heterogeneity 0.10; core [0.955, 0.898, 0.204, 0.879] rim [0.72, 0.706, 0.348, 0.773]
  - track 1 at frame 187: holes 0, rim-vs-core 0.21, rim-vs-outside 0.57, heterogeneity 0.10; core [0.957, 0.914, 0.167, 0.91] rim [0.828, 0.801, 0.261, 0.838]
  - track 2 at frame 187: holes 0, rim-vs-core 0.17, rim-vs-outside 0.54, heterogeneity 0.10; core [0.944, 0.886, 0.201, 0.884] rim [0.816, 0.798, 0.264, 0.837]
  - track 3 at frame 187: holes 0, rim-vs-core 0.35, rim-vs-outside 0.39, heterogeneity 0.09; core [0.952, 0.888, 0.2, 0.887] rim [0.717, 0.7, 0.338, 0.784]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 185 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 25.1 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.907)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 4.33 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.828)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.72, rim/outside 0.706 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.511)
  - radial I: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 1.72 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.875)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1820, R_eq 4.26): none; #1 (t=1870, R_eq 4.55): none; #2 (t=1870, R_eq 4.41): none; #3 (t=1870, R_eq 4.18): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
