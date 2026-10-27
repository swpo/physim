# Evidence pack: reacting-thermals (seed 8)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 36s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/20261027T0230-c51-review-thermals/rerun --seeds 7 8 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.7149], min area 6 px

## Measurements
- components: final 21, mean 15.9, max 45; occupancy final 0.02
- tracks: 398; persistent (alive >= 50% of run): 0; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 28, 24], H1 [0, 0, 0]
- motion: 150 long-lived tracks moved >= 1 body length; max speed 1.23/time; max body lengths 23.9
- replication (lineage window K = 20 frames = time 20, default): splits 100, persistent splits 38 (0 more failed only because the siblings re-merged within K), max generation 6, merges 21, merge/split ratio 0.21, nucleations 137
- channel total drift (end/start - 1): [-0.8644, -0.3213, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 208 at frame 479: holes 0, rim-vs-core 0.28, rim-vs-outside 0.56, heterogeneity 0.14; core [0.922, 0.097, 0.341, 0.971] rim [0.716, 0.135, 0.361, 0.784]
  - track 191 at frame 434: holes 0, rim-vs-core 0.31, rim-vs-outside 0.63, heterogeneity 0.15; core [0.969, 0.113, 0.354, 0.995] rim [0.725, 0.169, 0.309, 0.821]
  - track 319 at frame 555: holes 0, rim-vs-core 0.25, rim-vs-outside 0.71, heterogeneity 0.14; core [0.978, 0.102, 0.378, 1.0] rim [0.771, 0.15, 0.362, 0.874]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 5.23 (aggregate of 78 individuals; 4/78 membrane-like individually; rim level 0.629)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.91, rim/outside 0.678 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.249)
  - radial vorticity: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 1.05 (aggregate of 78 individuals; 16/78 membrane-like individually; rim level 0.481)
  - radial burn r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 6.22 (aggregate of 78 individuals; 7/78 membrane-like individually; rim level 0.646)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #208 (t=479, R_eq 2.82): ['heat T', 'burn r']; #191 (t=434, R_eq 2.11): none; #237 (t=489, R_eq 1.95): none; #319 (t=555, R_eq 2.03): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
