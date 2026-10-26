# Evidence pack: ringswim-dl2 (seed 5)

- world: `../../20261025T2209-c28-ringswim-sibmd-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 303s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2209-c28-ringswim-sibmd-claim/world.py --out collective/contrib/20261025T2315-c25-review-ringswim/pack --seeds 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5402], min area 6 px

## Measurements
- components: final 30, mean 38.1, max 100; occupancy final 0.20
- tracks: 1043; persistent (alive >= 50% of run): 0; longest 63 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 26.52, final 24; holes at thresholds 0.2/0.35/0.5 final [11, 31, 31]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 33, 30], H1 [36, 33, 23]
- motion: 76 long-lived tracks moved >= 1 body length; max speed 0.052/time; max body lengths 4.0
- replication (lineage window K = 20 frames = time 1000, default): splits 339, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 263, merge/split ratio 0.776, nucleations 1
- channel total drift (end/start - 1): [-0.3464, -0.8044, -0.272, -0.4396]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 598 at frame 119: holes 0, rim-vs-core 0.42, rim-vs-outside 0.84, heterogeneity 0.20; core [0.106, 0.783, 0.581, 0.635] rim [0.308, 0.42, 0.587, 0.696]
  - track 96 at frame 32: holes 1, rim-vs-core 0.16, rim-vs-outside 0.81, heterogeneity 0.20; core [0.103, 0.683, 0.552, 0.67] rim [0.192, 0.57, 0.547, 0.609]
  - track 464 at frame 92: holes 1, rim-vs-core 0.19, rim-vs-outside 0.69, heterogeneity 0.17; core [0.092, 0.584, 0.472, 0.777] rim [0.158, 0.497, 0.462, 0.622]
  - track 799 at frame 165: holes 1, rim-vs-core 0.20, rim-vs-outside 0.76, heterogeneity 0.20; core [0.105, 0.616, 0.546, 0.769] rim [0.188, 0.559, 0.533, 0.6]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 210 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 9.52, rim/outside 0.772 (aggregate of 210 individuals; 0/210 membrane-like individually; rim level 0.496)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 6.86 (aggregate of 210 individuals; 24/210 membrane-like individually; rim level 0.614)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.54, rim/outside 5.09 (aggregate of 210 individuals; 158/210 membrane-like individually; rim level 0.509)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.12, rim/outside 5.65 (aggregate of 210 individuals; 161/210 membrane-like individually; rim level 0.552)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #598 (t=5950, R_eq 7.65): ['L link', 'membrane (wall)']; #96 (t=1600, R_eq 10.81, ring): ['K catalyst', 'L link', 'membrane (wall)']; #464 (t=4600, R_eq 12.15, ring): ['L link', 'membrane (wall)']; #799 (t=8250, R_eq 12.67, ring): ['K catalyst', 'L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 123 of 210 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
