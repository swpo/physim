# Evidence pack: cips-layered-divide (seed 13)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261026T1526-c44-cips-seasons-negative/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [128, 128]; wall 472s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1526-c44-cips-seasons-negative/world.py --out /tmp/claude-0/cs/pulse025/seed13 --seeds 13 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0217, 0.9753], min area 6 px

## Measurements
- components: final 0, mean 5.5, max 8; occupancy final 0.00
- tracks: 44; persistent (alive >= 50% of run): 0; longest 99 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00367/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 4, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 36
- channel total drift (end/start - 1): [0.0, -0.9636, -0.7996, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 150: holes 0, rim-vs-core 0.53, rim-vs-outside 0.62, heterogeneity 0.16; core [0.987, 0.943, 0.291, 0.085] rim [0.785, 0.702, 0.434, 0.481]
  - track 21 at frame 150: holes 0, rim-vs-core 0.52, rim-vs-outside 0.62, heterogeneity 0.15; core [0.987, 0.944, 0.292, 0.084] rim [0.788, 0.704, 0.434, 0.472]
  - track 12 at frame 119: holes 0, rim-vs-core 0.57, rim-vs-outside 0.61, heterogeneity 0.16; core [0.984, 0.935, 0.291, 0.085] rim [0.764, 0.686, 0.438, 0.522]
  - track 3 at frame 59: holes 0, rim-vs-core 0.53, rim-vs-outside 0.61, heterogeneity 0.15; core [0.982, 0.923, 0.275, 0.089] rim [0.78, 0.69, 0.425, 0.492]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [34, 67, 101, 133, 166]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 34.5 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.915)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 11.4 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.857)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.38, rim/outside 0.772 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.63)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 5.94, rim/outside 20.1 (aggregate of 30 individuals; 29/30 membrane-like individually; rim level 0.641)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #20 (t=15000, R_eq 7.82): ['s']; #21 (t=15000, R_eq 7.76): ['s']; #12 (t=11900, R_eq 8.02): ['s']; #3 (t=5900, R_eq 8.35): ['s']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
