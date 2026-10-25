# Evidence pack: ringswim-dl2 (seed 24)

- world: `../../../20261025T2209-c28-ringswim-sibmd-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 395s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2209-c28-ringswim-sibmd-claim/world.py --out collective/contrib/20261025T2220-c24-review-ringswim-sibmd/pack/seed24 --seeds 24 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5399], min area 6 px

## Measurements
- components: final 30, mean 36.3, max 99; occupancy final 0.19
- tracks: 1002; persistent (alive >= 50% of run): 1; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.92 (1 = constant size)
- enclosures: components with a hole mean 25.38, final 26; holes at thresholds 0.2/0.35/0.5 final [12, 28, 28]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 30, 30], H1 [31, 27, 24]
- motion: 72 long-lived tracks moved >= 1 body length; max speed 0.0524/time; max body lengths 3.9
- replication (lineage window K = 20 frames = time 1000, default): splits 327, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 242, merge/split ratio 0.74, nucleations 0
- channel total drift (end/start - 1): [-0.3336, -0.8145, -0.3057, -0.442]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 150 at frame 61: holes 0, rim-vs-core 0.50, rim-vs-outside 0.92, heterogeneity 0.22; core [0.106, 0.803, 0.585, 0.527] rim [0.354, 0.417, 0.614, 0.733]
  - track 74 at frame 40: holes 1, rim-vs-core 0.18, rim-vs-outside 0.71, heterogeneity 0.16; core [0.089, 0.601, 0.475, 0.765] rim [0.15, 0.487, 0.459, 0.638]
  - track 353 at frame 76: holes 0, rim-vs-core 0.48, rim-vs-outside 0.86, heterogeneity 0.23; core [0.108, 0.798, 0.57, 0.55] rim [0.349, 0.406, 0.584, 0.699]
  - track 773 at frame 176: holes 1, rim-vs-core 0.21, rim-vs-outside 0.84, heterogeneity 0.19; core [0.093, 0.737, 0.53, 0.563] rim [0.186, 0.559, 0.544, 0.63]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 199 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 11.9, rim/outside 0.759 (aggregate of 199 individuals; 0/199 membrane-like individually; rim level 0.492)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 6.95 (aggregate of 199 individuals; 18/199 membrane-like individually; rim level 0.615)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.65, rim/outside 5.29 (aggregate of 199 individuals; 149/199 membrane-like individually; rim level 0.525)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.25, rim/outside 5.82 (aggregate of 199 individuals; 148/199 membrane-like individually; rim level 0.558)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #150 (t=3050, R_eq 8.2): ['L link', 'membrane (wall)']; #74 (t=2000, R_eq 11.98, ring): ['L link', 'membrane (wall)']; #353 (t=3800, R_eq 8.44): ['L link', 'membrane (wall)']; #773 (t=8800, R_eq 10.65, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 129 of 199 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
