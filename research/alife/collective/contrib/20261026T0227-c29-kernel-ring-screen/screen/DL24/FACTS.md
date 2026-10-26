# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 74s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/DL24 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5693], min area 6 px

## Measurements
- components: final 29, mean 18.3, max 33; occupancy final 0.24
- tracks: 298; persistent (alive >= 50% of run): 0; longest 73 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 31, 29], H1 [12, 0, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.0346/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 1000, default): splits 124, persistent splits 31 (0 more failed only because the siblings re-merged within K), max generation 8, merges 8, merge/split ratio 0.065, nucleations 0
- channel total drift (end/start - 1): [-0.4143, -0.7873, 0.1312, -0.233]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 168 at frame 138: holes 0, rim-vs-core 0.35, rim-vs-outside 0.91, heterogeneity 0.16; core [0.066, 0.557, 0.475, 0.872] rim [0.281, 0.52, 0.651, 0.669]
  - track 207 at frame 165: holes 0, rim-vs-core 0.46, rim-vs-outside 0.99, heterogeneity 0.19; core [0.111, 0.881, 0.725, 0.732] rim [0.333, 0.482, 0.678, 0.734]
  - track 211 at frame 166: holes 0, rim-vs-core 0.39, rim-vs-outside 0.94, heterogeneity 0.17; core [0.09, 0.8, 0.668, 0.764] rim [0.304, 0.475, 0.66, 0.721]
  - track 216 at frame 168: holes 0, rim-vs-core 0.43, rim-vs-outside 0.91, heterogeneity 0.18; core [0.095, 0.799, 0.662, 0.752] rim [0.336, 0.447, 0.631, 0.686]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 118 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 7.47, rim/outside 0.86 (aggregate of 118 individuals; 0/118 membrane-like individually; rim level 0.52)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.925, rim/outside 8.12 (aggregate of 118 individuals; 2/118 membrane-like individually; rim level 0.698)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 6.1 (aggregate of 118 individuals; 52/118 membrane-like individually; rim level 0.75)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 8.27 (aggregate of 118 individuals; 44/118 membrane-like individually; rim level 0.834)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #168 (t=6900, R_eq 11.03): ['L link']; #207 (t=8250, R_eq 6.33): ['L link', 'membrane (wall)']; #211 (t=8300, R_eq 6.96): ['L link', 'membrane (wall)']; #216 (t=8400, R_eq 7.48): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 118 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
