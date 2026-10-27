# Evidence pack: active-nematic-marangoni-turnover (seed 84)

- world: `../../20261026T1858-c45-marangoni-turnover-tuning/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 151 frames x 100 steps x dt 0.05 = time 750; grid [128, 128]; wall 208s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1858-c45-marangoni-turnover-tuning/world.py --out collective/contrib/20261027T0311-c51-review-marangoni-turnover/p0.20 --seeds 84 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8086, 0.5431], min area 6 px

## Measurements
- components: final 11, mean 9.4, max 15; occupancy final 0.04
- tracks: 71; persistent (alive >= 50% of run): 0; longest 46 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 13, 11], H1 [1, 0, 0]
- motion: 31 long-lived tracks moved >= 1 body length; max speed 0.357/time; max body lengths 5.5
- replication (lineage window K = 20 frames = time 100, default): splits 31, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.032, nucleations 8
- channel total drift (end/start - 1): [-0.5468, -0.725, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 67: holes 0, rim-vs-core 0.55, rim-vs-outside 0.41, heterogeneity 0.14; core [0.956, 0.931, 0.484, 0.0] rim [0.771, 0.656, 0.919, 0.0]
  - track 31 at frame 79: holes 0, rim-vs-core 0.49, rim-vs-outside 0.34, heterogeneity 0.14; core [0.957, 0.723, 0.477, 0.0] rim [0.769, 0.5, 0.873, 0.0]
  - track 24 at frame 64: holes 0, rim-vs-core 0.57, rim-vs-outside 0.37, heterogeneity 0.15; core [0.973, 0.83, 0.463, 0.0] rim [0.781, 0.541, 0.917, 0.0]
  - track 61 at frame 140: holes 0, rim-vs-core 0.53, rim-vs-outside 0.41, heterogeneity 0.14; core [0.959, 0.945, 0.444, 0.0] rim [0.758, 0.671, 0.848, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 4.58 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.723)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.853, rim/outside 8.05 (aggregate of 62 individuals; 7/62 membrane-like individually; rim level 0.598)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 3.27 (aggregate of 62 individuals; 29/62 membrane-like individually; rim level 0.626)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 62 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #25 (t=335, R_eq 4.33): none; #31 (t=395, R_eq 4.37): none; #24 (t=320, R_eq 3.83): ['surfactant s']; #61 (t=700, R_eq 4.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 62 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
