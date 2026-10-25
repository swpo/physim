# Evidence pack: ringswim-waste-256 (seed 0)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c07-ringswim-256/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 60 steps x dt 1.0 = time 12000; grid [128, 128]; wall 67s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T0922-c07-ringswim-256/world.py --out /tmp/claude-0/c28sd/chi2 --seeds 0 --size 128 128 --spf 60 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5578], min area 6 px

## Measurements
- components: final 12, mean 10.4, max 24; occupancy final 0.22
- tracks: 334; persistent (alive >= 50% of run): 0; longest 49 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 6.86, final 9; holes at thresholds 0.2/0.35/0.5 final [1, 10, 10]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 12, 12], H1 [13, 11, 7]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.0546/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 1200, default): splits 112, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 81, merge/split ratio 0.723, nucleations 0
- channel total drift (end/start - 1): [-0.3605, -0.7916, -0.2014, -0.4359]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 78 at frame 39: holes 1, rim-vs-core 0.32, rim-vs-outside 0.70, heterogeneity 0.21; core [0.141, 0.752, 0.683, 0.645] rim [0.231, 0.517, 0.5, 0.57]
  - track 6 at frame 22: holes 1, rim-vs-core 0.29, rim-vs-outside 0.82, heterogeneity 0.21; core [0.138, 0.791, 0.687, 0.614] rim [0.228, 0.558, 0.544, 0.595]
  - track 41 at frame 24: holes 1, rim-vs-core 0.17, rim-vs-outside 0.82, heterogeneity 0.20; core [0.113, 0.71, 0.599, 0.638] rim [0.194, 0.571, 0.544, 0.602]
  - track 186 at frame 118: holes 1, rim-vs-core 0.19, rim-vs-outside 0.71, heterogeneity 0.16; core [0.096, 0.569, 0.474, 0.799] rim [0.149, 0.487, 0.458, 0.637]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 58 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 11, rim/outside 0.783 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.529)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 8.94 (aggregate of 58 individuals; 3/58 membrane-like individually; rim level 0.65)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 6.6 (aggregate of 58 individuals; 39/58 membrane-like individually; rim level 0.561)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.05, rim/outside 7.56 (aggregate of 58 individuals; 42/58 membrane-like individually; rim level 0.587)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #78 (t=2340, R_eq 9.8, ring): ['L link', 'membrane (wall)']; #6 (t=1320, R_eq 8.35, ring): ['L link', 'membrane (wall)']; #41 (t=1440, R_eq 10.05, ring): ['L link', 'membrane (wall)']; #186 (t=7080, R_eq 13.18, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 29 of 58 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
