# Evidence pack: pps (seed 7)

- world: `../../../20261026T0215-c29-pps-lineage/world.py`, family `particle`
- parent: None; mutation: new class: Schmickl's Primordial Particle System, published parameters
- run: 201 frames x 150 steps x dt 1.0 = time 30000; grid [125, 125]; wall 108s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0215-c29-pps-lineage/world.py --out collective/contrib/20261026T0330-c34-review-pps-lineage/rerun/seed7 --seeds 7 --no-movie`
- segmentation: matter > 0.04 of robust range [0.0, 9.375], min area 6 px

## Measurements
- components: final 47, mean 38.2, max 77; occupancy final 0.18
- tracks: 2317; persistent (alive >= 50% of run): 2; longest 152 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.40 (1 = constant size)
- enclosures: components with a hole mean 0.25, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [75, 68, 54], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.00213/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 3000, default): splits 828, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 782, merge/split ratio 0.944, nucleations 1
- channel total drift (end/start - 1): [0.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 451 at frame 124: holes 0, rim-vs-core 0.25, rim-vs-outside 0.01, heterogeneity 0.15; core [0.19, 0.0, 0.19] rim [0.012, 0.0, 0.012]
  - track 938 at frame 143: holes 0, rim-vs-core 0.39, rim-vs-outside 0.02, heterogeneity 0.20; core [0.286, 0.0, 0.286] rim [0.012, 0.0, 0.012]
  - track 452 at frame 91: holes 0, rim-vs-core 0.35, rim-vs-outside 0.01, heterogeneity 0.25; core [0.249, 0.097, 0.235] rim [0.007, 0.0, 0.007]
  - track 535 at frame 99: holes 0, rim-vs-core 0.38, rim-vs-outside 0.01, heterogeneity 0.15; core [0.278, 0.0, 0.278] rim [0.008, 0.0, 0.008]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 238 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.477, rim/outside 2.96 (aggregate of 238 individuals; 48/238 membrane-like individually; rim level 0.116)
  - radial cell N>35: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.166, rim/outside 1.48 (aggregate of 238 individuals; 45/238 membrane-like individually; rim level 0.0067)
  - radial ring 15<N<=35: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.485, rim/outside 5.21 (aggregate of 238 individuals; 48/238 membrane-like individually; rim level 0.106)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #451 (t=18600, R_eq 2.59): none; #938 (t=21450, R_eq 2.65): none; #452 (t=13650, R_eq 4.07): ['ring 15<N<=35']; #535 (t=14850, R_eq 3.39): none

## Warnings
- radial: 6 of 238 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
