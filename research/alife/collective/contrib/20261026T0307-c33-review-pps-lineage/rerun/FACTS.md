# Evidence pack: pps (seed 13)

- world: `../../20261026T0215-c29-pps-lineage/world.py`, family `particle`
- parent: None; mutation: new class: Schmickl's Primordial Particle System, published parameters
- run: 201 frames x 150 steps x dt 1.0 = time 30000; grid [125, 125]; wall 110s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0215-c29-pps-lineage/world.py --out collective/contrib/wip-c33-pps/rerun --seeds 13 --frames 200 --no-movie`
- segmentation: matter > 0.04 of robust range [0.0, 8.5938], min area 6 px

## Measurements
- components: final 42, mean 27.9, max 81; occupancy final 0.18
- tracks: 2027; persistent (alive >= 50% of run): 0; longest 82 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.22, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [70, 65, 47], H1 [1, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.00397/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 3000, default): splits 728, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 709, merge/split ratio 0.974, nucleations 0
- channel total drift (end/start - 1): [0.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1064 at frame 160: holes 0, rim-vs-core 0.48, rim-vs-outside 0.03, heterogeneity 0.19; core [0.321, 0.0, 0.354] rim [0.0, 0.0, 0.0]
  - track 1132 at frame 163: holes 0, rim-vs-core 0.43, rim-vs-outside 0.04, heterogeneity 0.16; core [0.286, 0.0, 0.315] rim [0.0, 0.0, 0.0]
  - track 1168 at frame 158: holes 0, rim-vs-core 0.35, rim-vs-outside 0.03, heterogeneity 0.26; core [0.236, 0.077, 0.244] rim [0.0, 0.0, 0.0]
  - track 1515 at frame 178: holes 0, rim-vs-core 0.50, rim-vs-outside 0.01, heterogeneity 0.14; core [0.333, 0.0, 0.389] rim [0.011, 0.0, 0.013]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 175 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.515, rim/outside 3.08 (aggregate of 175 individuals; 43/175 membrane-like individually; rim level 0.121)
  - radial cell N>35: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.308, rim/outside 1.83 (aggregate of 175 individuals; 36/175 membrane-like individually; rim level 0.0115)
  - radial ring 15<N<=35: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.534, rim/outside 5.64 (aggregate of 175 individuals; 44/175 membrane-like individually; rim level 0.124)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1064 (t=24000, R_eq 2.59): none; #1132 (t=24450, R_eq 2.88): none; #1168 (t=23700, R_eq 3.78): none; #1515 (t=26700, R_eq 2.65): none

## Warnings
- radial: 8 of 175 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
