# Evidence pack: active-nematic-marangoni-turnover (seed 83)

- world: `../../../../20261026T1924-c45-marangoni-turnover-long/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 891s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1924-c45-marangoni-turnover-long/world.py --out collective/contrib/20261027T0033-c47-review-marangoni-turnover-long/runs/redist/seed83 --seeds 83 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8263, 0.5787], min area 6 px

## Measurements
- components: final 24, mean 18.7, max 30; occupancy final 0.07
- tracks: 257; persistent (alive >= 50% of run): 0; longest 114 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 24, 23], H1 [1, 0, 0]
- motion: 124 long-lived tracks moved >= 1 body length; max speed 0.477/time; max body lengths 7.2
- replication (lineage window K = 20 frames = time 100, default): splits 115, persistent splits 58 (0 more failed only because the siblings re-merged within K), max generation 11, merges 18, merge/split ratio 0.157, nucleations 8
- channel total drift (end/start - 1): [-0.5055, -0.521, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 58 at frame 171: holes 0, rim-vs-core 0.58, rim-vs-outside 0.34, heterogeneity 0.15; core [0.962, 0.671, 0.409, 0.0] rim [0.761, 0.444, 0.909, 0.0]
  - track 176 at frame 346: holes 0, rim-vs-core 0.57, rim-vs-outside 0.33, heterogeneity 0.14; core [0.94, 0.682, 0.463, 0.0] rim [0.746, 0.446, 0.943, 0.0]
  - track 94 at frame 218: holes 0, rim-vs-core 0.55, rim-vs-outside 0.39, heterogeneity 0.13; core [0.96, 0.916, 0.319, 0.0] rim [0.767, 0.596, 0.716, 0.0]
  - track 233 at frame 383: holes 0, rim-vs-core 0.56, rim-vs-outside 0.35, heterogeneity 0.14; core [0.954, 0.771, 0.395, 0.0] rim [0.755, 0.498, 0.844, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 123 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.781, rim/outside 4.28 (aggregate of 123 individuals; 1/123 membrane-like individually; rim level 0.686)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.774, rim/outside 8.11 (aggregate of 123 individuals; 9/123 membrane-like individually; rim level 0.524)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 3.21 (aggregate of 123 individuals; 48/123 membrane-like individually; rim level 0.59)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 123 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #58 (t=855, R_eq 4.26): none; #176 (t=1730, R_eq 4.3): none; #94 (t=1090, R_eq 3.39): ['surfactant s']; #233 (t=1915, R_eq 4.15): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 123 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
