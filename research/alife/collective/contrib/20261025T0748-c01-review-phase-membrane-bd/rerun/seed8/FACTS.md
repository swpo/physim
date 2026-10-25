# Evidence pack: phase-membrane (seed 8)

- world: `../../../../../threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 10s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out collective/contrib/20261025T0748-c01-review-phase-membrane-bd/rerun --seeds 7 8 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5423], min area 6 px

## Measurements
- components: final 21, mean 16.1, max 24; occupancy final 0.24
- tracks: 156; persistent (alive >= 50% of run): 4; longest 149 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.97 (1 = constant size)
- enclosures: components with a hole mean 9.70, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 3, 8]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 21, 21], H1 [15, 10, 3]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0109/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 63, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 3, merges 6, merge/split ratio 0.095, nucleations 0
- channel total drift (end/start - 1): [-0.4561, -0.7756, -0.005, -0.256]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 42 at frame 77: holes 1, rim-vs-core 0.19, rim-vs-outside 0.78, heterogeneity 0.19; core [0.099, 0.783, 0.56, 0.615] rim [0.162, 0.614, 0.511, 0.601]
  - track 28 at frame 59: holes 1, rim-vs-core 0.16, rim-vs-outside 0.80, heterogeneity 0.20; core [0.102, 0.747, 0.564, 0.677] rim [0.168, 0.63, 0.525, 0.598]
  - track 77 at frame 108: holes 0, rim-vs-core 0.60, rim-vs-outside 1.04, heterogeneity 0.23; core [0.123, 0.967, 0.684, 0.48] rim [0.339, 0.505, 0.652, 0.789]
  - track 130 at frame 145: holes 1, rim-vs-core 0.38, rim-vs-outside 0.83, heterogeneity 0.23; core [0.115, 0.898, 0.661, 0.523] rim [0.243, 0.57, 0.53, 0.599]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 105 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 8.09, rim/outside 0.842 (aggregate of 105 individuals; 0/105 membrane-like individually; rim level 0.474)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.984, rim/outside 6.66 (aggregate of 105 individuals; 0/105 membrane-like individually; rim level 0.719)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.58, rim/outside 5.03 (aggregate of 105 individuals; 78/105 membrane-like individually; rim level 0.612)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.93, rim/outside 5.44 (aggregate of 105 individuals; 74/105 membrane-like individually; rim level 0.648)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #42 (t=3850, R_eq 12.53, ring): ['L link', 'membrane (wall)']; #28 (t=2950, R_eq 11.66, ring): ['L link', 'membrane (wall)']; #77 (t=5400, R_eq 6.6): ['L link', 'membrane (wall)']; #130 (t=7250, R_eq 8.52, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 42 of 105 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
