# Evidence pack: fed-vortices (seed 55)

- world: `../../../20261027T0712-c53-fed-vortex-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 351s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py --out collective/contrib/20261027T1040-c54-review-fed-vortex/rerun --seeds 54 55 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2059], min area 6 px

## Measurements
- components: final 27, mean 30.9, max 41; occupancy final 0.14
- tracks: 320; persistent (alive >= 50% of run): 14; longest 914 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.70 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 27], H1 [0, 0, 0]
- motion: 157 long-lived tracks moved >= 1 body length; max speed 0.476/time; max body lengths 47.8
- replication (lineage window K = 20 frames = time 60, default): splits 97, persistent splits 38 (0 more failed only because the siblings re-merged within K), max generation 10, merges 84, merge/split ratio 0.866, nucleations 0
- channel total drift (end/start - 1): [-0.5544, 0.1825, 312.5915, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 454: holes 0, rim-vs-core 0.67, rim-vs-outside 0.31, heterogeneity 0.17; core [0.799, 0.097, 0.051, 0.616] rim [0.421, 0.321, 0.252, 0.154]
  - track 13 at frame 387: holes 0, rim-vs-core 0.75, rim-vs-outside 0.30, heterogeneity 0.19; core [0.822, 0.107, 0.921, 0.686] rim [0.411, 0.314, 0.702, 0.139]
  - track 37 at frame 387: holes 0, rim-vs-core 0.36, rim-vs-outside 0.62, heterogeneity 0.20; core [0.792, 0.128, 0.065, 0.664] rim [0.586, 0.228, 0.172, 0.401]
  - track 309 at frame 992: holes 0, rim-vs-core 0.51, rim-vs-outside 0.44, heterogeneity 0.17; core [0.77, 0.091, 0.894, 0.561] rim [0.473, 0.298, 0.735, 0.233]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 185 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.749, rim/outside 15 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.668)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 10.3, rim/outside 0.779 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.472)
  - radial vorticity (signed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.936, rim/outside 1.09 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.525)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.691, rim/outside 25.1 (aggregate of 185 individuals; 2/185 membrane-like individually; rim level 0.509)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=1362, R_eq 5.2): none; #13 (t=1161, R_eq 4.69): none; #37 (t=1161, R_eq 3.95): none; #309 (t=2976, R_eq 5.92): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
