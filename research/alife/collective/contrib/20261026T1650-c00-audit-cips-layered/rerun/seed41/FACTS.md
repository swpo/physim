# Evidence pack: cips-layered-divide (seed 41)

- world: `../../wrapworld.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 181 frames x 500 steps x dt 0.1 = time 9000; grid [192, 192]; wall 890s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/cips-layered/replication/wrapworld.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/cips-layered/replication/runs/seed41 --seeds 41 --spf 500 --frames 180 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0216, 0.9749], min area 6 px

## Measurements
- components: final 15, mean 9.9, max 15; occupancy final 0.08
- tracks: 24; persistent (alive >= 50% of run): 10; longest 126 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.80 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00336/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 9, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [-0.0, -0.5971, 0.6448, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 118: holes 0, rim-vs-core 0.39, rim-vs-outside 0.74, heterogeneity 0.16; core [0.987, 0.959, 0.04, 0.085] rim [0.845, 0.781, 0.18, 0.368]
  - track 8 at frame 121: holes 0, rim-vs-core 0.54, rim-vs-outside 0.60, heterogeneity 0.16; core [0.979, 0.933, 0.052, 0.075] rim [0.777, 0.711, 0.223, 0.492]
  - track 9 at frame 121: holes 0, rim-vs-core 0.57, rim-vs-outside 0.60, heterogeneity 0.16; core [0.98, 0.94, 0.049, 0.083] rim [0.769, 0.706, 0.23, 0.52]
  - track 18 at frame 166: holes 0, rim-vs-core 0.55, rim-vs-outside 0.64, heterogeneity 0.16; core [0.991, 0.963, 0.073, 0.073] rim [0.784, 0.717, 0.25, 0.483]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [30, 61, 91, 119, 150, 180]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.855, rim/outside 25.6 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.821)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.861, rim/outside 11.6 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.807)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 17.3, rim/outside 0.646 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.491)
  - radial s: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.24, rim/outside 14 (aggregate of 64 individuals; 56/64 membrane-like individually; rim level 0.432)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #6 (t=5900, R_eq 8.18): ['s']; #8 (t=6050, R_eq 8.81): ['s']; #9 (t=6050, R_eq 8.5): ['s']; #18 (t=8300, R_eq 7.18): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
