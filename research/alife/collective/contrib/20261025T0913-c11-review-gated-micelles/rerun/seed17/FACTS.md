# Evidence pack: fch-gated-micelles (seed 17)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 152s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py --out /tmp/claude-0/c11rev3/rerun --seeds 17 --frames 100 --no-movie`
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
  - track 3 at frame 51: holes 0, rim-vs-core 0.60, rim-vs-outside 0.23, heterogeneity 0.26; core [0.62, 0.443, 0.231] rim [0.166, 0.061, 0.329]
  - track 7 at frame 51: holes 0, rim-vs-core 0.63, rim-vs-outside 0.22, heterogeneity 0.26; core [0.623, 0.456, 0.237] rim [0.167, 0.034, 0.325]
  - track 8 at frame 51: holes 0, rim-vs-core 0.65, rim-vs-outside 0.23, heterogeneity 0.26; core [0.625, 0.477, 0.244] rim [0.17, 0.024, 0.34]
  - track 54 at frame 82: holes 0, rim-vs-core 0.58, rim-vs-outside 0.41, heterogeneity 0.28; core [0.633, 0.355, 0.361] rim [0.18, 0.097, 0.619]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 248 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.52, rim/outside 10.1 (aggregate of 248 individuals; 6/248 membrane-like individually; rim level 0.482)
  - radial cargo c: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.676, rim/outside 7.22 (aggregate of 248 individuals; 0/248 membrane-like individually; rim level 0.354)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 9.86, rim/outside 4.98 (aggregate of 248 individuals; 242/248 membrane-like individually; rim level 0.68)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #3 (t=204, R_eq 5.17): ['shell q']; #7 (t=204, R_eq 5.14): ['shell q']; #8 (t=204, R_eq 5.11): ['shell q']; #54 (t=328, R_eq 5.01): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
