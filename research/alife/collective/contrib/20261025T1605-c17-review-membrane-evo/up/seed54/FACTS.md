# Evidence pack: membrane-evo-up (seed 54)

- world: `../../world_up.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 93s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_up.py --out collective/contrib/c17-mevo-wip/up/seed54 --seeds 54 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7273], min area 6 px

## Measurements
- components: final 12, mean 11.4, max 26; occupancy final 0.29
- tracks: 139; persistent (alive >= 50% of run): 1; longest 88 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.14 (1 = constant size)
- enclosures: components with a hole mean 9.25, final 10; holes at thresholds 0.2/0.35/0.5 final [6, 11, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 12, 9], H1 [16, 13, 8]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00283/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 5000, default): splits 50, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 4, merges 6, merge/split ratio 0.12, nucleations 1
- channel total drift (end/start - 1): [-0.9016, None, 0.4959, 0.051]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 52 at frame 87: holes 1, rim-vs-core 0.36, rim-vs-outside 0.70, heterogeneity 0.20; core [0.825, 0.0, 0.664, 0.553] rim [0.491, 0.0, 0.561, 0.634]
  - track 82 at frame 109: holes 1, rim-vs-core 0.32, rim-vs-outside 0.77, heterogeneity 0.21; core [0.861, 0.0, 0.675, 0.514] rim [0.56, 0.0, 0.584, 0.594]
  - track 58 at frame 85: holes 1, rim-vs-core 0.45, rim-vs-outside 0.63, heterogeneity 0.21; core [0.827, 0.0, 0.688, 0.608] rim [0.413, 0.0, 0.519, 0.602]
  - track 110 at frame 143: holes 1, rim-vs-core 0.37, rim-vs-outside 0.73, heterogeneity 0.20; core [0.798, 0.0, 0.618, 0.562] rim [0.45, 0.0, 0.539, 0.65]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 8.99 (aggregate of 71 individuals; 9/71 membrane-like individually; rim level 0.531)
  - radial K2: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 1.37 (aggregate of 71 individuals; 1/71 membrane-like individually; rim level 0.0708)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.41, rim/outside 4.03 (aggregate of 71 individuals; 49/71 membrane-like individually; rim level 0.485)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.74, rim/outside 2.92 (aggregate of 71 individuals; 60/71 membrane-like individually; rim level 0.455)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #52 (t=21750, R_eq 9.17, ring): ['K1', 'L link', 'membrane (wall)']; #82 (t=27250, R_eq 10.4, ring): none; #58 (t=21250, R_eq 9.79, ring): ['L link', 'membrane (wall)']; #110 (t=35750, R_eq 7.86, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 57 of 71 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
