# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../../20261025T2209-c28-ringswim-sibmd-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 84s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2209-c28-ringswim-sibmd-claim/world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2347-c25-ringswim-local-drive/scan/k_s12_m15 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5567], min area 6 px

## Measurements
- components: final 4, mean 9.2, max 28; occupancy final 0.26
- tracks: 254; persistent (alive >= 50% of run): 0; longest 83 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.67, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 5, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 4, 4], H1 [5, 4, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.0472/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 1000, default): splits 97, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 28, merge/split ratio 0.289, nucleations 0
- channel total drift (end/start - 1): [-0.3941, -0.7644, -0.1346, -0.359]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 90 at frame 79: holes 1, rim-vs-core 0.29, rim-vs-outside 0.76, heterogeneity 0.19; core [0.108, 0.77, 0.57, 0.586] rim [0.168, 0.507, 0.495, 0.661]
  - track 116 at frame 101: holes 1, rim-vs-core 0.25, rim-vs-outside 0.85, heterogeneity 0.20; core [0.101, 0.735, 0.551, 0.557] rim [0.219, 0.53, 0.532, 0.628]
  - track 101 at frame 72: holes 1, rim-vs-core 0.24, rim-vs-outside 0.83, heterogeneity 0.18; core [0.048, 0.609, 0.389, 0.546] rim [0.18, 0.49, 0.506, 0.667]
  - track 113 at frame 76: holes 0, rim-vs-core 0.32, rim-vs-outside 0.96, heterogeneity 0.17; core [0.065, 0.6, 0.399, 0.656] rim [0.278, 0.48, 0.587, 0.754]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 55 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.08, rim/outside 0.865 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.53)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.992, rim/outside 6.37 (aggregate of 55 individuals; 1/55 membrane-like individually; rim level 0.616)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 4.82 (aggregate of 55 individuals; 34/55 membrane-like individually; rim level 0.581)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.34, rim/outside 6.13 (aggregate of 55 individuals; 27/55 membrane-like individually; rim level 0.646)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #90 (t=3950, R_eq 8.35, ring): ['L link', 'membrane (wall)']; #116 (t=5050, R_eq 9.87, ring): ['L link', 'membrane (wall)']; #101 (t=3600, R_eq 13.16): none; #113 (t=3800, R_eq 11.03): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 55 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
