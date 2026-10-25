# Evidence pack: lattice-chem-gate (seed 2)

- world: `../../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 225s; status ok
- command: `python -m labkit.run collective/contrib/c17-latgate-wip/world.py --out collective/contrib/c17-latgate-wip/nogate/seed2 --seeds 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 14.0], min area 6 px

## Measurements
- components: final 85, mean 64.5, max 91; occupancy final 0.16
- tracks: 7990; persistent (alive >= 50% of run): 0; longest 25 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.96, final 0; holes at thresholds 0.2/0.35/0.5 final [50, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [106, 34, 1], H1 [52, 8, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.7
- replication (lineage window K = 20 frames = time 1000, default): splits 2391, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2413, merge/split ratio 1.01, nucleations 1402
- channel total drift (end/start - 1): [2.3796, None, -0.6016, 1.2387]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 18: holes 0, rim-vs-core 0.10, rim-vs-outside 0.36, heterogeneity 0.21; core [0.632, 0.322, 0.11, 0.467] rim [0.563, 0.38, 0.151, 0.448]
  - track 4341 at frame 133: holes 0, rim-vs-core 0.29, rim-vs-outside 0.16, heterogeneity 0.19; core [0.72, 0.227, 0.133, 0.352] rim [0.474, 0.354, 0.202, 0.422]
  - track 5245 at frame 150: holes 0, rim-vs-core 0.16, rim-vs-outside 0.23, heterogeneity 0.20; core [0.571, 0.357, 0.209, 0.339] rim [0.515, 0.227, 0.175, 0.273]
  - track 17 at frame 15: holes 0, rim-vs-core 0.08, rim-vs-outside 0.32, heterogeneity 0.20; core [0.578, 0.306, 0.112, 0.398] rim [0.55, 0.342, 0.17, 0.36]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 321 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.919, rim/outside 1.58 (aggregate of 321 individuals; 38/321 membrane-like individually; rim level 0.464)
  - radial M (membrane): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 1.38 (aggregate of 321 individuals; 149/321 membrane-like individually; rim level 0.304)
  - radial X (food): peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.34, rim/outside 0.871 (aggregate of 321 individuals; 16/321 membrane-like individually; rim level 0.194)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #16 (t=900, R_eq 7.76): none; #4341 (t=6650, R_eq 2.93): ['M (membrane)']; #5245 (t=7500, R_eq 2.39): ['M (membrane)']; #17 (t=750, R_eq 6.21): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 30 of 321 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
