# Evidence pack: cips-fuel-turnover (seed 7)

- world: `../../20261026T2102-c48-cips-fuel-powered-division/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1100-c40-cips-layered-divide-claim; mutation: c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 891s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2102-c48-cips-fuel-powered-division/world.py --out collective/contrib/c53-rev-fpd/pack_const --seeds 7 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0212, 0.975], min area 6 px

## Measurements
- components: final 16, mean 12.8, max 16; occupancy final 0.09
- tracks: 24; persistent (alive >= 50% of run): 15; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.18 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00281/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 8, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 8
- channel total drift (end/start - 1): [-0.0, 0.6522, -0.1023, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 62: holes 0, rim-vs-core 0.57, rim-vs-outside 0.59, heterogeneity 0.16; core [0.978, 0.923, 0.063, 0.075] rim [0.763, 0.694, 0.236, 0.519]
  - track 8 at frame 73: holes 0, rim-vs-core 0.54, rim-vs-outside 0.62, heterogeneity 0.16; core [0.986, 0.946, 0.051, 0.084] rim [0.784, 0.704, 0.236, 0.483]
  - track 9 at frame 73: holes 0, rim-vs-core 0.54, rim-vs-outside 0.62, heterogeneity 0.16; core [0.983, 0.937, 0.044, 0.086] rim [0.782, 0.701, 0.23, 0.482]
  - track 10 at frame 77: holes 0, rim-vs-core 0.40, rim-vs-outside 0.69, heterogeneity 0.16; core [0.976, 0.917, 0.076, 0.07] rim [0.821, 0.756, 0.184, 0.385]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 82 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.885, rim/outside 36.1 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.864)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 13.1 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.832)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 23.3, rim/outside 0.652 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.493)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.63, rim/outside 19.9 (aggregate of 82 individuals; 78/82 membrane-like individually; rim level 0.526)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #3 (t=6200, R_eq 8.59): ['s']; #8 (t=7300, R_eq 8.14): ['s']; #9 (t=7300, R_eq 8.44): ['s']; #10 (t=7700, R_eq 8.81): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
