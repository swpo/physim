# Evidence pack: active-nematic-cargo (seed 0)

- world: `../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa)
- run: 121 frames x 200 steps x dt 0.05 = time 1200; grid [128, 128]; wall 459s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0405-c34-nematic-cargo/world.py --out collective/contrib/20261026T0405-c34-nematic-cargo/dthalf --seeds 0 --frames 120 --spf 200 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8196, 0.6359], min area 6 px

## Measurements
- components: final 23, mean 14.6, max 23; occupancy final 0.05
- tracks: 55; persistent (alive >= 50% of run): 12; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.85 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 23, 22], H1 [0, 0, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.0501/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 200, default): splits 21, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 4, merge/split ratio 0.19, nucleations 9
- channel total drift (end/start - 1): [-0.504, -0.5376, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 73: holes 0, rim-vs-core 0.72, rim-vs-outside 0.30, heterogeneity 0.23; core [0.91, 0.732, 0.524, 0.601] rim [0.745, 0.51, 0.889, 0.044]
  - track 11 at frame 76: holes 0, rim-vs-core 0.69, rim-vs-outside 0.32, heterogeneity 0.20; core [0.944, 0.835, 0.35, 0.5] rim [0.742, 0.56, 0.716, 0.019]
  - track 13 at frame 76: holes 0, rim-vs-core 0.93, rim-vs-outside 0.37, heterogeneity 0.24; core [0.975, 0.928, 0.309, 0.698] rim [0.75, 0.605, 0.81, 0.024]
  - track 41 at frame 109: holes 0, rim-vs-core 0.65, rim-vs-outside 0.50, heterogeneity 0.23; core [0.963, 0.94, 0.278, 0.669] rim [0.824, 0.769, 0.604, 0.151]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 100 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 5.06 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.782)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.773, rim/outside 8.51 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.646)
  - radial surfactant s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.85, rim/outside 3.1 (aggregate of 100 individuals; 81/100 membrane-like individually; rim level 0.594)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.32, rim/outside 1.85 (aggregate of 100 individuals; 10/100 membrane-like individually; rim level 0.197)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #10 (t=730, R_eq 4.44): ['cargo c']; #11 (t=760, R_eq 2.82): ['surfactant s']; #13 (t=760, R_eq 2.82): ['surfactant s']; #41 (t=1090, R_eq 3.19): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
