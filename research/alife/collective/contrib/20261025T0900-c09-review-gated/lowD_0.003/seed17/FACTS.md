# Evidence pack: fch-gated-micelles (seed 17)

- world: `../../world_lowD_0.003.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 150s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0900-c09-review-gated/world_lowD_0.003.py --out collective/contrib/20261025T0900-c09-review-gated/lowD_0.003/seed17 --seeds 17 --frames 100 --no-movie`
- segmentation: matter > 0.13 of robust range [0.115, 2.9901], min area 6 px

## Measurements
- components: final 51, mean 38.2, max 51; occupancy final 0.27
- tracks: 80; persistent (alive >= 50% of run): 33; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [56, 55, 55], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 80, default): splits 28, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 22
- channel total drift (end/start - 1): [0.665, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 51: holes 0, rim-vs-core 0.59, rim-vs-outside 0.24, heterogeneity 0.27; core [0.62, 0.489, 0.231] rim [0.166, 0.126, 0.329]
  - track 7 at frame 51: holes 0, rim-vs-core 0.61, rim-vs-outside 0.23, heterogeneity 0.26; core [0.623, 0.511, 0.237] rim [0.167, 0.111, 0.325]
  - track 8 at frame 51: holes 0, rim-vs-core 0.62, rim-vs-outside 0.24, heterogeneity 0.27; core [0.625, 0.525, 0.244] rim [0.17, 0.109, 0.34]
  - track 54 at frame 82: holes 0, rim-vs-core 0.55, rim-vs-outside 0.41, heterogeneity 0.27; core [0.633, 0.356, 0.361] rim [0.18, 0.171, 0.619]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 248 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.52, rim/outside 10.1 (aggregate of 248 individuals; 6/248 membrane-like individually; rim level 0.482)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.453, rim/outside 4.92 (aggregate of 248 individuals; 2/248 membrane-like individually; rim level 0.285)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 9.86, rim/outside 4.98 (aggregate of 248 individuals; 242/248 membrane-like individually; rim level 0.68)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #3 (t=204, R_eq 5.17): ['shell q']; #7 (t=204, R_eq 5.14): ['shell q']; #8 (t=204, R_eq 5.11): ['shell q']; #54 (t=328, R_eq 5.01): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
