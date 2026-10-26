# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 76s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/base --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5713], min area 6 px

## Measurements
- components: final 28, mean 18.1, max 32; occupancy final 0.26
- tracks: 337; persistent (alive >= 50% of run): 0; longest 80 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 28, 28], H1 [22, 5, 0]
- motion: 37 long-lived tracks moved >= 1 body length; max speed 0.0363/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 1000, default): splits 142, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 8, merges 8, merge/split ratio 0.056, nucleations 0
- channel total drift (end/start - 1): [-0.3835, -0.7817, 0.0185, -0.1777]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 221 at frame 161: holes 0, rim-vs-core 0.43, rim-vs-outside 0.76, heterogeneity 0.18; core [0.142, 0.792, 0.746, 0.834] rim [0.317, 0.467, 0.672, 0.624]
  - track 181 at frame 136: holes 0, rim-vs-core 0.72, rim-vs-outside 0.64, heterogeneity 0.20; core [0.303, 0.865, 0.979, 0.908] rim [0.436, 0.343, 0.629, 0.586]
  - track 234 at frame 155: holes 0, rim-vs-core 0.46, rim-vs-outside 0.90, heterogeneity 0.19; core [0.101, 0.835, 0.688, 0.722] rim [0.335, 0.442, 0.636, 0.698]
  - track 247 at frame 158: holes 0, rim-vs-core 0.28, rim-vs-outside 1.01, heterogeneity 0.17; core [0.089, 0.804, 0.628, 0.719] rim [0.218, 0.56, 0.632, 0.747]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 119 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.47, rim/outside 0.863 (aggregate of 119 individuals; 0/119 membrane-like individually; rim level 0.522)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 8.1 (aggregate of 119 individuals; 2/119 membrane-like individually; rim level 0.705)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 6.17 (aggregate of 119 individuals; 49/119 membrane-like individually; rim level 0.756)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 7.86 (aggregate of 119 individuals; 44/119 membrane-like individually; rim level 0.832)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #221 (t=8050, R_eq 7.63): none; #181 (t=6800, R_eq 3.7): none; #234 (t=7750, R_eq 7.16): ['L link', 'membrane (wall)']; #247 (t=7900, R_eq 7.31): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 119 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
