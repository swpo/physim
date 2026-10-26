# Evidence pack: pps (seed 2)

- world: `../../world.py`, family `particle`
- parent: None; mutation: new class: Schmickl's Primordial Particle System, published parameters
- run: 201 frames x 150 steps x dt 1.0 = time 30000; grid [125, 125]; wall 113s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0215-c29-pps-lineage/world.py --out collective/contrib/20261026T0215-c29-pps-lineage/pack --seeds 1 2 --no-movie`
- segmentation: matter > 0.04 of robust range [0.0, 8.5938], min area 6 px

## Measurements
- components: final 45, mean 32.0, max 94; occupancy final 0.19
- tracks: 2122; persistent (alive >= 50% of run): 0; longest 75 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.27, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [79, 74, 51], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.00266/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 3000, default): splits 760, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 713, merge/split ratio 0.938, nucleations 2
- channel total drift (end/start - 1): [0.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 653 at frame 118: holes 0, rim-vs-core 0.43, rim-vs-outside 0.02, heterogeneity 0.18; core [0.286, 0.0, 0.324] rim [0.0, 0.0, 0.0]
  - track 980 at frame 143: holes 0, rim-vs-core 0.40, rim-vs-outside 0.03, heterogeneity 0.22; core [0.278, 0.053, 0.289] rim [0.0, 0.0, 0.0]
  - track 1235 at frame 165: holes 0, rim-vs-core 0.39, rim-vs-outside 0.00, heterogeneity 0.25; core [0.264, 0.077, 0.288] rim [0.008, 0.0, 0.0]
  - track 1236 at frame 165: holes 0, rim-vs-core 0.16, rim-vs-outside 0.03, heterogeneity 0.15; core [0.143, 0.0, 0.148] rim [0.036, 0.0, 0.028]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 211 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.452, rim/outside 2.86 (aggregate of 211 individuals; 42/211 membrane-like individually; rim level 0.113)
  - radial cell N>35: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.172, rim/outside 1.61 (aggregate of 211 individuals; 43/211 membrane-like individually; rim level 0.0078)
  - radial ring 15<N<=35: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.5, rim/outside 5.42 (aggregate of 211 individuals; 55/211 membrane-like individually; rim level 0.121)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #653 (t=17700, R_eq 3.29): none; #980 (t=21450, R_eq 3.39): none; #1235 (t=24750, R_eq 3.74): ['ring 15<N<=35']; #1236 (t=24750, R_eq 2.59): none

## Warnings
- radial: 10 of 211 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
