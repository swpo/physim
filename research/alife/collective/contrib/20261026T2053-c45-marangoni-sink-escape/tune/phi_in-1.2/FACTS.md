# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 0)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 151 frames x 100 steps x dt 0.05 = time 750; grid [128, 128]; wall 249s; status ok
- command: `python -m labkit.run /tmp/claude-0/se/world.py --out /tmp/claude-0/se/runs/tune-1.2/seed0 --seeds 0 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.62 of robust range [-0.9418, 0.5864], min area 6 px

## Measurements
- components: final 14, mean 13.1, max 18; occupancy final 0.03
- tracks: 40; persistent (alive >= 50% of run): 9; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 15, 14], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.0875/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 100, default): splits 15, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.067, nucleations 9
- channel total drift (end/start - 1): [-0.5823, -0.7016, None, -0.0475]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 91: holes 0, rim-vs-core 0.52, rim-vs-outside 0.33, heterogeneity 0.12; core [0.971, 0.893, 0.36, 1.0] rim [0.795, 0.616, 0.763, 1.0]
  - track 15 at frame 92: holes 0, rim-vs-core 0.50, rim-vs-outside 0.37, heterogeneity 0.13; core [0.957, 0.912, 0.396, 1.0] rim [0.776, 0.641, 0.774, 1.0]
  - track 17 at frame 95: holes 0, rim-vs-core 0.44, rim-vs-outside 0.26, heterogeneity 0.08; core [0.926, 0.476, 0.516, 1.0] rim [0.763, 0.341, 0.898, 1.0]
  - track 34 at frame 125: holes 0, rim-vs-core 0.52, rim-vs-outside 0.35, heterogeneity 0.13; core [0.975, 0.965, 0.342, 1.0] rim [0.793, 0.673, 0.736, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.841, rim/outside 3.38 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.794)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 8.14 (aggregate of 83 individuals; 1/83 membrane-like individually; rim level 0.667)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.7, rim/outside 3.02 (aggregate of 83 individuals; 67/83 membrane-like individually; rim level 0.629)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.01 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.998)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #11 (t=455, R_eq 2.76): ['surfactant s']; #15 (t=460, R_eq 3.39): ['surfactant s']; #17 (t=475, R_eq 2.19): ['surfactant s']; #34 (t=625, R_eq 3.19): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
