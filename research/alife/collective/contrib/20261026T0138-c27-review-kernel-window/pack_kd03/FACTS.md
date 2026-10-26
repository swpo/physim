# Evidence pack: ringswim-dl2 (seed 9)

- world: `../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 252s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27u/world.py --out collective/contrib/wip-c27u/pack_kd03 --seeds 9 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5699], min area 6 px

## Measurements
- components: final 80, mean 70.8, max 113; occupancy final 0.22
- tracks: 1220; persistent (alive >= 50% of run): 0; longest 80 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.28, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [83, 82, 80], H1 [64, 7, 0]
- motion: 164 long-lived tracks moved >= 1 body length; max speed 0.0337/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 1000, default): splits 523, persistent splits 109 (1 more failed only because the siblings re-merged within K), max generation 7, merges 34, merge/split ratio 0.065, nucleations 2
- channel total drift (end/start - 1): [-0.3159, -0.8154, -0.1493, -0.2974]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 554 at frame 121: holes 0, rim-vs-core 0.30, rim-vs-outside 0.86, heterogeneity 0.16; core [0.087, 0.671, 0.554, 0.894] rim [0.243, 0.518, 0.61, 0.694]
  - track 270 at frame 64: holes 0, rim-vs-core 0.45, rim-vs-outside 0.85, heterogeneity 0.20; core [0.102, 0.798, 0.655, 0.762] rim [0.353, 0.433, 0.608, 0.674]
  - track 574 at frame 119: holes 0, rim-vs-core 0.48, rim-vs-outside 0.71, heterogeneity 0.17; core [0.142, 0.729, 0.717, 0.932] rim [0.309, 0.453, 0.626, 0.585]
  - track 959 at frame 170: holes 0, rim-vs-core 0.39, rim-vs-outside 0.91, heterogeneity 0.18; core [0.089, 0.791, 0.643, 0.747] rim [0.308, 0.471, 0.645, 0.712]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 443 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.96, rim/outside 0.865 (aggregate of 443 individuals; 0/443 membrane-like individually; rim level 0.52)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.949, rim/outside 6.62 (aggregate of 443 individuals; 20/443 membrane-like individually; rim level 0.687)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 5.31 (aggregate of 443 individuals; 200/443 membrane-like individually; rim level 0.723)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 6.7 (aggregate of 443 individuals; 158/443 membrane-like individually; rim level 0.803)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #554 (t=6050, R_eq 10.73): ['K catalyst', 'L link', 'membrane (wall)']; #270 (t=3200, R_eq 9.03): none; #574 (t=5950, R_eq 7.02): none; #959 (t=8500, R_eq 7.29): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 22 of 443 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
