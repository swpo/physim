# Evidence pack: active-nematic-cargo (seed 23)

- world: `../../../20261026T0405-c34-nematic-cargo/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 367s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0405-c34-nematic-cargo/world.py --out collective/contrib/c39-audit2-wip/chis0/seed23 --seeds 23 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8244, 0.6103], min area 6 px

## Measurements
- components: final 32, mean 22.6, max 33; occupancy final 0.07
- tracks: 110; persistent (alive >= 50% of run): 9; longest 173 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 32, 31], H1 [1, 0, 0]
- motion: 51 long-lived tracks moved >= 1 body length; max speed 0.0843/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 100, default): splits 42, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 4, merges 15, merge/split ratio 0.357, nucleations 10
- channel total drift (end/start - 1): [-0.4914, -0.3754, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 113: holes 0, rim-vs-core 0.30, rim-vs-outside 0.38, heterogeneity 0.08; core [0.923, 0.809, 0.93, 0.103] rim [0.759, 0.588, 0.816, 0.126]
  - track 30 at frame 126: holes 0, rim-vs-core 0.37, rim-vs-outside 0.36, heterogeneity 0.10; core [0.935, 0.886, 0.875, 0.103] rim [0.738, 0.604, 0.749, 0.129]
  - track 32 at frame 126: holes 0, rim-vs-core 0.29, rim-vs-outside 0.46, heterogeneity 0.10; core [0.934, 0.876, 0.898, 0.124] rim [0.776, 0.655, 0.8, 0.158]
  - track 96 at frame 187: holes 0, rim-vs-core 0.23, rim-vs-outside 0.54, heterogeneity 0.10; core [0.953, 0.923, 0.975, 0.102] rim [0.826, 0.748, 0.892, 0.117]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 151 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 4.82 (aggregate of 151 individuals; 0/151 membrane-like individually; rim level 0.762)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.754, rim/outside 8.33 (aggregate of 151 individuals; 0/151 membrane-like individually; rim level 0.652)
  - radial surfactant s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 2.16 (aggregate of 151 individuals; 0/151 membrane-like individually; rim level 0.797)
  - radial cargo c: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.32, rim/outside 0.682 (aggregate of 151 individuals; 0/151 membrane-like individually; rim level 0.266)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=565, R_eq 3.39): none; #30 (t=630, R_eq 3.34): none; #32 (t=630, R_eq 3.04): none; #96 (t=935, R_eq 3.48): none

## Warnings
- radial: 2 of 151 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
