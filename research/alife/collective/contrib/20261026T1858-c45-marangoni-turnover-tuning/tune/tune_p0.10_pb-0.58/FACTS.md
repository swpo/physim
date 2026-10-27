# Evidence pack: active-nematic-marangoni-turnover (seed 80)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 151 frames x 100 steps x dt 0.05 = time 750; grid [128, 128]; wall 263s; status ok
- command: `python -m labkit.run /tmp/claude-0/mt/world.py --out /tmp/claude-0/mt/runs/tune_p0.10_pb-0.58/seed80 --seeds 80 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8341, 0.5775], min area 6 px

## Measurements
- components: final 18, mean 20.0, max 28; occupancy final 0.06
- tracks: 118; persistent (alive >= 50% of run): 3; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 17], H1 [2, 0, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.268/time; max body lengths 7.4
- replication (lineage window K = 20 frames = time 100, default): splits 44, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 3, merges 11, merge/split ratio 0.25, nucleations 19
- channel total drift (end/start - 1): [-0.5195, -0.5326, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 50 at frame 101: holes 0, rim-vs-core 0.59, rim-vs-outside 0.42, heterogeneity 0.14; core [0.977, 0.931, 0.256, 0.0] rim [0.793, 0.61, 0.721, 0.0]
  - track 4 at frame 54: holes 0, rim-vs-core 0.56, rim-vs-outside 0.39, heterogeneity 0.14; core [0.955, 0.918, 0.356, 0.0] rim [0.755, 0.608, 0.782, 0.0]
  - track 35 at frame 74: holes 0, rim-vs-core 0.53, rim-vs-outside 0.33, heterogeneity 0.14; core [0.942, 0.769, 0.436, 0.0] rim [0.751, 0.516, 0.857, 0.0]
  - track 57 at frame 89: holes 0, rim-vs-core 0.69, rim-vs-outside 0.35, heterogeneity 0.16; core [0.965, 0.847, 0.335, 0.0] rim [0.755, 0.451, 0.866, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 128 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 4.21 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.686)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 7.93 (aggregate of 128 individuals; 8/128 membrane-like individually; rim level 0.542)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 3.25 (aggregate of 128 individuals; 56/128 membrane-like individually; rim level 0.574)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 128 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #50 (t=505, R_eq 3.24): ['surfactant s']; #4 (t=270, R_eq 3.74): none; #35 (t=370, R_eq 4.03): none; #57 (t=445, R_eq 2.82): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 128 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
