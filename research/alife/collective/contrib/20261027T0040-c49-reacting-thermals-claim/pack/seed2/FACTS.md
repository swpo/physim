# Evidence pack: reacting-thermals (seed 2)

- world: `../../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 59s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/20261027T0040-c49-reacting-thermals-claim/pack --seeds 0 1 2 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.31 of robust range [0.0, 0.8183], min area 6 px

## Measurements
- components: final 30, mean 16.4, max 41; occupancy final 0.03
- tracks: 476; persistent (alive >= 50% of run): 0; longest 164 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 35, 32], H1 [0, 0, 0]
- motion: 161 long-lived tracks moved >= 1 body length; max speed 1.15/time; max body lengths 21.6
- replication (lineage window K = 20 frames = time 20, default): splits 95, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 7, merges 22, merge/split ratio 0.232, nucleations 232
- channel total drift (end/start - 1): [-0.8712, -0.3525, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 341 at frame 519: holes 0, rim-vs-core 0.36, rim-vs-outside 0.62, heterogeneity 0.20; core [0.947, 0.129, 0.45, 0.986] rim [0.684, 0.199, 0.511, 0.763]
  - track 154 at frame 303: holes 0, rim-vs-core 0.36, rim-vs-outside 0.61, heterogeneity 0.15; core [0.97, 0.145, 0.663, 1.0] rim [0.706, 0.175, 0.541, 0.793]
  - track 350 at frame 529: holes 0, rim-vs-core 0.34, rim-vs-outside 0.53, heterogeneity 0.17; core [0.933, 0.114, 0.675, 0.946] rim [0.673, 0.175, 0.604, 0.748]
  - track 359 at frame 529: holes 0, rim-vs-core 0.26, rim-vs-outside 0.57, heterogeneity 0.16; core [0.914, 0.116, 0.424, 0.944] rim [0.729, 0.171, 0.543, 0.815]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 73 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 5.22 (aggregate of 73 individuals; 1/73 membrane-like individually; rim level 0.635)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.37, rim/outside 0.697 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.266)
  - radial vorticity: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 1.03 (aggregate of 73 individuals; 10/73 membrane-like individually; rim level 0.469)
  - radial burn r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 6.26 (aggregate of 73 individuals; 4/73 membrane-like individually; rim level 0.659)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #341 (t=519, R_eq 2.46): none; #154 (t=303, R_eq 3.29): none; #350 (t=529, R_eq 2.33): none; #359 (t=529, R_eq 2.19): ['vorticity']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 73 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
