# Evidence pack: ringswim-dl2 (seed 0)

- world: `../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 78s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/pack_mu0 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5118], min area 6 px

## Measurements
- components: final 14, mean 14.5, max 103; occupancy final 0.13
- tracks: 435; persistent (alive >= 50% of run): 0; longest 87 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 6.12, final 8; holes at thresholds 0.2/0.35/0.5 final [6, 8, 11]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 15, 14], H1 [14, 11, 6]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0184/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 1000, default): splits 133, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 56, merge/split ratio 0.421, nucleations 0
- channel total drift (end/start - 1): [-0.2925, -0.8704, -0.4759, -0.5893]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 337 at frame 146: holes 0, rim-vs-core 0.39, rim-vs-outside 0.92, heterogeneity 0.19; core [0.095, 0.835, 0.557, 0.761] rim [0.273, 0.493, 0.568, 0.729]
  - track 77 at frame 35: holes 0, rim-vs-core 0.41, rim-vs-outside 0.90, heterogeneity 0.19; core [0.102, 0.833, 0.571, 0.761] rim [0.29, 0.476, 0.561, 0.713]
  - track 319 at frame 126: holes 1, rim-vs-core 0.18, rim-vs-outside 0.71, heterogeneity 0.18; core [0.049, 0.561, 0.308, 0.772] rim [0.137, 0.498, 0.396, 0.66]
  - track 401 at frame 182: holes 0, rim-vs-core 0.88, rim-vs-outside 0.53, heterogeneity 0.23; core [0.241, 0.917, 0.819, 0.825] rim [0.434, 0.241, 0.366, 0.555]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 86 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 6.2, rim/outside 0.782 (aggregate of 86 individuals; 1/86 membrane-like individually; rim level 0.448)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 4.5 (aggregate of 86 individuals; 26/86 membrane-like individually; rim level 0.615)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.7, rim/outside 3.8 (aggregate of 86 individuals; 61/86 membrane-like individually; rim level 0.473)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 3.6 (aggregate of 86 individuals; 48/86 membrane-like individually; rim level 0.533)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #337 (t=7300, R_eq 6.91): ['L link', 'membrane (wall)']; #77 (t=1750, R_eq 7.07): ['L link']; #319 (t=6300, R_eq 17, ring): ['L link', 'membrane (wall)']; #401 (t=9100, R_eq 4.98): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 43 of 86 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
