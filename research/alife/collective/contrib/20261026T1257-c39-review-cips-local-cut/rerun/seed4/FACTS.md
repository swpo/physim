# Evidence pack: cips-layered-divide (seed 4)

- world: `../../../20261026T1210-c40-cips-local-cut/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 41 frames x 1000 steps x dt 0.1 = time 4000; grid [192, 192]; wall 256s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1210-c40-cips-local-cut/world.py --out collective/contrib/c39-rev-cut-wip/rerun/seed4 --seeds 4 --frames 40 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0281, 0.9711], min area 6 px

## Measurements
- components: final 6, mean 3.3, max 6; occupancy final 0.03
- tracks: 9; persistent (alive >= 50% of run): 3; longest 37 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 2000, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 3
- channel total drift (end/start - 1): [0.0, -0.7067, 0.762, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 21: holes 0, rim-vs-core 0.57, rim-vs-outside 0.62, heterogeneity 0.15; core [0.983, 0.955, 0.005, 0.145] rim [0.783, 0.724, 0.147, 0.604]
  - track 1 at frame 18: holes 0, rim-vs-core 0.60, rim-vs-outside 0.61, heterogeneity 0.16; core [0.985, 0.96, 0.008, 0.128] rim [0.779, 0.727, 0.156, 0.62]
  - track 0 at frame 16: holes 0, rim-vs-core 0.66, rim-vs-outside 0.61, heterogeneity 0.17; core [0.982, 0.952, 0.011, 0.123] rim [0.752, 0.712, 0.163, 0.674]
  - track 3 at frame 35: holes 0, rim-vs-core 0.60, rim-vs-outside 0.64, heterogeneity 0.17; core [0.994, 0.978, 0.014, 0.115] rim [0.783, 0.738, 0.179, 0.598]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 22 components >= 12 px at frames [7, 13, 20, 27, 33, 40]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 22.7 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.83)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.886, rim/outside 12 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.838)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 21.4, rim/outside 0.616 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.469)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 2.8, rim/outside 11.7 (aggregate of 22 individuals; 18/22 membrane-like individually; rim level 0.572)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #2 (t=2100, R_eq 9.52): ['s']; #1 (t=1800, R_eq 9.37): ['s']; #0 (t=1600, R_eq 9.62): ['s']; #3 (t=3500, R_eq 8.04): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
