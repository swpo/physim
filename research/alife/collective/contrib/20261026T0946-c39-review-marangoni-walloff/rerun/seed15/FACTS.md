# Evidence pack: active-nematic-marangoni (seed 15)

- world: `../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 427s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/c39-mar-walloff-wip/rerun/seed15 --seeds 15 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8395, 0.5706], min area 6 px

## Measurements
- components: final 30, mean 22.5, max 33; occupancy final 0.09
- tracks: 106; persistent (alive >= 50% of run): 12; longest 168 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.41 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 31, 30], H1 [0, 0, 0]
- motion: 56 long-lived tracks moved >= 1 body length; max speed 0.305/time; max body lengths 11.2
- replication (lineage window K = 20 frames = time 100, default): splits 39, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 3, merges 18, merge/split ratio 0.462, nucleations 9
- channel total drift (end/start - 1): [-0.5049, -0.4247, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 118: holes 0, rim-vs-core 0.72, rim-vs-outside 0.36, heterogeneity 0.23; core [0.953, 0.813, 0.403, 0.424] rim [0.752, 0.516, 0.88, 0.013]
  - track 30 at frame 128: holes 0, rim-vs-core 0.70, rim-vs-outside 0.33, heterogeneity 0.23; core [0.937, 0.739, 0.444, 0.375] rim [0.713, 0.435, 0.905, 0.01]
  - track 34 at frame 131: holes 0, rim-vs-core 0.71, rim-vs-outside 0.33, heterogeneity 0.22; core [0.943, 0.663, 0.416, 0.415] rim [0.735, 0.399, 0.892, 0.011]
  - track 35 at frame 131: holes 0, rim-vs-core 0.73, rim-vs-outside 0.31, heterogeneity 0.24; core [0.937, 0.733, 0.46, 0.462] rim [0.735, 0.445, 0.921, 0.02]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 152 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 4.66 (aggregate of 152 individuals; 1/152 membrane-like individually; rim level 0.712)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 8.94 (aggregate of 152 individuals; 8/152 membrane-like individually; rim level 0.537)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 3.33 (aggregate of 152 individuals; 75/152 membrane-like individually; rim level 0.601)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.412, rim/outside 1.98 (aggregate of 152 individuals; 19/152 membrane-like individually; rim level 0.126)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=590, R_eq 4.18): none; #30 (t=640, R_eq 3.95): ['surfactant s']; #34 (t=655, R_eq 4.18): none; #35 (t=655, R_eq 3.74): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 152 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
