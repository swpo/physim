# Evidence pack: ringswim-waste-mu0 (seed 0)

- world: `../world_mu0.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 43s; status ok
- command: `python -m labkit.run collective/contrib/_c07swim/world_mu0.py --out collective/contrib/_c07swim/pack_mu0 --seeds 0 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5371], min area 6 px

## Measurements
- components: final 18, mean 14.9, max 23; occupancy final 0.28
- tracks: 253; persistent (alive >= 50% of run): 0; longest 69 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 9.40, final 13; holes at thresholds 0.2/0.35/0.5 final [4, 13, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [17, 16, 8]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.00829/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 2000, default): splits 110, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 4, merges 3, merge/split ratio 0.027, nucleations 0
- channel total drift (end/start - 1): [-0.4384, -0.726, -0.0375, -0.2361]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 139 at frame 121: holes 0, rim-vs-core 0.53, rim-vs-outside 0.45, heterogeneity 0.15; core [0.294, 0.732, 0.948, 0.85] rim [0.375, 0.444, 0.759, 0.452]
  - track 119 at frame 101: holes 1, rim-vs-core 0.24, rim-vs-outside 0.83, heterogeneity 0.18; core [0.087, 0.649, 0.483, 0.819] rim [0.178, 0.549, 0.547, 0.628]
  - track 37 at frame 29: holes 1, rim-vs-core 0.17, rim-vs-outside 0.80, heterogeneity 0.18; core [0.095, 0.707, 0.575, 0.713] rim [0.156, 0.574, 0.542, 0.638]
  - track 202 at frame 168: holes 0, rim-vs-core 0.35, rim-vs-outside 0.99, heterogeneity 0.18; core [0.057, 0.691, 0.427, 0.583] rim [0.229, 0.536, 0.632, 0.745]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 89 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 14.6, rim/outside 0.815 (aggregate of 89 individuals; 0/89 membrane-like individually; rim level 0.499)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 8.8 (aggregate of 89 individuals; 5/89 membrane-like individually; rim level 0.729)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.77, rim/outside 6.54 (aggregate of 89 individuals; 79/89 membrane-like individually; rim level 0.66)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.8, rim/outside 6.66 (aggregate of 89 individuals; 77/89 membrane-like individually; rim level 0.674)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #139 (t=12100, R_eq 3.87): none; #119 (t=10100, R_eq 11.6): none; #37 (t=2900, R_eq 12.26, ring): ['L link', 'membrane (wall)']; #202 (t=16800, R_eq 10.17): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 56 of 89 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
