# Evidence pack: fch-gated-micelles (seed 9)

- world: `../../../../contrib/20261025T0816-c03-fch-gated-micelles/world_beta0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 160s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0816-c03-fch-gated-micelles/world_beta0.py --out collective/work_c05/rev_fg/beta0/seed9 --seeds 9 --frames 100 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1205, 2.9927], min area 6 px

## Measurements
- components: final 54, mean 37.3, max 54; occupancy final 0.26
- tracks: 89; persistent (alive >= 50% of run): 32; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.18 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [54, 54, 54], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 80, default): splits 30, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 22
- channel total drift (end/start - 1): [0.6684, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 51: holes 0, rim-vs-core 0.24, rim-vs-outside 0.33, heterogeneity 0.17; core [0.594, 0.507, 0.255] rim [0.358, 0.493, 0.282]
  - track 8 at frame 51: holes 0, rim-vs-core 0.17, rim-vs-outside 0.35, heterogeneity 0.17; core [0.541, 0.487, 0.317] rim [0.385, 0.48, 0.251]
  - track 11 at frame 51: holes 0, rim-vs-core 0.46, rim-vs-outside 0.21, heterogeneity 0.17; core [0.609, 0.484, 0.257] rim [0.158, 0.462, 0.317]
  - track 61 at frame 83: holes 0, rim-vs-core 0.48, rim-vs-outside 0.34, heterogeneity 0.22; core [0.615, 0.855, 0.37] rim [0.164, 0.832, 0.529]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 242 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.515, rim/outside 9.3 (aggregate of 242 individuals; 1/242 membrane-like individually; rim level 0.484)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.965, rim/outside 1.06 (aggregate of 242 individuals; 0/242 membrane-like individually; rim level 0.639)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 11, rim/outside 4.78 (aggregate of 242 individuals; 239/242 membrane-like individually; rim level 0.698)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #7 (t=204, R_eq 4.98): ['shell q']; #8 (t=204, R_eq 5.11): ['shell q']; #11 (t=204, R_eq 5.08): ['shell q']; #61 (t=332, R_eq 5.17): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
