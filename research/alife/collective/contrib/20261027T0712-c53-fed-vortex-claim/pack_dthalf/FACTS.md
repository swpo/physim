# Evidence pack: fed-vortices (seed 0)

- world: `../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 300 steps x dt 0.01 (--dt; world META dt 0.02) = time 3000; grid [128, 128]; wall 570s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/pack_dthalf --seeds 0 --frames 1000 --spf 300 --dt 0.01 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2046], min area 6 px

## Measurements
- components: final 27, mean 30.0, max 50; occupancy final 0.14
- tracks: 239; persistent (alive >= 50% of run): 8; longest 1001 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 3.92 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 32, 29], H1 [0, 0, 0]
- motion: 135 long-lived tracks moved >= 1 body length; max speed 0.536/time; max body lengths 34.5
- replication (lineage window K = 20 frames = time 60, default): splits 64, persistent splits 32 (0 more failed only because the siblings re-merged within K), max generation 9, merges 64, merge/split ratio 1, nucleations 0
- channel total drift (end/start - 1): [-0.5672, 0.1786, 661.9046, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 48 at frame 504: holes 0, rim-vs-core 0.73, rim-vs-outside 0.28, heterogeneity 0.19; core [0.803, 0.11, 0.059, 0.64] rim [0.389, 0.34, 0.276, 0.122]
  - track 44 at frame 496: holes 0, rim-vs-core 0.54, rim-vs-outside 0.56, heterogeneity 0.20; core [0.846, 0.115, 0.931, 0.739] rim [0.554, 0.255, 0.781, 0.338]
  - track 2 at frame 437: holes 0, rim-vs-core 0.78, rim-vs-outside 0.31, heterogeneity 0.20; core [0.836, 0.114, 0.053, 0.72] rim [0.407, 0.333, 0.266, 0.143]
  - track 214 at frame 966: holes 0, rim-vs-core 0.86, rim-vs-outside 0.36, heterogeneity 0.22; core [0.879, 0.124, 0.947, 0.844] rim [0.434, 0.342, 0.718, 0.179]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 172 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.768, rim/outside 18.8 (aggregate of 172 individuals; 1/172 membrane-like individually; rim level 0.692)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 11.4, rim/outside 0.769 (aggregate of 172 individuals; 0/172 membrane-like individually; rim level 0.479)
  - radial vorticity (signed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.966, rim/outside 1.03 (aggregate of 172 individuals; 0/172 membrane-like individually; rim level 0.501)
  - radial eating: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.723, rim/outside 32.3 (aggregate of 172 individuals; 2/172 membrane-like individually; rim level 0.544)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #48 (t=1512, R_eq 5.14): none; #44 (t=1488, R_eq 4.65): none; #2 (t=1311, R_eq 4.62): none; #214 (t=2898, R_eq 4.07): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.01 only relabels time (world META dt 0.02): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 1 of 172 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
