# Evidence pack: cips-fuel (seed 1)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 199s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1845-c23-cips-metabolic-claim/world.py --out collective/contrib/20261025T1845-c23-cips-metabolic-claim/fork --seeds 0 1 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0001, 0.9975], min area 6 px

## Measurements
- components: final 0, mean 111.5, max 298; occupancy final 0.00
- tracks: 403; persistent (alive >= 50% of run): 0; longest 137 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 4, 1], H1 [11, 2, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00518/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 200, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 81, merge/split ratio 81, nucleations 320
- channel total drift (end/start - 1): [0.0, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 86: holes 0, rim-vs-core 0.22, rim-vs-outside 0.46, heterogeneity 0.08; core [0.979, 0.895, 0.668] rim [0.81, 0.758, 0.715]
  - track 1 at frame 86: holes 0, rim-vs-core 0.23, rim-vs-outside 0.46, heterogeneity 0.07; core [0.984, 0.922, 0.651] rim [0.819, 0.772, 0.703]
  - track 2 at frame 88: holes 0, rim-vs-core 0.28, rim-vs-outside 0.51, heterogeneity 0.09; core [0.984, 0.949, 0.64] rim [0.78, 0.775, 0.706]
  - track 6 at frame 88: holes 0, rim-vs-core 0.27, rim-vs-outside 0.49, heterogeneity 0.08; core [0.98, 0.924, 0.654] rim [0.778, 0.758, 0.713]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 728 components >= 12 px at frames [50, 101, 151]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 36.5 (aggregate of 728 individuals; 0/728 membrane-like individually; rim level 0.919)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 2.89 (aggregate of 728 individuals; 0/728 membrane-like individually; rim level 0.706)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.27, rim/outside 0.891 (aggregate of 728 individuals; 0/728 membrane-like individually; rim level 0.628)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=860, R_eq 2.88): none; #1 (t=860, R_eq 3.09): none; #2 (t=880, R_eq 3.57): none; #6 (t=880, R_eq 3.29): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
