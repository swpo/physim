# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 94)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 711s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py --out /tmp/claude-0/se3/runs/S/seed94 --seeds 94 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.62 of robust range [-0.9487, 0.5727], min area 6 px

## Measurements
- components: final 24, mean 23.1, max 29; occupancy final 0.08
- tracks: 135; persistent (alive >= 50% of run): 11; longest 266 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.35 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 24, 23], H1 [1, 0, 0]
- motion: 79 long-lived tracks moved >= 1 body length; max speed 0.306/time; max body lengths 11.0
- replication (lineage window K = 20 frames = time 100, default): splits 51, persistent splits 37 (0 more failed only because the siblings re-merged within K), max generation 6, merges 25, merge/split ratio 0.49, nucleations 7
- channel total drift (end/start - 1): [-0.6373, -0.506, None, -0.1643]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 188: holes 0, rim-vs-core 0.63, rim-vs-outside 0.31, heterogeneity 0.15; core [0.937, 0.852, 0.458, 1.0] rim [0.74, 0.484, 0.924, 1.0]
  - track 39 at frame 194: holes 0, rim-vs-core 0.55, rim-vs-outside 0.32, heterogeneity 0.13; core [0.957, 0.748, 0.385, 1.0] rim [0.776, 0.472, 0.823, 1.0]
  - track 40 at frame 194: holes 0, rim-vs-core 0.57, rim-vs-outside 0.40, heterogeneity 0.13; core [0.979, 0.939, 0.247, 1.0] rim [0.788, 0.601, 0.659, 1.0]
  - track 123 at frame 298: holes 0, rim-vs-core 0.37, rim-vs-outside 0.22, heterogeneity 0.22; core [0.886, 0.286, 0.596, 0.533] rim [0.743, 0.238, 0.925, 0.591]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 146 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 3.44 (aggregate of 146 individuals; 0/146 membrane-like individually; rim level 0.732)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.764, rim/outside 8.65 (aggregate of 146 individuals; 5/146 membrane-like individually; rim level 0.53)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 3.36 (aggregate of 146 individuals; 68/146 membrane-like individually; rim level 0.604)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.01 (aggregate of 146 individuals; 0/146 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #30 (t=940, R_eq 3.7): ['surfactant s']; #39 (t=970, R_eq 3.95): none; #40 (t=970, R_eq 3.34): ['surfactant s']; #123 (t=1490, R_eq 3.43): ['order |Q|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 146 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
