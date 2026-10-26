# Evidence pack: active-nematic-marangoni (seed 1)

- world: `../../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 420s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T0505-c34-nematic-marangoni/pack --seeds 0 1 2 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8392, 0.5631], min area 6 px

## Measurements
- components: final 29, mean 17.7, max 31; occupancy final 0.09
- tracks: 99; persistent (alive >= 50% of run): 6; longest 128 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.28 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 29, 29], H1 [0, 0, 0]
- motion: 54 long-lived tracks moved >= 1 body length; max speed 0.333/time; max body lengths 7.0
- replication (lineage window K = 20 frames = time 100, default): splits 41, persistent splits 28 (0 more failed only because the siblings re-merged within K), max generation 5, merges 14, merge/split ratio 0.341, nucleations 4
- channel total drift (end/start - 1): [-0.4928, -0.4115, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 138: holes 0, rim-vs-core 0.74, rim-vs-outside 0.33, heterogeneity 0.24; core [0.939, 0.691, 0.489, 0.494] rim [0.735, 0.441, 0.958, 0.013]
  - track 22 at frame 138: holes 0, rim-vs-core 0.82, rim-vs-outside 0.38, heterogeneity 0.27; core [0.969, 0.913, 0.369, 0.466] rim [0.752, 0.557, 0.924, 0.036]
  - track 32 at frame 143: holes 0, rim-vs-core 0.79, rim-vs-outside 0.39, heterogeneity 0.24; core [0.967, 0.921, 0.345, 0.528] rim [0.772, 0.563, 0.803, 0.026]
  - track 64 at frame 170: holes 0, rim-vs-core 0.80, rim-vs-outside 0.41, heterogeneity 0.23; core [0.963, 0.901, 0.333, 0.581] rim [0.764, 0.608, 0.76, 0.011]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 119 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.782, rim/outside 4.51 (aggregate of 119 individuals; 0/119 membrane-like individually; rim level 0.695)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 8.65 (aggregate of 119 individuals; 11/119 membrane-like individually; rim level 0.543)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 3.23 (aggregate of 119 individuals; 50/119 membrane-like individually; rim level 0.587)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.516, rim/outside 2.12 (aggregate of 119 individuals; 19/119 membrane-like individually; rim level 0.157)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #20 (t=690, R_eq 4.55): ['order |Q|', 'cargo c']; #22 (t=690, R_eq 4.41): ['surfactant s']; #32 (t=715, R_eq 3.34): ['surfactant s']; #64 (t=850, R_eq 3.61): ['surfactant s']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
