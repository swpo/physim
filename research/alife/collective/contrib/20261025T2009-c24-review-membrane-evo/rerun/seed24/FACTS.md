# Evidence pack: membrane-evo-up (seed 24)

- world: `../../../../../threads/autopoiesis/worlds/membrane_evo_up/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 157s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo_up/world.py --out collective/contrib/20261025T2009-c24-review-membrane-evo/rerun/seed24 --seeds 24 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7252], min area 6 px

## Measurements
- components: final 16, mean 9.2, max 17; occupancy final 0.29
- tracks: 152; persistent (alive >= 50% of run): 0; longest 62 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 7.35, final 14; holes at thresholds 0.2/0.35/0.5 final [7, 14, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 16, 16], H1 [18, 16, 8]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.00287/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 5000, default): splits 54, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 4, merges 18, merge/split ratio 0.333, nucleations 2
- channel total drift (end/start - 1): [-0.8588, None, 0.381, -0.1382]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 49 at frame 102: holes 1, rim-vs-core 0.43, rim-vs-outside 0.83, heterogeneity 0.23; core [0.859, 0.0, 0.631, 0.457] rim [0.47, 0.0, 0.595, 0.646]
  - track 27 at frame 66: holes 1, rim-vs-core 0.40, rim-vs-outside 0.84, heterogeneity 0.21; core [0.807, 0.0, 0.593, 0.51] rim [0.457, 0.0, 0.566, 0.695]
  - track 30 at frame 66: holes 1, rim-vs-core 0.35, rim-vs-outside 0.74, heterogeneity 0.21; core [0.842, 0.0, 0.678, 0.542] rim [0.521, 0.0, 0.581, 0.625]
  - track 66 at frame 105: holes 1, rim-vs-core 0.43, rim-vs-outside 0.78, heterogeneity 0.22; core [0.878, 0.0, 0.652, 0.477] rim [0.485, 0.0, 0.583, 0.639]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 10.5 (aggregate of 67 individuals; 5/67 membrane-like individually; rim level 0.517)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 1.68 (aggregate of 67 individuals; 5/67 membrane-like individually; rim level 0.145)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.48, rim/outside 3.77 (aggregate of 67 individuals; 46/67 membrane-like individually; rim level 0.534)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 4.46, rim/outside 2.8 (aggregate of 67 individuals; 53/67 membrane-like individually; rim level 0.492)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #49 (t=25500, R_eq 7.48, ring): ['L link', 'membrane (wall)']; #27 (t=16500, R_eq 7.4, ring): ['L link', 'membrane (wall)']; #30 (t=16500, R_eq 8.04, ring): ['L link', 'membrane (wall)']; #66 (t=26250, R_eq 7.46, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 54 of 67 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
