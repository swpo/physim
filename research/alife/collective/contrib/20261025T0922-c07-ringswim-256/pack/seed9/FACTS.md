# Evidence pack: ringswim-waste (seed 9)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [256, 256]; wall 603s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py --out /tmp/claude-0/c07/big/s9 --seeds 9 --size 256 256 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5581], min area 6 px

## Measurements
- components: final 26, mean 38.3, max 74; occupancy final 0.18
- tracks: 1947; persistent (alive >= 50% of run): 0; longest 32 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 26.26, final 21; holes at thresholds 0.2/0.35/0.5 final [2, 28, 31]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 28, 27], H1 [33, 30, 12]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.048/time; max body lengths 5.5
- replication (lineage window K = 20 frames = time 2000, default): splits 650, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 570, merge/split ratio 0.877, nucleations 8
- channel total drift (end/start - 1): [-0.3052, -0.8286, -0.342, -0.5365]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 124 at frame 18: holes 0, rim-vs-core 0.26, rim-vs-outside 0.70, heterogeneity 0.17; core [0.089, 0.622, 0.436, 0.692] rim [0.241, 0.415, 0.497, 0.671]
  - track 128 at frame 15: holes 0, rim-vs-core 0.27, rim-vs-outside 0.77, heterogeneity 0.15; core [0.098, 0.681, 0.514, 0.765] rim [0.232, 0.458, 0.56, 0.696]
  - track 1079 at frame 113: holes 0, rim-vs-core 0.69, rim-vs-outside 0.54, heterogeneity 0.20; core [0.253, 0.798, 0.861, 0.859] rim [0.397, 0.325, 0.509, 0.538]
  - track 190 at frame 18: holes 0, rim-vs-core 0.49, rim-vs-outside 0.90, heterogeneity 0.21; core [0.1, 0.808, 0.601, 0.53] rim [0.308, 0.425, 0.569, 0.747]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 218 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 9.02, rim/outside 0.792 (aggregate of 218 individuals; 0/218 membrane-like individually; rim level 0.526)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 8.32 (aggregate of 218 individuals; 10/218 membrane-like individually; rim level 0.64)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 6.24 (aggregate of 218 individuals; 138/218 membrane-like individually; rim level 0.562)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.91, rim/outside 6.75 (aggregate of 218 individuals; 144/218 membrane-like individually; rim level 0.574)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #124 (t=1800, R_eq 8.81): ['L link', 'membrane (wall)']; #128 (t=1500, R_eq 6.63): ['L link', 'membrane (wall)']; #1079 (t=11300, R_eq 4.75): none; #190 (t=1800, R_eq 8.12): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 105 of 218 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
