# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 90)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 511s; status ok
- command: `python -m labkit.run /tmp/claude-0/se/world.py --out /tmp/claude-0/se/runs2/S_mar0/seed90 --seeds 90 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0193, 0.5457], min area 6 px

## Measurements
- components: final 3, mean 6.9, max 15; occupancy final 0.01
- tracks: 64; persistent (alive >= 50% of run): 0; longest 107 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 4, 2], H1 [1, 0, 0]
- motion: 26 long-lived tracks moved >= 1 body length; max speed 0.0801/time; max body lengths 4.4
- replication (lineage window K = 20 frames = time 100, default): splits 27, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 4, merges 3, merge/split ratio 0.111, nucleations 7
- channel total drift (end/start - 1): [-0.6666, -0.9251, None, -0.0307]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 145: holes 0, rim-vs-core 0.50, rim-vs-outside 0.40, heterogeneity 0.11; core [0.998, 1.0, 0.315, 1.0] rim [0.831, 0.772, 0.726, 1.0]
  - track 14 at frame 83: holes 0, rim-vs-core 0.46, rim-vs-outside 0.41, heterogeneity 0.12; core [0.984, 0.963, 0.504, 1.0] rim [0.824, 0.725, 0.858, 1.0]
  - track 24 at frame 118: holes 0, rim-vs-core 0.46, rim-vs-outside 0.33, heterogeneity 0.11; core [0.984, 0.846, 0.506, 1.0] rim [0.857, 0.627, 0.89, 1.0]
  - track 56 at frame 247: holes 0, rim-vs-core 0.54, rim-vs-outside 0.40, heterogeneity 0.12; core [0.998, 0.998, 0.346, 1.0] rim [0.85, 0.778, 0.819, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 44 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 2.76 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.817)
  - radial order |Q|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 6.73 (aggregate of 44 individuals; 1/44 membrane-like individually; rim level 0.73)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 2.91 (aggregate of 44 individuals; 29/44 membrane-like individually; rim level 0.663)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.996, rim/outside 1.06 (aggregate of 44 individuals; 1/44 membrane-like individually; rim level 0.983)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #28 (t=725, R_eq 3.04): ['surfactant s']; #14 (t=415, R_eq 3.74): none; #24 (t=590, R_eq 3.99): none; #56 (t=1235, R_eq 2.88): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 44 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
