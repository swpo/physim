# Evidence pack: fch-metabolic-micelles (seed 1)

- world: `../../../20261025T0922-c03-fch-metabolic/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 308s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world.py --out collective/contrib/20261025T0935-c03-shell-needed-for-metabolism/pack_full/seed1 --seeds 1 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.0804, 2.9843], min area 6 px

## Measurements
- components: final 53, mean 37.4, max 53; occupancy final 0.27
- tracks: 89; persistent (alive >= 50% of run): 29; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.10 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [53, 53, 53], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 160, default): splits 35, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 18
- channel total drift (end/start - 1): [0.7287, 3.4714, None, -0.7171]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 51: holes 0, rim-vs-core 0.69, rim-vs-outside 0.22, heterogeneity 0.24; core [0.617, 0.626, 0.233, 0.061] rim [0.171, 0.102, 0.287, 0.13]
  - track 5 at frame 51: holes 0, rim-vs-core 0.78, rim-vs-outside 0.19, heterogeneity 0.25; core [0.615, 0.654, 0.232, 0.041] rim [0.167, 0.015, 0.271, 0.108]
  - track 8 at frame 51: holes 0, rim-vs-core 0.80, rim-vs-outside 0.21, heterogeneity 0.24; core [0.639, 0.666, 0.202, 0.047] rim [0.18, 0.018, 0.286, 0.131]
  - track 61 at frame 80: holes 0, rim-vs-core 0.37, rim-vs-outside 0.37, heterogeneity 0.21; core [0.652, 0.252, 0.355, 0.076] rim [0.33, 0.094, 0.459, 0.094]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 238 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.516, rim/outside 7.98 (aggregate of 238 individuals; 1/238 membrane-like individually; rim level 0.488)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.417, rim/outside 8.73 (aggregate of 238 individuals; 0/238 membrane-like individually; rim level 0.255)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 11.9, rim/outside 4.53 (aggregate of 238 individuals; 237/238 membrane-like individually; rim level 0.687)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.98, rim/outside 0.92 (aggregate of 238 individuals; 0/238 membrane-like individually; rim level 0.238)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #2 (t=408, R_eq 5.05): ['shell q']; #5 (t=408, R_eq 5.11): ['shell q']; #8 (t=408, R_eq 5.11): ['shell q']; #61 (t=640, R_eq 5.11): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
