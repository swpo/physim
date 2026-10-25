# Evidence pack: ringswim-waste (seed 10)

- world: `../../world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 104s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1245-c13-review-ringswim/world_claim.py --out collective/contrib/20261025T1245-c13-review-ringswim/rerun --seeds 9 10 --spf 100 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5571], min area 6 px

## Measurements
- components: final 5, mean 10.9, max 19; occupancy final 0.16
- tracks: 597; persistent (alive >= 50% of run): 0; longest 21 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 7.25, final 4; holes at thresholds 0.2/0.35/0.5 final [2, 5, 6]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 5, 5], H1 [7, 6, 4]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0408/time; max body lengths 4.0
- replication (lineage window K = 20 frames = time 2000, default): splits 205, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 178, merge/split ratio 0.868, nucleations 1
- channel total drift (end/start - 1): [-0.2911, -0.8381, -0.4023, -0.4658]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 415 at frame 138: holes 1, rim-vs-core 0.20, rim-vs-outside 0.84, heterogeneity 0.24; core [0.096, 0.749, 0.575, 0.554] rim [0.219, 0.588, 0.565, 0.57]
  - track 293 at frame 101: holes 1, rim-vs-core 0.40, rim-vs-outside 0.73, heterogeneity 0.24; core [0.145, 0.807, 0.712, 0.577] rim [0.283, 0.494, 0.506, 0.558]
  - track 302 at frame 103: holes 0, rim-vs-core 0.36, rim-vs-outside 0.80, heterogeneity 0.19; core [0.092, 0.715, 0.534, 0.621] rim [0.274, 0.411, 0.537, 0.693]
  - track 3 at frame 10: holes 1, rim-vs-core 0.16, rim-vs-outside 0.82, heterogeneity 0.17; core [0.084, 0.656, 0.492, 0.645] rim [0.163, 0.513, 0.495, 0.643]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 58 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 9.5, rim/outside 0.806 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.533)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 8.41 (aggregate of 58 individuals; 1/58 membrane-like individually; rim level 0.658)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 6.39 (aggregate of 58 individuals; 36/58 membrane-like individually; rim level 0.586)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.3, rim/outside 6.91 (aggregate of 58 individuals; 43/58 membrane-like individually; rim level 0.608)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #415 (t=13800, R_eq 11.18): ['L link']; #293 (t=10100, R_eq 8.78, ring): ['L link', 'membrane (wall)']; #302 (t=10300, R_eq 8.25): ['L link', 'membrane (wall)']; #3 (t=1000, R_eq 10.16, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 30 of 58 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
