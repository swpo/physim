# Evidence pack: fed-vortices (seed 47)

- world: `../../../20261027T0712-c53-fed-vortex-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 283s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py --out collective/contrib/c57-w18/rerun/seed47 --seeds 47 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.30 of robust range [0.0, 0.2033], min area 6 px

## Measurements
- components: final 25, mean 27.3, max 41; occupancy final 0.14
- tracks: 258; persistent (alive >= 50% of run): 8; longest 1001 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 7.73 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 27, 25], H1 [0, 0, 0]
- motion: 133 long-lived tracks moved >= 1 body length; max speed 0.413/time; max body lengths 27.9
- replication (lineage window K = 20 frames = time 60, default): splits 74, persistent splits 36 (0 more failed only because the siblings re-merged within K), max generation 9, merges 68, merge/split ratio 0.919, nucleations 0
- channel total drift (end/start - 1): [-0.5617, 0.1824, -221.9186, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 504: holes 0, rim-vs-core 0.79, rim-vs-outside 0.33, heterogeneity 0.20; core [0.837, 0.151, 0.931, 0.772] rim [0.424, 0.301, 0.719, 0.157]
  - track 43 at frame 504: holes 0, rim-vs-core 0.67, rim-vs-outside 0.32, heterogeneity 0.18; core [0.806, 0.104, 0.921, 0.638] rim [0.432, 0.308, 0.723, 0.165]
  - track 95 at frame 580: holes 0, rim-vs-core 0.67, rim-vs-outside 0.30, heterogeneity 0.17; core [0.787, 0.107, 0.911, 0.599] rim [0.407, 0.344, 0.71, 0.138]
  - track 237 at frame 941: holes 0, rim-vs-core 0.83, rim-vs-outside 0.30, heterogeneity 0.21; core [0.844, 0.119, 0.055, 0.757] rim [0.399, 0.326, 0.277, 0.13]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 160 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 15.1 (aggregate of 160 individuals; 0/160 membrane-like individually; rim level 0.679)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.7, rim/outside 0.767 (aggregate of 160 individuals; 0/160 membrane-like individually; rim level 0.484)
  - radial vorticity (signed): peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.984 (aggregate of 160 individuals; 0/160 membrane-like individually; rim level 0.482)
  - radial eating: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.751, rim/outside 24.8 (aggregate of 160 individuals; 5/160 membrane-like individually; rim level 0.526)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #22 (t=1512, R_eq 3.57): none; #43 (t=1512, R_eq 4.95): none; #95 (t=1740, R_eq 5.64): none; #237 (t=2823, R_eq 4.41): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 160 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
