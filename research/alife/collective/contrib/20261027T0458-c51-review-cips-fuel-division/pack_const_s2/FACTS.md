# Evidence pack: cips-fuel-turnover (seed 2)

- world: `../../20261026T2102-c48-cips-fuel-powered-division/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1100-c40-cips-layered-divide-claim; mutation: c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 607s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2102-c48-cips-fuel-powered-division/world.py --out collective/contrib/20261027T0458-c51-review-cips-fuel-division/pack_const_s2 --seeds 2 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0211, 0.976], min area 6 px

## Measurements
- components: final 17, mean 12.1, max 17; occupancy final 0.09
- tracks: 26; persistent (alive >= 50% of run): 12; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.18 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00438/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 2000, default): splits 9, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 8
- channel total drift (end/start - 1): [0.0, 0.6482, -0.1017, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 63: holes 0, rim-vs-core 0.57, rim-vs-outside 0.62, heterogeneity 0.16; core [0.984, 0.946, 0.048, 0.084] rim [0.774, 0.701, 0.234, 0.509]
  - track 6 at frame 63: holes 0, rim-vs-core 0.56, rim-vs-outside 0.58, heterogeneity 0.16; core [0.975, 0.919, 0.062, 0.073] rim [0.764, 0.7, 0.223, 0.509]
  - track 8 at frame 76: holes 0, rim-vs-core 0.38, rim-vs-outside 0.74, heterogeneity 0.15; core [0.987, 0.958, 0.032, 0.085] rim [0.848, 0.775, 0.183, 0.35]
  - track 20 at frame 108: holes 0, rim-vs-core 0.56, rim-vs-outside 0.64, heterogeneity 0.17; core [0.989, 0.96, 0.075, 0.074] rim [0.778, 0.711, 0.253, 0.491]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 35.9 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.876)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 12.9 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.84)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 22.4, rim/outside 0.654 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.49)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.36, rim/outside 18.9 (aggregate of 79 individuals; 74/79 membrane-like individually; rim level 0.519)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #5 (t=6300, R_eq 8.2): ['s']; #6 (t=6300, R_eq 8.92): ['s']; #8 (t=7600, R_eq 8.18): ['s']; #20 (t=10800, R_eq 7.29): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
