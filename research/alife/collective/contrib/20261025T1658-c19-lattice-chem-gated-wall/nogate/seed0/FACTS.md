# Evidence pack: lattice-chem-gate (seed 0)

- world: `../../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 351s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1658-c19-lattice-chem-gated-wall/world.py --out collective/contrib/20261025T1658-c19-lattice-chem-gated-wall/nogate/seed0 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 14.0], min area 6 px

## Measurements
- components: final 78, mean 68.8, max 102; occupancy final 0.18
- tracks: 8289; persistent (alive >= 50% of run): 0; longest 22 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.49, final 0; holes at thresholds 0.2/0.35/0.5 final [46, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [116, 48, 2], H1 [53, 12, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 1000, default): splits 2422, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2409, merge/split ratio 0.995, nucleations 1660
- channel total drift (end/start - 1): [2.3506, None, -0.6064, 1.2445]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 26 at frame 17: holes 0, rim-vs-core 0.21, rim-vs-outside 0.27, heterogeneity 0.21; core [0.653, 0.292, 0.107, 0.439] rim [0.492, 0.393, 0.184, 0.384]
  - track 0 at frame 13: holes 0, rim-vs-core 0.13, rim-vs-outside 0.30, heterogeneity 0.21; core [0.622, 0.361, 0.103, 0.461] rim [0.544, 0.354, 0.164, 0.375]
  - track 16 at frame 15: holes 0, rim-vs-core 0.07, rim-vs-outside 0.29, heterogeneity 0.20; core [0.503, 0.311, 0.141, 0.432] rim [0.533, 0.333, 0.164, 0.376]
  - track 4 at frame 13: holes 0, rim-vs-core 0.09, rim-vs-outside 0.35, heterogeneity 0.20; core [0.531, 0.321, 0.108, 0.448] rim [0.567, 0.378, 0.162, 0.414]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 320 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.928, rim/outside 1.61 (aggregate of 320 individuals; 28/320 membrane-like individually; rim level 0.464)
  - radial M (membrane): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 1.4 (aggregate of 320 individuals; 144/320 membrane-like individually; rim level 0.302)
  - radial X (food): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.35, rim/outside 0.865 (aggregate of 320 individuals; 23/320 membrane-like individually; rim level 0.194)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #26 (t=850, R_eq 6.26): none; #0 (t=650, R_eq 6.63): none; #16 (t=750, R_eq 7.57): none; #4 (t=650, R_eq 7.07): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 34 of 320 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
