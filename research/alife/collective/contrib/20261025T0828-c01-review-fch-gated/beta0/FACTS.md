# Evidence pack: fch-gated-micelles (seed 3)

- world: `../../20261025T0816-c03-fch-gated-micelles/world_beta0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 150s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0816-c03-fch-gated-micelles/world_beta0.py --out collective/contrib/20261025T0828-c01-review-fch-gated/beta0 --seeds 3 --frames 100 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1153, 2.9878], min area 6 px

## Measurements
- components: final 52, mean 38.8, max 52; occupancy final 0.26
- tracks: 88; persistent (alive >= 50% of run): 38; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 12.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [52, 52, 52], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 80, default): splits 32, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.031, nucleations 20
- channel total drift (end/start - 1): [0.6636, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 0, rim-vs-core 0.45, rim-vs-outside 0.22, heterogeneity 0.17; core [0.613, 0.475, 0.251] rim [0.165, 0.454, 0.325]
  - track 6 at frame 51: holes 0, rim-vs-core 0.17, rim-vs-outside 0.35, heterogeneity 0.17; core [0.544, 0.491, 0.312] rim [0.38, 0.484, 0.257]
  - track 7 at frame 51: holes 0, rim-vs-core 0.46, rim-vs-outside 0.21, heterogeneity 0.17; core [0.612, 0.489, 0.261] rim [0.159, 0.467, 0.304]
  - track 44 at frame 69: holes 0, rim-vs-core 0.43, rim-vs-outside 0.34, heterogeneity 0.20; core [0.659, 0.691, 0.294] rim [0.265, 0.668, 0.455]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 247 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.516, rim/outside 10.1 (aggregate of 247 individuals; 1/247 membrane-like individually; rim level 0.487)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.965, rim/outside 1.06 (aggregate of 247 individuals; 0/247 membrane-like individually; rim level 0.624)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 10.8, rim/outside 4.87 (aggregate of 247 individuals; 244/247 membrane-like individually; rim level 0.688)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #0 (t=200, R_eq 4.95): ['shell q']; #6 (t=204, R_eq 5.01): ['shell q']; #7 (t=204, R_eq 4.98): ['shell q']; #44 (t=276, R_eq 5.14): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
