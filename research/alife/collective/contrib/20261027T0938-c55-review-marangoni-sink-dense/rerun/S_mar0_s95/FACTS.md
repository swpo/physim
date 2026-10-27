# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 95)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 574s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/mar/S0 --seeds 95 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0016, 0.5459], min area 6 px

## Measurements
- components: final 1, mean 6.4, max 20; occupancy final 0.00
- tracks: 45; persistent (alive >= 50% of run): 1; longest 289 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 1], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.0823/time; max body lengths 3.8
- replication (lineage window K = 20 frames = time 100, default): splits 17, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.059, nucleations 10
- channel total drift (end/start - 1): [-0.9093, -0.9675, None, -0.312]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 177: holes 0, rim-vs-core 0.60, rim-vs-outside 0.44, heterogeneity 0.13; core [0.998, 0.995, 0.458, 1.0] rim [0.848, 0.773, 0.99, 1.0]
  - track 19 at frame 99: holes 0, rim-vs-core 0.47, rim-vs-outside 0.39, heterogeneity 0.11; core [0.996, 0.996, 0.382, 1.0] rim [0.852, 0.807, 0.783, 1.0]
  - track 26 at frame 108: holes 0, rim-vs-core 0.48, rim-vs-outside 0.44, heterogeneity 0.12; core [0.995, 0.991, 0.307, 1.0] rim [0.888, 0.85, 0.751, 1.0]
  - track 39 at frame 118: holes 0, rim-vs-core 0.61, rim-vs-outside 0.44, heterogeneity 0.13; core [0.999, 1.0, 0.374, 1.0] rim [0.854, 0.808, 0.939, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 36 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.89, rim/outside 3 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.855)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 7.35 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.802)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.65, rim/outside 2.91 (aggregate of 36 individuals; 30/36 membrane-like individually; rim level 0.691)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.03 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #21 (t=885, R_eq 3.19): ['surfactant s']; #19 (t=495, R_eq 3.43): ['surfactant s']; #26 (t=540, R_eq 2.82): ['surfactant s']; #39 (t=590, R_eq 2.99): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
