# Evidence pack: membrane-evo-up (seed 55)

- world: `../../world_up.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 93s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_up.py --out collective/contrib/c17-mevo-wip/up/seed55 --seeds 55 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7271], min area 6 px

## Measurements
- components: final 15, mean 11.3, max 22; occupancy final 0.33
- tracks: 157; persistent (alive >= 50% of run): 1; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.97 (1 = constant size)
- enclosures: components with a hole mean 9.77, final 12; holes at thresholds 0.2/0.35/0.5 final [11, 12, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [17, 13, 9]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00455/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 5000, default): splits 57, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 16, merge/split ratio 0.281, nucleations 1
- channel total drift (end/start - 1): [-0.9798, None, 0.6668, 0.2159]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 67 at frame 114: holes 1, rim-vs-core 0.41, rim-vs-outside 0.80, heterogeneity 0.21; core [0.812, 0.0, 0.591, 0.485] rim [0.456, 0.0, 0.57, 0.684]
  - track 29 at frame 66: holes 1, rim-vs-core 0.35, rim-vs-outside 0.67, heterogeneity 0.20; core [0.815, 0.0, 0.663, 0.59] rim [0.482, 0.0, 0.551, 0.626]
  - track 54 at frame 85: holes 1, rim-vs-core 0.40, rim-vs-outside 0.81, heterogeneity 0.21; core [0.822, 0.0, 0.562, 0.409] rim [0.498, 0.0, 0.571, 0.64]
  - track 42 at frame 75: holes 0, rim-vs-core 0.58, rim-vs-outside 0.92, heterogeneity 0.21; core [0.77, 0.0, 0.508, 0.456] rim [0.348, 0.0, 0.589, 0.839]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 8.6 (aggregate of 77 individuals; 11/77 membrane-like individually; rim level 0.389)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 2.36 (aggregate of 77 individuals; 1/77 membrane-like individually; rim level 0.238)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 3.18 (aggregate of 77 individuals; 48/77 membrane-like individually; rim level 0.48)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.77, rim/outside 2.35 (aggregate of 77 individuals; 55/77 membrane-like individually; rim level 0.451)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #67 (t=28500, R_eq 8.18, ring): ['L link', 'membrane (wall)']; #29 (t=16500, R_eq 9.84, ring): ['K1', 'L link', 'membrane (wall)']; #54 (t=21250, R_eq 11.47, ring): ['membrane (wall)']; #42 (t=18750, R_eq 7.07): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 62 of 77 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
