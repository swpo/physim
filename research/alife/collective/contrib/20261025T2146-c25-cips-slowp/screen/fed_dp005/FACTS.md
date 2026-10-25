# Evidence pack: cips-fuel (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 82s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/../world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/fed_dp005 --seeds 0 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0077, 1.0163], min area 6 px

## Measurements
- components: final 73, mean 52.1, max 75; occupancy final 0.04
- tracks: 92; persistent (alive >= 50% of run): 59; longest 292 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [287, 277, 196], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 92
- channel total drift (end/start - 1): [0.0, -0.1459, 0.1004]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 156: holes 0, rim-vs-core 0.18, rim-vs-outside 0.68, heterogeneity 0.07; core [0.998, 0.996, 0.044] rim [0.917, 0.863, 0.13]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 60 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.85, rim/outside 27.2 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.84)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 8.86 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.855)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 21.8, rim/outside 0.505 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.229)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1560, R_eq 1.78): none; #1 (t=1560, R_eq 1.87): none; #2 (t=1560, R_eq 1.49): none; #6 (t=1590, R_eq 1.6): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
