# Evidence pack: cips-fuel (seed 24)

- world: `../../../20261025T1845-c23-cips-metabolic-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 251 frames x 100 steps x dt 0.1 = time 2500; grid [256, 256]; wall 393s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1845-c23-cips-metabolic-claim/world.py --out collective/contrib/20261025T2105-c24-review-cips-localcut/cut30/seed24 --seeds 24 --frames 250 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 0.9988], min area 6 px

## Measurements
- components: final 176, mean 202.2, max 300; occupancy final 0.14
- tracks: 434; persistent (alive >= 50% of run): 188; longest 232 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [179, 176, 175], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00681/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 118, merge/split ratio n/a, nucleations 316
- channel total drift (end/start - 1): [0.0, -0.236, 0.1114]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 134: holes 0, rim-vs-core 0.30, rim-vs-outside 0.50, heterogeneity 0.09; core [0.976, 0.871, 0.458] rim [0.759, 0.689, 0.551]
  - track 4 at frame 134: holes 0, rim-vs-core 0.27, rim-vs-outside 0.49, heterogeneity 0.09; core [0.975, 0.86, 0.451] rim [0.774, 0.693, 0.534]
  - track 8 at frame 137: holes 0, rim-vs-core 0.29, rim-vs-outside 0.50, heterogeneity 0.09; core [0.974, 0.863, 0.471] rim [0.763, 0.692, 0.557]
  - track 9 at frame 137: holes 0, rim-vs-core 0.21, rim-vs-outside 0.46, heterogeneity 0.07; core [0.973, 0.822, 0.463] rim [0.816, 0.694, 0.524]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1288 components >= 12 px at frames [42, 84, 126, 166, 208, 250]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 43.1 (aggregate of 1288 individuals; 0/1288 membrane-like individually; rim level 0.932)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 3.8 (aggregate of 1288 individuals; 0/1288 membrane-like individually; rim level 0.812)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.66, rim/outside 0.817 (aggregate of 1288 individuals; 0/1288 membrane-like individually; rim level 0.628)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=1340, R_eq 3.43): none; #4 (t=1340, R_eq 3.29): none; #8 (t=1370, R_eq 3.29): none; #9 (t=1370, R_eq 2.76): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
