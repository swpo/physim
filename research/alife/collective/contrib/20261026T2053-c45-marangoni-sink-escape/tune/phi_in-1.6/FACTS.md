# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 0)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 151 frames x 100 steps x dt 0.05 = time 750; grid [128, 128]; wall 247s; status ok
- command: `python -m labkit.run /tmp/claude-0/se/world.py --out /tmp/claude-0/se/runs/tune-1.6/seed0 --seeds 0 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.1002, 0.5849], min area 6 px

## Measurements
- components: final 12, mean 11.4, max 16; occupancy final 0.03
- tracks: 42; persistent (alive >= 50% of run): 5; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.31 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [18, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 12, 12], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.0619/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 100, default): splits 15, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 3, merge/split ratio 0.2, nucleations 8
- channel total drift (end/start - 1): [-0.6343, -0.7344, None, -0.0792]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 91: holes 0, rim-vs-core 0.49, rim-vs-outside 0.31, heterogeneity 0.11; core [0.966, 0.769, 0.413, 1.0] rim [0.8, 0.523, 0.806, 1.0]
  - track 14 at frame 92: holes 0, rim-vs-core 0.51, rim-vs-outside 0.36, heterogeneity 0.13; core [0.972, 0.944, 0.363, 1.0] rim [0.812, 0.677, 0.767, 1.0]
  - track 17 at frame 81: holes 0, rim-vs-core 0.47, rim-vs-outside 0.33, heterogeneity 0.12; core [0.967, 0.927, 0.443, 1.0] rim [0.823, 0.632, 0.773, 1.0]
  - track 31 at frame 129: holes 0, rim-vs-core 0.44, rim-vs-outside 0.45, heterogeneity 0.13; core [0.981, 0.961, 0.326, 1.0] rim [0.855, 0.767, 0.701, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 74 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 2.69 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.842)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 8.76 (aggregate of 74 individuals; 1/74 membrane-like individually; rim level 0.721)
  - radial surfactant s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.92, rim/outside 3 (aggregate of 74 individuals; 64/74 membrane-like individually; rim level 0.636)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #10 (t=455, R_eq 2.65): ['surfactant s']; #14 (t=460, R_eq 3.24): ['surfactant s']; #17 (t=405, R_eq 3.61): none; #31 (t=645, R_eq 3.34): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
