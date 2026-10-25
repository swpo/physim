# Evidence pack: membrane-evo-up (seed 26)

- world: `../../../../../threads/autopoiesis/worlds/membrane_evo_up/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 105s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo_up/world.py --out collective/contrib/20261025T1623-c19-review-membrane-evo/up/seed26 --seeds 26 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7147], min area 6 px

## Measurements
- components: final 12, mean 9.4, max 22; occupancy final 0.33
- tracks: 202; persistent (alive >= 50% of run): 0; longest 80 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 7.53, final 12; holes at thresholds 0.2/0.35/0.5 final [10, 13, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 12, 12], H1 [20, 13, 11]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00233/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 5000, default): splits 71, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 33, merge/split ratio 0.465, nucleations 0
- channel total drift (end/start - 1): [-0.9842, None, 0.6513, 0.0564]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 75: holes 1, rim-vs-core 0.36, rim-vs-outside 0.77, heterogeneity 0.21; core [0.832, 0.0, 0.599, 0.502] rim [0.507, 0.0, 0.549, 0.638]
  - track 77 at frame 97: holes 0, rim-vs-core 0.59, rim-vs-outside 0.92, heterogeneity 0.21; core [0.853, 0.0, 0.59, 0.543] rim [0.338, 0.0, 0.595, 0.821]
  - track 31 at frame 62: holes 0, rim-vs-core 0.40, rim-vs-outside 0.89, heterogeneity 0.21; core [0.804, 0.0, 0.555, 0.473] rim [0.476, 0.0, 0.573, 0.701]
  - track 82 at frame 87: holes 1, rim-vs-core 0.38, rim-vs-outside 0.74, heterogeneity 0.21; core [0.813, 0.0, 0.605, 0.548] rim [0.457, 0.0, 0.53, 0.656]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 8.01 (aggregate of 64 individuals; 1/64 membrane-like individually; rim level 0.296)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 2.12 (aggregate of 64 individuals; 5/64 membrane-like individually; rim level 0.302)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 2.59 (aggregate of 64 individuals; 33/64 membrane-like individually; rim level 0.475)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.9, rim/outside 1.86 (aggregate of 64 individuals; 41/64 membrane-like individually; rim level 0.419)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #28 (t=18750, R_eq 8.96, ring): ['membrane (wall)']; #77 (t=24250, R_eq 6.02): ['L link', 'membrane (wall)']; #31 (t=15500, R_eq 7.55): ['L link', 'membrane (wall)']; #82 (t=21750, R_eq 8.39, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 50 of 64 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
