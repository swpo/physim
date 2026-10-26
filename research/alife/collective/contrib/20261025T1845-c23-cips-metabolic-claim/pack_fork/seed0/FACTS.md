# Evidence pack: cips-fuel (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 242s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1845-c23-cips-metabolic-claim/world.py --out collective/contrib/20261025T1845-c23-cips-metabolic-claim/fork --seeds 0 1 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0001, 0.9974], min area 6 px

## Measurements
- components: final 0, mean 111.4, max 301; occupancy final 0.00
- tracks: 394; persistent (alive >= 50% of run): 0; longest 138 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 6, 1], H1 [10, 5, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 86, merge/split ratio n/a, nucleations 308
- channel total drift (end/start - 1): [-0.0, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 86: holes 0, rim-vs-core 0.26, rim-vs-outside 0.49, heterogeneity 0.08; core [0.982, 0.928, 0.654] rim [0.786, 0.763, 0.712]
  - track 16 at frame 88: holes 0, rim-vs-core 0.27, rim-vs-outside 0.49, heterogeneity 0.08; core [0.987, 0.961, 0.608] rim [0.794, 0.784, 0.681]
  - track 1 at frame 88: holes 0, rim-vs-core 0.26, rim-vs-outside 0.49, heterogeneity 0.08; core [0.983, 0.933, 0.656] rim [0.79, 0.766, 0.715]
  - track 3 at frame 88: holes 0, rim-vs-core 0.25, rim-vs-outside 0.49, heterogeneity 0.07; core [0.988, 0.952, 0.644] rim [0.821, 0.783, 0.707]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 715 components >= 12 px at frames [50, 101, 151]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 37.5 (aggregate of 715 individuals; 0/715 membrane-like individually; rim level 0.922)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.907, rim/outside 2.89 (aggregate of 715 individuals; 0/715 membrane-like individually; rim level 0.714)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 0.889 (aggregate of 715 individuals; 0/715 membrane-like individually; rim level 0.633)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=860, R_eq 3.29): none; #16 (t=880, R_eq 3.95): none; #1 (t=880, R_eq 3.29): none; #3 (t=880, R_eq 3.43): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
