# Evidence pack: active-nematic-marangoni-turnover (seed 81)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 693s; status ok
- command: `python -m labkit.run /tmp/claude-0/mt/world.py --out /tmp/claude-0/mt/runs/long_p0.10_redist/seed81 --seeds 81 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8288, 0.5863], min area 6 px

## Measurements
- components: final 19, mean 20.8, max 30; occupancy final 0.08
- tracks: 230; persistent (alive >= 50% of run): 0; longest 169 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 21, 18], H1 [1, 0, 0]
- motion: 130 long-lived tracks moved >= 1 body length; max speed 0.366/time; max body lengths 7.9
- replication (lineage window K = 20 frames = time 100, default): splits 105, persistent splits 60 (0 more failed only because the siblings re-merged within K), max generation 9, merges 14, merge/split ratio 0.133, nucleations 7
- channel total drift (end/start - 1): [-0.4912, -0.4965, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 131 at frame 316: holes 0, rim-vs-core 0.62, rim-vs-outside 0.32, heterogeneity 0.15; core [0.949, 0.725, 0.468, 0.0] rim [0.731, 0.417, 0.964, 0.0]
  - track 138 at frame 319: holes 0, rim-vs-core 0.58, rim-vs-outside 0.31, heterogeneity 0.14; core [0.952, 0.64, 0.457, 0.0] rim [0.75, 0.393, 0.944, 0.0]
  - track 54 at frame 175: holes 0, rim-vs-core 0.63, rim-vs-outside 0.35, heterogeneity 0.16; core [0.95, 0.717, 0.434, 0.0] rim [0.729, 0.424, 0.948, 0.0]
  - track 209 at frame 380: holes 0, rim-vs-core 0.58, rim-vs-outside 0.41, heterogeneity 0.15; core [0.957, 0.905, 0.367, 0.0] rim [0.737, 0.568, 0.789, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 130 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 4.2 (aggregate of 130 individuals; 1/130 membrane-like individually; rim level 0.677)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 7.61 (aggregate of 130 individuals; 10/130 membrane-like individually; rim level 0.521)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 3.02 (aggregate of 130 individuals; 43/130 membrane-like individually; rim level 0.56)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 130 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #131 (t=1580, R_eq 4.03): none; #138 (t=1595, R_eq 3.91): none; #54 (t=875, R_eq 4.44): none; #209 (t=1900, R_eq 3.87): ['surfactant s']

## Warnings
- radial: 6 of 130 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
