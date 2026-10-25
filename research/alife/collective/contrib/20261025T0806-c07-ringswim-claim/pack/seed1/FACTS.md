# Evidence pack: ringswim-waste (seed 1)

- world: `../../world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 126s; status ok
- command: `python -m labkit.run collective/contrib/_c07swim/world_claim.py --out collective/contrib/_c07swim/pack --seeds 0 1 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5536], min area 6 px

## Measurements
- components: final 7, mean 8.3, max 26; occupancy final 0.22
- tracks: 477; persistent (alive >= 50% of run): 0; longest 27 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 5.98, final 6; holes at thresholds 0.2/0.35/0.5 final [0, 8, 9]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 8, 7], H1 [9, 9, 2]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0212/time; max body lengths 4.8
- replication (lineage window K = 20 frames = time 2000, default): splits 155, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 142, merge/split ratio 0.916, nucleations 1
- channel total drift (end/start - 1): [-0.3459, -0.7973, -0.24, -0.3291]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 425 at frame 188: holes 1, rim-vs-core 0.36, rim-vs-outside 0.79, heterogeneity 0.22; core [0.125, 0.798, 0.669, 0.57] rim [0.251, 0.504, 0.511, 0.592]
  - track 111 at frame 29: holes 1, rim-vs-core 0.22, rim-vs-outside 0.84, heterogeneity 0.23; core [0.114, 0.783, 0.624, 0.542] rim [0.208, 0.595, 0.566, 0.583]
  - track 296 at frame 121: holes 1, rim-vs-core 0.34, rim-vs-outside 0.91, heterogeneity 0.23; core [0.093, 0.782, 0.499, 0.421] rim [0.2, 0.557, 0.515, 0.649]
  - track 96 at frame 24: holes 1, rim-vs-core 0.17, rim-vs-outside 0.79, heterogeneity 0.18; core [0.113, 0.683, 0.592, 0.678] rim [0.165, 0.547, 0.51, 0.627]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 45 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 6.71, rim/outside 0.79 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.536)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.942, rim/outside 8.96 (aggregate of 45 individuals; 1/45 membrane-like individually; rim level 0.582)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 6.25 (aggregate of 45 individuals; 20/45 membrane-like individually; rim level 0.515)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 7.06 (aggregate of 45 individuals; 20/45 membrane-like individually; rim level 0.505)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #425 (t=18800, R_eq 8.31, ring): ['L link', 'membrane (wall)']; #111 (t=2900, R_eq 10.28, ring): ['L link', 'membrane (wall)']; #296 (t=12100, R_eq 13.87): none; #96 (t=2400, R_eq 10.48, ring): ['K catalyst', 'L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 45 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
