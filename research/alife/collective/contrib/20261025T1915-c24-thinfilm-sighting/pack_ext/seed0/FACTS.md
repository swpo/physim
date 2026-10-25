# Evidence pack: thinfilm-active (seed 0)

- world: `../../world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 200 steps x dt 0.25 = time 4000; grid [128, 128]; wall 204s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T1915-c24-thinfilm-sighting/world.py --out /home/user/physim/research/alife/collective/contrib/20261025T1915-c24-thinfilm-sighting/pack_ext --seeds 0 1 --frames 80 --no-movie`
- segmentation: matter > 0.07 of robust range [-0.0405, 7.8313], min area 6 px

## Measurements
- components: final 3, mean 1.8, max 5; occupancy final 0.37
- tracks: 49; persistent (alive >= 50% of run): 0; longest 15 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.31, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 2], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 1000, default): splits 19, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 11, merge/split ratio 0.579, nucleations 0
- channel total drift (end/start - 1): [0.0, 7.7516, -486.2715, 224.7143]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 30: holes 1, rim-vs-core 0.45, rim-vs-outside 0.60, heterogeneity 0.27; core [0.803, 0.892, 0.715, 0.479] rim [0.386, 0.848, 0.553, 0.486]
  - track 32 at frame 59: holes 0, rim-vs-core 0.08, rim-vs-outside 0.05, heterogeneity 0.05; core [0.142, 0.825, 0.625, 0.909] rim [0.093, 0.776, 0.616, 0.879]
  - track 27 at frame 45: holes 1, rim-vs-core 0.44, rim-vs-outside 0.59, heterogeneity 0.25; core [0.646, 0.562, 0.55, 0.333] rim [0.323, 0.841, 0.518, 0.421]
  - track 40 at frame 70: holes 0, rim-vs-core 0.32, rim-vs-outside 0.48, heterogeneity 0.24; core [0.561, 0.773, 0.477, 0.71] rim [0.264, 0.876, 0.545, 0.669]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 15 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.667, rim/outside 2.62 (aggregate of 15 individuals; 3/15 membrane-like individually; rim level 0.236)
  - radial |p| polar order: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.94, rim/outside 1.5 (aggregate of 15 individuals; 0/15 membrane-like individually; rim level 0.73)
  - radial p_x: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.993, rim/outside 0.999 (aggregate of 15 individuals; 0/15 membrane-like individually; rim level 0.566)
  - radial p_y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 1.07 (aggregate of 15 individuals; 0/15 membrane-like individually; rim level 0.525)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #23 (t=1500, R_eq 41): none; #32 (t=2950, R_eq 5.78): none; #27 (t=2250, R_eq 47.17): none; #40 (t=3500, R_eq 28.32): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 15 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 3 of 15 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
