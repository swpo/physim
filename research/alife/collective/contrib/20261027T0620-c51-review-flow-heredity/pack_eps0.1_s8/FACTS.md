# Evidence pack: reacting-thermals (seed 8)

- world: `../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 801 frames x 25 steps x dt 0.04 = time 800; grid [128, 128]; wall 81s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0620-c51-review-flow-heredity/world.py --out collective/contrib/20261027T0620-c51-review-flow-heredity/pack_eps0.1_s8 --seeds 8 --frames 800 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.7167], min area 6 px

## Measurements
- components: final 31, mean 20.1, max 45; occupancy final 0.03
- tracks: 665; persistent (alive >= 50% of run): 0; longest 193 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 35, 34], H1 [0, 0, 0]
- motion: 263 long-lived tracks moved >= 1 body length; max speed 1.27/time; max body lengths 34.6
- replication (lineage window K = 20 frames = time 20, default): splits 140, persistent splits 47 (0 more failed only because the siblings re-merged within K), max generation 7, merges 28, merge/split ratio 0.2, nucleations 315
- channel total drift (end/start - 1): [-0.8387, -0.3679, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 163 at frame 376: holes 0, rim-vs-core 0.18, rim-vs-outside 0.46, heterogeneity 0.07; core [0.878, 0.029, 1.0, 0.095] rim [0.729, 0.055, 0.897, 0.071]
  - track 286 at frame 504: holes 0, rim-vs-core 0.27, rim-vs-outside 0.52, heterogeneity 0.10; core [0.988, 0.012, 0.931, 0.224] rim [0.753, 0.077, 0.819, 0.165]
  - track 388 at frame 592: holes 0, rim-vs-core 0.39, rim-vs-outside 0.52, heterogeneity 0.11; core [0.977, 0.049, 0.954, 0.377] rim [0.717, 0.103, 0.689, 0.268]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 98 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 6.52 (aggregate of 98 individuals; 1/98 membrane-like individually; rim level 0.708)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.39, rim/outside 0.628 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.206)
  - radial label a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 5.3 (aggregate of 98 individuals; 1/98 membrane-like individually; rim level 0.619)
  - radial label b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 3.75 (aggregate of 98 individuals; 1/98 membrane-like individually; rim level 0.246)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #163 (t=376, R_eq 2.39): ['label b']; #317 (t=551, R_eq 1.87): none; #286 (t=504, R_eq 2.26): none; #388 (t=592, R_eq 2.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 98 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
