# Evidence pack: membrane-evo-up (seed 37)

- world: `../../../../../threads/autopoiesis/worlds/membrane_evo_up/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 124s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo_up/world.py --out collective/work_c05/rev_db/rerun/seed37 --seeds 37 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7201], min area 6 px

## Measurements
- components: final 14, mean 10.6, max 30; occupancy final 0.30
- tracks: 109; persistent (alive >= 50% of run): 2; longest 124 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.72 (1 = constant size)
- enclosures: components with a hole mean 9.70, final 14; holes at thresholds 0.2/0.35/0.5 final [7, 14, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 14, 14], H1 [14, 14, 14]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00176/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 5000, default): splits 38, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.6682, None, 0.2865, 0.1407]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 99: holes 0, rim-vs-core 0.77, rim-vs-outside 0.98, heterogeneity 0.24; core [0.902, 0.0, 0.697, 0.284] rim [0.347, 0.0, 0.689, 0.82]
  - track 63 at frame 116: holes 1, rim-vs-core 0.46, rim-vs-outside 0.75, heterogeneity 0.21; core [0.897, 0.0, 0.667, 0.345] rim [0.537, 0.0, 0.566, 0.607]
  - track 62 at frame 110: holes 1, rim-vs-core 0.33, rim-vs-outside 0.71, heterogeneity 0.20; core [0.81, 0.0, 0.666, 0.599] rim [0.504, 0.0, 0.551, 0.627]
  - track 33 at frame 65: holes 1, rim-vs-core 0.28, rim-vs-outside 0.74, heterogeneity 0.20; core [0.751, 0.0, 0.574, 0.506] rim [0.511, 0.0, 0.521, 0.63]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 8.04 (aggregate of 67 individuals; 13/67 membrane-like individually; rim level 0.55)
  - radial K2: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 1.09 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.0189)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 4.68 (aggregate of 67 individuals; 40/67 membrane-like individually; rim level 0.452)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.74, rim/outside 3.55 (aggregate of 67 individuals; 55/67 membrane-like individually; rim level 0.458)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #38 (t=24750, R_eq 7): ['L link', 'membrane (wall)']; #63 (t=29000, R_eq 11.04, ring): ['L link', 'membrane (wall)']; #62 (t=27500, R_eq 9.47, ring): ['L link', 'membrane (wall)']; #33 (t=16250, R_eq 10.06, ring): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 61 of 67 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
