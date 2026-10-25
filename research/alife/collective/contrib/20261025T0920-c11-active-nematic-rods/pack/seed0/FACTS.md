# Evidence pack: active-nematic-droplets (seed 0)

- world: `../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 290s; status ok
- command: `python -m labkit.run /tmp/claude-0/c11ex/world.py --out /tmp/claude-0/c11ex/p_d06 --seeds 0 --no-movie`
- segmentation: matter > 0.49 of robust range [-0.9351, 0.9591], min area 6 px

## Measurements
- components: final 24, mean 12.6, max 30; occupancy final 0.17
- tracks: 281; persistent (alive >= 50% of run): 0; longest 87 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 26, 18], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0625/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 100, default): splits 109, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 61, merge/split ratio 0.56, nucleations 9
- channel total drift (end/start - 1): [0.0, 0.9273, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 70 at frame 158: holes 0, rim-vs-core 0.26, rim-vs-outside 0.28, heterogeneity 0.10; core [0.803, 0.572, 0.387] rim [0.623, 0.385, 0.392]
  - track 134 at frame 168: holes 0, rim-vs-core 0.28, rim-vs-outside 0.28, heterogeneity 0.11; core [0.808, 0.613, 0.421] rim [0.621, 0.405, 0.436]
  - track 141 at frame 170: holes 0, rim-vs-core 0.49, rim-vs-outside 0.31, heterogeneity 0.24; core [0.923, 0.818, 0.393] rim [0.636, 0.44, 0.514]
  - track 211 at frame 180: holes 0, rim-vs-core 0.42, rim-vs-outside 0.30, heterogeneity 0.25; core [0.911, 0.699, 0.419] rim [0.629, 0.422, 0.548]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.763, rim/outside 4.07 (aggregate of 85 individuals; 1/85 membrane-like individually; rim level 0.605)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.669, rim/outside 6.4 (aggregate of 85 individuals; 1/85 membrane-like individually; rim level 0.427)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #70 (t=790, R_eq 5.23): none; #134 (t=840, R_eq 4.41): none; #141 (t=850, R_eq 6): none; #211 (t=900, R_eq 5.81): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 85 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
