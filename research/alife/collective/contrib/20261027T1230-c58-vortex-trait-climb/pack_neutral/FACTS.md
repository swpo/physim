# Evidence pack: fed-vortices (seed 1)

- world: `../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 2001 frames x 150 steps x dt 0.02 = time 6000; grid [128, 128]; wall 1081s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261027T1230-c58-vortex-trait-climb/world.py --out /home/user/physim/research/alife/collective/contrib/20261027T1230-c58-vortex-trait-climb/pack_neutral --seeds 1 --frames 2000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.204], min area 6 px

## Measurements
- components: final 30, mean 29.2, max 49; occupancy final 0.15
- tracks: 584; persistent (alive >= 50% of run): 5; longest 1476 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.03 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 32, 30], H1 [0, 0, 0]
- motion: 296 long-lived tracks moved >= 1 body length; max speed 0.459/time; max body lengths 39.1
- replication (lineage window K = 20 frames = time 60, default): splits 185, persistent splits 83 (0 more failed only because the siblings re-merged within K), max generation 18, merges 168, merge/split ratio 0.908, nucleations 0
- channel total drift (end/start - 1): [-0.5268, 0.1551, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 200 at frame 1277: holes 0, rim-vs-core 0.74, rim-vs-outside 0.37, heterogeneity 0.19; core [0.82, 0.108, 0.865, 0.668] rim [0.403, 0.344, 0.337, 0.463]
  - track 227 at frame 1244: holes 0, rim-vs-core 0.70, rim-vs-outside 0.38, heterogeneity 0.16; core [0.828, 0.101, 0.88, 0.303] rim [0.427, 0.343, 0.357, 0.321]
  - track 149 at frame 891: holes 0, rim-vs-core 0.67, rim-vs-outside 0.39, heterogeneity 0.15; core [0.852, 0.118, 0.878, 0.332] rim [0.432, 0.301, 0.384, 0.332]
  - track 570 at frame 2000: holes 0, rim-vs-core 0.59, rim-vs-outside 0.33, heterogeneity 0.15; core [0.747, 0.121, 0.84, 0.554] rim [0.395, 0.28, 0.405, 0.438]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 172 components >= 12 px at frames [336, 672, 1008, 1328, 1664, 2000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.765, rim/outside 17.1 (aggregate of 172 individuals; 0/172 membrane-like individually; rim level 0.689)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 12.9, rim/outside 0.772 (aggregate of 172 individuals; 0/172 membrane-like individually; rim level 0.476)
  - radial label c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.771, rim/outside 21 (aggregate of 172 individuals; 0/172 membrane-like individually; rim level 0.729)
  - radial trait theta*c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside 1.22 (aggregate of 172 individuals; 0/172 membrane-like individually; rim level 0.407)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #200 (t=3831, R_eq 5.2): none; #227 (t=3732, R_eq 5.41): none; #149 (t=2673, R_eq 3.99): none; #570 (t=6000, R_eq 4.69): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
