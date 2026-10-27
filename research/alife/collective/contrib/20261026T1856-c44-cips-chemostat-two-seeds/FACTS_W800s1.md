# Evidence pack: cips-layered-chemostat (seed 1)

- world: `../world_wash.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 301 frames x 1000 steps x dt 0.1 = time 30000; grid [192, 192]; wall 2153s; status ok
- command: `python -m labkit.run world_wash.py --out W800s1 --seeds 1 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.021, 0.9757], min area 6 px

## Measurements
- components: final 12, mean 11.4, max 16; occupancy final 0.07
- tracks: 63; persistent (alive >= 50% of run): 1; longest 186 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 12, 12], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.00363/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 2000, default): splits 28, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 5, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [-0.0148, -0.6443, 0.6953, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 134: holes 0, rim-vs-core 0.36, rim-vs-outside 0.75, heterogeneity 0.16; core [0.981, 0.935, 0.056, 0.077] rim [0.846, 0.786, 0.157, 0.36]
  - track 9 at frame 108: holes 0, rim-vs-core 0.60, rim-vs-outside 0.62, heterogeneity 0.17; core [0.987, 0.952, 0.057, 0.08] rim [0.765, 0.698, 0.243, 0.534]
  - track 17 at frame 136: holes 0, rim-vs-core 0.35, rim-vs-outside 0.78, heterogeneity 0.16; core [0.981, 0.933, 0.05, 0.083] rim [0.851, 0.796, 0.15, 0.358]
  - track 51 at frame 287: holes 0, rim-vs-core 0.57, rim-vs-outside 0.62, heterogeneity 0.17; core [0.988, 0.952, 0.05, 0.079] rim [0.775, 0.703, 0.231, 0.502]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 73 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 31 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.858)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 11.9 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.827)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 21.7, rim/outside 0.648 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.48)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.2, rim/outside 17 (aggregate of 73 individuals; 67/73 membrane-like individually; rim level 0.494)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #10 (t=13400, R_eq 8.33): ['s']; #9 (t=10800, R_eq 7.69): ['s']; #17 (t=13600, R_eq 8.31): ['s']; #51 (t=28700, R_eq 7.76): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
