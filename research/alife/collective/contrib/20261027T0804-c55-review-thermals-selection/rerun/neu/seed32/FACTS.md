# Evidence pack: reacting-thermals (seed 32)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0222-c49-thermals-selection-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 1201 frames x 25 steps x dt 0.04 = time 1200; grid [128, 128]; wall 147s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0222-c49-thermals-selection-claim/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/rev/neu --seeds 31 32 --frames 1200 --spf 25 --no-movie`
- segmentation: matter > 0.31 of robust range [0.0, 0.794], min area 6 px

## Measurements
- components: final 24, mean 17.9, max 46; occupancy final 0.02
- tracks: 922; persistent (alive >= 50% of run): 0; longest 227 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 31, 28], H1 [0, 0, 0]
- motion: 350 long-lived tracks moved >= 1 body length; max speed 1.17/time; max body lengths 41.5
- replication (lineage window K = 20 frames = time 20, default): splits 197, persistent splits 49 (0 more failed only because the siblings re-merged within K), max generation 7, merges 36, merge/split ratio 0.183, nucleations 470
- channel total drift (end/start - 1): [-0.8589, -0.3427, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 757 at frame 1079: holes 0, rim-vs-core 0.26, rim-vs-outside 0.58, heterogeneity 0.11; core [0.962, 0.001, 0.295, 0.959] rim [0.777, 0.061, 0.235, 0.805]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [202, 403, 605, 797, 998, 1200]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 5.27 (aggregate of 75 individuals; 3/75 membrane-like individually; rim level 0.715)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.08, rim/outside 0.578 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.178)
  - radial label a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.869, rim/outside 3.85 (aggregate of 75 individuals; 2/75 membrane-like individually; rim level 0.461)
  - radial label b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 4.67 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.469)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #213 (t=454, R_eq 1.78): none; #705 (t=1059, R_eq 1.78): none; #596 (t=918, R_eq 2.19): none; #757 (t=1079, R_eq 2.71): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 75 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
