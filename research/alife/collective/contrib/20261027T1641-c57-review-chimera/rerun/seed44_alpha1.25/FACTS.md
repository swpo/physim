# Evidence pack: chimera-field (seed 44)

- world: `../../20261027T1049-c55-chimera-field-negative/world.py`, family `nonlocal-oscillators`
- parent: None; mutation: -
- run: 151 frames x 100 steps x dt 0.1 = time 1500; grid [128, 128]; wall 28s; status ok
- command: `python -m labkit.run collective/contrib/20261027T1049-c55-chimera-field-negative/world.py --out collective/contrib/c57-w16/a1.25 --seeds 44 --frames 150 --spf 100 --no-movie`
- segmentation: matter > 0.31 of robust range [0.0, 0.9717], min area 6 px

## Measurements
- components: final 1, mean 1.7, max 6; occupancy final 0.65
- tracks: 168; persistent (alive >= 50% of run): 0; longest 10 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.66, final 0; holes at thresholds 0.2/0.35/0.5 final [4, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 7, 5], H1 [2, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 200, default): splits 57, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 42, merge/split ratio 0.737, nucleations 1
- channel total drift (end/start - 1): [None, -0.4289, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 99 at frame 93: holes 1, rim-vs-core 0.24, rim-vs-outside 0.40, heterogeneity 0.18; core [0.647, 0.656, 0.0, 0.418] rim [0.512, 0.476, 0.0, 0.341]
  - track 126 at frame 120: holes 1, rim-vs-core 0.19, rim-vs-outside 0.47, heterogeneity 0.18; core [0.676, 0.513, 0.0, 0.445] rim [0.521, 0.454, 0.0, 0.348]
  - track 20 at frame 18: holes 1, rim-vs-core 0.38, rim-vs-outside 0.42, heterogeneity 0.19; core [0.795, 0.464, 0.0, 0.527] rim [0.47, 0.525, 0.0, 0.338]
  - track 31 at frame 33: holes 1, rim-vs-core 0.20, rim-vs-outside 0.46, heterogeneity 0.19; core [0.735, 0.525, 0.0, 0.474] rim [0.559, 0.507, 0.0, 0.373]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 9 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial incoherence 1-|Z|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 2.13 (aggregate of 9 individuals; 0/9 membrane-like individually; rim level 0.419)
  - radial cos phase: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.53, rim/outside 0.9 (aggregate of 9 individuals; 0/9 membrane-like individually; rim level 0.588)
  - radial fuel Y: flat profile (no radial structure; level 0; aggregate of 9 individuals)
  - radial local frequency: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 2.44 (aggregate of 9 individuals; 1/9 membrane-like individually; rim level 0.325)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #99 (t=930, R_eq 60.12, ring): none; #126 (t=1200, R_eq 62.58, ring): none; #20 (t=180, R_eq 52.57): none; #31 (t=330, R_eq 61.54): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- radial: 1 of 9 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 6 of 9 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
