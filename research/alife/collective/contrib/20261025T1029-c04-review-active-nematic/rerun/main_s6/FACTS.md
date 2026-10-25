# Evidence pack: active-nematic-droplets (seed 6)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1014-c11-active-nematic-colony/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 277s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1014-c11-active-nematic-colony/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev9/main_s6 --seeds 6 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8228, 0.6115], min area 6 px

## Measurements
- components: final 30, mean 16.6, max 31; occupancy final 0.06
- tracks: 91; persistent (alive >= 50% of run): 3; longest 106 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.22 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 30, 30], H1 [0, 0, 0]
- motion: 42 long-lived tracks moved >= 1 body length; max speed 0.0913/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 100, default): splits 37, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 4, merges 9, merge/split ratio 0.243, nucleations 7
- channel total drift (end/start - 1): [-0.4995, -0.4617, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 148: holes 0, rim-vs-core 0.33, rim-vs-outside 0.34, heterogeneity 0.14; core [0.924, 0.821, 0.48] rim [0.725, 0.557, 0.493]
  - track 37 at frame 150: holes 0, rim-vs-core 0.40, rim-vs-outside 0.37, heterogeneity 0.18; core [0.951, 0.933, 0.493] rim [0.717, 0.61, 0.453]
  - track 27 at frame 126: holes 0, rim-vs-core 0.38, rim-vs-outside 0.46, heterogeneity 0.21; core [0.986, 0.999, 0.502] rim [0.738, 0.716, 0.496]
  - track 65 at frame 183: holes 0, rim-vs-core 0.38, rim-vs-outside 0.35, heterogeneity 0.15; core [0.953, 0.935, 0.443] rim [0.74, 0.621, 0.426]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 116 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.827, rim/outside 4.73 (aggregate of 116 individuals; 0/116 membrane-like individually; rim level 0.764)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.779, rim/outside 7.92 (aggregate of 116 individuals; 1/116 membrane-like individually; rim level 0.641)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #33 (t=740, R_eq 3.57): none; #37 (t=750, R_eq 3.43): none; #27 (t=630, R_eq 4.26): none; #65 (t=915, R_eq 3.19): none

## Warnings
- radial: 1 of 116 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
