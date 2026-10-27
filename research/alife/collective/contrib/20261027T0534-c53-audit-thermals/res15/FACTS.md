# Evidence pack: reacting-thermals (seed 34)

- world: `../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 40 steps x dt 0.025 (--dt; world META dt 0.04) = time 600; grid [192, 192]; wall 207s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/res15 --seeds 34 --size 192 192 --frames 600 --spf 40 --dt 0.025 --min-area 14 --no-movie`
- segmentation: matter > 0.41 of robust range [0.0, 0.6058], min area 14 px

## Measurements
- components: final 28, mean 24.4, max 44; occupancy final 0.03
- tracks: 399; persistent (alive >= 50% of run): 0; longest 278 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 40, 30], H1 [0, 0, 0]
- motion: 216 long-lived tracks moved >= 1 body length; max speed 1.57/time; max body lengths 28.3
- replication (lineage window K = 20 frames = time 20, default): splits 130, persistent splits 65 (0 more failed only because the siblings re-merged within K), max generation 7, merges 9, merge/split ratio 0.069, nucleations 106
- channel total drift (end/start - 1): [-0.7649, -0.3548, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 146 at frame 277: holes 0, rim-vs-core 0.25, rim-vs-outside 0.38, heterogeneity 0.14; core [0.821, 0.052, 0.456, 0.839] rim [0.653, 0.095, 0.511, 0.666]
  - track 166 at frame 297: holes 0, rim-vs-core 0.21, rim-vs-outside 0.44, heterogeneity 0.12; core [0.828, 0.079, 0.485, 0.886] rim [0.688, 0.109, 0.488, 0.729]
  - track 173 at frame 287: holes 0, rim-vs-core 0.30, rim-vs-outside 0.54, heterogeneity 0.15; core [0.942, 0.065, 0.415, 0.974] rim [0.715, 0.116, 0.424, 0.778]
  - track 298 at frame 519: holes 0, rim-vs-core 0.28, rim-vs-outside 0.46, heterogeneity 0.13; core [0.862, 0.09, 0.385, 0.936] rim [0.669, 0.138, 0.373, 0.734]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 107 components >= 28 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 5.74 (aggregate of 107 individuals; 1/107 membrane-like individually; rim level 0.634)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.12, rim/outside 0.618 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.201)
  - radial vorticity: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.01 (aggregate of 107 individuals; 5/107 membrane-like individually; rim level 0.463)
  - radial burn r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 7.01 (aggregate of 107 individuals; 2/107 membrane-like individually; rim level 0.614)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #146 (t=277, R_eq 3.09): none; #166 (t=297, R_eq 3.09): none; #173 (t=287, R_eq 3.34): none; #298 (t=519, R_eq 3.95): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.025 only relabels time (world META dt 0.04): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 14 of 107 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
