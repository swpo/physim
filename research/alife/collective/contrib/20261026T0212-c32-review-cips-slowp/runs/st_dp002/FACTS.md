# Evidence pack: cips-fuel (seed 2)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 59s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0212-c32-review-cips-slowp/world.py --out collective/contrib/20261026T0212-c32-review-cips-slowp/runs/st_dp002 --seeds 2 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.0063, 0.9199], min area 6 px

## Measurements
- components: final 34, mean 18.9, max 34; occupancy final 0.02
- tracks: 54; persistent (alive >= 50% of run): 19; longest 257 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [277, 172, 73], H1 [30, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00234/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 200, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 52
- channel total drift (end/start - 1): [0.0, -0.3087, 0.2565]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 174: holes 0, rim-vs-core 0.08, rim-vs-outside 0.35, heterogeneity 0.03; core [0.857, 0.846, 0.0] rim [0.916, 0.902, 0.004]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 29 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 3.6 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.698)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 2.41 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.772)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 14.3, rim/outside 0.589 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.332)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=1740, R_eq 1.87): none; #4 (t=1760, R_eq 2.03): none; #5 (t=1820, R_eq 1.87): none; #6 (t=1840, R_eq 1.78): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
