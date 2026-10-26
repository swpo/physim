# Evidence pack: active-nematic-marangoni (seed 64)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 535s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/minority/scout/seed64 --seeds 64 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8354, 0.5613], min area 6 px

## Measurements
- components: final 29, mean 17.0, max 30; occupancy final 0.09
- tracks: 78; persistent (alive >= 50% of run): 4; longest 115 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.45 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 29, 29], H1 [0, 0, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.341/time; max body lengths 9.8
- replication (lineage window K = 20 frames = time 100, default): splits 33, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 5, merges 8, merge/split ratio 0.242, nucleations 4
- channel total drift (end/start - 1): [-0.4993, -0.4385, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 139: holes 0, rim-vs-core 0.73, rim-vs-outside 0.33, heterogeneity 0.24; core [0.94, 0.852, 0.437, 0.443] rim [0.729, 0.506, 0.87, 0.012]
  - track 28 at frame 148: holes 0, rim-vs-core 0.81, rim-vs-outside 0.35, heterogeneity 0.26; core [0.962, 0.808, 0.426, 0.425] rim [0.745, 0.441, 0.971, 0.01]
  - track 30 at frame 148: holes 0, rim-vs-core 0.69, rim-vs-outside 0.30, heterogeneity 0.23; core [0.945, 0.646, 0.43, 0.461] rim [0.753, 0.411, 0.867, 0.021]
  - track 67 at frame 187: holes 0, rim-vs-core 0.75, rim-vs-outside 0.36, heterogeneity 0.23; core [0.957, 0.875, 0.366, 0.409] rim [0.748, 0.499, 0.836, 0.013]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 118 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 4.55 (aggregate of 118 individuals; 1/118 membrane-like individually; rim level 0.707)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 8.43 (aggregate of 118 individuals; 9/118 membrane-like individually; rim level 0.54)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 3.25 (aggregate of 118 individuals; 52/118 membrane-like individually; rim level 0.607)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.416, rim/outside 1.92 (aggregate of 118 individuals; 12/118 membrane-like individually; rim level 0.139)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #21 (t=695, R_eq 3.87): ['surfactant s']; #28 (t=740, R_eq 4.41): ['surfactant s']; #30 (t=740, R_eq 4.41): ['order |Q|', 'cargo c']; #67 (t=935, R_eq 3.19): ['surfactant s']

## Warnings
- radial: 3 of 118 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
