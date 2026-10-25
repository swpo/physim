# Evidence pack: fch-metabolic-micelles-lowDc (seed 4)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1052-c07-metabolic-no-shell-needed/world_nogate_Dc0.03.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 313s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1052-c07-metabolic-no-shell-needed/world_nogate_Dc0.03.py --out /tmp/claude-0/c11rev20/Dc0.03 --seeds 4 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.1011, 2.9046], min area 6 px

## Measurements
- components: final 25, mean 24.6, max 25; occupancy final 0.11
- tracks: 38; persistent (alive >= 50% of run): 25; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 13.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 25, 25], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 160, default): splits 8, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 16
- channel total drift (end/start - 1): [-0.1313, 1.2141, None, -0.3535]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 0, rim-vs-core 0.55, rim-vs-outside 0.33, heterogeneity 0.20; core [0.636, 0.585, 0.344, 0.046] rim [0.184, 0.306, 0.468, 0.111]
  - track 7 at frame 51: holes 0, rim-vs-core 0.54, rim-vs-outside 0.29, heterogeneity 0.21; core [0.619, 0.608, 0.363, 0.047] rim [0.172, 0.314, 0.427, 0.116]
  - track 8 at frame 51: holes 0, rim-vs-core 0.54, rim-vs-outside 0.31, heterogeneity 0.20; core [0.628, 0.58, 0.358, 0.04] rim [0.178, 0.302, 0.456, 0.104]
  - track 10 at frame 51: holes 0, rim-vs-core 0.58, rim-vs-outside 0.29, heterogeneity 0.20; core [0.632, 0.709, 0.319, 0.068] rim [0.178, 0.364, 0.404, 0.155]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 150 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.516, rim/outside 25 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.493)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.577, rim/outside 4.68 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.53)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 13.1, rim/outside 6.96 (aggregate of 150 individuals; 150/150 membrane-like individually; rim level 0.779)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.02, rim/outside 0.84 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.25)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #0 (t=400, R_eq 4.65): ['shell q']; #7 (t=408, R_eq 4.72): ['shell q']; #8 (t=408, R_eq 4.69): ['shell q']; #10 (t=408, R_eq 4.69): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
