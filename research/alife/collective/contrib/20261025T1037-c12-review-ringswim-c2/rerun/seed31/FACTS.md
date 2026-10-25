# Evidence pack: ringswim-waste (seed 31)

- world: `../../world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 185s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1037-c12-review-ringswim-c2/world_claim.py --out collective/contrib/20261025T1037-c12-review-ringswim-c2/rerun/seed31 --seeds 31 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5573], min area 6 px

## Measurements
- components: final 12, mean 11.2, max 22; occupancy final 0.19
- tracks: 608; persistent (alive >= 50% of run): 0; longest 29 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 7.31, final 8; holes at thresholds 0.2/0.35/0.5 final [1, 9, 10]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 12], H1 [11, 11, 6]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0326/time; max body lengths 5.2
- replication (lineage window K = 20 frames = time 2000, default): splits 208, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 170, merge/split ratio 0.817, nucleations 1
- channel total drift (end/start - 1): [-0.3251, -0.8064, -0.2642, -0.455]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 126 at frame 47: holes 0, rim-vs-core 0.29, rim-vs-outside 0.77, heterogeneity 0.17; core [0.079, 0.62, 0.453, 0.677] rim [0.25, 0.406, 0.536, 0.674]
  - track 277 at frame 99: holes 1, rim-vs-core 0.30, rim-vs-outside 0.73, heterogeneity 0.22; core [0.135, 0.763, 0.671, 0.621] rim [0.235, 0.528, 0.525, 0.575]
  - track 53 at frame 18: holes 0, rim-vs-core 0.62, rim-vs-outside 0.48, heterogeneity 0.20; core [0.204, 0.752, 0.715, 0.789] rim [0.38, 0.299, 0.438, 0.52]
  - track 195 at frame 67: holes 0, rim-vs-core 0.57, rim-vs-outside 0.95, heterogeneity 0.23; core [0.123, 0.878, 0.687, 0.499] rim [0.346, 0.435, 0.603, 0.756]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 56 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 6.95, rim/outside 0.8 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.52)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 6.95 (aggregate of 56 individuals; 2/56 membrane-like individually; rim level 0.612)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.4, rim/outside 5.47 (aggregate of 56 individuals; 33/56 membrane-like individually; rim level 0.539)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.86, rim/outside 6.24 (aggregate of 56 individuals; 36/56 membrane-like individually; rim level 0.555)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #126 (t=4700, R_eq 9.74): none; #277 (t=9900, R_eq 9.15, ring): ['L link', 'membrane (wall)']; #53 (t=1800, R_eq 5.86): ['L link', 'membrane (wall)']; #195 (t=6700, R_eq 6.7): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 27 of 56 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
