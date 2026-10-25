# Evidence pack: ringswim-dl2 (seed 7)

- world: `../../20261025T2209-c28-ringswim-sibmd-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 270s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2209-c28-ringswim-sibmd-claim/world.py --out collective/contrib/20261025T2232-c21-review-ringswim/pack --seeds 7 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5404], min area 6 px

## Measurements
- components: final 34, mean 38.8, max 118; occupancy final 0.21
- tracks: 1017; persistent (alive >= 50% of run): 0; longest 86 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 26.75, final 29; holes at thresholds 0.2/0.35/0.5 final [15, 34, 36]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 38, 34], H1 [40, 36, 27]
- motion: 72 long-lived tracks moved >= 1 body length; max speed 0.0589/time; max body lengths 4.2
- replication (lineage window K = 20 frames = time 1000, default): splits 318, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 248, merge/split ratio 0.78, nucleations 0
- channel total drift (end/start - 1): [-0.362, -0.7945, -0.2398, -0.3824]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 543 at frame 119: holes 1, rim-vs-core 0.20, rim-vs-outside 0.70, heterogeneity 0.18; core [0.103, 0.594, 0.508, 0.799] rim [0.153, 0.508, 0.466, 0.627]
  - track 287 at frame 54: holes 1, rim-vs-core 0.18, rim-vs-outside 0.83, heterogeneity 0.20; core [0.115, 0.73, 0.597, 0.63] rim [0.19, 0.578, 0.552, 0.614]
  - track 91 at frame 32: holes 1, rim-vs-core 0.17, rim-vs-outside 0.75, heterogeneity 0.16; core [0.082, 0.598, 0.459, 0.741] rim [0.158, 0.501, 0.486, 0.631]
  - track 705 at frame 141: holes 1, rim-vs-core 0.30, rim-vs-outside 0.65, heterogeneity 0.20; core [0.112, 0.692, 0.563, 0.7] rim [0.221, 0.466, 0.472, 0.562]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 214 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 9.55, rim/outside 0.772 (aggregate of 214 individuals; 0/214 membrane-like individually; rim level 0.491)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 6.85 (aggregate of 214 individuals; 19/214 membrane-like individually; rim level 0.62)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 5.08 (aggregate of 214 individuals; 160/214 membrane-like individually; rim level 0.528)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.17, rim/outside 5.81 (aggregate of 214 individuals; 162/214 membrane-like individually; rim level 0.571)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #543 (t=5950, R_eq 11.55, ring): ['L link', 'membrane (wall)']; #287 (t=2700, R_eq 10.56, ring): ['L link', 'membrane (wall)']; #91 (t=1600, R_eq 10.79, ring): ['L link', 'membrane (wall)']; #705 (t=7050, R_eq 9.34, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 138 of 214 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
