# Evidence pack: active-nematic-marangoni-turnover (seed 81)

- world: `../../../../20261026T1858-c45-marangoni-turnover-tuning/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 151 frames x 100 steps x dt 0.05 = time 750; grid [128, 128]; wall 329s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1858-c45-marangoni-turnover-tuning/world.py --out collective/contrib/20261027T0026-c47-review-marangoni-turnover/runs/p010_redist/seed81 --seeds 81 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.826, 0.5631], min area 6 px

## Measurements
- components: final 27, mean 14.9, max 28; occupancy final 0.08
- tracks: 89; persistent (alive >= 50% of run): 2; longest 76 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.23 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 28, 27], H1 [0, 0, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 0.366/time; max body lengths 7.4
- replication (lineage window K = 20 frames = time 100, default): splits 40, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 6, merges 2, merge/split ratio 0.05, nucleations 7
- channel total drift (end/start - 1): [-0.4912, -0.4477, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 31 at frame 113: holes 0, rim-vs-core 0.49, rim-vs-outside 0.35, heterogeneity 0.12; core [0.935, 0.824, 0.433, 0.0] rim [0.75, 0.557, 0.805, 0.0]
  - track 13 at frame 68: holes 0, rim-vs-core 0.70, rim-vs-outside 0.38, heterogeneity 0.17; core [0.974, 0.837, 0.409, 0.0] rim [0.767, 0.501, 0.984, 0.0]
  - track 21 at frame 89: holes 0, rim-vs-core 0.62, rim-vs-outside 0.35, heterogeneity 0.16; core [0.97, 0.686, 0.404, 0.0] rim [0.765, 0.437, 0.929, 0.0]
  - track 65 at frame 135: holes 0, rim-vs-core 0.56, rim-vs-outside 0.35, heterogeneity 0.14; core [0.939, 0.902, 0.451, 0.0] rim [0.739, 0.584, 0.872, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 101 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 4.39 (aggregate of 101 individuals; 0/101 membrane-like individually; rim level 0.707)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.77, rim/outside 8.2 (aggregate of 101 individuals; 6/101 membrane-like individually; rim level 0.558)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 3.36 (aggregate of 101 individuals; 50/101 membrane-like individually; rim level 0.611)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 101 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #31 (t=565, R_eq 4.22): none; #13 (t=340, R_eq 4.65): ['surfactant s']; #21 (t=445, R_eq 4.37): none; #65 (t=675, R_eq 3.87): none

## Warnings
- radial: 4 of 101 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
