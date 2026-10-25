# Evidence pack: ringswim-waste-chi0 (seed 0)

- world: `../world_chi0.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 133s; status ok
- command: `python -m labkit.run collective/contrib/_c07swim/world_chi0.py --out collective/contrib/_c07swim/pack_chi0 --seeds 0 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5628], min area 6 px

## Measurements
- components: final 22, mean 19.0, max 24; occupancy final 0.23
- tracks: 264; persistent (alive >= 50% of run): 2; longest 116 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.90 (1 = constant size)
- enclosures: components with a hole mean 3.41, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 3, 18]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 22, 22], H1 [22, 21, 1]
- motion: 60 long-lived tracks moved >= 1 body length; max speed 0.0266/time; max body lengths 9.2
- replication (lineage window K = 20 frames = time 2000, default): splits 90, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 54, merge/split ratio 0.6, nucleations 0
- channel total drift (end/start - 1): [-0.3734, -0.7948, -0.1267, -0.3662]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 104 at frame 109: holes 0, rim-vs-core 0.67, rim-vs-outside 1.00, heterogeneity 0.25; core [0.123, 0.936, 0.933, 0.436] rim [0.357, 0.472, 0.643, 0.741]
  - track 81 at frame 94: holes 1, rim-vs-core 0.27, rim-vs-outside 0.83, heterogeneity 0.18; core [0.096, 0.729, 0.692, 0.656] rim [0.224, 0.504, 0.631, 0.589]
  - track 123 at frame 101: holes 0, rim-vs-core 0.44, rim-vs-outside 0.84, heterogeneity 0.20; core [0.111, 0.796, 0.769, 0.645] rim [0.31, 0.426, 0.629, 0.657]
  - track 208 at frame 175: holes 0, rim-vs-core 0.84, rim-vs-outside 0.60, heterogeneity 0.25; core [0.228, 0.889, 0.969, 0.655] rim [0.461, 0.27, 0.46, 0.579]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 114 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 17.3, rim/outside 0.835 (aggregate of 114 individuals; 0/114 membrane-like individually; rim level 0.545)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 12.2 (aggregate of 114 individuals; 0/114 membrane-like individually; rim level 0.722)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 9.6 (aggregate of 114 individuals; 0/114 membrane-like individually; rim level 0.748)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.67, rim/outside 11.1 (aggregate of 114 individuals; 106/114 membrane-like individually; rim level 0.794)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #104 (t=10900, R_eq 6.51): ['membrane (wall)']; #81 (t=9400, R_eq 8.1, ring): ['membrane (wall)']; #123 (t=10100, R_eq 6.48): ['membrane (wall)']; #208 (t=17500, R_eq 5.44): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 22 of 114 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
