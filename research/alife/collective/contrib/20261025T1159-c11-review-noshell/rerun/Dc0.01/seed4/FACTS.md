# Evidence pack: fch-metabolic-micelles-lowDc (seed 4)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1052-c07-metabolic-no-shell-needed/world_nogate_Dc0.01.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 312s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1052-c07-metabolic-no-shell-needed/world_nogate_Dc0.01.py --out /tmp/claude-0/c11rev20/Dc0.01 --seeds 4 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.0989, 2.9803], min area 6 px

## Measurements
- components: final 45, mean 39.7, max 45; occupancy final 0.23
- tracks: 79; persistent (alive >= 50% of run): 44; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 14.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [45, 45, 45], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 160, default): splits 28, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.036, nucleations 16
- channel total drift (end/start - 1): [0.5035, 2.8874, None, -0.6206]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 0, rim-vs-core 0.58, rim-vs-outside 0.27, heterogeneity 0.20; core [0.618, 0.556, 0.256, 0.047] rim [0.178, 0.197, 0.368, 0.1]
  - track 7 at frame 51: holes 0, rim-vs-core 0.59, rim-vs-outside 0.26, heterogeneity 0.20; core [0.616, 0.588, 0.256, 0.051] rim [0.173, 0.209, 0.349, 0.11]
  - track 10 at frame 51: holes 0, rim-vs-core 0.62, rim-vs-outside 0.22, heterogeneity 0.21; core [0.601, 0.654, 0.259, 0.057] rim [0.158, 0.231, 0.291, 0.128]
  - track 38 at frame 61: holes 0, rim-vs-core 0.38, rim-vs-outside 0.35, heterogeneity 0.20; core [0.627, 0.477, 0.314, 0.056] rim [0.326, 0.241, 0.336, 0.091]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 246 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.512, rim/outside 9.83 (aggregate of 246 individuals; 0/246 membrane-like individually; rim level 0.486)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.414, rim/outside 5.22 (aggregate of 246 individuals; 0/246 membrane-like individually; rim level 0.325)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12.7, rim/outside 4.8 (aggregate of 246 individuals; 246/246 membrane-like individually; rim level 0.698)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 3.13, rim/outside 0.893 (aggregate of 246 individuals; 0/246 membrane-like individually; rim level 0.192)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #0 (t=400, R_eq 4.82): ['shell q']; #7 (t=408, R_eq 4.89): ['shell q']; #10 (t=408, R_eq 4.98): ['shell q']; #38 (t=488, R_eq 4.98): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
