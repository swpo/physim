# Evidence pack: fed-thinfilm (seed 0)

- world: `../../world.py`, family `thin-film`
- parent: collective/contrib/20261025T1915-c24-thinfilm-sighting; mutation: non-conserved film: condensation from a consumed, regrowing vapour along the film's own chemical potential, and decay of liquid inside drops
- run: 161 frames x 200 steps x dt 0.25 = time 8000; grid [128, 128]; wall 236s; status ok
- command: `python -m labkit.run collective/contrib/c57-w4/world.py --out collective/contrib/c57-w4/pack_m2/seed0 --seeds 0 --size 128 128 --frames 160 --no-movie`
- segmentation: matter > 0.08 of robust range [0.1452, 4.7318], min area 6 px

## Measurements
- components: final 6, mean 6.0, max 11; occupancy final 0.50
- tracks: 237; persistent (alive >= 50% of run): 0; longest 37 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.29, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 10, 4], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0652/time; max body lengths 6.2
- replication (lineage window K = 20 frames = time 1000, default): splits 72, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 76, merge/split ratio 1.06, nucleations 23
- channel total drift (end/start - 1): [-0.1017, 12.9122, 5849.1104, 2134.4934, -0.0451]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 176 at frame 130: holes 0, rim-vs-core 0.14, rim-vs-outside 0.13, heterogeneity 0.05; core [0.246, 0.881, 0.853, 0.759, 0.547] rim [0.143, 0.86, 0.818, 0.78, 0.468]
  - track 197 at frame 143: holes 0, rim-vs-core 0.09, rim-vs-outside 0.07, heterogeneity 0.03; core [0.161, 0.877, 0.714, 0.875, 0.532] rim [0.106, 0.838, 0.703, 0.856, 0.476]
  - track 45 at frame 36: holes 0, rim-vs-core 0.24, rim-vs-outside 0.19, heterogeneity 0.08; core [0.358, 0.912, 0.943, 0.621, 0.548] rim [0.153, 0.852, 0.908, 0.601, 0.446]
  - track 165 at frame 116: holes 0, rim-vs-core 0.26, rim-vs-outside 0.35, heterogeneity 0.09; core [0.468, 0.929, 0.582, 0.951, 0.632] rim [0.234, 0.887, 0.605, 0.907, 0.533]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.604, rim/outside 1.85 (aggregate of 35 individuals; 1/35 membrane-like individually; rim level 0.213)
  - radial |p| polar order: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.955, rim/outside 1.09 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.849)
  - radial p_x: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 1.01 (aggregate of 35 individuals; 1/35 membrane-like individually; rim level 0.686)
  - radial p_y: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.973, rim/outside 1 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.744)
  - radial vapour V: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 1.22 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.522)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #176 (t=6500, R_eq 8.37): none; #197 (t=7150, R_eq 9.47): none; #45 (t=1800, R_eq 10.25): none; #165 (t=5800, R_eq 18.79): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 35 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 4 of 35 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
