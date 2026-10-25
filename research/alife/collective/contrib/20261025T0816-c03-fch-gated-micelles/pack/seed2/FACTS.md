# Evidence pack: fch-gated-micelles (seed 2)

- world: `../../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 151s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py --out collective/contrib/20261025T0816-c03-fch-gated-micelles/pack/seed2 --seeds 2 --frames 100 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1138, 2.9836], min area 6 px

## Measurements
- components: final 59, mean 40.0, max 59; occupancy final 0.27
- tracks: 107; persistent (alive >= 50% of run): 37; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 8.18 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [59, 59, 59], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 80, default): splits 39, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.026, nucleations 17
- channel total drift (end/start - 1): [0.6575, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 50: holes 0, rim-vs-core 0.62, rim-vs-outside 0.23, heterogeneity 0.25; core [0.609, 0.459, 0.269] rim [0.162, 0.029, 0.341]
  - track 16 at frame 51: holes 0, rim-vs-core 0.61, rim-vs-outside 0.25, heterogeneity 0.25; core [0.611, 0.46, 0.256] rim [0.168, 0.053, 0.355]
  - track 22 at frame 51: holes 0, rim-vs-core 0.60, rim-vs-outside 0.31, heterogeneity 0.26; core [0.654, 0.494, 0.234] rim [0.228, 0.101, 0.398]
  - track 54 at frame 71: holes 0, rim-vs-core 0.59, rim-vs-outside 0.27, heterogeneity 0.28; core [0.609, 0.411, 0.364] rim [0.157, 0.04, 0.435]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 263 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.508, rim/outside 10.5 (aggregate of 263 individuals; 0/263 membrane-like individually; rim level 0.482)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.639, rim/outside 6.54 (aggregate of 263 individuals; 0/263 membrane-like individually; rim level 0.32)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12, rim/outside 5.05 (aggregate of 263 individuals; 263/263 membrane-like individually; rim level 0.703)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #8 (t=200, R_eq 5.01): ['shell q']; #16 (t=204, R_eq 4.92): ['shell q']; #22 (t=204, R_eq 4.98): ['shell q']; #54 (t=284, R_eq 5.11): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
