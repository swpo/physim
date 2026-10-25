# Evidence pack: ringswim-waste-chi0 (seed 31)

- world: `../../world_chi0.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 175s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1037-c12-review-ringswim-c2/world_chi0.py --out collective/contrib/20261025T1037-c12-review-ringswim-c2/rerun_chi0/seed31 --seeds 31 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5572], min area 6 px

## Measurements
- components: final 23, mean 23.4, max 28; occupancy final 0.24
- tracks: 249; persistent (alive >= 50% of run): 7; longest 154 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.97 (1 = constant size)
- enclosures: components with a hole mean 1.96, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 3, 19]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 24, 23], H1 [24, 24, 2]
- motion: 53 long-lived tracks moved >= 1 body length; max speed 0.0147/time; max body lengths 4.6
- replication (lineage window K = 20 frames = time 2000, default): splits 85, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 54, merge/split ratio 0.635, nucleations 0
- channel total drift (end/start - 1): [-0.3862, -0.7836, -0.0739, -0.3011]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 70 at frame 104: holes 0, rim-vs-core 0.40, rim-vs-outside 0.95, heterogeneity 0.18; core [0.083, 0.775, 0.734, 0.58] rim [0.281, 0.461, 0.669, 0.724]
  - track 78 at frame 94: holes 0, rim-vs-core 0.28, rim-vs-outside 0.96, heterogeneity 0.16; core [0.127, 0.761, 0.761, 0.785] rim [0.234, 0.54, 0.708, 0.666]
  - track 57 at frame 72: holes 0, rim-vs-core 0.38, rim-vs-outside 0.90, heterogeneity 0.18; core [0.078, 0.751, 0.695, 0.577] rim [0.281, 0.457, 0.662, 0.712]
  - track 102 at frame 101: holes 0, rim-vs-core 0.39, rim-vs-outside 0.88, heterogeneity 0.17; core [0.079, 0.77, 0.73, 0.606] rim [0.262, 0.45, 0.65, 0.698]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 143 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 17.1, rim/outside 0.853 (aggregate of 143 individuals; 0/143 membrane-like individually; rim level 0.537)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.95, rim/outside 12.9 (aggregate of 143 individuals; 1/143 membrane-like individually; rim level 0.747)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 10.5 (aggregate of 143 individuals; 0/143 membrane-like individually; rim level 0.777)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.86, rim/outside 11.7 (aggregate of 143 individuals; 136/143 membrane-like individually; rim level 0.832)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #70 (t=10400, R_eq 6.96): ['membrane (wall)']; #78 (t=9400, R_eq 6.31): ['membrane (wall)']; #57 (t=7200, R_eq 7.44): ['membrane (wall)']; #102 (t=10100, R_eq 6.86): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 16 of 143 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
