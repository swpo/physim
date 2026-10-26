# Evidence pack: cips-turnover (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS on a consumed fuel plus uniform, fuel-independent enzyme turnover d(e0-e) (Zwicker-type made-outside / lost-inside)
- run: 241 frames x 500 steps x dt 0.1 = time 12000; grid [256, 256]; wall 879s; status ok
- command: `python -m labkit.run collective/work_c35/world.py --out collective/work_c35/lkB/s0 --seeds 0 --frames 240 --spf 500 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0095, 0.9811], min area 6 px

## Measurements
- components: final 18, mean 11.0, max 18; occupancy final 0.11
- tracks: 18; persistent (alive >= 50% of run): 18; longest 163 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 27.08 (1 = constant size)
- enclosures: components with a hole mean 0.19, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 1000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 18
- channel total drift (end/start - 1): [-0.0004, -0.568, 0.612]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 159: holes 0, rim-vs-core 0.30, rim-vs-outside 0.72, heterogeneity 0.12; core [0.979, 0.909, 0.024] rim [0.796, 0.725, 0.184]
  - track 1 at frame 159: holes 0, rim-vs-core 0.24, rim-vs-outside 0.81, heterogeneity 0.11; core [0.98, 0.91, 0.023] rim [0.831, 0.749, 0.129]
  - track 2 at frame 163: holes 0, rim-vs-core 0.22, rim-vs-outside 0.80, heterogeneity 0.11; core [0.981, 0.918, 0.027] rim [0.858, 0.78, 0.137]
  - track 3 at frame 165: holes 0, rim-vs-core 0.29, rim-vs-outside 0.74, heterogeneity 0.11; core [0.984, 0.94, 0.046] rim [0.816, 0.758, 0.193]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 74 components >= 12 px at frames [81, 121, 159, 200, 240]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.847, rim/outside 28 (aggregate of 74 individuals; 3/74 membrane-like individually; rim level 0.785)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 13.1 (aggregate of 74 individuals; 3/74 membrane-like individually; rim level 0.782)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 14.5, rim/outside 0.65 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.504)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=7950, R_eq 13.3): none; #1 (t=7950, R_eq 14.23, ring): ['e', 'p']; #2 (t=8150, R_eq 12.41): none; #3 (t=8250, R_eq 12.01): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 74 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
