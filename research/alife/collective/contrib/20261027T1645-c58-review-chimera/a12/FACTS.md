# Evidence pack: chimera-field (seed 5)

- world: `../../20261027T1049-c55-chimera-field-negative/world.py`, family `nonlocal-oscillators`
- parent: None; mutation: -
- run: 301 frames x 50 steps x dt 0.1 = time 1500; grid [128, 128]; wall 28s; status ok
- command: `python -m labkit.run collective/contrib/20261027T1049-c55-chimera-field-negative/world.py --out collective/contrib/20261027T1645-c58-review-chimera/a12 --seeds 5 --frames 300 --spf 50 --no-movie`
- segmentation: matter > 0.31 of robust range [0.0, 0.9705], min area 6 px

## Measurements
- components: final 1, mean 1.8, max 7; occupancy final 0.64
- tracks: 282; persistent (alive >= 50% of run): 0; longest 10 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.55, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 5, 3], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 100, default): splits 107, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 61, merge/split ratio 0.57, nucleations 2
- channel total drift (end/start - 1): [None, -19.3244, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 50 at frame 66: holes 0, rim-vs-core 0.29, rim-vs-outside 0.43, heterogeneity 0.18; core [0.768, 0.49, 0.0, 0.506] rim [0.533, 0.55, 0.0, 0.354]
  - track 64 at frame 86: holes 4, rim-vs-core 0.24, rim-vs-outside 0.43, heterogeneity 0.18; core [0.747, 0.504, 0.0, 0.497] rim [0.546, 0.457, 0.0, 0.371]
  - track 168 at frame 199: holes 3, rim-vs-core 0.27, rim-vs-outside 0.45, heterogeneity 0.18; core [0.722, 0.628, 0.0, 0.484] rim [0.544, 0.467, 0.0, 0.361]
  - track 23 at frame 23: holes 1, rim-vs-core 0.34, rim-vs-outside 0.42, heterogeneity 0.18; core [0.739, 0.675, 0.0, 0.479] rim [0.518, 0.457, 0.0, 0.331]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 8 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial incoherence 1-|Z|: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.972, rim/outside 2.45 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.482)
  - radial cos phase: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.891, rim/outside 1.97 (aggregate of 8 individuals; 1/8 membrane-like individually; rim level 0.495)
  - radial fuel Y: flat profile (no radial structure; level 0; aggregate of 8 individuals)
  - radial local frequency: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.934, rim/outside 1.76 (aggregate of 8 individuals; 1/8 membrane-like individually; rim level 0.318)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #50 (t=330, R_eq 55.87): none; #64 (t=430, R_eq 59.91): none; #168 (t=995, R_eq 57.36): none; #23 (t=115, R_eq 51.55): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 8 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 6 of 8 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
