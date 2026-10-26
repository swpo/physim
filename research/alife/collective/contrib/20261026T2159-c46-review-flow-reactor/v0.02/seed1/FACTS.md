# Evidence pack: cips-layered-flow (seed 1)

- world: `../../../20261026T1729-c44-cips-flow-reactor-budding-niche/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 301 frames x 1000 steps x dt 0.1 = time 30000; grid [128, 128]; wall 790s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1729-c44-cips-flow-reactor-budding-niche/world.py --out collective/contrib/20261026T2159-c46-review-flow-reactor/v0.02/seed1 --seeds 1 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0178, 0.983], min area 6 px

## Measurements
- components: final 18, mean 15.6, max 18; occupancy final 0.15
- tracks: 200; persistent (alive >= 50% of run): 0; longest 57 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 17], H1 [0, 0, 0]
- motion: 64 long-lived tracks moved >= 1 body length; max speed 0.0218/time; max body lengths 8.8
- replication (lineage window K = 20 frames = time 2000, default): splits 70, persistent splits 57 (0 more failed only because the siblings re-merged within K), max generation 16, merges 54, merge/split ratio 0.771, nucleations 6
- channel total drift (end/start - 1): [0.4756, -0.3431, 0.3587, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 45: holes 0, rim-vs-core 0.53, rim-vs-outside 0.63, heterogeneity 0.16; core [0.987, 0.945, 0.214, 0.073] rim [0.785, 0.7, 0.355, 0.479]
  - track 32 at frame 86: holes 0, rim-vs-core 0.71, rim-vs-outside 0.38, heterogeneity 0.16; core [0.957, 0.89, 0.269, 0.119] rim [0.686, 0.631, 0.405, 0.705]
  - track 10 at frame 43: holes 0, rim-vs-core 0.54, rim-vs-outside 0.63, heterogeneity 0.16; core [0.986, 0.942, 0.195, 0.075] rim [0.785, 0.695, 0.342, 0.491]
  - track 178 at frame 285: holes 0, rim-vs-core 0.72, rim-vs-outside 0.38, heterogeneity 0.17; core [0.957, 0.896, 0.272, 0.121] rim [0.682, 0.634, 0.412, 0.712]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 101 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 22.2 (aggregate of 101 individuals; 1/101 membrane-like individually; rim level 0.905)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 7.78 (aggregate of 101 individuals; 0/101 membrane-like individually; rim level 0.787)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.2, rim/outside 0.759 (aggregate of 101 individuals; 0/101 membrane-like individually; rim level 0.493)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 6.86, rim/outside 19.1 (aggregate of 101 individuals; 96/101 membrane-like individually; rim level 0.611)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #15 (t=4500, R_eq 6.08): ['s']; #32 (t=8600, R_eq 5.73): ['s']; #10 (t=4300, R_eq 6.33): ['s']; #178 (t=28500, R_eq 5.81): ['s']

## Warnings
- radial: 2 of 101 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
