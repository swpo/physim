# Evidence pack: phase-membrane-bd-twin (seed 7)

- world: `../twin_pm.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0748-c01-review-phase-membrane-bd/twin_pm.py --out collective/contrib/20261025T0748-c01-review-phase-membrane-bd/twin_lam0001 --seeds 7 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9171], min area 6 px

## Measurements
- components: final 53, mean 40.3, max 53; occupancy final 0.33
- tracks: 123; persistent (alive >= 50% of run): 39; longest 161 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 16.00 (1 = constant size)
- enclosures: components with a hole mean 8.35, final 6; holes at thresholds 0.2/0.35/0.5 final [0, 6, 21]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [95, 54, 53], H1 [31, 10, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 1000, default): splits 45, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 2, merges 6, merge/split ratio 0.133, nucleations 0
- channel total drift (end/start - 1): [-0.5552, -0.6576, 0.2689, 0.2188]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 81: holes 0, rim-vs-core 0.87, rim-vs-outside 0.51, heterogeneity 0.24; core [0.094, 0.783, 0.583, 0.514] rim [0.268, 0.11, 0.119, 0.749]
  - track 29 at frame 81: holes 1, rim-vs-core 0.38, rim-vs-outside 0.74, heterogeneity 0.24; core [0.074, 0.797, 0.554, 0.425] rim [0.154, 0.521, 0.4, 0.625]
  - track 30 at frame 81: holes 1, rim-vs-core 0.65, rim-vs-outside 0.44, heterogeneity 0.23; core [0.098, 0.778, 0.584, 0.575] rim [0.198, 0.266, 0.201, 0.627]
  - track 89 at frame 97: holes 0, rim-vs-core 0.71, rim-vs-outside 0.59, heterogeneity 0.24; core [0.097, 0.793, 0.592, 0.547] rim [0.247, 0.236, 0.24, 0.771]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 257 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.44, rim/outside 0.843 (aggregate of 257 individuals; 0/257 membrane-like individually; rim level 0.392)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 12.5 (aggregate of 257 individuals; 55/257 membrane-like individually; rim level 0.658)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.52, rim/outside 10.9 (aggregate of 257 individuals; 155/257 membrane-like individually; rim level 0.517)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.01, rim/outside 5.55 (aggregate of 257 individuals; 194/257 membrane-like individually; rim level 0.66)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #20 (t=4050, R_eq 5.44): ['L link', 'membrane (wall)']; #29 (t=4050, R_eq 6.41, ring): ['K catalyst', 'L link', 'membrane (wall)']; #30 (t=4050, R_eq 5.86, ring): ['L link', 'membrane (wall)']; #89 (t=4850, R_eq 4.89): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 74 of 257 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
