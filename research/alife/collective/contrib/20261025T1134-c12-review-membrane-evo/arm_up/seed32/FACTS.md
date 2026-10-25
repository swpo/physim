# Evidence pack: membrane-evo-up (seed 32)

- world: `../../world_up.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 156s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1134-c12-review-membrane-evo/world_up.py --out collective/contrib/20261025T1134-c12-review-membrane-evo/arm_up/seed32 --seeds 32 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7334], min area 6 px

## Measurements
- components: final 11, mean 11.3, max 18; occupancy final 0.31
- tracks: 128; persistent (alive >= 50% of run): 0; longest 70 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 9.79, final 9; holes at thresholds 0.2/0.35/0.5 final [8, 9, 9]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 11, 11], H1 [13, 9, 1]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00229/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 5000, default): splits 51, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 11, merge/split ratio 0.216, nucleations 0
- channel total drift (end/start - 1): [-0.9582, None, 0.5831, -0.0903]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 44 at frame 89: holes 1, rim-vs-core 0.33, rim-vs-outside 0.76, heterogeneity 0.20; core [0.83, 0.0, 0.621, 0.483] rim [0.533, 0.0, 0.562, 0.624]
  - track 46 at frame 98: holes 1, rim-vs-core 0.37, rim-vs-outside 0.74, heterogeneity 0.20; core [0.867, 0.0, 0.654, 0.498] rim [0.529, 0.0, 0.547, 0.616]
  - track 55 at frame 113: holes 1, rim-vs-core 0.40, rim-vs-outside 0.68, heterogeneity 0.22; core [0.838, 0.0, 0.712, 0.555] rim [0.471, 0.0, 0.572, 0.606]
  - track 60 at frame 108: holes 2, rim-vs-core 0.35, rim-vs-outside 0.74, heterogeneity 0.21; core [0.856, 0.0, 0.656, 0.461] rim [0.538, 0.0, 0.56, 0.583]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 74 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 8.6 (aggregate of 74 individuals; 6/74 membrane-like individually; rim level 0.519)
  - radial K2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.852, rim/outside 1.4 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.097)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.4, rim/outside 3.78 (aggregate of 74 individuals; 43/74 membrane-like individually; rim level 0.516)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.55, rim/outside 2.87 (aggregate of 74 individuals; 54/74 membrane-like individually; rim level 0.485)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #44 (t=22250, R_eq 10.09, ring): ['K1', 'L link', 'membrane (wall)']; #46 (t=24500, R_eq 10.97, ring): ['L link', 'membrane (wall)']; #55 (t=28250, R_eq 8.74, ring): ['K1', 'L link', 'membrane (wall)']; #60 (t=27000, R_eq 12.46): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 60 of 74 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
