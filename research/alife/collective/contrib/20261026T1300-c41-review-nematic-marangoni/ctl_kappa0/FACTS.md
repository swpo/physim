# Evidence pack: active-nematic-marangoni (seed 31)

- world: `../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 507s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T1300-c41-review-nematic-marangoni/ctl_kappa0 --seeds 31 --frames 200 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8395, 0.5794], min area 6 px

## Measurements
- components: final 30, mean 23.0, max 33; occupancy final 0.10
- tracks: 95; persistent (alive >= 50% of run): 16; longest 157 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.08 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 30, 27], H1 [0, 0, 0]
- motion: 52 long-lived tracks moved >= 1 body length; max speed 0.315/time; max body lengths 11.5
- replication (lineage window K = 20 frames = time 100, default): splits 38, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 4, merges 11, merge/split ratio 0.289, nucleations 8
- channel total drift (end/start - 1): [-0.4988, -0.3844, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 111: holes 0, rim-vs-core 0.51, rim-vs-outside 0.40, heterogeneity 0.14; core [0.94, 0.932, 0.364, 0.754] rim [0.749, 0.612, 0.707, 0.715]
  - track 22 at frame 123: holes 0, rim-vs-core 0.57, rim-vs-outside 0.36, heterogeneity 0.14; core [0.945, 0.761, 0.399, 0.879] rim [0.752, 0.484, 0.852, 0.842]
  - track 25 at frame 124: holes 0, rim-vs-core 0.59, rim-vs-outside 0.32, heterogeneity 0.16; core [0.958, 0.565, 0.369, 0.884] rim [0.753, 0.337, 0.872, 0.837]
  - track 55 at frame 146: holes 0, rim-vs-core 0.58, rim-vs-outside 0.41, heterogeneity 0.14; core [0.962, 0.899, 0.319, 0.834] rim [0.764, 0.599, 0.769, 0.805]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 155 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 4.54 (aggregate of 155 individuals; 0/155 membrane-like individually; rim level 0.709)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.777, rim/outside 8.95 (aggregate of 155 individuals; 6/155 membrane-like individually; rim level 0.53)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 3.32 (aggregate of 155 individuals; 79/155 membrane-like individually; rim level 0.6)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.948, rim/outside 1.27 (aggregate of 155 individuals; 0/155 membrane-like individually; rim level 0.772)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #17 (t=555, R_eq 3.87): none; #22 (t=615, R_eq 3.83): none; #25 (t=620, R_eq 4.26): ['order |Q|']; #55 (t=730, R_eq 3.57): ['surfactant s']

## Warnings
- radial: 3 of 155 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
