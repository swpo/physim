# Evidence pack: ringswim-waste (seed 6)

- world: `../../20261025T0806-c07-ringswim-claim/world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 72s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py --out collective/contrib/20261025T1023-c06-review-c07-ringswim/rerun --seeds 6 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5547], min area 6 px

## Measurements
- components: final 6, mean 9.6, max 32; occupancy final 0.21
- tracks: 328; persistent (alive >= 50% of run): 0; longest 34 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 6.27, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 4, 8]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 7, 7], H1 [9, 8, 1]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.0498/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 1000, default): splits 109, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 84, merge/split ratio 0.771, nucleations 0
- channel total drift (end/start - 1): [-0.3229, -0.8099, -0.2873, -0.4105]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 290 at frame 165: holes 2, rim-vs-core 0.21, rim-vs-outside 0.87, heterogeneity 0.22; core [0.066, 0.703, 0.471, 0.498] rim [0.201, 0.571, 0.525, 0.585]
  - track 148 at frame 64: holes 1, rim-vs-core 0.28, rim-vs-outside 0.85, heterogeneity 0.21; core [0.055, 0.681, 0.428, 0.468] rim [0.202, 0.534, 0.523, 0.634]
  - track 305 at frame 183: holes 1, rim-vs-core 0.21, rim-vs-outside 0.77, heterogeneity 0.19; core [0.121, 0.723, 0.609, 0.632] rim [0.181, 0.551, 0.51, 0.609]
  - track 60 at frame 22: holes 1, rim-vs-core 0.38, rim-vs-outside 0.86, heterogeneity 0.22; core [0.116, 0.794, 0.626, 0.545] rim [0.273, 0.477, 0.51, 0.624]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 6.28, rim/outside 0.806 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.526)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 7.9 (aggregate of 48 individuals; 2/48 membrane-like individually; rim level 0.623)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 6 (aggregate of 48 individuals; 31/48 membrane-like individually; rim level 0.54)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.88, rim/outside 6.26 (aggregate of 48 individuals; 35/48 membrane-like individually; rim level 0.565)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #290 (t=8250, R_eq 13.48): none; #148 (t=3200, R_eq 13.97): none; #305 (t=9150, R_eq 10.85, ring): ['K catalyst', 'L link', 'membrane (wall)']; #60 (t=1100, R_eq 8, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 23 of 48 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
