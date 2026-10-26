# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 80s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/chi5kd08 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5771], min area 6 px

## Measurements
- components: final 69, mean 46.2, max 69; occupancy final 0.38
- tracks: 257; persistent (alive >= 50% of run): 21; longest 179 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.44 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [69, 69, 69], H1 [5, 0, 0]
- motion: 26 long-lived tracks moved >= 1 body length; max speed 0.0334/time; max body lengths 4.7
- replication (lineage window K = 20 frames = time 1000, default): splits 105, persistent splits 64 (0 more failed only because the siblings re-merged within K), max generation 6, merges 8, merge/split ratio 0.076, nucleations 0
- channel total drift (end/start - 1): [-0.5599, -0.7026, 0.4111, 0.3079]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 72 at frame 111: holes 0, rim-vs-core 0.24, rim-vs-outside 1.00, heterogeneity 0.17; core [0.093, 0.768, 0.62, 0.842] rim [0.204, 0.586, 0.564, 0.75]
  - track 126 at frame 129: holes 0, rim-vs-core 0.66, rim-vs-outside 0.63, heterogeneity 0.19; core [0.16, 0.857, 0.751, 0.844] rim [0.329, 0.348, 0.446, 0.615]
  - track 129 at frame 129: holes 0, rim-vs-core 0.29, rim-vs-outside 0.93, heterogeneity 0.15; core [0.067, 0.747, 0.572, 0.849] rim [0.218, 0.522, 0.583, 0.75]
  - track 194 at frame 150: holes 0, rim-vs-core 0.64, rim-vs-outside 0.55, heterogeneity 0.18; core [0.136, 0.774, 0.699, 0.863] rim [0.298, 0.337, 0.398, 0.542]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 307 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 6.06, rim/outside 0.944 (aggregate of 307 individuals; 0/307 membrane-like individually; rim level 0.405)
  - radial K catalyst: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.893, rim/outside 8.7 (aggregate of 307 individuals; 1/307 membrane-like individually; rim level 0.724)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.66, rim/outside 8.02 (aggregate of 307 individuals; 238/307 membrane-like individually; rim level 0.801)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 7 (aggregate of 307 individuals; 4/307 membrane-like individually; rim level 0.915)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #72 (t=5550, R_eq 6.79): ['L link']; #126 (t=6450, R_eq 5.32): ['L link']; #129 (t=6450, R_eq 6.58): ['L link']; #194 (t=7500, R_eq 5.81): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 307 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
