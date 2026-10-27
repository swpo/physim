# Evidence pack: fed-vortices (seed 2)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1501 frames x 150 steps x dt 0.02 = time 4500; grid [128, 128]; wall 849s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvh/world.py --out collective/contrib/c53-fvh/pack_neutral --seeds 1 2 --frames 1500 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2045], min area 6 px

## Measurements
- components: final 26, mean 27.7, max 38; occupancy final 0.15
- tracks: 564; persistent (alive >= 50% of run): 4; longest 1040 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.80 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 29, 26], H1 [0, 0, 0]
- motion: 296 long-lived tracks moved >= 1 body length; max speed 0.55/time; max body lengths 65.9
- replication (lineage window K = 20 frames = time 60, default): splits 182, persistent splits 77 (0 more failed only because the siblings re-merged within K), max generation 14, merges 166, merge/split ratio 0.912, nucleations 0
- channel total drift (end/start - 1): [-0.5434, 0.1578, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 69 at frame 542: holes 0, rim-vs-core 0.66, rim-vs-outside 0.34, heterogeneity 0.18; core [0.812, 0.101, 0.416, 0.707] rim [0.401, 0.308, 0.176, 0.298]
  - track 168 at frame 857: holes 0, rim-vs-core 0.70, rim-vs-outside 0.43, heterogeneity 0.17; core [0.831, 0.098, 0.154, 0.964] rim [0.424, 0.331, 0.064, 0.452]
  - track 125 at frame 681: holes 0, rim-vs-core 0.71, rim-vs-outside 0.34, heterogeneity 0.19; core [0.854, 0.138, 0.412, 0.689] rim [0.399, 0.332, 0.148, 0.247]
  - track 529 at frame 1462: holes 0, rim-vs-core 0.58, rim-vs-outside 0.33, heterogeneity 0.15; core [0.75, 0.102, 0.447, 0.634] rim [0.409, 0.311, 0.208, 0.293]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 162 components >= 12 px at frames [252, 504, 756, 996, 1248, 1500]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.769, rim/outside 14.3 (aggregate of 162 individuals; 2/162 membrane-like individually; rim level 0.647)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.05, rim/outside 0.765 (aggregate of 162 individuals; 0/162 membrane-like individually; rim level 0.468)
  - radial label a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.781, rim/outside 15.3 (aggregate of 162 individuals; 5/162 membrane-like individually; rim level 0.427)
  - radial label b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.755, rim/outside 14.4 (aggregate of 162 individuals; 5/162 membrane-like individually; rim level 0.402)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #69 (t=1626, R_eq 4.72): none; #168 (t=2571, R_eq 5.17): none; #125 (t=2043, R_eq 3.83): none; #529 (t=4386, R_eq 5.53): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 162 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
