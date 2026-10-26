# Evidence pack: cips-fuel (seed 2)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 400 steps x dt 0.025 (--dt; world META dt 0.1) = time 3000; grid [128, 128]; wall 221s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0212-c32-review-cips-slowp/world.py --out collective/contrib/20261026T0212-c32-review-cips-slowp/runs/st_dp005_Lsc6 --seeds 2 --size 128 128 --frames 300 --spf 400 --dt 0.025 --no-movie`
- segmentation: matter > 0.52 of robust range [-0.0002, 0.9707], min area 6 px

## Measurements
- components: final 93, mean 103.6, max 121; occupancy final 0.12
- tracks: 180; persistent (alive >= 50% of run): 104; longest 298 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [113, 113, 112], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00499/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 20, merge/split ratio n/a, nucleations 160
- channel total drift (end/start - 1): [0.0, -0.3896, 0.3238]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 151: holes 0, rim-vs-core 0.20, rim-vs-outside 0.57, heterogeneity 0.06; core [0.991, 0.979, 0.013] rim [0.856, 0.879, 0.128]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 386 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.928, rim/outside 50.9 (aggregate of 386 individuals; 0/386 membrane-like individually; rim level 0.923)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.941, rim/outside 5.56 (aggregate of 386 individuals; 0/386 membrane-like individually; rim level 0.933)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 26.9, rim/outside 0.56 (aggregate of 386 individuals; 0/386 membrane-like individually; rim level 0.433)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1510, R_eq 1.69): none; #1 (t=1510, R_eq 1.69): none; #2 (t=1510, R_eq 1.69): none; #3 (t=1510, R_eq 2.99): none

## Warnings
- --dt 0.025 only relabels time (world META dt 0.1): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
