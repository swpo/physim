# Evidence pack: fch-metabolic-micelles (seed 4)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c03-fch-metabolic/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 323s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world.py --out /tmp/claude-0/c11rev15/world --seeds 4 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.082, 2.9828], min area 6 px

## Measurements
- components: final 56, mean 37.9, max 56; occupancy final 0.27
- tracks: 102; persistent (alive >= 50% of run): 36; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 15.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [56, 56, 56], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0233/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 160, default): splits 39, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.026, nucleations 16
- channel total drift (end/start - 1): [0.6476, 3.3025, None, -0.6869]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 0, rim-vs-core 0.75, rim-vs-outside 0.21, heterogeneity 0.24; core [0.617, 0.644, 0.255, 0.046] rim [0.169, 0.042, 0.3, 0.109]
  - track 7 at frame 51: holes 0, rim-vs-core 0.72, rim-vs-outside 0.22, heterogeneity 0.24; core [0.615, 0.643, 0.247, 0.051] rim [0.171, 0.075, 0.303, 0.114]
  - track 14 at frame 51: holes 0, rim-vs-core 0.66, rim-vs-outside 0.23, heterogeneity 0.23; core [0.619, 0.597, 0.223, 0.092] rim [0.174, 0.125, 0.287, 0.162]
  - track 71 at frame 83: holes 0, rim-vs-core 0.54, rim-vs-outside 0.36, heterogeneity 0.21; core [0.639, 0.225, 0.359, 0.09] rim [0.185, 0.012, 0.55, 0.12]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 245 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.515, rim/outside 7.64 (aggregate of 245 individuals; 0/245 membrane-like individually; rim level 0.487)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.424, rim/outside 7.79 (aggregate of 245 individuals; 0/245 membrane-like individually; rim level 0.253)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12.4, rim/outside 4.51 (aggregate of 245 individuals; 245/245 membrane-like individually; rim level 0.698)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.85, rim/outside 0.924 (aggregate of 245 individuals; 0/245 membrane-like individually; rim level 0.242)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #0 (t=400, R_eq 4.95): ['shell q']; #7 (t=408, R_eq 4.95): ['shell q']; #14 (t=408, R_eq 4.92): ['shell q']; #71 (t=664, R_eq 5.08): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
