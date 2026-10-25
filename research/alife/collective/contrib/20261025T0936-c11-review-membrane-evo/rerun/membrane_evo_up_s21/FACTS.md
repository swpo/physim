# Evidence pack: membrane-evo-up (seed 21)

- world: `../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/membrane_evo_up/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 92s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo_up/world.py --out /tmp/claude-0/c11rev5/membrane_evo_up_s21 --seeds 21 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7221], min area 6 px

## Measurements
- components: final 12, mean 10.8, max 17; occupancy final 0.31
- tracks: 122; persistent (alive >= 50% of run): 0; longest 79 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 9.33, final 8; holes at thresholds 0.2/0.35/0.5 final [9, 8, 9]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 12, 9], H1 [15, 10, 4]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.00764/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 5000, default): splits 45, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 11, merge/split ratio 0.244, nucleations 0
- channel total drift (end/start - 1): [-0.969, None, 0.5682, -0.042]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 93: holes 1, rim-vs-core 0.39, rim-vs-outside 0.68, heterogeneity 0.22; core [0.842, 0.0, 0.741, 0.537] rim [0.495, 0.0, 0.581, 0.602]
  - track 56 at frame 118: holes 0, rim-vs-core 0.62, rim-vs-outside 0.97, heterogeneity 0.22; core [0.846, 0.0, 0.591, 0.443] rim [0.371, 0.0, 0.64, 0.84]
  - track 65 at frame 125: holes 1, rim-vs-core 0.35, rim-vs-outside 0.73, heterogeneity 0.20; core [0.764, 0.0, 0.593, 0.581] rim [0.432, 0.0, 0.53, 0.666]
  - track 91 at frame 151: holes 1, rim-vs-core 0.30, rim-vs-outside 0.77, heterogeneity 0.19; core [0.789, 0.0, 0.553, 0.485] rim [0.52, 0.0, 0.522, 0.624]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 70 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 9.29 (aggregate of 70 individuals; 5/70 membrane-like individually; rim level 0.535)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 1.79 (aggregate of 70 individuals; 2/70 membrane-like individually; rim level 0.0982)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 4.35 (aggregate of 70 individuals; 49/70 membrane-like individually; rim level 0.515)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 4.13, rim/outside 3.22 (aggregate of 70 individuals; 56/70 membrane-like individually; rim level 0.487)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #38 (t=23250, R_eq 9.11, ring): ['K1', 'L link', 'membrane (wall)']; #56 (t=29500, R_eq 6.48): ['L link', 'membrane (wall)']; #65 (t=31250, R_eq 8.65, ring): ['L link', 'membrane (wall)']; #91 (t=37750, R_eq 11.17): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 57 of 70 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
