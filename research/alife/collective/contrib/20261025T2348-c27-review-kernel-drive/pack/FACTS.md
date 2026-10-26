# Evidence pack: ringswim-dl2 (seed 9)

- world: `../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 247s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27n/world.py --out collective/contrib/wip-c27n/pack --seeds 9 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5618], min area 6 px

## Measurements
- components: final 81, mean 71.0, max 115; occupancy final 0.18
- tracks: 1017; persistent (alive >= 50% of run): 1; longest 103 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.72 (1 = constant size)
- enclosures: components with a hole mean 0.23, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [88, 83, 80], H1 [52, 7, 0]
- motion: 182 long-lived tracks moved >= 1 body length; max speed 0.0319/time; max body lengths 4.2
- replication (lineage window K = 20 frames = time 1000, default): splits 438, persistent splits 123 (0 more failed only because the siblings re-merged within K), max generation 7, merges 16, merge/split ratio 0.037, nucleations 0
- channel total drift (end/start - 1): [-0.3029, -0.8483, -0.1858, -0.4076]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 583 at frame 150: holes 0, rim-vs-core 0.41, rim-vs-outside 0.84, heterogeneity 0.16; core [0.096, 0.733, 0.653, 0.831] rim [0.342, 0.456, 0.641, 0.652]
  - track 674 at frame 160: holes 0, rim-vs-core 0.45, rim-vs-outside 0.84, heterogeneity 0.19; core [0.111, 0.82, 0.742, 0.823] rim [0.314, 0.459, 0.644, 0.673]
  - track 409 at frame 101: holes 0, rim-vs-core 0.78, rim-vs-outside 0.49, heterogeneity 0.21; core [0.263, 0.826, 0.942, 0.873] rim [0.428, 0.294, 0.543, 0.495]
  - track 855 at frame 182: holes 0, rim-vs-core 0.72, rim-vs-outside 0.63, heterogeneity 0.21; core [0.201, 0.857, 0.886, 0.85] rim [0.379, 0.324, 0.533, 0.562]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 427 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 9.03, rim/outside 0.831 (aggregate of 427 individuals; 0/427 membrane-like individually; rim level 0.551)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.921, rim/outside 12.9 (aggregate of 427 individuals; 4/427 membrane-like individually; rim level 0.716)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 8.96 (aggregate of 427 individuals; 187/427 membrane-like individually; rim level 0.79)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 13.3 (aggregate of 427 individuals; 168/427 membrane-like individually; rim level 0.85)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #583 (t=7500, R_eq 7.51): ['L link']; #674 (t=8000, R_eq 6.7): none; #409 (t=5050, R_eq 4.44): none; #855 (t=9100, R_eq 4.82): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 427 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
