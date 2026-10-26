# Evidence pack: active-nematic-marangoni (seed 7)

- world: `../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 473s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/wip-c33-nm/mar0 --seeds 7 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8254, 0.6082], min area 6 px

## Measurements
- components: final 32, mean 21.5, max 33; occupancy final 0.07
- tracks: 96; persistent (alive >= 50% of run): 10; longest 139 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 32, 32], H1 [1, 0, 0]
- motion: 52 long-lived tracks moved >= 1 body length; max speed 0.0993/time; max body lengths 4.7
- replication (lineage window K = 20 frames = time 100, default): splits 40, persistent splits 32 (0 more failed only because the siblings re-merged within K), max generation 5, merges 8, merge/split ratio 0.2, nucleations 8
- channel total drift (end/start - 1): [-0.4954, -0.3969, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 131: holes 0, rim-vs-core 0.57, rim-vs-outside 0.33, heterogeneity 0.20; core [0.928, 0.809, 0.364, 0.369] rim [0.726, 0.537, 0.658, 0.019]
  - track 27 at frame 133: holes 0, rim-vs-core 0.73, rim-vs-outside 0.35, heterogeneity 0.22; core [0.958, 0.954, 0.325, 0.467] rim [0.747, 0.64, 0.748, 0.012]
  - track 31 at frame 136: holes 0, rim-vs-core 0.66, rim-vs-outside 0.33, heterogeneity 0.21; core [0.93, 0.856, 0.378, 0.455] rim [0.736, 0.583, 0.746, 0.016]
  - track 84 at frame 190: holes 0, rim-vs-core 0.36, rim-vs-outside 0.52, heterogeneity 0.23; core [0.944, 0.871, 0.374, 0.342] rim [0.822, 0.708, 0.63, 0.203]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 142 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.806, rim/outside 4.66 (aggregate of 142 individuals; 0/142 membrane-like individually; rim level 0.75)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.747, rim/outside 7.88 (aggregate of 142 individuals; 0/142 membrane-like individually; rim level 0.626)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.62, rim/outside 2.9 (aggregate of 142 individuals; 107/142 membrane-like individually; rim level 0.583)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.251, rim/outside 1.55 (aggregate of 142 individuals; 15/142 membrane-like individually; rim level 0.136)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #25 (t=655, R_eq 3.09): ['surfactant s']; #27 (t=665, R_eq 3.39): ['surfactant s']; #31 (t=680, R_eq 3.43): ['surfactant s']; #84 (t=950, R_eq 2.76): ['surfactant s']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
