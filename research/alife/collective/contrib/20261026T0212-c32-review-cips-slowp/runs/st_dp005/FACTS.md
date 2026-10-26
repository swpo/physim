# Evidence pack: cips-fuel (seed 2)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 58s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0212-c32-review-cips-slowp/world.py --out collective/contrib/20261026T0212-c32-review-cips-slowp/runs/st_dp005 --seeds 2 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.0013, 0.9157], min area 6 px

## Measurements
- components: final 80, mean 57.9, max 80; occupancy final 0.05
- tracks: 98; persistent (alive >= 50% of run): 70; longest 283 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [269, 258, 157], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 98
- channel total drift (end/start - 1): [0.0, -0.3802, 0.316]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 80 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 6.26 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.741)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.907, rim/outside 3.33 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.855)
  - radial F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 18.2, rim/outside 0.53 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.368)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=1590, R_eq 1.78): none; #3 (t=1610, R_eq 1.49): none; #6 (t=1610, R_eq 1.49): none; #7 (t=1640, R_eq 1.49): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
