# Evidence pack: active-nematic-marangoni-turnover (seed 80)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 151 frames x 100 steps x dt 0.05 = time 750; grid [128, 128]; wall 275s; status ok
- command: `python -m labkit.run /tmp/claude-0/mt/world.py --out /tmp/claude-0/mt/runs/tune_p0.20_redist/seed80 --seeds 80 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8126, 0.5551], min area 6 px

## Measurements
- components: final 8, mean 12.2, max 20; occupancy final 0.03
- tracks: 110; persistent (alive >= 50% of run): 0; longest 53 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 8, 7], H1 [1, 0, 0]
- motion: 30 long-lived tracks moved >= 1 body length; max speed 0.44/time; max body lengths 8.3
- replication (lineage window K = 20 frames = time 100, default): splits 45, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 0.089, nucleations 14
- channel total drift (end/start - 1): [-0.5046, -0.7939, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 52 at frame 93: holes 0, rim-vs-core 0.57, rim-vs-outside 0.35, heterogeneity 0.14; core [0.957, 0.793, 0.465, 0.0] rim [0.752, 0.515, 0.918, 0.0]
  - track 71 at frame 113: holes 0, rim-vs-core 0.56, rim-vs-outside 0.40, heterogeneity 0.14; core [0.956, 0.899, 0.468, 0.0] rim [0.762, 0.63, 0.925, 0.0]
  - track 17 at frame 45: holes 0, rim-vs-core 0.69, rim-vs-outside 0.52, heterogeneity 0.17; core [0.988, 0.991, 0.364, 0.0] rim [0.76, 0.784, 0.983, 0.0]
  - track 12 at frame 40: holes 0, rim-vs-core 0.58, rim-vs-outside 0.36, heterogeneity 0.14; core [0.969, 0.93, 0.392, 0.0] rim [0.752, 0.575, 0.8, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 80 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 4.32 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.708)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.797, rim/outside 7.88 (aggregate of 80 individuals; 7/80 membrane-like individually; rim level 0.57)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 3.28 (aggregate of 80 individuals; 41/80 membrane-like individually; rim level 0.595)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 80 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #52 (t=465, R_eq 4.22): none; #71 (t=565, R_eq 4.79): none; #17 (t=225, R_eq 4.95): none; #12 (t=200, R_eq 3.7): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 80 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
