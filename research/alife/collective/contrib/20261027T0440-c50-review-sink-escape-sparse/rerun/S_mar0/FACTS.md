# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 94)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 633s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py --out /tmp/claude-0/se3/runs/S_mar0/seed94 --seeds 94 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.61 of robust range [-0.935, 0.607], min area 6 px

## Measurements
- components: final 22, mean 18.9, max 26; occupancy final 0.05
- tracks: 123; persistent (alive >= 50% of run): 5; longest 209 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 23, 19], H1 [3, 0, 0]
- motion: 54 long-lived tracks moved >= 1 body length; max speed 0.0772/time; max body lengths 5.2
- replication (lineage window K = 20 frames = time 100, default): splits 52, persistent splits 31 (0 more failed only because the siblings re-merged within K), max generation 4, merges 12, merge/split ratio 0.231, nucleations 7
- channel total drift (end/start - 1): [-0.6373, -0.5976, None, -0.1643]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 63 at frame 218: holes 0, rim-vs-core 0.50, rim-vs-outside 0.37, heterogeneity 0.13; core [0.944, 0.909, 0.324, 1.0] rim [0.739, 0.606, 0.664, 1.0]
  - track 69 at frame 218: holes 0, rim-vs-core 0.52, rim-vs-outside 0.33, heterogeneity 0.13; core [0.949, 0.839, 0.337, 1.0] rim [0.756, 0.552, 0.729, 1.0]
  - track 74 at frame 226: holes 0, rim-vs-core 0.52, rim-vs-outside 0.35, heterogeneity 0.13; core [0.957, 0.917, 0.292, 1.0] rim [0.767, 0.619, 0.673, 1.0]
  - track 85 at frame 261: holes 0, rim-vs-core 0.45, rim-vs-outside 0.30, heterogeneity 0.11; core [0.933, 0.84, 0.344, 1.0] rim [0.762, 0.572, 0.656, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 123 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.851, rim/outside 3.44 (aggregate of 123 individuals; 0/123 membrane-like individually; rim level 0.778)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.797, rim/outside 7.43 (aggregate of 123 individuals; 3/123 membrane-like individually; rim level 0.635)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.54, rim/outside 2.87 (aggregate of 123 individuals; 93/123 membrane-like individually; rim level 0.579)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 123 individuals; 0/123 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #63 (t=1090, R_eq 3.29): ['surfactant s']; #69 (t=1090, R_eq 2.88): ['surfactant s']; #74 (t=1130, R_eq 3.04): ['surfactant s']; #85 (t=1305, R_eq 3.24): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 123 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
