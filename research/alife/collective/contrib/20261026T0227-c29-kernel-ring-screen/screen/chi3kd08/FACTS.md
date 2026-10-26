# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 73s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/chi3kd08 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5693], min area 6 px

## Measurements
- components: final 32, mean 20.1, max 34; occupancy final 0.22
- tracks: 333; persistent (alive >= 50% of run): 0; longest 82 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 32, 32], H1 [19, 0, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.0338/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 1000, default): splits 142, persistent splits 31 (0 more failed only because the siblings re-merged within K), max generation 6, merges 7, merge/split ratio 0.049, nucleations 1
- channel total drift (end/start - 1): [-0.3559, -0.8222, -0.0731, -0.2856]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 173 at frame 131: holes 0, rim-vs-core 0.27, rim-vs-outside 0.85, heterogeneity 0.15; core [0.065, 0.608, 0.545, 0.939] rim [0.182, 0.546, 0.574, 0.707]
  - track 224 at frame 163: holes 0, rim-vs-core 0.52, rim-vs-outside 0.60, heterogeneity 0.17; core [0.134, 0.764, 0.719, 0.868] rim [0.293, 0.401, 0.544, 0.587]
  - track 157 at frame 114: holes 0, rim-vs-core 0.58, rim-vs-outside 0.50, heterogeneity 0.16; core [0.144, 0.718, 0.717, 0.888] rim [0.316, 0.372, 0.511, 0.504]
  - track 297 at frame 190: holes 0, rim-vs-core 0.40, rim-vs-outside 0.86, heterogeneity 0.16; core [0.094, 0.751, 0.669, 0.866] rim [0.286, 0.465, 0.606, 0.669]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 128 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 9.76, rim/outside 0.856 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.539)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 11 (aggregate of 128 individuals; 1/128 membrane-like individually; rim level 0.736)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 8.52 (aggregate of 128 individuals; 79/128 membrane-like individually; rim level 0.78)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 9.95 (aggregate of 128 individuals; 40/128 membrane-like individually; rim level 0.875)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #173 (t=6550, R_eq 8.21): none; #224 (t=8150, R_eq 6): ['L link']; #157 (t=5700, R_eq 5.97): none; #297 (t=9500, R_eq 6.53): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 128 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
