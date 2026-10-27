# Evidence pack: reacting-thermals (seed 21)

- world: `../../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [192, 192]; wall 152s; status ok
- command: `python -m labkit.run /tmp/claude-0/tc/world.py --out /tmp/claude-0/tc/res15/seed21 --seeds 21 --size 192 192 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7549], min area 6 px

## Measurements
- components: final 40, mean 22.6, max 51; occupancy final 0.03
- tracks: 446; persistent (alive >= 50% of run): 0; longest 269 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [43, 43, 37], H1 [0, 0, 0]
- motion: 200 long-lived tracks moved >= 1 body length; max speed 1.56/time; max body lengths 36.4
- replication (lineage window K = 20 frames = time 20, default): splits 159, persistent splits 65 (0 more failed only because the siblings re-merged within K), max generation 9, merges 7, merge/split ratio 0.044, nucleations 83
- channel total drift (end/start - 1): [-0.8572, -0.361, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 220 at frame 469: holes 0, rim-vs-core 0.32, rim-vs-outside 0.51, heterogeneity 0.15; core [0.887, 0.152, 0.488, 0.981] rim [0.655, 0.2, 0.454, 0.768]
  - track 247 at frame 469: holes 0, rim-vs-core 0.35, rim-vs-outside 0.54, heterogeneity 0.15; core [0.916, 0.136, 0.522, 0.98] rim [0.657, 0.181, 0.507, 0.747]
  - track 253 at frame 479: holes 0, rim-vs-core 0.37, rim-vs-outside 0.58, heterogeneity 0.17; core [0.964, 0.143, 0.452, 0.992] rim [0.668, 0.209, 0.444, 0.788]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 144 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 6.13 (aggregate of 144 individuals; 0/144 membrane-like individually; rim level 0.644)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.24, rim/outside 0.726 (aggregate of 144 individuals; 0/144 membrane-like individually; rim level 0.265)
  - radial vorticity: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 1.02 (aggregate of 144 individuals; 12/144 membrane-like individually; rim level 0.472)
  - radial burn r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 8.54 (aggregate of 144 individuals; 0/144 membrane-like individually; rim level 0.684)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #220 (t=469, R_eq 3.43): none; #247 (t=469, R_eq 3.29): none; #253 (t=479, R_eq 3.24): ['vorticity']; #412 (t=585, R_eq 2.03): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 144 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
