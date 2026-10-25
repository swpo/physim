# Evidence pack: fch-gated-micelles (seed 19)

- world: `../../world_lowD_0.1.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 149s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1236-c09-review-slowd-twins/world_lowD_0.1.py --out collective/contrib/20261025T1236-c09-review-slowd-twins/lowD_0.1/seed19 --seeds 19 --frames 100 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1183, 2.9883], min area 6 px

## Measurements
- components: final 56, mean 38.0, max 56; occupancy final 0.27
- tracks: 89; persistent (alive >= 50% of run): 30; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 14.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [56, 56, 56], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 80, default): splits 29, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.034, nucleations 25
- channel total drift (end/start - 1): [0.6696, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 50: holes 0, rim-vs-core 0.48, rim-vs-outside 0.21, heterogeneity 0.20; core [0.617, 0.564, 0.235] rim [0.163, 0.411, 0.306]
  - track 4 at frame 51: holes 0, rim-vs-core 0.51, rim-vs-outside 0.29, heterogeneity 0.20; core [0.647, 0.587, 0.217] rim [0.189, 0.434, 0.392]
  - track 7 at frame 51: holes 0, rim-vs-core 0.49, rim-vs-outside 0.22, heterogeneity 0.20; core [0.62, 0.555, 0.228] rim [0.165, 0.399, 0.31]
  - track 69 at frame 84: holes 0, rim-vs-core 0.51, rim-vs-outside 0.38, heterogeneity 0.23; core [0.627, 0.968, 0.378] rim [0.173, 0.866, 0.594]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 249 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.509, rim/outside 10.2 (aggregate of 249 individuals; 1/249 membrane-like individually; rim level 0.48)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 1.51 (aggregate of 249 individuals; 0/249 membrane-like individually; rim level 0.623)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 11.2, rim/outside 5 (aggregate of 249 individuals; 247/249 membrane-like individually; rim level 0.699)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #2 (t=200, R_eq 5.14): ['shell q']; #4 (t=204, R_eq 5.14): ['shell q']; #7 (t=204, R_eq 5.17): ['shell q']; #69 (t=336, R_eq 5.05): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
