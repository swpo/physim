# Evidence pack: active-nematic-marangoni-turnover (seed 82)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 682s; status ok
- command: `python -m labkit.run /tmp/claude-0/mt/world.py --out /tmp/claude-0/mt/runs/long_nodil/seed82 --seeds 82 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.843, 0.5762], min area 6 px

## Measurements
- components: final 30, mean 28.1, max 33; occupancy final 0.09
- tracks: 157; persistent (alive >= 50% of run): 17; longest 371 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 30, 30], H1 [0, 0, 0]
- motion: 93 long-lived tracks moved >= 1 body length; max speed 0.364/time; max body lengths 14.8
- replication (lineage window K = 20 frames = time 100, default): splits 57, persistent splits 40 (0 more failed only because the siblings re-merged within K), max generation 6, merges 33, merge/split ratio 0.579, nucleations 10
- channel total drift (end/start - 1): [-0.5029, -0.3976, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 215: holes 0, rim-vs-core 0.60, rim-vs-outside 0.31, heterogeneity 0.16; core [0.945, 0.709, 0.39, 0.0] rim [0.752, 0.433, 0.881, 0.0]
  - track 32 at frame 225: holes 0, rim-vs-core 0.60, rim-vs-outside 0.37, heterogeneity 0.14; core [0.953, 0.84, 0.367, 0.0] rim [0.754, 0.524, 0.834, 0.0]
  - track 46 at frame 239: holes 0, rim-vs-core 0.58, rim-vs-outside 0.32, heterogeneity 0.14; core [0.941, 0.65, 0.429, 0.0] rim [0.742, 0.415, 0.919, 0.0]
  - track 150 at frame 390: holes 0, rim-vs-core 0.59, rim-vs-outside 0.37, heterogeneity 0.14; core [0.949, 0.907, 0.365, 0.0] rim [0.757, 0.559, 0.798, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 181 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 4.7 (aggregate of 181 individuals; 0/181 membrane-like individually; rim level 0.707)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.756, rim/outside 9.45 (aggregate of 181 individuals; 12/181 membrane-like individually; rim level 0.53)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 3.28 (aggregate of 181 individuals; 99/181 membrane-like individually; rim level 0.595)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 181 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #22 (t=1075, R_eq 4.07): none; #32 (t=1125, R_eq 3.7): none; #46 (t=1195, R_eq 4.3): none; #150 (t=1950, R_eq 3.57): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 181 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
