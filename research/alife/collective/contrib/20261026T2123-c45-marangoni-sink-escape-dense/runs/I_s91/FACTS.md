# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 91)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 558s; status ok
- command: `python -m labkit.run /tmp/claude-0/se/world.py --out /tmp/claude-0/se/runs2/I/seed91 --seeds 91 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.65 of robust range [-0.9926, 0.5363], min area 6 px

## Measurements
- components: final 1, mean 7.2, max 20; occupancy final 0.00
- tracks: 71; persistent (alive >= 50% of run): 0; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 31 long-lived tracks moved >= 1 body length; max speed 0.365/time; max body lengths 8.5
- replication (lineage window K = 20 frames = time 100, default): splits 28, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 5, merge/split ratio 0.179, nucleations 10
- channel total drift (end/start - 1): [-0.8914, -0.9775, None, -0.2358]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 39 at frame 140: holes 0, rim-vs-core 0.62, rim-vs-outside 0.37, heterogeneity 0.14; core [0.982, 0.932, 0.502, 1.0] rim [0.808, 0.571, 0.972, 1.0]
  - track 4 at frame 65: holes 0, rim-vs-core 0.61, rim-vs-outside 0.33, heterogeneity 0.17; core [0.992, 0.719, 0.461, 1.0] rim [0.818, 0.455, 0.981, 1.0]
  - track 24 at frame 94: holes 0, rim-vs-core 0.55, rim-vs-outside 0.42, heterogeneity 0.14; core [0.977, 0.991, 0.466, 1.0] rim [0.786, 0.678, 0.872, 1.0]
  - track 64 at frame 215: holes 0, rim-vs-core 0.49, rim-vs-outside 0.47, heterogeneity 0.13; core [0.987, 0.971, 0.263, 1.0] rim [0.83, 0.712, 0.644, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 46 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 2.98 (aggregate of 46 individuals; 1/46 membrane-like individually; rim level 0.76)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.837, rim/outside 8.02 (aggregate of 46 individuals; 5/46 membrane-like individually; rim level 0.636)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 3.31 (aggregate of 46 individuals; 23/46 membrane-like individually; rim level 0.632)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.988, rim/outside 1.03 (aggregate of 46 individuals; 0/46 membrane-like individually; rim level 0.988)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #39 (t=700, R_eq 3.95): none; #4 (t=325, R_eq 4.3): none; #24 (t=470, R_eq 3.83): ['surfactant s']; #64 (t=1075, R_eq 3.19): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 46 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
