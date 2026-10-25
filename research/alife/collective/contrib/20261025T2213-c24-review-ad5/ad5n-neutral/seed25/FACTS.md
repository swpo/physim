# Evidence pack: ad5n-neutral (seed 25)

- world: `../../../../../threads/active-droplets/worlds/ad5n-neutral/world.py`, family `phase-field`
- parent: ad5-evolve; mutation: neutral control: all four alleles have the same catalytic rate k=0.13
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 307s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5n-neutral/world.py --out collective/contrib/20261025T2213-c24-review-ad5/ad5n-neutral/seed25 --seeds 25 --frames 200 --no-movie`
- segmentation: matter > 0.43 of robust range [-1.0636, 1.4237], min area 6 px

## Measurements
- components: final 8, mean 8.7, max 10; occupancy final 0.10
- tracks: 14; persistent (alive >= 50% of run): 9; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 6.79 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00113/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 4, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.0679, -0.5319, 0.9081, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 0, rim-vs-core 0.44, rim-vs-outside 0.67, heterogeneity 0.13; core [0.955, 0.04, 0.689, 0.001, 0.649, 0.0] rim [0.683, 0.131, 0.418, 0.0, 0.465, 0.0]
  - track 3 at frame 101: holes 0, rim-vs-core 0.28, rim-vs-outside 0.79, heterogeneity 0.04; core [0.968, 0.035, 0.0, 0.0, 0.0, 1.0] rim [0.697, 0.121, 0.0, 0.0, 0.0, 0.997]
  - track 6 at frame 118: holes 0, rim-vs-core 0.37, rim-vs-outside 0.74, heterogeneity 0.07; core [0.97, 0.032, 0.932, 0.058, 0.0, 0.0] rim [0.749, 0.109, 0.646, 0.043, 0.0, 0.0]
  - track 7 at frame 118: holes 0, rim-vs-core 0.44, rim-vs-outside 0.68, heterogeneity 0.07; core [0.967, 0.034, 0.95, 0.0, 0.0, 0.0] rim [0.709, 0.119, 0.609, 0.0, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 54 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.952, rim/outside 56.5 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.928)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 15.5, rim/outside 0.693 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.226)
  - radial a0: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 52.3 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.729)
  - radial a1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 9.07 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.0818)
  - radial a2: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.967, rim/outside 12 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.112)
  - radial a3: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.946, rim/outside 8.91 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.0808)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=10100, R_eq 7.96): none; #3 (t=10100, R_eq 7.59): none; #6 (t=11800, R_eq 7.84): none; #7 (t=11800, R_eq 7.57): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 54 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
