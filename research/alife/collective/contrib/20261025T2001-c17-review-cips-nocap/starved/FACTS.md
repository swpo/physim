# Evidence pack: cips-fuel (seed 4)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 257s; status ok
- command: `python -m labkit.run world.py --out starved --seeds 4 --frames 300 --spf 100 --no-movie`
- segmentation: matter > 0.53 of robust range [0.0009, 0.9502], min area 6 px

## Measurements
- components: final 84, mean 84.0, max 154; occupancy final 0.14
- tracks: 262; persistent (alive >= 50% of run): 75; longest 239 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [90, 85, 82], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.024/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 200, default): splits 1, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 87, merge/split ratio 87, nucleations 173
- channel total drift (end/start - 1): [0.0, -0.5215, 0.4338]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 182: holes 0, rim-vs-core 0.23, rim-vs-outside 0.29, heterogeneity 0.07; core [0.938, 0.901, 0.01] rim [0.745, 0.789, 0.065]
  - track 2 at frame 184: holes 0, rim-vs-core 0.27, rim-vs-outside 0.30, heterogeneity 0.08; core [0.924, 0.89, 0.013] rim [0.694, 0.767, 0.084]
  - track 3 at frame 184: holes 0, rim-vs-core 0.25, rim-vs-outside 0.31, heterogeneity 0.07; core [0.912, 0.878, 0.015] rim [0.696, 0.766, 0.083]
  - track 233 at frame 234: holes 0, rim-vs-core 0.20, rim-vs-outside 0.25, heterogeneity 0.06; core [0.881, 0.9, 0.021] rim [0.706, 0.811, 0.076]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 540 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 10.4 (aggregate of 540 individuals; 0/540 membrane-like individually; rim level 0.78)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 2.73 (aggregate of 540 individuals; 0/540 membrane-like individually; rim level 0.857)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 14.1, rim/outside 0.51 (aggregate of 540 individuals; 0/540 membrane-like individually; rim level 0.394)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1820, R_eq 4.69): none; #2 (t=1840, R_eq 4.82): none; #3 (t=1840, R_eq 4.55): none; #233 (t=2340, R_eq 4.79): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 540 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
