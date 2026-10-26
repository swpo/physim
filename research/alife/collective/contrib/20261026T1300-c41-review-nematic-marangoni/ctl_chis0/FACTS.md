# Evidence pack: active-nematic-marangoni (seed 31)

- world: `../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 569s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T1300-c41-review-nematic-marangoni/ctl_chis0 --seeds 31 --frames 200 --no-movie`
- segmentation: matter > 0.52 of robust range [-0.8292, 0.7505], min area 6 px

## Measurements
- components: final 36, mean 27.1, max 39; occupancy final 0.07
- tracks: 133; persistent (alive >= 50% of run): 12; longest 163 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 36, 35], H1 [0, 0, 0]
- motion: 56 long-lived tracks moved >= 1 body length; max speed 0.177/time; max body lengths 5.5
- replication (lineage window K = 20 frames = time 100, default): splits 61, persistent splits 34 (0 more failed only because the siblings re-merged within K), max generation 7, merges 3, merge/split ratio 0.049, nucleations 8
- channel total drift (end/start - 1): [-0.4988, -0.3388, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 119: holes 0, rim-vs-core 0.39, rim-vs-outside 0.38, heterogeneity 0.10; core [0.961, 0.727, 0.977, 0.094] rim [0.706, 0.476, 0.829, 0.12]
  - track 18 at frame 106: holes 0, rim-vs-core 0.43, rim-vs-outside 0.40, heterogeneity 0.13; core [0.955, 0.805, 0.984, 0.096] rim [0.703, 0.488, 0.84, 0.127]
  - track 37 at frame 129: holes 0, rim-vs-core 0.38, rim-vs-outside 0.38, heterogeneity 0.09; core [0.919, 0.954, 0.917, 0.105] rim [0.712, 0.658, 0.79, 0.135]
  - track 88 at frame 168: holes 0, rim-vs-core 0.33, rim-vs-outside 0.37, heterogeneity 0.09; core [0.877, 0.79, 0.861, 0.103] rim [0.691, 0.543, 0.737, 0.138]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 178 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 5.49 (aggregate of 178 individuals; 0/178 membrane-like individually; rim level 0.771)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.727, rim/outside 9.15 (aggregate of 178 individuals; 0/178 membrane-like individually; rim level 0.601)
  - radial surfactant s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 2.2 (aggregate of 178 individuals; 0/178 membrane-like individually; rim level 0.8)
  - radial cargo c: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.32, rim/outside 0.645 (aggregate of 178 individuals; 0/178 membrane-like individually; rim level 0.241)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #23 (t=595, R_eq 3.48): none; #18 (t=530, R_eq 3.61): none; #37 (t=645, R_eq 3.19): none; #88 (t=840, R_eq 3.04): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
