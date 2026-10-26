# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 75s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/chi3DL24 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5875], min area 6 px

## Measurements
- components: final 36, mean 27.9, max 44; occupancy final 0.23
- tracks: 351; persistent (alive >= 50% of run): 1; longest 103 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 30.70 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 36, 36], H1 [11, 0, 0]
- motion: 47 long-lived tracks moved >= 1 body length; max speed 0.031/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 1000, default): splits 153, persistent splits 43 (0 more failed only because the siblings re-merged within K), max generation 5, merges 7, merge/split ratio 0.046, nucleations 0
- channel total drift (end/start - 1): [-0.436, -0.7915, 0.1468, -0.2367]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 184 at frame 129: holes 0, rim-vs-core 0.42, rim-vs-outside 0.62, heterogeneity 0.14; core [0.101, 0.641, 0.587, 0.93] rim [0.223, 0.464, 0.545, 0.573]
  - track 172 at frame 111: holes 0, rim-vs-core 0.29, rim-vs-outside 0.96, heterogeneity 0.16; core [0.11, 0.76, 0.658, 0.85] rim [0.22, 0.542, 0.578, 0.719]
  - track 183 at frame 119: holes 0, rim-vs-core 0.36, rim-vs-outside 0.85, heterogeneity 0.15; core [0.104, 0.735, 0.625, 0.841] rim [0.285, 0.465, 0.597, 0.689]
  - track 267 at frame 171: holes 0, rim-vs-core 0.69, rim-vs-outside 0.53, heterogeneity 0.20; core [0.219, 0.802, 0.818, 0.856] rim [0.398, 0.312, 0.488, 0.538]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 188 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.13, rim/outside 0.893 (aggregate of 188 individuals; 0/188 membrane-like individually; rim level 0.481)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 7.3 (aggregate of 188 individuals; 3/188 membrane-like individually; rim level 0.684)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 5.76 (aggregate of 188 individuals; 89/188 membrane-like individually; rim level 0.755)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 7.6 (aggregate of 188 individuals; 33/188 membrane-like individually; rim level 0.844)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #184 (t=6450, R_eq 6.91): none; #172 (t=5550, R_eq 6.84): ['L link']; #183 (t=5950, R_eq 6.75): ['L link']; #267 (t=8550, R_eq 5.17): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 188 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
