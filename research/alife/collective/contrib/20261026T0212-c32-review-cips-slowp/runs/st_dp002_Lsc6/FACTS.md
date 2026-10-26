# Evidence pack: cips-fuel (seed 2)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 400 steps x dt 0.025 (--dt; world META dt 0.1) = time 3000; grid [128, 128]; wall 222s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0212-c32-review-cips-slowp/world.py --out collective/contrib/20261026T0212-c32-review-cips-slowp/runs/st_dp002_Lsc6 --seeds 2 --size 128 128 --frames 300 --spf 400 --dt 0.025 --no-movie`
- segmentation: matter > 0.51 of robust range [-0.002, 0.9867], min area 6 px

## Measurements
- components: final 59, mean 51.9, max 59; occupancy final 0.04
- tracks: 84; persistent (alive >= 50% of run): 55; longest 297 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [276, 275, 164], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 84
- channel total drift (end/start - 1): [0.0, -0.2798, 0.2324]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 19.3 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.895)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.943, rim/outside 4.92 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.882)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 30.1, rim/outside 0.449 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.291)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=1540, R_eq 1.49): none; #3 (t=1540, R_eq 1.69): none; #6 (t=1540, R_eq 1.78): none; #7 (t=1540, R_eq 1.69): none

## Warnings
- --dt 0.025 only relabels time (world META dt 0.1): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
