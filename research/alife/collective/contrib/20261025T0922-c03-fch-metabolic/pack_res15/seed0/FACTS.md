# Evidence pack: fch-metabolic-micelles (seed 0)

- world: `../../world_res15.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [192, 192]; wall 708s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world_res15.py --out collective/contrib/20261025T0922-c03-fch-metabolic/pack_res15/seed0 --seeds 0 --frames 100 --spf 400 --size 192 192 --no-movie`
- segmentation: matter > 0.15 of robust range [0.0675, 2.9828], min area 6 px

## Measurements
- components: final 59, mean 40.2, max 59; occupancy final 0.26
- tracks: 95; persistent (alive >= 50% of run): 36; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.03 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [59, 59, 59], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 160, default): splits 30, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 28
- channel total drift (end/start - 1): [0.7009, 3.4049, None, -0.7046]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 51: holes 0, rim-vs-core 0.65, rim-vs-outside 0.50, heterogeneity 0.24; core [0.697, 0.901, 0.131, 0.056] rim [0.402, 0.347, 0.285, 0.106]
  - track 17 at frame 51: holes 0, rim-vs-core 0.94, rim-vs-outside 0.32, heterogeneity 0.24; core [0.704, 0.884, 0.117, 0.07] rim [0.239, 0.104, 0.359, 0.161]
  - track 22 at frame 51: holes 0, rim-vs-core 0.95, rim-vs-outside 0.34, heterogeneity 0.24; core [0.708, 0.886, 0.121, 0.049] rim [0.241, 0.108, 0.387, 0.128]
  - track 63 at frame 83: holes 0, rim-vs-core 0.71, rim-vs-outside 0.52, heterogeneity 0.19; core [0.715, 0.186, 0.211, 0.08] rim [0.24, 0.011, 0.705, 0.1]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 260 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.545, rim/outside 10.5 (aggregate of 260 individuals; 0/260 membrane-like individually; rim level 0.515)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.626, rim/outside 13.9 (aggregate of 260 individuals; 0/260 membrane-like individually; rim level 0.352)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 11.8, rim/outside 4.92 (aggregate of 260 individuals; 260/260 membrane-like individually; rim level 0.637)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.64, rim/outside 0.926 (aggregate of 260 individuals; 0/260 membrane-like individually; rim level 0.258)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #10 (t=408, R_eq 7.2): ['shell q']; #17 (t=408, R_eq 7.2): ['shell q']; #22 (t=408, R_eq 7.2): ['shell q']; #63 (t=664, R_eq 7.46): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
