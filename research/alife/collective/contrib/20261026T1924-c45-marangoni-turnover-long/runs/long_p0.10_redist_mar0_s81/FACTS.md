# Evidence pack: active-nematic-marangoni-turnover (seed 81)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 654s; status ok
- command: `python -m labkit.run /tmp/claude-0/mt/world.py --out /tmp/claude-0/mt/runs/long_p0.10_redist_mar0/seed81 --seeds 81 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8125, 0.5713], min area 6 px

## Measurements
- components: final 11, mean 9.9, max 14; occupancy final 0.03
- tracks: 132; persistent (alive >= 50% of run): 0; longest 164 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 12, 9], H1 [4, 0, 0]
- motion: 39 long-lived tracks moved >= 1 body length; max speed 0.0762/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 100, default): splits 58, persistent splits 30 (0 more failed only because the siblings re-merged within K), max generation 9, merges 8, merge/split ratio 0.138, nucleations 7
- channel total drift (end/start - 1): [-0.4912, -0.7543, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 158: holes 0, rim-vs-core 0.49, rim-vs-outside 0.40, heterogeneity 0.12; core [0.973, 0.954, 0.368, 0.0] rim [0.79, 0.698, 0.746, 0.0]
  - track 80 at frame 316: holes 0, rim-vs-core 0.52, rim-vs-outside 0.41, heterogeneity 0.13; core [0.971, 0.952, 0.318, 0.0] rim [0.789, 0.706, 0.734, 0.0]
  - track 88 at frame 339: holes 0, rim-vs-core 0.45, rim-vs-outside 0.37, heterogeneity 0.12; core [0.94, 0.864, 0.451, 0.0] rim [0.748, 0.606, 0.763, 0.0]
  - track 109 at frame 387: holes 0, rim-vs-core 0.46, rim-vs-outside 0.38, heterogeneity 0.12; core [0.954, 0.922, 0.388, 0.0] rim [0.764, 0.663, 0.715, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 61 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.846, rim/outside 4.13 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.725)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.85, rim/outside 6.19 (aggregate of 61 individuals; 3/61 membrane-like individually; rim level 0.614)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 2.86 (aggregate of 61 individuals; 35/61 membrane-like individually; rim level 0.617)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 61 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #27 (t=790, R_eq 3.43): ['surfactant s']; #80 (t=1580, R_eq 2.99): ['surfactant s']; #88 (t=1695, R_eq 3.7): ['surfactant s']; #109 (t=1935, R_eq 3.7): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 61 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
