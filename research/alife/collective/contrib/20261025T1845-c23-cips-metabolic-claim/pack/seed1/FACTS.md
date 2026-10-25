# Evidence pack: cips-fuel (seed 1)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 245s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1845-c23-cips-metabolic-claim/world.py --out collective/contrib/20261025T1845-c23-cips-metabolic-claim/fed1 --seeds 1 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 0.999], min area 6 px

## Measurements
- components: final 182, mean 208.4, max 298; occupancy final 0.14
- tracks: 440; persistent (alive >= 50% of run): 210; longest 283 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [185, 184, 182], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00518/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 200, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 118, merge/split ratio 118, nucleations 320
- channel total drift (end/start - 1): [0.0, -0.2187, 0.151]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 159: holes 0, rim-vs-core 0.23, rim-vs-outside 0.48, heterogeneity 0.08; core [0.981, 0.837, 0.187] rim [0.83, 0.703, 0.287]
  - track 1 at frame 159: holes 0, rim-vs-core 0.24, rim-vs-outside 0.48, heterogeneity 0.08; core [0.978, 0.855, 0.169] rim [0.822, 0.709, 0.28]
  - track 2 at frame 161: holes 0, rim-vs-core 0.27, rim-vs-outside 0.49, heterogeneity 0.09; core [0.983, 0.891, 0.133] rim [0.823, 0.722, 0.267]
  - track 3 at frame 161: holes 0, rim-vs-core 0.26, rim-vs-outside 0.49, heterogeneity 0.09; core [0.975, 0.842, 0.182] rim [0.797, 0.691, 0.296]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1314 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.949, rim/outside 46.6 (aggregate of 1314 individuals; 0/1314 membrane-like individually; rim level 0.94)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 3.95 (aggregate of 1314 individuals; 0/1314 membrane-like individually; rim level 0.815)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.16, rim/outside 0.679 (aggregate of 1314 individuals; 0/1314 membrane-like individually; rim level 0.451)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1590, R_eq 2.82): none; #1 (t=1590, R_eq 3.09): none; #2 (t=1610, R_eq 3.43): none; #3 (t=1610, R_eq 3.09): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
