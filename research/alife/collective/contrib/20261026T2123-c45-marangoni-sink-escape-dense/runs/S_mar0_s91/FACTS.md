# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 91)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 512s; status ok
- command: `python -m labkit.run /tmp/claude-0/se/world.py --out /tmp/claude-0/se/runs2/S_mar0/seed91 --seeds 91 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.64 of robust range [-0.99, 0.565], min area 6 px

## Measurements
- components: final 2, mean 8.3, max 16; occupancy final 0.00
- tracks: 64; persistent (alive >= 50% of run): 1; longest 171 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.94 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.0885/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 100, default): splits 24, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 6, merge/split ratio 0.25, nucleations 10
- channel total drift (end/start - 1): [-0.8904, -0.9687, None, -0.2358]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 52 at frame 237: holes 0, rim-vs-core 0.49, rim-vs-outside 0.41, heterogeneity 0.13; core [0.981, 0.968, 0.369, 1.0] rim [0.813, 0.74, 0.774, 1.0]
  - track 17 at frame 94: holes 0, rim-vs-core 0.49, rim-vs-outside 0.37, heterogeneity 0.12; core [0.99, 0.993, 0.333, 1.0] rim [0.827, 0.741, 0.726, 1.0]
  - track 22 at frame 97: holes 0, rim-vs-core 0.44, rim-vs-outside 0.41, heterogeneity 0.11; core [0.986, 0.973, 0.34, 1.0] rim [0.832, 0.756, 0.694, 1.0]
  - track 54 at frame 212: holes 0, rim-vs-core 0.50, rim-vs-outside 0.40, heterogeneity 0.12; core [0.989, 0.973, 0.396, 1.0] rim [0.828, 0.748, 0.815, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 50 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 3.01 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.822)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.835, rim/outside 7.31 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.731)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.52, rim/outside 2.91 (aggregate of 50 individuals; 35/50 membrane-like individually; rim level 0.641)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.05 (aggregate of 50 individuals; 1/50 membrane-like individually; rim level 0.98)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #52 (t=1185, R_eq 3.43): ['surfactant s']; #17 (t=470, R_eq 3.14): ['surfactant s']; #22 (t=485, R_eq 3.43): ['surfactant s']; #54 (t=1060, R_eq 3.66): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
