# Evidence pack: cips-fuel (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 84s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/../world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/st_dp002 --seeds 0 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.0064, 0.9191], min area 6 px

## Measurements
- components: final 40, mean 19.7, max 40; occupancy final 0.02
- tracks: 69; persistent (alive >= 50% of run): 13; longest 244 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [280, 181, 78], H1 [36, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 69
- channel total drift (end/start - 1): [0.0, -0.3075, 0.2558]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 179: holes 0, rim-vs-core 0.03, rim-vs-outside 0.47, heterogeneity 0.03; core [0.925, 0.876, 0.0] rim [0.906, 0.901, 0.013]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 22 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.776, rim/outside 3.32 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.696)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 2.25 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.76)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 17, rim/outside 0.66 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.373)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=1790, R_eq 1.6): none; #8 (t=1790, R_eq 2.11): none; #11 (t=1840, R_eq 1.49): none; #13 (t=1870, R_eq 1.69): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
