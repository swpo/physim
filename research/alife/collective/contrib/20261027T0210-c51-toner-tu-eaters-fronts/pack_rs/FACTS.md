# Evidence pack: eating-flocks (seed 0)

- world: `../world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 151 frames x 80 steps x dt 0.25 = time 3000; grid [128, 128]; wall 21s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/world.py --out collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/pack_rs --seeds 0 --frames 150 --spf 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0484], min area 6 px

## Measurements
- components: final 15, mean 13.4, max 25; occupancy final 0.13
- tracks: 1005; persistent (alive >= 50% of run): 0; longest 14 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 15, 5], H1 [7, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 7.4
- replication (lineage window K = 20 frames = time 400, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio 3, nucleations 966
- channel total drift (end/start - 1): [0.537, -0.4718, -0.3353, 4.9705]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 151 at frame 25: holes 0, rim-vs-core 0.15, rim-vs-outside 0.53, heterogeneity 0.09; core [0.667, 0.052, 0.904, 0.965] rim [0.58, 0.149, 0.849, 0.926]
  - track 707 at frame 108: holes 0, rim-vs-core 0.19, rim-vs-outside 0.47, heterogeneity 0.12; core [0.695, 0.025, 0.931, 0.18] rim [0.571, 0.135, 0.864, 0.246]
  - track 914 at frame 144: holes 0, rim-vs-core 0.21, rim-vs-outside 0.65, heterogeneity 0.12; core [0.783, 0.002, 0.922, 0.95] rim [0.616, 0.121, 0.874, 0.914]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 89 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial density rho: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.85, rim/outside 2.25 (aggregate of 89 individuals; 4/89 membrane-like individually; rim level 0.412)
  - radial food c: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.31, rim/outside 0.819 (aggregate of 89 individuals; 0/89 membrane-like individually; rim level 0.375)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.89, rim/outside 2.09 (aggregate of 89 individuals; 3/89 membrane-like individually; rim level 0.682)
  - radial p_x: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 1.01 (aggregate of 89 individuals; 0/89 membrane-like individually; rim level 0.496)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #151 (t=500, R_eq 6.48, ring): none; #707 (t=2160, R_eq 8.96, ring): ['density rho', '|p|']; #763 (t=2340, R_eq 6.18): none; #914 (t=2880, R_eq 12.8, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 17 of 89 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
