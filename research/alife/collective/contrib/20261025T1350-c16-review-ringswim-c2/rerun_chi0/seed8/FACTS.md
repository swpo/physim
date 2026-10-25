# Evidence pack: ringswim-waste-chi0 (seed 8)

- world: `../../../20261025T0806-c07-ringswim-claim/world_chi0.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 144s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_chi0.py --out collective/contrib/20261025T1350-c16-review-ringswim-c2/rerun_chi0/seed8 --seeds 8 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5606], min area 6 px

## Measurements
- components: final 19, mean 20.5, max 25; occupancy final 0.21
- tracks: 288; persistent (alive >= 50% of run): 2; longest 144 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.18 (1 = constant size)
- enclosures: components with a hole mean 2.63, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 19], H1 [19, 18, 0]
- motion: 57 long-lived tracks moved >= 1 body length; max speed 0.0196/time; max body lengths 6.2
- replication (lineage window K = 20 frames = time 2000, default): splits 97, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 4, merges 67, merge/split ratio 0.691, nucleations 3
- channel total drift (end/start - 1): [-0.343, -0.8051, -0.1754, -0.4164]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 104 at frame 129: holes 1, rim-vs-core 0.31, rim-vs-outside 0.90, heterogeneity 0.19; core [0.102, 0.779, 0.749, 0.609] rim [0.236, 0.52, 0.638, 0.598]
  - track 133 at frame 136: holes 0, rim-vs-core 0.47, rim-vs-outside 0.95, heterogeneity 0.19; core [0.094, 0.823, 0.803, 0.574] rim [0.288, 0.455, 0.653, 0.732]
  - track 65 at frame 74: holes 0, rim-vs-core 0.70, rim-vs-outside 0.57, heterogeneity 0.21; core [0.189, 0.794, 0.879, 0.723] rim [0.396, 0.267, 0.52, 0.535]
  - track 251 at frame 183: holes 0, rim-vs-core 0.27, rim-vs-outside 0.93, heterogeneity 0.18; core [0.097, 0.751, 0.718, 0.644] rim [0.211, 0.525, 0.641, 0.623]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 120 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 12.7, rim/outside 0.843 (aggregate of 120 individuals; 0/120 membrane-like individually; rim level 0.545)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 11.3 (aggregate of 120 individuals; 1/120 membrane-like individually; rim level 0.737)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 9.19 (aggregate of 120 individuals; 1/120 membrane-like individually; rim level 0.772)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.48, rim/outside 11 (aggregate of 120 individuals; 107/120 membrane-like individually; rim level 0.805)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #104 (t=12900, R_eq 7.82, ring): ['membrane (wall)']; #133 (t=13600, R_eq 6.33): ['membrane (wall)']; #65 (t=7400, R_eq 5.84): ['membrane (wall)']; #251 (t=18300, R_eq 7.63): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 120 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
