# Evidence pack: fed-vortices (seed 4)

- world: `../../../collective/contrib/20261027T0845-c53-fed-vortex-selection-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1501 frames x 150 steps x dt 0.02 = time 4500; grid [128, 128]; wall 905s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0845-c53-fed-vortex-selection-claim/world.py --out c56work/vs/pack_neu --seeds 4 --frames 1500 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2036], min area 6 px

## Measurements
- components: final 35, mean 27.9, max 39; occupancy final 0.15
- tracks: 561; persistent (alive >= 50% of run): 2; longest 1070 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.15 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 35, 35], H1 [0, 0, 0]
- motion: 283 long-lived tracks moved >= 1 body length; max speed 0.557/time; max body lengths 84.3
- replication (lineage window K = 20 frames = time 60, default): splits 187, persistent splits 73 (0 more failed only because the siblings re-merged within K), max generation 14, merges 154, merge/split ratio 0.824, nucleations 0
- channel total drift (end/start - 1): [-0.525, 0.1249, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 139 at frame 882: holes 0, rim-vs-core 0.70, rim-vs-outside 0.37, heterogeneity 0.16; core [0.813, 0.099, 0.897, 0.017] rim [0.421, 0.332, 0.372, 0.007]
  - track 52 at frame 466: holes 0, rim-vs-core 0.67, rim-vs-outside 0.39, heterogeneity 0.15; core [0.853, 0.114, 0.9, 0.01] rim [0.434, 0.291, 0.413, 0.004]
  - track 194 at frame 832: holes 0, rim-vs-core 0.67, rim-vs-outside 0.33, heterogeneity 0.18; core [0.83, 0.108, 0.532, 0.586] rim [0.398, 0.312, 0.213, 0.235]
  - track 554 at frame 1500: holes 0, rim-vs-core 0.61, rim-vs-outside 0.32, heterogeneity 0.17; core [0.768, 0.12, 0.453, 0.668] rim [0.402, 0.298, 0.2, 0.295]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 174 components >= 12 px at frames [252, 504, 756, 996, 1248, 1500]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.759, rim/outside 17.4 (aggregate of 174 individuals; 2/174 membrane-like individually; rim level 0.672)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 12.7, rim/outside 0.767 (aggregate of 174 individuals; 0/174 membrane-like individually; rim level 0.469)
  - radial label a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.764, rim/outside 18.9 (aggregate of 174 individuals; 3/174 membrane-like individually; rim level 0.433)
  - radial label b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.761, rim/outside 17.3 (aggregate of 174 individuals; 1/174 membrane-like individually; rim level 0.471)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #139 (t=2646, R_eq 5.32): none; #52 (t=1398, R_eq 3.91): none; #194 (t=2496, R_eq 4.55): none; #554 (t=4500, R_eq 5.05): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 174 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
