# Evidence pack: fch-metabolic-micelles-lowDc (seed 7)

- world: `../../world_nogate_Dc0.01.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 461s; status ok
- command: `python -m labkit.run collective/contrib/_c07f2/world_nogate_Dc0.01.py --out collective/contrib/_c07f2/nogate_Dc0.01/seed7 --seeds 7 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1141, 2.9929], min area 6 px

## Measurements
- components: final 46, mean 38.3, max 46; occupancy final 0.24
- tracks: 71; persistent (alive >= 50% of run): 42; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 46, 46], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 160, default): splits 22, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 22
- channel total drift (end/start - 1): [0.5589, 2.9235, None, -0.6327]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 51: holes 0, rim-vs-core 0.25, rim-vs-outside 0.42, heterogeneity 0.20; core [0.567, 0.479, 0.339, 0.041] rim [0.367, 0.338, 0.304, 0.065]
  - track 8 at frame 51: holes 0, rim-vs-core 0.65, rim-vs-outside 0.25, heterogeneity 0.21; core [0.621, 0.724, 0.217, 0.067] rim [0.169, 0.278, 0.319, 0.158]
  - track 9 at frame 51: holes 0, rim-vs-core 0.58, rim-vs-outside 0.27, heterogeneity 0.21; core [0.619, 0.547, 0.269, 0.044] rim [0.169, 0.2, 0.383, 0.102]
  - track 65 at frame 89: holes 0, rim-vs-core 0.49, rim-vs-outside 0.29, heterogeneity 0.20; core [0.616, 0.229, 0.347, 0.196] rim [0.16, 0.083, 0.453, 0.237]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 239 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.524, rim/outside 12 (aggregate of 239 individuals; 7/239 membrane-like individually; rim level 0.484)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.421, rim/outside 5.81 (aggregate of 239 individuals; 2/239 membrane-like individually; rim level 0.3)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 11.8, rim/outside 5.11 (aggregate of 239 individuals; 232/239 membrane-like individually; rim level 0.697)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 3.37, rim/outside 0.888 (aggregate of 239 individuals; 0/239 membrane-like individually; rim level 0.182)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #7 (t=408, R_eq 5.08): ['shell q']; #8 (t=408, R_eq 5.05): ['shell q']; #9 (t=408, R_eq 5.01): ['shell q']; #65 (t=712, R_eq 5.17): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
