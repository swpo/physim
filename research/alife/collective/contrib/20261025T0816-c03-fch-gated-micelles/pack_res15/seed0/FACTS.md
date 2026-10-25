# Evidence pack: fch-gated-micelles (seed 0)

- world: `../../world_res15.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [192, 192]; wall 359s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0816-c03-fch-gated-micelles/world_res15.py --out collective/contrib/20261025T0816-c03-fch-gated-micelles/pack_res15/seed0 --seeds 0 --frames 100 --size 192 192 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1166, 2.9912], min area 6 px

## Measurements
- components: final 54, mean 38.5, max 54; occupancy final 0.25
- tracks: 85; persistent (alive >= 50% of run): 30; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.56 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [54, 54, 54], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 80, default): splits 25, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 28
- channel total drift (end/start - 1): [0.6651, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 51: holes 0, rim-vs-core 0.74, rim-vs-outside 0.36, heterogeneity 0.25; core [0.703, 0.541, 0.141] rim [0.227, 0.063, 0.456]
  - track 9 at frame 51: holes 0, rim-vs-core 0.73, rim-vs-outside 0.37, heterogeneity 0.26; core [0.696, 0.523, 0.157] rim [0.218, 0.065, 0.47]
  - track 10 at frame 51: holes 0, rim-vs-core 0.73, rim-vs-outside 0.34, heterogeneity 0.25; core [0.694, 0.535, 0.149] rim [0.216, 0.058, 0.432]
  - track 56 at frame 82: holes 0, rim-vs-core 0.76, rim-vs-outside 0.53, heterogeneity 0.27; core [0.705, 0.399, 0.224] rim [0.227, 0.094, 0.727]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 242 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.549, rim/outside 14.4 (aggregate of 242 individuals; 3/242 membrane-like individually; rim level 0.515)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 9.6 (aggregate of 242 individuals; 0/242 membrane-like individually; rim level 0.418)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 9.86, rim/outside 4.96 (aggregate of 242 individuals; 236/242 membrane-like individually; rim level 0.642)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #8 (t=204, R_eq 7.38): ['shell q']; #9 (t=204, R_eq 7.42): ['shell q']; #10 (t=204, R_eq 7.46): ['shell q']; #56 (t=328, R_eq 7.42): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
