# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 91)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 555s; status ok
- command: `python -m labkit.run /tmp/claude-0/se/world.py --out /tmp/claude-0/se/runs/I/seed91 --seeds 91 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.62 of robust range [-0.9312, 0.5687], min area 6 px

## Measurements
- components: final 24, mean 22.3, max 33; occupancy final 0.08
- tracks: 126; persistent (alive >= 50% of run): 8; longest 275 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.47 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 24, 24], H1 [0, 0, 0]
- motion: 68 long-lived tracks moved >= 1 body length; max speed 0.436/time; max body lengths 10.7
- replication (lineage window K = 20 frames = time 100, default): splits 48, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 5, merges 20, merge/split ratio 0.417, nucleations 10
- channel total drift (end/start - 1): [-0.5767, -0.5016, None, -0.0278]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 183: holes 0, rim-vs-core 0.56, rim-vs-outside 0.38, heterogeneity 0.14; core [0.946, 0.915, 0.374, 1.0] rim [0.755, 0.609, 0.803, 1.0]
  - track 36 at frame 194: holes 0, rim-vs-core 0.51, rim-vs-outside 0.36, heterogeneity 0.14; core [0.943, 0.863, 0.343, 1.0] rim [0.758, 0.556, 0.709, 1.0]
  - track 57 at frame 221: holes 0, rim-vs-core 0.57, rim-vs-outside 0.32, heterogeneity 0.14; core [0.954, 0.679, 0.413, 1.0] rim [0.764, 0.419, 0.888, 1.0]
  - track 92 at frame 269: holes 0, rim-vs-core 0.66, rim-vs-outside 0.40, heterogeneity 0.15; core [0.976, 0.919, 0.297, 1.0] rim [0.794, 0.56, 0.818, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 143 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 3.57 (aggregate of 143 individuals; 1/143 membrane-like individually; rim level 0.73)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.781, rim/outside 8.86 (aggregate of 143 individuals; 6/143 membrane-like individually; rim level 0.545)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 3.32 (aggregate of 143 individuals; 78/143 membrane-like individually; rim level 0.592)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 143 individuals; 0/143 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #24 (t=915, R_eq 4.07): none; #36 (t=970, R_eq 3.29): ['surfactant s']; #57 (t=1105, R_eq 4.03): ['surfactant s']; #92 (t=1345, R_eq 3.24): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 143 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
