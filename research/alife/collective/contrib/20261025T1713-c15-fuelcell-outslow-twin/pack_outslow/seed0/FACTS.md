# Evidence pack: nematic-fuelcell-outslow (seed 0)

- world: `../../world_outslow.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 685s; status ok
- command: `python -m labkit.run /root/w/world_outslow.py --out /root/w/outslow/s0 --seeds 0 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8559, 0.6881], min area 6 px

## Measurements
- components: final 25, mean 15.4, max 25; occupancy final 0.09
- tracks: 46; persistent (alive >= 50% of run): 10; longest 164 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.40 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 26, 23], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.0469/time; max body lengths 3.6
- replication (lineage window K = 20 frames = time 100, default): splits 18, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.056, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.1784, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 119: holes 0, rim-vs-core 0.41, rim-vs-outside 0.40, heterogeneity 0.11; core [0.941, 0.903, 0.924, 0.93] rim [0.711, 0.59, 0.843, 0.833]
  - track 11 at frame 123: holes 0, rim-vs-core 0.41, rim-vs-outside 0.37, heterogeneity 0.11; core [0.952, 0.929, 0.897, 0.933] rim [0.727, 0.609, 0.819, 0.832]
  - track 12 at frame 123: holes 0, rim-vs-core 0.43, rim-vs-outside 0.37, heterogeneity 0.11; core [0.947, 0.923, 0.918, 0.937] rim [0.716, 0.594, 0.835, 0.829]
  - track 25 at frame 160: holes 0, rim-vs-core 0.43, rim-vs-outside 0.35, heterogeneity 0.11; core [0.935, 0.897, 0.943, 0.959] rim [0.694, 0.566, 0.86, 0.86]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 107 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.802, rim/outside 4.79 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.682)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.772, rim/outside 7.53 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.582)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.912, rim/outside 1.5 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.859)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 1.96 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.84)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=595, R_eq 4.03): none; #11 (t=615, R_eq 3.34): none; #12 (t=615, R_eq 3.78): none; #25 (t=800, R_eq 3.74): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 107 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
