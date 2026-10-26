# Evidence pack: cips-layered-lownoise (seed 3)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 251 frames x 1000 steps x dt 0.1 = time 25000; grid [192, 192]; wall 1567s; status ok
- command: `python -m labkit.run world.py --out pack/seed3 --seeds 3 --frames 250 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0212, 0.9754], min area 6 px

## Measurements
- components: final 17, mean 10.0, max 17; occupancy final 0.09
- tracks: 32; persistent (alive >= 50% of run): 8; longest 152 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.40 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.00378/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 2000, default): splits 15, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 2
- channel total drift (end/start - 1): [-0.0, -0.5883, 0.634, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 174: holes 0, rim-vs-core 0.55, rim-vs-outside 0.64, heterogeneity 0.16; core [0.989, 0.956, 0.058, 0.077] rim [0.784, 0.711, 0.241, 0.491]
  - track 12 at frame 179: holes 0, rim-vs-core 0.51, rim-vs-outside 0.67, heterogeneity 0.17; core [0.99, 0.959, 0.046, 0.079] rim [0.8, 0.727, 0.224, 0.456]
  - track 15 at frame 183: holes 0, rim-vs-core 0.63, rim-vs-outside 0.64, heterogeneity 0.18; core [0.987, 0.948, 0.051, 0.082] rim [0.751, 0.685, 0.245, 0.57]
  - track 26 at frame 206: holes 0, rim-vs-core 0.62, rim-vs-outside 0.62, heterogeneity 0.17; core [0.985, 0.94, 0.048, 0.08] rim [0.754, 0.683, 0.236, 0.558]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [42, 84, 126, 166, 208, 250]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.95, rim/outside 54.5 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.944)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 14.7 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.884)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 44.2, rim/outside 0.652 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.491)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 6.73, rim/outside 31.2 (aggregate of 71 individuals; 71/71 membrane-like individually; rim level 0.68)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #11 (t=17400, R_eq 7.29): ['s']; #12 (t=17900, R_eq 7.51): ['s']; #15 (t=18300, R_eq 7.76): ['s']; #26 (t=20600, R_eq 7.82): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
