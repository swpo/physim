# Evidence pack: fch-metabolic-micelles (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c03-fch-metabolic/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 319s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev11/world --seeds 5 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.0807, 2.9834], min area 6 px

## Measurements
- components: final 55, mean 38.3, max 55; occupancy final 0.27
- tracks: 90; persistent (alive >= 50% of run): 32; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 23.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [55, 55, 55], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 160, default): splits 33, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [0.6992, 3.5331, None, -0.7227]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 51: holes 0, rim-vs-core 0.70, rim-vs-outside 0.24, heterogeneity 0.23; core [0.632, 0.597, 0.229, 0.045] rim [0.181, 0.081, 0.325, 0.105]
  - track 10 at frame 51: holes 0, rim-vs-core 0.80, rim-vs-outside 0.19, heterogeneity 0.25; core [0.618, 0.675, 0.234, 0.048] rim [0.169, 0.017, 0.282, 0.12]
  - track 16 at frame 51: holes 0, rim-vs-core 0.66, rim-vs-outside 0.24, heterogeneity 0.22; core [0.631, 0.541, 0.225, 0.054] rim [0.183, 0.075, 0.329, 0.114]
  - track 78 at frame 90: holes 0, rim-vs-core 0.50, rim-vs-outside 0.38, heterogeneity 0.18; core [0.63, 0.134, 0.367, 0.122] rim [0.189, 0.036, 0.581, 0.138]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 246 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.516, rim/outside 8.44 (aggregate of 246 individuals; 0/246 membrane-like individually; rim level 0.489)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.438, rim/outside 8.94 (aggregate of 246 individuals; 0/246 membrane-like individually; rim level 0.259)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12.5, rim/outside 4.73 (aggregate of 246 individuals; 246/246 membrane-like individually; rim level 0.702)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.99, rim/outside 0.922 (aggregate of 246 individuals; 0/246 membrane-like individually; rim level 0.238)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #7 (t=408, R_eq 5.05): ['shell q']; #10 (t=408, R_eq 5.11): ['shell q']; #16 (t=408, R_eq 5.05): ['shell q']; #78 (t=720, R_eq 4.89): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
