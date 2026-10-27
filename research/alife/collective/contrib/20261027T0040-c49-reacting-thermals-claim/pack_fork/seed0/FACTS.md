# Evidence pack: reacting-thermals (seed 0)

- world: `../../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 58s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/20261027T0040-c49-reacting-thermals-claim/pack_fork --seeds 0 1 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7546], min area 6 px

## Measurements
- components: final 0, mean 6.5, max 43; occupancy final 0.00
- tracks: 222; persistent (alive >= 50% of run): 0; longest 115 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 65 long-lived tracks moved >= 1 body length; max speed 1.28/time; max body lengths 18.3
- replication (lineage window K = 20 frames = time 20, default): splits 66, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 6, merges 9, merge/split ratio 0.136, nucleations 45
- channel total drift (end/start - 1): [-1.0, -1.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 112 at frame 222: holes 0, rim-vs-core 0.25, rim-vs-outside 0.49, heterogeneity 0.15; core [0.901, 0.337, 0.533, 0.956] rim [0.715, 0.365, 0.476, 0.802]
  - track 125 at frame 267: holes 0, rim-vs-core 0.28, rim-vs-outside 0.62, heterogeneity 0.16; core [0.958, 0.337, 0.495, 0.995] rim [0.732, 0.375, 0.49, 0.828]
  - track 192 at frame 378: holes 0, rim-vs-core 0.26, rim-vs-outside 0.61, heterogeneity 0.15; core [0.942, 0.355, 0.573, 0.992] rim [0.729, 0.388, 0.527, 0.856]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [101, 202, 303, 398]):
  - radial heat T: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.97, rim/outside 5.15 (aggregate of 35 individuals; 1/35 membrane-like individually; rim level 0.627)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.36, rim/outside 0.828 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.472)
  - radial vorticity: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 1.06 (aggregate of 35 individuals; 7/35 membrane-like individually; rim level 0.462)
  - radial burn r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 5.76 (aggregate of 35 individuals; 2/35 membrane-like individually; rim level 0.673)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #112 (t=222, R_eq 3.48, ring): none; #138 (t=333, R_eq 2.03): none; #125 (t=267, R_eq 2.99): ['vorticity']; #192 (t=378, R_eq 2.82): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 35 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
