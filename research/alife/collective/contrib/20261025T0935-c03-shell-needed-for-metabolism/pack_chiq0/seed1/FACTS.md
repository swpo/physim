# Evidence pack: fch-metabolic-micelles (seed 1)

- world: `../../../20261025T0922-c03-fch-metabolic/world_chiq0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 310s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world_chiq0.py --out collective/contrib/20261025T0935-c03-shell-needed-for-metabolism/pack_chiq0/seed1 --seeds 1 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.19 of robust range [0.0059, 2.6296], min area 6 px

## Measurements
- components: final 0, mean 9.4, max 24; occupancy final 0.00
- tracks: 31; persistent (alive >= 50% of run): 2; longest 57 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 160, default): splits 6, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 18
- channel total drift (end/start - 1): [-0.9802, -0.9994, None, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 29: holes 0, rim-vs-core 0.45, rim-vs-outside 0.21, heterogeneity 0.07; core [0.797, 0.18, 1.0, 0.561] rim [0.352, 0.173, 0.989, 0.573]
  - track 7 at frame 29: holes 0, rim-vs-core 0.45, rim-vs-outside 0.19, heterogeneity 0.07; core [0.764, 0.172, 0.996, 0.575] rim [0.314, 0.165, 0.96, 0.585]
  - track 5 at frame 22: holes 0, rim-vs-core 0.48, rim-vs-outside 0.19, heterogeneity 0.08; core [0.798, 0.299, 1.0, 0.324] rim [0.317, 0.282, 0.976, 0.354]
  - track 9 at frame 22: holes 0, rim-vs-core 0.48, rim-vs-outside 0.18, heterogeneity 0.08; core [0.785, 0.291, 0.994, 0.338] rim [0.308, 0.275, 0.943, 0.367]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 50 components >= 12 px at frames [17, 33, 50]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.607, rim/outside 16.8 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.598)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.838, rim/outside 1.09 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.253)
  - radial shell q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 1.16 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.941)
  - radial precursor p: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.36, rim/outside 0.98 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.49)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=232, R_eq 3.19): none; #7 (t=232, R_eq 3.29): none; #5 (t=176, R_eq 3.61): none; #9 (t=176, R_eq 3.61): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
