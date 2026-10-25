# Evidence pack: membrane-evo-up (seed 52)

- world: `../../world_up.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 92s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_up.py --out collective/contrib/c17-mevo-wip/up/seed52 --seeds 52 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7146], min area 6 px

## Measurements
- components: final 11, mean 9.5, max 17; occupancy final 0.29
- tracks: 163; persistent (alive >= 50% of run): 0; longest 58 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 8.01, final 11; holes at thresholds 0.2/0.35/0.5 final [8, 11, 11]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 11, 11], H1 [15, 11, 9]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00308/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 5000, default): splits 57, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 24, merge/split ratio 0.421, nucleations 0
- channel total drift (end/start - 1): [-1.0, None, 0.6166, -0.1149]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 75: holes 0, rim-vs-core 0.71, rim-vs-outside 0.93, heterogeneity 0.23; core [0.89, 0.0, 0.645, 0.392] rim [0.323, 0.0, 0.635, 0.824]
  - track 37 at frame 65: holes 1, rim-vs-core 0.26, rim-vs-outside 0.75, heterogeneity 0.20; core [0.789, 0.0, 0.586, 0.538] rim [0.542, 0.0, 0.543, 0.625]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 8.34 (aggregate of 59 individuals; 1/59 membrane-like individually; rim level 0.313)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 2.3 (aggregate of 59 individuals; 2/59 membrane-like individually; rim level 0.302)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 2.84 (aggregate of 59 individuals; 29/59 membrane-like individually; rim level 0.485)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4, rim/outside 1.89 (aggregate of 59 individuals; 37/59 membrane-like individually; rim level 0.393)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #30 (t=18750, R_eq 7.05): ['L link', 'membrane (wall)']; #0 (t=5750, R_eq 17.19, ring): ['membrane (wall)']; #3 (t=5500, R_eq 16.25, ring): none; #37 (t=16250, R_eq 10.37, ring): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 49 of 59 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
