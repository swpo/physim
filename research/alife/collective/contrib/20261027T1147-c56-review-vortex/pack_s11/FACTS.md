# Evidence pack: fed-vortices (seed 11)

- world: `../../../collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 325s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py --out c56work/vx/pack_s11 --seeds 11 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2056], min area 6 px

## Measurements
- components: final 33, mean 30.5, max 39; occupancy final 0.15
- tracks: 374; persistent (alive >= 50% of run): 11; longest 846 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 34, 33], H1 [0, 0, 0]
- motion: 192 long-lived tracks moved >= 1 body length; max speed 0.444/time; max body lengths 54.3
- replication (lineage window K = 20 frames = time 60, default): splits 117, persistent splits 44 (0 more failed only because the siblings re-merged within K), max generation 9, merges 102, merge/split ratio 0.872, nucleations 0
- channel total drift (end/start - 1): [-0.5067, 0.1364, 1834.816, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 59 at frame 437: holes 0, rim-vs-core 0.67, rim-vs-outside 0.25, heterogeneity 0.18; core [0.765, 0.116, 0.073, 0.587] rim [0.378, 0.284, 0.274, 0.102]
  - track 89 at frame 580: holes 0, rim-vs-core 0.67, rim-vs-outside 0.30, heterogeneity 0.18; core [0.794, 0.099, 0.054, 0.611] rim [0.41, 0.316, 0.256, 0.143]
  - track 90 at frame 580: holes 0, rim-vs-core 0.70, rim-vs-outside 0.29, heterogeneity 0.18; core [0.798, 0.102, 0.055, 0.622] rim [0.4, 0.31, 0.261, 0.131]
  - track 346 at frame 966: holes 0, rim-vs-core 0.51, rim-vs-outside 0.55, heterogeneity 0.17; core [0.8, 0.085, 0.907, 0.637] rim [0.513, 0.249, 0.754, 0.277]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 180 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.754, rim/outside 15.7 (aggregate of 180 individuals; 3/180 membrane-like individually; rim level 0.653)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.94, rim/outside 0.772 (aggregate of 180 individuals; 0/180 membrane-like individually; rim level 0.472)
  - radial vorticity (signed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.94, rim/outside 1.15 (aggregate of 180 individuals; 0/180 membrane-like individually; rim level 0.559)
  - radial eating: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.688, rim/outside 26.1 (aggregate of 180 individuals; 5/180 membrane-like individually; rim level 0.488)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #59 (t=1311, R_eq 4.37): none; #89 (t=1740, R_eq 5.11): none; #90 (t=1740, R_eq 4.85): none; #346 (t=2898, R_eq 6.58): ['eating']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 180 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
