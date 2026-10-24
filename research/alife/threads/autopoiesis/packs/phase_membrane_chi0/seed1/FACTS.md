# Evidence pack: phase-membrane-chi0 (seed 1)

- world: `../../../worlds/phase_membrane_chi0/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: CONTROL: chi=0 (no link adsorption to the wall); is the ring load-bearing?
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane_chi0/world.py --out threads/autopoiesis/packs/phase_membrane_chi0 --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.5262], min area 6 px

## Measurements
- components: final 42, mean 31.3, max 42; occupancy final 0.36
- tracks: 120; persistent (alive >= 50% of run): 32; longest 154 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.04 (1 = constant size)
- enclosures: components with a hole mean 1.70, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 42, 42], H1 [42, 41, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 1000, default): splits 44, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 0.091, nucleations 0
- channel total drift (end/start - 1): [-0.5318, -0.6835, 0.2861, 0.281]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 58 at frame 83: holes 0, rim-vs-core 0.43, rim-vs-outside 0.96, heterogeneity 0.18; core [0.085, 0.842, 0.726, 0.65] rim [0.274, 0.468, 0.662, 0.697]
  - track 66 at frame 86: holes 0, rim-vs-core 0.37, rim-vs-outside 1.07, heterogeneity 0.18; core [0.074, 0.876, 0.74, 0.53] rim [0.229, 0.598, 0.71, 0.71]
  - track 72 at frame 101: holes 0, rim-vs-core 0.39, rim-vs-outside 1.04, heterogeneity 0.19; core [0.074, 0.861, 0.727, 0.56] rim [0.248, 0.551, 0.688, 0.707]
  - track 94 at frame 114: holes 0, rim-vs-core 0.43, rim-vs-outside 1.00, heterogeneity 0.18; core [0.087, 0.866, 0.754, 0.637] rim [0.268, 0.49, 0.677, 0.719]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 201 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 13.5, rim/outside 0.919 (aggregate of 201 individuals; 0/201 membrane-like individually; rim level 0.48)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.907, rim/outside 13.9 (aggregate of 201 individuals; 1/201 membrane-like individually; rim level 0.795)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 9.87 (aggregate of 201 individuals; 4/201 membrane-like individually; rim level 0.774)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.08, rim/outside 9.17 (aggregate of 201 individuals; 187/201 membrane-like individually; rim level 0.841)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #58 (t=4150, R_eq 8.04): none; #66 (t=4300, R_eq 7.09): ['membrane (wall)']; #72 (t=5050, R_eq 7.38): ['membrane (wall)']; #94 (t=5700, R_eq 7.25): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 201 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
