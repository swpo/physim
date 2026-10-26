# Evidence pack: phoretic-colloids (seed 0)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 56s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33/world.py --out collective/contrib/wip-c33/pack --seeds 0 1 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5758], min area 6 px

## Measurements
- components: final 19, mean 24.6, max 43; occupancy final 0.08
- tracks: 242; persistent (alive >= 50% of run): 9; longest 329 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 23, 12], H1 [0, 0, 0]
- motion: 51 long-lived tracks moved >= 1 body length; max speed 0.404/time; max body lengths 7.8
- replication (lineage window K = 20 frames = time 10, default): splits 10, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 43, merge/split ratio 4.3, nucleations 179
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 80 at frame 239: holes 0, rim-vs-core 0.25, rim-vs-outside 0.26, heterogeneity 0.13; core [0.726, 0.264, 0.335] rim [0.484, 0.332, 0.297]
  - track 96 at frame 249: holes 0, rim-vs-core 0.33, rim-vs-outside 0.33, heterogeneity 0.16; core [0.777, 0.449, 0.632] rim [0.467, 0.43, 0.506]
  - track 55 at frame 188: holes 0, rim-vs-core 0.25, rim-vs-outside 0.29, heterogeneity 0.17; core [0.656, 0.506, 0.42] rim [0.529, 0.296, 0.363]
  - track 216 at frame 373: holes 0, rim-vs-core 0.36, rim-vs-outside 0.30, heterogeneity 0.18; core [0.853, 0.212, 0.56] rim [0.509, 0.191, 0.449]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 130 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 12 (aggregate of 130 individuals; 6/130 membrane-like individually; rim level 0.608)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.836, rim/outside 11.5 (aggregate of 130 individuals; 42/130 membrane-like individually; rim level 0.386)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.804, rim/outside 2.49 (aggregate of 130 individuals; 0/130 membrane-like individually; rim level 0.518)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #80 (t=119.5, R_eq 2.33): ['B density']; #96 (t=124.5, R_eq 4.11): none; #55 (t=94, R_eq 2.82): none; #216 (t=186.5, R_eq 3.83): ['B density']

## Warnings
- radial: 1 of 130 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
