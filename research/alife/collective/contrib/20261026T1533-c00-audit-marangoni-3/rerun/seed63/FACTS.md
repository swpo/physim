# Evidence pack: active-nematic-marangoni (seed 63)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 566s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/minority/scout/seed63 --seeds 63 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.84, 0.5639], min area 6 px

## Measurements
- components: final 29, mean 19.5, max 31; occupancy final 0.09
- tracks: 100; persistent (alive >= 50% of run): 7; longest 140 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.91 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 28], H1 [0, 0, 0]
- motion: 51 long-lived tracks moved >= 1 body length; max speed 0.371/time; max body lengths 7.3
- replication (lineage window K = 20 frames = time 100, default): splits 40, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 5, merges 15, merge/split ratio 0.375, nucleations 6
- channel total drift (end/start - 1): [-0.4864, -0.4192, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 131: holes 0, rim-vs-core 0.70, rim-vs-outside 0.34, heterogeneity 0.22; core [0.936, 0.769, 0.455, 0.45] rim [0.753, 0.513, 0.908, 0.016]
  - track 23 at frame 133: holes 0, rim-vs-core 0.72, rim-vs-outside 0.33, heterogeneity 0.23; core [0.954, 0.679, 0.394, 0.467] rim [0.754, 0.437, 0.851, 0.013]
  - track 28 at frame 134: holes 0, rim-vs-core 0.59, rim-vs-outside 0.39, heterogeneity 0.21; core [0.947, 0.745, 0.373, 0.434] rim [0.794, 0.525, 0.74, 0.065]
  - track 90 at frame 185: holes 0, rim-vs-core 0.74, rim-vs-outside 0.32, heterogeneity 0.25; core [0.969, 0.602, 0.379, 0.436] rim [0.766, 0.392, 0.913, 0.01]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 132 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.802, rim/outside 4.51 (aggregate of 132 individuals; 0/132 membrane-like individually; rim level 0.706)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 8.86 (aggregate of 132 individuals; 7/132 membrane-like individually; rim level 0.558)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 3.22 (aggregate of 132 individuals; 59/132 membrane-like individually; rim level 0.589)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.484, rim/outside 2 (aggregate of 132 individuals; 21/132 membrane-like individually; rim level 0.14)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=655, R_eq 4.62): none; #23 (t=665, R_eq 4.18): none; #28 (t=670, R_eq 3.87): none; #90 (t=925, R_eq 4.26): ['order |Q|']

## Warnings
- radial: 6 of 132 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
