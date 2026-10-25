# Evidence pack: ringswim-waste (seed 2)

- world: `../world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 149s; status ok
- command: `python -m labkit.run collective/contrib/_c07swim/world_claim.py --out collective/contrib/_c07swim/pack_s2 --seeds 2 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5581], min area 6 px

## Measurements
- components: final 9, mean 10.8, max 17; occupancy final 0.16
- tracks: 578; persistent (alive >= 50% of run): 0; longest 29 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 7.22, final 7; holes at thresholds 0.2/0.35/0.5 final [2, 7, 7]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 9, 9], H1 [8, 7, 5]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0237/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 2000, default): splits 205, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 168, merge/split ratio 0.82, nucleations 4
- channel total drift (end/start - 1): [-0.3166, -0.8308, -0.3233, -0.6065]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 452 at frame 146: holes 1, rim-vs-core 0.27, rim-vs-outside 0.60, heterogeneity 0.20; core [0.112, 0.631, 0.534, 0.737] rim [0.197, 0.476, 0.448, 0.547]
  - track 2 at frame 13: holes 1, rim-vs-core 0.25, rim-vs-outside 0.70, heterogeneity 0.20; core [0.119, 0.68, 0.594, 0.711] rim [0.204, 0.518, 0.499, 0.57]
  - track 502 at frame 171: holes 1, rim-vs-core 0.19, rim-vs-outside 0.77, heterogeneity 0.18; core [0.109, 0.708, 0.579, 0.61] rim [0.175, 0.538, 0.514, 0.623]
  - track 444 at frame 141: holes 1, rim-vs-core 0.17, rim-vs-outside 0.75, heterogeneity 0.16; core [0.095, 0.613, 0.499, 0.752] rim [0.16, 0.505, 0.481, 0.634]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 9.93, rim/outside 0.807 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.517)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 8.41 (aggregate of 67 individuals; 4/67 membrane-like individually; rim level 0.654)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 6.15 (aggregate of 67 individuals; 49/67 membrane-like individually; rim level 0.582)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.24, rim/outside 7.02 (aggregate of 67 individuals; 52/67 membrane-like individually; rim level 0.619)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #452 (t=14600, R_eq 9.97, ring): ['L link', 'membrane (wall)']; #2 (t=1300, R_eq 9.62, ring): ['L link', 'membrane (wall)']; #502 (t=17100, R_eq 11.75, ring): ['K catalyst', 'L link', 'membrane (wall)']; #444 (t=14100, R_eq 11.62, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 36 of 67 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
