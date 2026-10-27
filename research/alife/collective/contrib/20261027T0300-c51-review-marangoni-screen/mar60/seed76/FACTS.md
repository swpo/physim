# Evidence pack: active-nematic-marangoni (seed 76)

- world: `../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 269s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261027T0300-c51-review-marangoni-screen/mar60/seed76 --seeds 76 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.61 of robust range [-0.8311, 0.5266], min area 6 px

## Measurements
- components: final 31, mean 22.4, max 31; occupancy final 0.09
- tracks: 142; persistent (alive >= 50% of run): 9; longest 153 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 31, 29], H1 [0, 0, 0]
- motion: 62 long-lived tracks moved >= 1 body length; max speed 0.443/time; max body lengths 9.4
- replication (lineage window K = 20 frames = time 100, default): splits 54, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 4, merges 25, merge/split ratio 0.463, nucleations 8
- channel total drift (end/start - 1): [-0.495, -0.5508, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 124: holes 0, rim-vs-core 0.52, rim-vs-outside 0.30, heterogeneity 0.13; core [0.938, 0.577, 0.518, 0.0] rim [0.737, 0.335, 0.928, 0.0]
  - track 14 at frame 104: holes 0, rim-vs-core 0.53, rim-vs-outside 0.37, heterogeneity 0.14; core [0.955, 0.882, 0.4, 0.0] rim [0.767, 0.549, 0.773, 0.0]
  - track 62 at frame 145: holes 0, rim-vs-core 0.57, rim-vs-outside 0.36, heterogeneity 0.14; core [0.952, 0.675, 0.508, 0.0] rim [0.748, 0.411, 0.964, 0.0]
  - track 105 at frame 171: holes 0, rim-vs-core 0.54, rim-vs-outside 0.31, heterogeneity 0.15; core [0.958, 0.618, 0.458, 0.0] rim [0.759, 0.31, 0.86, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 150 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 4.33 (aggregate of 150 individuals; 1/150 membrane-like individually; rim level 0.721)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.818, rim/outside 8.77 (aggregate of 150 individuals; 22/150 membrane-like individually; rim level 0.512)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 3.13 (aggregate of 150 individuals; 50/150 membrane-like individually; rim level 0.621)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 150 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #30 (t=620, R_eq 3.87): none; #14 (t=520, R_eq 3.39): ['surfactant s']; #62 (t=725, R_eq 4.26): none; #105 (t=855, R_eq 3.57): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 150 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
