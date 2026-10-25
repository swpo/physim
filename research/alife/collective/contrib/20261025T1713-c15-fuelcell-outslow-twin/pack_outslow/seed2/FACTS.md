# Evidence pack: nematic-fuelcell-outslow (seed 2)

- world: `../../world_outslow.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 679s; status ok
- command: `python -m labkit.run /root/w/world_outslow.py --out /root/w/outslow/s2 --seeds 2 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8623, 0.6817], min area 6 px

## Measurements
- components: final 22, mean 13.2, max 23; occupancy final 0.10
- tracks: 51; persistent (alive >= 50% of run): 8; longest 170 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 40.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 22, 21], H1 [1, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.0614/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 100, default): splits 20, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.15, nucleations 8
- channel total drift (end/start - 1): [-0.5106, -0.1024, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 116: holes 0, rim-vs-core 0.37, rim-vs-outside 0.39, heterogeneity 0.11; core [0.929, 0.87, 0.932, 0.898] rim [0.716, 0.586, 0.859, 0.817]
  - track 8 at frame 109: holes 0, rim-vs-core 0.36, rim-vs-outside 0.36, heterogeneity 0.11; core [0.921, 0.771, 0.973, 0.957] rim [0.697, 0.507, 0.901, 0.886]
  - track 10 at frame 124: holes 0, rim-vs-core 0.40, rim-vs-outside 0.41, heterogeneity 0.11; core [0.952, 0.933, 0.885, 0.924] rim [0.723, 0.625, 0.801, 0.824]
  - track 20 at frame 168: holes 0, rim-vs-core 0.41, rim-vs-outside 0.38, heterogeneity 0.11; core [0.951, 0.934, 0.91, 0.94] rim [0.723, 0.614, 0.828, 0.833]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 91 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 4.17 (aggregate of 91 individuals; 3/91 membrane-like individually; rim level 0.63)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 6.23 (aggregate of 91 individuals; 4/91 membrane-like individually; rim level 0.527)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 1.5 (aggregate of 91 individuals; 0/91 membrane-like individually; rim level 0.843)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 1.95 (aggregate of 91 individuals; 0/91 membrane-like individually; rim level 0.811)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=580, R_eq 4.65): none; #8 (t=545, R_eq 4.82): none; #10 (t=620, R_eq 3.7): none; #20 (t=840, R_eq 3.87): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 91 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
