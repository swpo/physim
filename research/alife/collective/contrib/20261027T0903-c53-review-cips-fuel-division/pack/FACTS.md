# Evidence pack: cips-fuel-turnover (seed 7)

- world: `../../20261026T2102-c48-cips-fuel-powered-division/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1100-c40-cips-layered-divide-claim; mutation: c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 899s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2102-c48-cips-fuel-powered-division/world.py --out collective/contrib/c53-rev-fpd/pack --seeds 7 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.022, 0.9754], min area 6 px

## Measurements
- components: final 17, mean 12.4, max 17; occupancy final 0.08
- tracks: 26; persistent (alive >= 50% of run): 14; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.15 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00316/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 9, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 8
- channel total drift (end/start - 1): [-0.0239, 0.5784, -0.0933, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 62: holes 0, rim-vs-core 0.55, rim-vs-outside 0.61, heterogeneity 0.16; core [0.981, 0.935, 0.048, 0.08] rim [0.775, 0.7, 0.229, 0.502]
  - track 8 at frame 74: holes 0, rim-vs-core 0.55, rim-vs-outside 0.63, heterogeneity 0.16; core [0.986, 0.948, 0.046, 0.081] rim [0.783, 0.704, 0.232, 0.485]
  - track 10 at frame 77: holes 0, rim-vs-core 0.40, rim-vs-outside 0.71, heterogeneity 0.17; core [0.977, 0.919, 0.068, 0.075] rim [0.823, 0.76, 0.174, 0.394]
  - track 11 at frame 77: holes 0, rim-vs-core 0.55, rim-vs-outside 0.63, heterogeneity 0.16; core [0.989, 0.953, 0.06, 0.076] rim [0.78, 0.704, 0.244, 0.487]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 82 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.918, rim/outside 39.2 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.904)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.881, rim/outside 13 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.855)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 27.1, rim/outside 0.652 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.493)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 5.26, rim/outside 21 (aggregate of 82 individuals; 79/82 membrane-like individually; rim level 0.549)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #3 (t=6200, R_eq 8.08): ['s']; #8 (t=7400, R_eq 7.88): ['s']; #10 (t=7700, R_eq 8.35): ['s']; #11 (t=7700, R_eq 7.42): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
