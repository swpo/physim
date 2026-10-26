# Evidence pack: cips-fuel (seed 3)

- world: `../../../20261025T1845-c23-cips-metabolic-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 288s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1845-c23-cips-metabolic-claim/world.py --out collective/contrib/20261025T1945-c19-review-cips-nocap/reservoir/seed3 --seeds 3 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0011, 1.0025], min area 6 px

## Measurements
- components: final 161, mean 214.5, max 407; occupancy final 0.14
- tracks: 651; persistent (alive >= 50% of run): 168; longest 292 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [161, 161, 161], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0128/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 223, merge/split ratio n/a, nucleations 428
- channel total drift (end/start - 1): [0.0, -0.2017, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 156: holes 0, rim-vs-core 0.15, rim-vs-outside 0.51, heterogeneity 0.04; core [0.992, 0.683, 0.0] rim [0.889, 0.572, 0.0]
  - track 7 at frame 156: holes 0, rim-vs-core 0.16, rim-vs-outside 0.51, heterogeneity 0.05; core [0.993, 0.694, 0.0] rim [0.883, 0.579, 0.0]
  - track 11 at frame 156: holes 0, rim-vs-core 0.19, rim-vs-outside 0.54, heterogeneity 0.06; core [0.992, 0.703, 0.0] rim [0.851, 0.581, 0.0]
  - track 13 at frame 156: holes 0, rim-vs-core 0.17, rim-vs-outside 0.53, heterogeneity 0.05; core [0.989, 0.677, 0.0] rim [0.863, 0.566, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1222 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.966, rim/outside 56.9 (aggregate of 1222 individuals; 0/1222 membrane-like individually; rim level 0.96)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 4.11 (aggregate of 1222 individuals; 0/1222 membrane-like individually; rim level 0.746)
  - radial F: flat profile (no radial structure; level 0; aggregate of 1222 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=1560, R_eq 2.59): none; #7 (t=1560, R_eq 2.65): none; #11 (t=1560, R_eq 2.76): none; #13 (t=1560, R_eq 2.59): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
