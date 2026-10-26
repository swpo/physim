# Evidence pack: cips-fuel (seed 5)

- world: `../../../20261026T0146-c25-cips-slowp-negative-fix/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 74s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0146-c25-cips-slowp-negative-fix/world.py --out collective/contrib/20261026T0221-c30-review-cips-slowp/rerun/st_dp002 --seeds 5 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.0063, 0.9198], min area 6 px

## Measurements
- components: final 35, mean 22.0, max 36; occupancy final 0.02
- tracks: 52; persistent (alive >= 50% of run): 23; longest 275 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [266, 183, 77], H1 [41, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00434/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 52
- channel total drift (end/start - 1): [0.0, -0.3104, 0.2579]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 16 components >= 12 px at frames [101, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 3.75 (aggregate of 16 individuals; 1/16 membrane-like individually; rim level 0.685)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.912, rim/outside 2.55 (aggregate of 16 individuals; 0/16 membrane-like individually; rim level 0.767)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 13.3, rim/outside 0.58 (aggregate of 16 individuals; 0/16 membrane-like individually; rim level 0.343)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1640, R_eq 1.78): none; #1 (t=1690, R_eq 1.49): none; #2 (t=1710, R_eq 1.87): none; #6 (t=1760, R_eq 1.49): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
