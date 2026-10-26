# Evidence pack: cips-layered-chemostat (seed 0)

- world: `../world_wash.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 301 frames x 1000 steps x dt 0.1 = time 30000; grid [192, 192]; wall 2021s; status ok
- command: `python -m labkit.run world_wash.py --out W400 --seeds 0 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0229, 0.9742], min area 6 px

## Measurements
- components: final 0, mean 6.1, max 15; occupancy final 0.00
- tracks: 40; persistent (alive >= 50% of run): 0; longest 131 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.00333/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 17, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [-0.0, -0.7609, 0.82, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 68: holes 0, rim-vs-core 0.57, rim-vs-outside 0.61, heterogeneity 0.16; core [0.986, 0.956, 0.026, 0.09] rim [0.785, 0.718, 0.199, 0.528]
  - track 10 at frame 101: holes 0, rim-vs-core 0.40, rim-vs-outside 0.75, heterogeneity 0.17; core [0.988, 0.959, 0.026, 0.094] rim [0.843, 0.79, 0.146, 0.402]
  - track 9 at frame 96: holes 0, rim-vs-core 0.60, rim-vs-outside 0.62, heterogeneity 0.17; core [0.985, 0.953, 0.025, 0.096] rim [0.768, 0.706, 0.201, 0.566]
  - track 34 at frame 179: holes 0, rim-vs-core 0.55, rim-vs-outside 0.63, heterogeneity 0.16; core [0.985, 0.952, 0.021, 0.092] rim [0.783, 0.717, 0.188, 0.517]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [50, 101, 151, 199]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.889, rim/outside 33.6 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.864)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 12.4 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.843)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 25.9, rim/outside 0.631 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.468)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 3.93, rim/outside 17.6 (aggregate of 35 individuals; 33/35 membrane-like individually; rim level 0.505)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #0 (t=6800, R_eq 8.33): ['s']; #10 (t=10100, R_eq 8.25): ['s']; #9 (t=9600, R_eq 8.5): ['s']; #34 (t=17900, R_eq 8.44): ['s']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
