# Evidence pack: fch-gated-micelles (seed 1)

- world: `../../world_beta0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 152s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0816-c03-fch-gated-micelles/world_beta0.py --out collective/contrib/20261025T0816-c03-fch-gated-micelles/pack_beta0/seed1 --seeds 1 --frames 100 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1143, 2.9871], min area 6 px

## Measurements
- components: final 53, mean 37.7, max 53; occupancy final 0.26
- tracks: 89; persistent (alive >= 50% of run): 33; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.07 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [53, 53, 53], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 80, default): splits 35, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 18
- channel total drift (end/start - 1): [0.6732, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 51: holes 0, rim-vs-core 0.46, rim-vs-outside 0.23, heterogeneity 0.18; core [0.612, 0.522, 0.268] rim [0.163, 0.5, 0.345]
  - track 7 at frame 51: holes 0, rim-vs-core 0.46, rim-vs-outside 0.21, heterogeneity 0.17; core [0.614, 0.488, 0.258] rim [0.159, 0.465, 0.313]
  - track 9 at frame 51: holes 0, rim-vs-core 0.46, rim-vs-outside 0.21, heterogeneity 0.17; core [0.613, 0.475, 0.249] rim [0.159, 0.452, 0.302]
  - track 68 at frame 87: holes 0, rim-vs-core 0.49, rim-vs-outside 0.37, heterogeneity 0.22; core [0.622, 0.893, 0.384] rim [0.169, 0.87, 0.575]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 241 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.521, rim/outside 10.8 (aggregate of 241 individuals; 7/241 membrane-like individually; rim level 0.482)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.962, rim/outside 1.06 (aggregate of 241 individuals; 0/241 membrane-like individually; rim level 0.635)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 10.6, rim/outside 5.01 (aggregate of 241 individuals; 233/241 membrane-like individually; rim level 0.686)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #5 (t=204, R_eq 5.05): ['shell q']; #7 (t=204, R_eq 5.08): ['shell q']; #9 (t=204, R_eq 5.08): ['shell q']; #68 (t=348, R_eq 5.14): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
