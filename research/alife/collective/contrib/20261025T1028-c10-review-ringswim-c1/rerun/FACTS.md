# Evidence pack: ringswim-waste (seed 27)

- world: `../../20261025T0806-c07-ringswim-claim/world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 166s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py --out collective/contrib/20261025T1028-c10-review-ringswim-c1/rerun --seeds 27 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5534], min area 6 px

## Measurements
- components: final 6, mean 8.1, max 19; occupancy final 0.16
- tracks: 377; persistent (alive >= 50% of run): 0; longest 28 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 5.86, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 4, 6]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 9, 6], H1 [6, 6, 1]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0445/time; max body lengths 5.6
- replication (lineage window K = 20 frames = time 2000, default): splits 128, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 106, merge/split ratio 0.828, nucleations 7
- channel total drift (end/start - 1): [-0.3363, -0.8276, -0.2451, -0.6219]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 191 at frame 101: holes 1, rim-vs-core 0.17, rim-vs-outside 0.79, heterogeneity 0.21; core [0.078, 0.67, 0.486, 0.627] rim [0.183, 0.554, 0.508, 0.58]
  - track 34 at frame 13: holes 1, rim-vs-core 0.29, rim-vs-outside 0.77, heterogeneity 0.19; core [0.108, 0.708, 0.577, 0.642] rim [0.227, 0.465, 0.482, 0.597]
  - track 278 at frame 155: holes 1, rim-vs-core 0.21, rim-vs-outside 0.78, heterogeneity 0.21; core [0.114, 0.707, 0.596, 0.649] rim [0.225, 0.554, 0.537, 0.58]
  - track 27 at frame 13: holes 1, rim-vs-core 0.16, rim-vs-outside 0.76, heterogeneity 0.19; core [0.075, 0.622, 0.46, 0.701] rim [0.164, 0.545, 0.513, 0.612]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 45 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 7.77, rim/outside 0.784 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.539)
  - radial K catalyst: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.977, rim/outside 9.14 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.591)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 6.45 (aggregate of 45 individuals; 21/45 membrane-like individually; rim level 0.518)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 7.71 (aggregate of 45 individuals; 21/45 membrane-like individually; rim level 0.522)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #191 (t=10100, R_eq 13.75): none; #34 (t=1300, R_eq 8.63, ring): ['L link', 'membrane (wall)']; #278 (t=15500, R_eq 8.81, ring): ['L link', 'membrane (wall)']; #27 (t=1300, R_eq 10.54, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 45 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
