# Evidence pack: cips-fuel (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 81s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/../world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/st_dp005 --seeds 0 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.0011, 0.9173], min area 6 px

## Measurements
- components: final 76, mean 53.5, max 76; occupancy final 0.04
- tracks: 95; persistent (alive >= 50% of run): 65; longest 286 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [282, 275, 170], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 94
- channel total drift (end/start - 1): [0.0, -0.3742, 0.3113]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 164: holes 0, rim-vs-core 0.10, rim-vs-outside 0.61, heterogeneity 0.04; core [0.982, 0.961, 0.0] rim [0.894, 0.936, 0.04]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 10.7 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.854)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.959, rim/outside 4.32 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.91)
  - radial F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 16.1, rim/outside 0.493 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.363)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=1590, R_eq 1.69): none; #2 (t=1590, R_eq 1.78): none; #3 (t=1590, R_eq 1.49): none; #5 (t=1640, R_eq 2.11): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
