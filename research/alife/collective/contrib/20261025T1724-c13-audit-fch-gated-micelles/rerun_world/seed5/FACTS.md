# Evidence pack: fch-gated-micelles (seed 5)

- world: `../../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 147s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1724-c13-audit-fch-gated-micelles/world.py --out collective/contrib/20261025T1724-c13-audit-fch-gated-micelles/rerun_world/seed5 --seeds 5 --frames 100 --no-movie`
- segmentation: matter > 0.14 of robust range [0.111, 2.9835], min area 6 px

## Measurements
- components: final 52, mean 40.5, max 52; occupancy final 0.27
- tracks: 84; persistent (alive >= 50% of run): 48; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 5.06 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [55, 55, 55], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 80, default): splits 30, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [0.6579, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 50: holes 0, rim-vs-core 0.64, rim-vs-outside 0.28, heterogeneity 0.24; core [0.622, 0.506, 0.247] rim [0.183, 0.062, 0.388]
  - track 5 at frame 51: holes 0, rim-vs-core 0.57, rim-vs-outside 0.26, heterogeneity 0.25; core [0.603, 0.453, 0.271] rim [0.167, 0.092, 0.358]
  - track 7 at frame 51: holes 0, rim-vs-core 0.63, rim-vs-outside 0.27, heterogeneity 0.26; core [0.613, 0.502, 0.276] rim [0.173, 0.06, 0.389]
  - track 51 at frame 71: holes 0, rim-vs-core 0.61, rim-vs-outside 0.34, heterogeneity 0.27; core [0.629, 0.405, 0.309] rim [0.183, 0.041, 0.5]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 260 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.513, rim/outside 12.4 (aggregate of 260 individuals; 3/260 membrane-like individually; rim level 0.481)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.608, rim/outside 8.15 (aggregate of 260 individuals; 0/260 membrane-like individually; rim level 0.327)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 10.7, rim/outside 5.39 (aggregate of 260 individuals; 257/260 membrane-like individually; rim level 0.681)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #3 (t=200, R_eq 4.69): ['shell q']; #5 (t=204, R_eq 4.79): ['shell q']; #7 (t=204, R_eq 4.75): ['shell q']; #51 (t=284, R_eq 4.92): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
