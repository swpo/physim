# Evidence pack: active-nematic-marangoni (seed 70)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 342s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/ms/runs/base/seed70 --seeds 70 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8406, 0.5761], min area 6 px

## Measurements
- components: final 31, mean 22.1, max 31; occupancy final 0.10
- tracks: 90; persistent (alive >= 50% of run): 15; longest 163 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.78 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 30], H1 [0, 0, 0]
- motion: 52 long-lived tracks moved >= 1 body length; max speed 0.299/time; max body lengths 7.3
- replication (lineage window K = 20 frames = time 100, default): splits 36, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 4, merges 11, merge/split ratio 0.306, nucleations 7
- channel total drift (end/start - 1): [-0.4979, -0.3777, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 119: holes 0, rim-vs-core 0.53, rim-vs-outside 0.30, heterogeneity 0.15; core [0.95, 0.679, 0.418, 0.0] rim [0.763, 0.434, 0.855, 0.0]
  - track 20 at frame 126: holes 0, rim-vs-core 0.56, rim-vs-outside 0.33, heterogeneity 0.14; core [0.95, 0.666, 0.413, 0.0] rim [0.755, 0.415, 0.88, 0.0]
  - track 21 at frame 126: holes 0, rim-vs-core 0.48, rim-vs-outside 0.34, heterogeneity 0.13; core [0.918, 0.766, 0.441, 0.0] rim [0.752, 0.545, 0.827, 0.0]
  - track 70 at frame 166: holes 0, rim-vs-core 0.58, rim-vs-outside 0.39, heterogeneity 0.15; core [0.947, 0.874, 0.372, 0.0] rim [0.749, 0.56, 0.818, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 149 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.785, rim/outside 4.58 (aggregate of 149 individuals; 0/149 membrane-like individually; rim level 0.705)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 8.93 (aggregate of 149 individuals; 4/149 membrane-like individually; rim level 0.548)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 3.23 (aggregate of 149 individuals; 63/149 membrane-like individually; rim level 0.591)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 149 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #15 (t=595, R_eq 4.3): ['order |Q|']; #20 (t=630, R_eq 3.99): none; #21 (t=630, R_eq 4.55): none; #70 (t=830, R_eq 3.52): ['surfactant s']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
