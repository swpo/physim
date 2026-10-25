# Evidence pack: nematic-fuelcell-outslow (seed 0)

- world: `../../world_outslow.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 670s; status ok
- command: `python -m labkit.run /root/w/world_outslow.py --out /root/w/outslow03/s0 --seeds 0 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8622, 0.7068], min area 6 px

## Measurements
- components: final 21, mean 14.2, max 22; occupancy final 0.09
- tracks: 39; persistent (alive >= 50% of run): 10; longest 155 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 26.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 22, 21], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.0643/time; max body lengths 3.9
- replication (lineage window K = 20 frames = time 100, default): splits 14, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.143, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.0905, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 124: holes 0, rim-vs-core 0.44, rim-vs-outside 0.37, heterogeneity 0.11; core [0.945, 0.919, 0.9, 0.95] rim [0.703, 0.577, 0.812, 0.828]
  - track 10 at frame 124: holes 0, rim-vs-core 0.42, rim-vs-outside 0.37, heterogeneity 0.11; core [0.948, 0.918, 0.942, 0.952] rim [0.722, 0.595, 0.864, 0.847]
  - track 12 at frame 131: holes 0, rim-vs-core 0.41, rim-vs-outside 0.37, heterogeneity 0.12; core [0.93, 0.879, 0.975, 0.963] rim [0.697, 0.559, 0.897, 0.868]
  - track 25 at frame 166: holes 0, rim-vs-core 0.44, rim-vs-outside 0.37, heterogeneity 0.11; core [0.936, 0.901, 0.95, 0.968] rim [0.693, 0.569, 0.859, 0.862]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 96 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 4.74 (aggregate of 96 individuals; 1/96 membrane-like individually; rim level 0.661)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.773, rim/outside 7.32 (aggregate of 96 individuals; 2/96 membrane-like individually; rim level 0.57)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 1.52 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.851)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.912, rim/outside 1.79 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.846)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=620, R_eq 3.7): none; #10 (t=620, R_eq 3.43): none; #12 (t=655, R_eq 4.15): none; #25 (t=830, R_eq 3.95): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 96 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
