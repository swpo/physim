# Evidence pack: ringswim-waste (seed 3)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 101 frames x 100 steps x dt 1.0 = time 10000; grid [128, 128]; wall 43s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/rev6/a7 --seeds 3 --frames 100 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6111], min area 6 px

## Measurements
- components: final 0, mean 7.1, max 26; occupancy final 0.00
- tracks: 166; persistent (alive >= 50% of run): 0; longest 17 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.27, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 4, 3], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 64, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 8, merge/split ratio 0.125, nucleations 1
- channel total drift (end/start - 1): [-0.0162, -0.9999, -0.9917, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 8: holes 0, rim-vs-core 0.45, rim-vs-outside 0.88, heterogeneity 0.19; core [0.131, 0.798, 0.894, 0.916] rim [0.23, 0.537, 0.65, 0.653]
  - track 63 at frame 19: holes 0, rim-vs-core 0.69, rim-vs-outside 0.66, heterogeneity 0.21; core [0.102, 0.836, 0.825, 0.794] rim [0.319, 0.317, 0.474, 0.601]
  - track 99 at frame 39: holes 0, rim-vs-core 0.44, rim-vs-outside 0.77, heterogeneity 0.19; core [0.067, 0.787, 0.657, 0.898] rim [0.244, 0.479, 0.571, 0.646]
  - track 146 at frame 80: holes 0, rim-vs-core 0.35, rim-vs-outside 0.40, heterogeneity 0.11; core [0.305, 0.574, 0.954, 0.714] rim [0.35, 0.421, 0.81, 0.436]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [17, 33, 50, 67, 83]):
  - radial S: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.6, rim/outside 0.795 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.553)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 13.6 (aggregate of 32 individuals; 2/32 membrane-like individually; rim level 0.786)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.41, rim/outside 11.4 (aggregate of 32 individuals; 13/32 membrane-like individually; rim level 0.848)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.87, rim/outside 11 (aggregate of 32 individuals; 23/32 membrane-like individually; rim level 0.818)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #2 (t=800, R_eq 5.38): none; #63 (t=1900, R_eq 5.97): ['L link', 'membrane (wall)']; #99 (t=3900, R_eq 7.46): none; #146 (t=8000, R_eq 3.09): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 32 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
