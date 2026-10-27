# Evidence pack: active-nematic-marangoni-turnover (seed 83)

- world: `../../../20261026T1924-c45-marangoni-turnover-long/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 744s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1924-c45-marangoni-turnover-long/world.py --out collective/contrib/c49rev7/runs/nodil_s83 --seeds 83 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.842, 0.5796], min area 6 px

## Measurements
- components: final 29, mean 26.5, max 34; occupancy final 0.09
- tracks: 166; persistent (alive >= 50% of run): 11; longest 350 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.82 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 29, 28], H1 [0, 0, 0]
- motion: 94 long-lived tracks moved >= 1 body length; max speed 0.282/time; max body lengths 15.1
- replication (lineage window K = 20 frames = time 100, default): splits 61, persistent splits 34 (0 more failed only because the siblings re-merged within K), max generation 5, merges 35, merge/split ratio 0.574, nucleations 8
- channel total drift (end/start - 1): [-0.5055, -0.4642, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 229: holes 0, rim-vs-core 0.54, rim-vs-outside 0.34, heterogeneity 0.15; core [0.931, 0.777, 0.462, 0.0] rim [0.743, 0.534, 0.901, 0.0]
  - track 56 at frame 259: holes 0, rim-vs-core 0.52, rim-vs-outside 0.35, heterogeneity 0.13; core [0.934, 0.797, 0.386, 0.0] rim [0.735, 0.503, 0.766, 0.0]
  - track 65 at frame 262: holes 0, rim-vs-core 0.63, rim-vs-outside 0.37, heterogeneity 0.15; core [0.964, 0.89, 0.319, 0.0] rim [0.759, 0.506, 0.775, 0.0]
  - track 144 at frame 370: holes 0, rim-vs-core 0.52, rim-vs-outside 0.40, heterogeneity 0.13; core [0.95, 0.921, 0.326, 0.0] rim [0.763, 0.627, 0.707, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 171 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 4.7 (aggregate of 171 individuals; 0/171 membrane-like individually; rim level 0.711)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 9.46 (aggregate of 171 individuals; 8/171 membrane-like individually; rim level 0.538)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 3.21 (aggregate of 171 individuals; 75/171 membrane-like individually; rim level 0.589)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 171 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #25 (t=1145, R_eq 4.3): none; #56 (t=1295, R_eq 3.99): ['surfactant s']; #65 (t=1310, R_eq 3.09): ['surfactant s']; #144 (t=1850, R_eq 3.7): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 171 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
