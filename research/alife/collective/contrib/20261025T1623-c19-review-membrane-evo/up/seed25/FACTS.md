# Evidence pack: membrane-evo-up (seed 25)

- world: `../../../../../threads/autopoiesis/worlds/membrane_evo_up/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 104s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo_up/world.py --out collective/contrib/20261025T1623-c19-review-membrane-evo/up/seed25 --seeds 25 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7027], min area 6 px

## Measurements
- components: final 12, mean 9.6, max 16; occupancy final 0.33
- tracks: 185; persistent (alive >= 50% of run): 0; longest 46 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 8.16, final 12; holes at thresholds 0.2/0.35/0.5 final [11, 12, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 12, 12], H1 [17, 12, 12]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00319/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 5000, default): splits 65, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 36, merge/split ratio 0.554, nucleations 1
- channel total drift (end/start - 1): [-0.9917, None, 0.6582, 0.0603]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 46 at frame 77: holes 1, rim-vs-core 0.41, rim-vs-outside 0.71, heterogeneity 0.21; core [0.86, 0.0, 0.655, 0.553] rim [0.478, 0.0, 0.539, 0.625]
  - track 113 at frame 134: holes 1, rim-vs-core 0.33, rim-vs-outside 0.68, heterogeneity 0.21; core [0.19, 0.691, 0.681, 0.601] rim [0.11, 0.401, 0.553, 0.635]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 70 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 7.48 (aggregate of 70 individuals; 2/70 membrane-like individually; rim level 0.291)
  - radial K2: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 2.21 (aggregate of 70 individuals; 1/70 membrane-like individually; rim level 0.323)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 2.6 (aggregate of 70 individuals; 37/70 membrane-like individually; rim level 0.489)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.59, rim/outside 1.85 (aggregate of 70 individuals; 46/70 membrane-like individually; rim level 0.413)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #46 (t=19250, R_eq 8.65, ring): ['L link', 'membrane (wall)']; #56 (t=19500, R_eq 12.07, ring): none; #97 (t=31250, R_eq 10.62, ring): ['L link', 'membrane (wall)']; #113 (t=33500, R_eq 8.65, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 55 of 70 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
