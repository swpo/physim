# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 93)

- world: `../../../../collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 583s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py --out collective/contrib/20261027T0621-c52-review-sink-dense/S/seed93 --seeds 93 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.64 of robust range [-1.012, 0.5687], min area 6 px

## Measurements
- components: final 7, mean 18.1, max 25; occupancy final 0.02
- tracks: 112; persistent (alive >= 50% of run): 11; longest 250 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 7, 7], H1 [0, 0, 0]
- motion: 60 long-lived tracks moved >= 1 body length; max speed 0.334/time; max body lengths 11.2
- replication (lineage window K = 20 frames = time 100, default): splits 40, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 4, merges 20, merge/split ratio 0.5, nucleations 12
- channel total drift (end/start - 1): [-1.0681, -0.8674, None, -0.236]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 44 at frame 196: holes 0, rim-vs-core 0.57, rim-vs-outside 0.33, heterogeneity 0.14; core [0.959, 0.706, 0.395, 1.0] rim [0.774, 0.451, 0.874, 1.0]
  - track 54 at frame 204: holes 0, rim-vs-core 0.49, rim-vs-outside 0.29, heterogeneity 0.13; core [0.949, 0.643, 0.408, 1.0] rim [0.774, 0.42, 0.81, 1.0]
  - track 60 at frame 210: holes 0, rim-vs-core 0.58, rim-vs-outside 0.31, heterogeneity 0.16; core [0.964, 0.631, 0.395, 1.0] rim [0.782, 0.413, 0.905, 1.0]
  - track 97 at frame 269: holes 0, rim-vs-core 0.71, rim-vs-outside 0.42, heterogeneity 0.16; core [0.988, 0.924, 0.281, 1.0] rim [0.831, 0.62, 0.907, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 108 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 3.01 (aggregate of 108 individuals; 0/108 membrane-like individually; rim level 0.75)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 8.69 (aggregate of 108 individuals; 8/108 membrane-like individually; rim level 0.533)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 3.27 (aggregate of 108 individuals; 49/108 membrane-like individually; rim level 0.594)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.02 (aggregate of 108 individuals; 0/108 membrane-like individually; rim level 0.997)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #44 (t=980, R_eq 4.37): none; #54 (t=1020, R_eq 4.75): ['order |Q|']; #60 (t=1050, R_eq 4.48): ['order |Q|']; #97 (t=1345, R_eq 3.57): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 108 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
