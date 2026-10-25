# Evidence pack: active-nematic-droplets (seed 41)

- world: `../../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1141-c11-active-nematic-ringed/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 468s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T1141-c11-active-nematic-ringed/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/nematic-ringed/replication/base --seeds 41 43 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8203, 0.6001], min area 6 px

## Measurements
- components: final 30, mean 17.9, max 31; occupancy final 0.06
- tracks: 88; persistent (alive >= 50% of run): 6; longest 167 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 30, 29], H1 [0, 0, 0]
- motion: 34 long-lived tracks moved >= 1 body length; max speed 0.0777/time; max body lengths 4.2
- replication (lineage window K = 20 frames = time 100, default): splits 38, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 4, merges 6, merge/split ratio 0.158, nucleations 6
- channel total drift (end/start - 1): [-0.5024, -0.4323, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 118: holes 0, rim-vs-core 0.49, rim-vs-outside 0.34, heterogeneity 0.15; core [0.953, 0.917, 0.414] rim [0.753, 0.622, 0.747]
  - track 25 at frame 141: holes 0, rim-vs-core 0.47, rim-vs-outside 0.36, heterogeneity 0.17; core [0.943, 0.897, 0.475] rim [0.75, 0.625, 0.811]
  - track 29 at frame 138: holes 0, rim-vs-core 0.52, rim-vs-outside 0.36, heterogeneity 0.18; core [0.947, 0.891, 0.47] rim [0.72, 0.588, 0.823]
  - track 71 at frame 188: holes 0, rim-vs-core 0.55, rim-vs-outside 0.37, heterogeneity 0.19; core [0.948, 0.926, 0.462] rim [0.711, 0.602, 0.844]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 120 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 4.61 (aggregate of 120 individuals; 0/120 membrane-like individually; rim level 0.747)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.761, rim/outside 7.59 (aggregate of 120 individuals; 1/120 membrane-like individually; rim level 0.643)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 2.1 (aggregate of 120 individuals; 84/120 membrane-like individually; rim level 0.654)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #10 (t=590, R_eq 3.04): ['surfactant s']; #25 (t=705, R_eq 3.39): ['surfactant s']; #29 (t=690, R_eq 3.7): ['surfactant s']; #71 (t=940, R_eq 3.24): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 120 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
