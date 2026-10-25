# Evidence pack: active-nematic-droplets (seed 4)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1014-c11-active-nematic-colony/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 287s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1014-c11-active-nematic-colony/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/nem/act/seed4 --seeds 4 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8254, 0.6277], min area 6 px

## Measurements
- components: final 31, mean 22.1, max 32; occupancy final 0.07
- tracks: 93; persistent (alive >= 50% of run): 11; longest 176 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.78 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 32, 30], H1 [0, 0, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 0.0879/time; max body lengths 4.6
- replication (lineage window K = 20 frames = time 100, default): splits 36, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 4, merges 10, merge/split ratio 0.278, nucleations 11
- channel total drift (end/start - 1): [-0.5085, -0.3867, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 113: holes 0, rim-vs-core 0.32, rim-vs-outside 0.32, heterogeneity 0.13; core [0.94, 0.759, 0.461] rim [0.739, 0.511, 0.476]
  - track 28 at frame 121: holes 0, rim-vs-core 0.37, rim-vs-outside 0.37, heterogeneity 0.16; core [0.943, 0.928, 0.462] rim [0.73, 0.631, 0.435]
  - track 33 at frame 123: holes 0, rim-vs-core 0.15, rim-vs-outside 0.49, heterogeneity 0.16; core [0.895, 0.758, 0.417] rim [0.799, 0.654, 0.471]
  - track 83 at frame 185: holes 0, rim-vs-core 0.33, rim-vs-outside 0.38, heterogeneity 0.14; core [0.964, 0.956, 0.438] rim [0.771, 0.686, 0.449]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 150 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.811, rim/outside 4.69 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.753)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.748, rim/outside 7.98 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.615)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=565, R_eq 2.59): none; #28 (t=605, R_eq 3.39): none; #33 (t=615, R_eq 3.48): none; #83 (t=925, R_eq 3.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 150 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
