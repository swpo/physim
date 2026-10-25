# Evidence pack: fch-metabolic-micelles (seed 9)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c03-fch-metabolic/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 320s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev16/full9 --seeds 9 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.0816, 2.9812], min area 6 px

## Measurements
- components: final 58, mean 39.0, max 58; occupancy final 0.28
- tracks: 100; persistent (alive >= 50% of run): 32; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [58, 58, 58], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 160, default): splits 35, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.029, nucleations 21
- channel total drift (end/start - 1): [0.7421, 3.5144, None, -0.722]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 51: holes 0, rim-vs-core 0.82, rim-vs-outside 0.22, heterogeneity 0.24; core [0.638, 0.711, 0.195, 0.053] rim [0.186, 0.038, 0.298, 0.138]
  - track 20 at frame 51: holes 0, rim-vs-core 0.79, rim-vs-outside 0.20, heterogeneity 0.24; core [0.633, 0.649, 0.203, 0.048] rim [0.176, 0.011, 0.275, 0.134]
  - track 15 at frame 46: holes 0, rim-vs-core 0.85, rim-vs-outside 0.17, heterogeneity 0.24; core [0.615, 0.727, 0.2, 0.087] rim [0.166, 0.015, 0.222, 0.183]
  - track 62 at frame 80: holes 0, rim-vs-core 0.51, rim-vs-outside 0.36, heterogeneity 0.19; core [0.644, 0.173, 0.343, 0.069] rim [0.195, 0.009, 0.524, 0.09]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 248 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.513, rim/outside 8.67 (aggregate of 248 individuals; 0/248 membrane-like individually; rim level 0.486)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.421, rim/outside 8.78 (aggregate of 248 individuals; 0/248 membrane-like individually; rim level 0.243)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12.5, rim/outside 4.71 (aggregate of 248 individuals; 248/248 membrane-like individually; rim level 0.698)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.96, rim/outside 0.92 (aggregate of 248 individuals; 0/248 membrane-like individually; rim level 0.237)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #16 (t=408, R_eq 5.05): ['shell q']; #20 (t=408, R_eq 5.14): ['shell q']; #15 (t=368, R_eq 4.98): ['shell q']; #62 (t=640, R_eq 5.14): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
