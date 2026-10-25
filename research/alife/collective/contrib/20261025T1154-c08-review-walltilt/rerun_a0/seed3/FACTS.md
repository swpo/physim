# Evidence pack: ringswim-waste (seed 3)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 101 frames x 100 steps x dt 1.0 = time 10000; grid [128, 128]; wall 18s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/rev6/a0 --seeds 3 --frames 100 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5331], min area 6 px

## Measurements
- components: final 17, mean 14.8, max 20; occupancy final 0.29
- tracks: 142; persistent (alive >= 50% of run): 2; longest 54 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.43 (1 = constant size)
- enclosures: components with a hole mean 9.15, final 12; holes at thresholds 0.2/0.35/0.5 final [2, 12, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 17, 17], H1 [17, 16, 10]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0108/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 58, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 3, merge/split ratio 0.052, nucleations 1
- channel total drift (end/start - 1): [-0.4507, -0.7222, 0.009, -0.1946]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 79 at frame 67: holes 1, rim-vs-core 0.23, rim-vs-outside 0.84, heterogeneity 0.20; core [0.11, 0.791, 0.657, 0.641] rim [0.176, 0.601, 0.559, 0.612]
  - track 53 at frame 48: holes 0, rim-vs-core 0.34, rim-vs-outside 0.83, heterogeneity 0.18; core [0.084, 0.698, 0.517, 0.666] rim [0.284, 0.436, 0.588, 0.666]
  - track 34 at frame 26: holes 1, rim-vs-core 0.19, rim-vs-outside 0.84, heterogeneity 0.19; core [0.095, 0.753, 0.586, 0.625] rim [0.174, 0.578, 0.55, 0.626]
  - track 95 at frame 76: holes 1, rim-vs-core 0.20, rim-vs-outside 0.84, heterogeneity 0.19; core [0.101, 0.769, 0.61, 0.62] rim [0.17, 0.594, 0.558, 0.627]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 89 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 14.4, rim/outside 0.798 (aggregate of 89 individuals; 0/89 membrane-like individually; rim level 0.494)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 7.98 (aggregate of 89 individuals; 6/89 membrane-like individually; rim level 0.7)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.75, rim/outside 6.01 (aggregate of 89 individuals; 75/89 membrane-like individually; rim level 0.609)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.65, rim/outside 5.84 (aggregate of 89 individuals; 74/89 membrane-like individually; rim level 0.64)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #79 (t=6700, R_eq 10.7, ring): ['L link', 'membrane (wall)']; #53 (t=4800, R_eq 9.66): ['L link', 'membrane (wall)']; #34 (t=2600, R_eq 11.01, ring): ['L link', 'membrane (wall)']; #95 (t=7600, R_eq 10.95, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 61 of 89 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
