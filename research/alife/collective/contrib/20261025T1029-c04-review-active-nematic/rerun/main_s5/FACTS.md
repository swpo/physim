# Evidence pack: active-nematic-droplets (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1014-c11-active-nematic-colony/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 277s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1014-c11-active-nematic-colony/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev9/main_s5 --seeds 5 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8261, 0.6366], min area 6 px

## Measurements
- components: final 30, mean 21.3, max 30; occupancy final 0.07
- tracks: 98; persistent (alive >= 50% of run): 11; longest 166 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 30, 28], H1 [0, 0, 0]
- motion: 46 long-lived tracks moved >= 1 body length; max speed 0.078/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 100, default): splits 40, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 4, merges 8, merge/split ratio 0.2, nucleations 10
- channel total drift (end/start - 1): [-0.5101, -0.3482, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 118: holes 0, rim-vs-core 0.37, rim-vs-outside 0.34, heterogeneity 0.17; core [0.933, 0.863, 0.483] rim [0.713, 0.561, 0.459]
  - track 40 at frame 136: holes 0, rim-vs-core 0.34, rim-vs-outside 0.37, heterogeneity 0.15; core [0.944, 0.887, 0.507] rim [0.746, 0.607, 0.505]
  - track 41 at frame 136: holes 0, rim-vs-core 0.33, rim-vs-outside 0.39, heterogeneity 0.16; core [0.95, 0.904, 0.562] rim [0.751, 0.636, 0.554]
  - track 89 at frame 187: holes 0, rim-vs-core 0.38, rim-vs-outside 0.40, heterogeneity 0.17; core [0.97, 0.963, 0.409] rim [0.745, 0.662, 0.383]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 146 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 4.74 (aggregate of 146 individuals; 0/146 membrane-like individually; rim level 0.754)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.755, rim/outside 8.14 (aggregate of 146 individuals; 1/146 membrane-like individually; rim level 0.631)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=590, R_eq 3.14): none; #40 (t=680, R_eq 3.14): none; #41 (t=680, R_eq 3.34): none; #89 (t=935, R_eq 3.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 146 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
