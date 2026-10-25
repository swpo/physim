# Evidence pack: ringswim-waste (seed 25)

- world: `../../../20261025T0806-c07-ringswim-claim/world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 156s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py --out collective/contrib/20261025T1010-c10-review-ringswim/rerun --seeds 25 26 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5525], min area 6 px

## Measurements
- components: final 2, mean 5.9, max 20; occupancy final 0.13
- tracks: 280; persistent (alive >= 50% of run): 0; longest 36 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 4.33, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [1, 1, 1]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0751/time; max body lengths 6.4
- replication (lineage window K = 20 frames = time 2000, default): splits 91, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 82, merge/split ratio 0.901, nucleations 1
- channel total drift (end/start - 1): [-0.2636, -0.8488, -0.4597, -0.6707]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 34 at frame 17: holes 1, rim-vs-core 0.20, rim-vs-outside 0.81, heterogeneity 0.20; core [0.124, 0.731, 0.616, 0.6] rim [0.192, 0.564, 0.524, 0.601]
  - track 155 at frame 86: holes 0, rim-vs-core 0.48, rim-vs-outside 1.03, heterogeneity 0.20; core [0.035, 0.674, 0.368, 0.33] rim [0.211, 0.538, 0.549, 0.713]
  - track 114 at frame 54: holes 1, rim-vs-core 0.17, rim-vs-outside 0.72, heterogeneity 0.22; core [0.093, 0.653, 0.491, 0.678] rim [0.19, 0.539, 0.49, 0.596]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 27 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 3.37, rim/outside 0.805 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.55)
  - radial K catalyst: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 5.76 (aggregate of 27 individuals; 2/27 membrane-like individually; rim level 0.488)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 4.41 (aggregate of 27 individuals; 15/27 membrane-like individually; rim level 0.417)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 4.59 (aggregate of 27 individuals; 12/27 membrane-like individually; rim level 0.412)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #278 (t=18300, R_eq 26.39, ring): none; #34 (t=1700, R_eq 10.49, ring): ['L link', 'membrane (wall)']; #155 (t=8600, R_eq 15.57, ring): ['K catalyst']; #114 (t=5400, R_eq 11.78, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 14 of 27 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
