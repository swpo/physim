# Evidence pack: ringswim-waste (seed 0)

- world: `../../world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 148s; status ok
- command: `python -m labkit.run collective/contrib/_c07swim/world_claim.py --out collective/contrib/_c07swim/pack --seeds 0 1 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5566], min area 6 px

## Measurements
- components: final 5, mean 9.7, max 22; occupancy final 0.19
- tracks: 473; persistent (alive >= 50% of run): 0; longest 32 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 6.65, final 4; holes at thresholds 0.2/0.35/0.5 final [0, 6, 6]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 6, 5], H1 [7, 6, 1]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.0226/time; max body lengths 3.9
- replication (lineage window K = 20 frames = time 2000, default): splits 156, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 135, merge/split ratio 0.865, nucleations 5
- channel total drift (end/start - 1): [-0.3081, -0.8209, -0.3386, -0.5199]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 60 at frame 25: holes 1, rim-vs-core 0.17, rim-vs-outside 0.80, heterogeneity 0.20; core [0.114, 0.698, 0.598, 0.67] rim [0.192, 0.576, 0.547, 0.607]
  - track 59 at frame 24: holes 1, rim-vs-core 0.27, rim-vs-outside 0.79, heterogeneity 0.21; core [0.135, 0.76, 0.675, 0.643] rim [0.221, 0.562, 0.534, 0.574]
  - track 6 at frame 13: holes 1, rim-vs-core 0.28, rim-vs-outside 0.82, heterogeneity 0.21; core [0.135, 0.785, 0.678, 0.62] rim [0.229, 0.557, 0.539, 0.588]
  - track 63 at frame 24: holes 0, rim-vs-core 0.56, rim-vs-outside 0.96, heterogeneity 0.23; core [0.108, 0.836, 0.629, 0.469] rim [0.358, 0.429, 0.598, 0.755]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 51 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 9.11, rim/outside 0.758 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.512)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 7.81 (aggregate of 51 individuals; 4/51 membrane-like individually; rim level 0.616)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 5.97 (aggregate of 51 individuals; 35/51 membrane-like individually; rim level 0.522)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.93, rim/outside 6.08 (aggregate of 51 individuals; 33/51 membrane-like individually; rim level 0.553)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #60 (t=2500, R_eq 10.59, ring): ['L link', 'membrane (wall)']; #59 (t=2400, R_eq 8.81, ring): ['L link', 'membrane (wall)']; #6 (t=1300, R_eq 8.27, ring): ['L link', 'membrane (wall)']; #63 (t=2400, R_eq 7.57): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 27 of 51 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
