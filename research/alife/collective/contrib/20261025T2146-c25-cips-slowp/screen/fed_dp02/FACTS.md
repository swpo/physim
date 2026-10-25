# Evidence pack: cips-fuel (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 79s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/../world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/fed_dp02 --seeds 0 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0025, 1.0089], min area 6 px

## Measurements
- components: final 130, mean 124.1, max 133; occupancy final 0.11
- tracks: 177; persistent (alive >= 50% of run): 132; longest 296 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [145, 141, 133], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio n/a, nucleations 175
- channel total drift (end/start - 1): [0.0, -0.151, 0.104]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 154: holes 0, rim-vs-core 0.21, rim-vs-outside 0.65, heterogeneity 0.07; core [0.998, 0.979, 0.105] rim [0.913, 0.816, 0.215]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 376 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.968, rim/outside 54.3 (aggregate of 376 individuals; 0/376 membrane-like individually; rim level 0.96)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.885, rim/outside 5.66 (aggregate of 376 individuals; 0/376 membrane-like individually; rim level 0.874)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.4, rim/outside 0.595 (aggregate of 376 individuals; 0/376 membrane-like individually; rim level 0.346)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1540, R_eq 1.69): none; #1 (t=1540, R_eq 1.69): none; #2 (t=1540, R_eq 1.69): none; #3 (t=1540, R_eq 2.11): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
