# Evidence pack: active-nematic-marangoni-turnover (seed 81)

- world: `../../../../20261026T1858-c45-marangoni-turnover-tuning/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 151 frames x 100 steps x dt 0.05 = time 750; grid [128, 128]; wall 330s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1858-c45-marangoni-turnover-tuning/world.py --out collective/contrib/20261027T0026-c47-review-marangoni-turnover/runs/p010/seed81 --seeds 81 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8246, 0.5575], min area 6 px

## Measurements
- components: final 23, mean 13.6, max 25; occupancy final 0.07
- tracks: 74; persistent (alive >= 50% of run): 2; longest 85 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.87 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 23, 23], H1 [0, 0, 0]
- motion: 35 long-lived tracks moved >= 1 body length; max speed 0.329/time; max body lengths 5.5
- replication (lineage window K = 20 frames = time 100, default): splits 33, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.03, nucleations 7
- channel total drift (end/start - 1): [-0.5207, -0.4966, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 67: holes 0, rim-vs-core 0.57, rim-vs-outside 0.36, heterogeneity 0.15; core [0.962, 0.802, 0.425, 0.0] rim [0.764, 0.532, 0.885, 0.0]
  - track 7 at frame 61: holes 0, rim-vs-core 0.62, rim-vs-outside 0.44, heterogeneity 0.15; core [0.959, 0.964, 0.442, 0.0] rim [0.749, 0.712, 0.965, 0.0]
  - track 31 at frame 116: holes 0, rim-vs-core 0.60, rim-vs-outside 0.39, heterogeneity 0.14; core [0.97, 0.941, 0.352, 0.0] rim [0.771, 0.61, 0.806, 0.0]
  - track 52 at frame 126: holes 0, rim-vs-core 0.50, rim-vs-outside 0.40, heterogeneity 0.13; core [0.943, 0.918, 0.398, 0.0] rim [0.748, 0.631, 0.757, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 89 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 4.44 (aggregate of 89 individuals; 1/89 membrane-like individually; rim level 0.7)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 8.27 (aggregate of 89 individuals; 4/89 membrane-like individually; rim level 0.571)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 3.19 (aggregate of 89 individuals; 34/89 membrane-like individually; rim level 0.593)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 89 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=335, R_eq 4.44): none; #7 (t=305, R_eq 4.92): none; #31 (t=580, R_eq 3.52): ['surfactant s']; #52 (t=630, R_eq 3.99): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 89 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
