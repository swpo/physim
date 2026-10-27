# Evidence pack: fed-vortices (seed 13)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 751 frames x 150 steps x dt 0.02 = time 2250; grid [128, 128]; wall 251s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/vort/fork --seeds 13 --frames 750 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2064], min area 6 px

## Measurements
- components: final 0, mean 29.1, max 49; occupancy final 0.00
- tracks: 221; persistent (alive >= 50% of run): 15; longest 681 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 10, 4], H1 [0, 0, 0]
- motion: 112 long-lived tracks moved >= 1 body length; max speed 0.394/time; max body lengths 51.5
- replication (lineage window K = 20 frames = time 60, default): splits 59, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 5, merges 54, merge/split ratio 0.915, nucleations 0
- channel total drift (end/start - 1): [-1.0, 0.0037, 1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 340: holes 0, rim-vs-core 0.74, rim-vs-outside 0.33, heterogeneity 0.19; core [0.831, 0.1, 0.934, 0.687] rim [0.417, 0.329, 0.713, 0.156]
  - track 8 at frame 340: holes 0, rim-vs-core 0.70, rim-vs-outside 0.30, heterogeneity 0.18; core [0.807, 0.099, 0.059, 0.647] rim [0.414, 0.302, 0.264, 0.145]
  - track 29 at frame 340: holes 0, rim-vs-core 0.81, rim-vs-outside 0.30, heterogeneity 0.21; core [0.824, 0.124, 0.924, 0.737] rim [0.39, 0.312, 0.699, 0.125]
  - track 200 at frame 649: holes 0, rim-vs-core 0.85, rim-vs-outside 0.32, heterogeneity 0.22; core [0.858, 0.118, 0.939, 0.799] rim [0.409, 0.331, 0.709, 0.145]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 158 components >= 12 px at frames [126, 252, 378, 498, 624]):
  - radial |vorticity|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.754, rim/outside 15.9 (aggregate of 158 individuals; 0/158 membrane-like individually; rim level 0.682)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 12.3, rim/outside 0.778 (aggregate of 158 individuals; 0/158 membrane-like individually; rim level 0.465)
  - radial vorticity (signed): peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 0.999 (aggregate of 158 individuals; 0/158 membrane-like individually; rim level 0.484)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.687, rim/outside 27.8 (aggregate of 158 individuals; 2/158 membrane-like individually; rim level 0.522)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=1020, R_eq 4.95): none; #8 (t=1020, R_eq 4.72): none; #29 (t=1020, R_eq 4.03): none; #200 (t=1947, R_eq 4.11): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 158 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
