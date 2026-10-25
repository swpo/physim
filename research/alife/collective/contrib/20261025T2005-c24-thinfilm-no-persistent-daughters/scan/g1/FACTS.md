# Evidence pack: thinfilm-active (seed 0)

- world: `../world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 200 steps x dt 0.25 = time 4000; grid [128, 128]; wall 215s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/tfscan/world.py --out /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/tfscan/g1 --seeds 0 --frames 80 --no-movie`
- segmentation: matter > 0.08 of robust range [0.03, 5.8944], min area 6 px

## Measurements
- components: final 2, mean 5.4, max 20; occupancy final 0.20
- tracks: 75; persistent (alive >= 50% of run): 1; longest 48 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.46 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0394/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 1000, default): splits 19, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 28, merge/split ratio 1.47, nucleations 0
- channel total drift (end/start - 1): [-0.0, 2.4687, -425.1098, 42.6093]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 26 at frame 31: holes 0, rim-vs-core 0.26, rim-vs-outside 0.26, heterogeneity 0.14; core [0.411, 0.902, 0.048, 0.581] rim [0.174, 0.853, 0.129, 0.571]
  - track 41 at frame 26: holes 0, rim-vs-core 0.22, rim-vs-outside 0.18, heterogeneity 0.13; core [0.344, 0.883, 0.835, 0.808] rim [0.139, 0.827, 0.799, 0.768]
  - track 68 at frame 40: holes 0, rim-vs-core 0.36, rim-vs-outside 0.46, heterogeneity 0.24; core [0.583, 0.728, 0.442, 0.45] rim [0.348, 0.871, 0.544, 0.652]
  - track 70 at frame 56: holes 0, rim-vs-core 0.41, rim-vs-outside 0.60, heterogeneity 0.27; core [0.78, 0.848, 0.528, 0.372] rim [0.405, 0.915, 0.618, 0.494]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.622, rim/outside 5.21 (aggregate of 30 individuals; 1/30 membrane-like individually; rim level 0.319)
  - radial |p| polar order: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 2.09 (aggregate of 30 individuals; 2/30 membrane-like individually; rim level 0.846)
  - radial p_x: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.986, rim/outside 0.97 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.504)
  - radial p_y: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 1.04 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.507)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #26 (t=1550, R_eq 12.87): none; #41 (t=1300, R_eq 9.89): none; #68 (t=2000, R_eq 15.25): ['|p| polar order']; #70 (t=2800, R_eq 24.72): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 30 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
