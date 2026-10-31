# Evidence pack: fed-vortices-noise (seed 4)

- world: `../../../../scripts/noisy_world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 151 frames x 150 steps x dt 0.02 = time 450; grid [128, 128]; wall 71s; status ok
- command: `nsweep behav fv level 0.01`
- segmentation: matter > 0.29 of robust range [0.0001, 0.2096], min area 6 px

## Measurements
- components: final 29, mean 31.9, max 38; occupancy final 0.12
- tracks: 99; persistent (alive >= 50% of run): 26; longest 151 frames; alive start-to-end: 9
- size of persistent tracks: max/min area ratio 10.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 29], H1 [0, 0, 0]
- motion: 44 long-lived tracks moved >= 1 body length; max speed 0.279/time; max body lengths 12.8
- replication (lineage window K = 20 frames = time 60, default): splits 25, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 11, merge/split ratio 0.44, nucleations 0
- channel total drift (end/start - 1): [-0.5857, 0.2218, 394.0915, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 76: holes 0, rim-vs-core 0.69, rim-vs-outside 0.28, heterogeneity 0.18; core [0.785, 0.104, 0.904, 0.604] rim [0.388, 0.304, 0.69, 0.117]
  - track 2 at frame 76: holes 0, rim-vs-core 0.79, rim-vs-outside 0.30, heterogeneity 0.20; core [0.831, 0.115, 0.924, 0.739] rim [0.409, 0.296, 0.702, 0.139]
  - track 4 at frame 76: holes 0, rim-vs-core 0.67, rim-vs-outside 0.32, heterogeneity 0.17; core [0.802, 0.092, 0.913, 0.613] rim [0.423, 0.314, 0.709, 0.156]
  - track 94 at frame 135: holes 0, rim-vs-core 0.72, rim-vs-outside 0.28, heterogeneity 0.19; core [0.799, 0.108, 0.911, 0.635] rim [0.389, 0.312, 0.69, 0.123]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 190 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.748, rim/outside 12.5 (aggregate of 190 individuals; 1/190 membrane-like individually; rim level 0.67)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.01, rim/outside 0.784 (aggregate of 190 individuals; 0/190 membrane-like individually; rim level 0.455)
  - radial vorticity (signed): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 1.1 (aggregate of 190 individuals; 0/190 membrane-like individually; rim level 0.527)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.661, rim/outside 24.2 (aggregate of 190 individuals; 4/190 membrane-like individually; rim level 0.508)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=228, R_eq 4.79): none; #2 (t=228, R_eq 3.99): none; #4 (t=228, R_eq 5.11): none; #94 (t=405, R_eq 4.79): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 190 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
