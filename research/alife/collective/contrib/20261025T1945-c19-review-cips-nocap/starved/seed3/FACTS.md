# Evidence pack: cips-fuel (seed 3)

- world: `../../../20261025T1845-c23-cips-metabolic-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 315s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1845-c23-cips-metabolic-claim/world.py --out collective/contrib/20261025T1945-c19-review-cips-nocap/starved/seed3 --seeds 3 --frames 300 --no-movie`
- segmentation: matter > 0.53 of robust range [0.0009, 0.9439], min area 6 px

## Measurements
- components: final 82, mean 84.7, max 157; occupancy final 0.14
- tracks: 260; persistent (alive >= 50% of run): 73; longest 237 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [88, 84, 75], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0141/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 85, merge/split ratio n/a, nucleations 175
- channel total drift (end/start - 1): [0.0, -0.5221, 0.4343]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 184: holes 0, rim-vs-core 0.23, rim-vs-outside 0.27, heterogeneity 0.07; core [0.901, 0.869, 0.017] rim [0.704, 0.772, 0.079]
  - track 4 at frame 184: holes 0, rim-vs-core 0.25, rim-vs-outside 0.30, heterogeneity 0.07; core [0.916, 0.87, 0.014] rim [0.704, 0.762, 0.08]
  - track 5 at frame 184: holes 0, rim-vs-core 0.17, rim-vs-outside 0.38, heterogeneity 0.07; core [0.938, 0.919, 0.01] rim [0.793, 0.832, 0.052]
  - track 8 at frame 184: holes 0, rim-vs-core 0.23, rim-vs-outside 0.29, heterogeneity 0.07; core [0.913, 0.881, 0.014] rim [0.718, 0.781, 0.074]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 536 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 9.96 (aggregate of 536 individuals; 2/536 membrane-like individually; rim level 0.774)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 2.63 (aggregate of 536 individuals; 1/536 membrane-like individually; rim level 0.853)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 12.2, rim/outside 0.506 (aggregate of 536 individuals; 0/536 membrane-like individually; rim level 0.388)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=1840, R_eq 4.22): none; #4 (t=1840, R_eq 4.41): none; #5 (t=1840, R_eq 5.17): none; #8 (t=1840, R_eq 4.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 536 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
