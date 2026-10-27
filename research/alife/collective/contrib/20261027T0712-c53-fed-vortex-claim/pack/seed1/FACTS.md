# Evidence pack: fed-vortices (seed 1)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 283s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/pack --seeds 0 1 2 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2055], min area 6 px

## Measurements
- components: final 23, mean 31.2, max 49; occupancy final 0.14
- tracks: 281; persistent (alive >= 50% of run): 11; longest 955 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 27, 23], H1 [0, 0, 0]
- motion: 153 long-lived tracks moved >= 1 body length; max speed 0.397/time; max body lengths 38.6
- replication (lineage window K = 20 frames = time 60, default): splits 79, persistent splits 39 (0 more failed only because the siblings re-merged within K), max generation 9, merges 75, merge/split ratio 0.949, nucleations 0
- channel total drift (end/start - 1): [-0.5597, 0.1872, 249.6131, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 63 at frame 496: holes 0, rim-vs-core 0.74, rim-vs-outside 0.28, heterogeneity 0.19; core [0.807, 0.115, 0.063, 0.652] rim [0.388, 0.333, 0.279, 0.121]
  - track 106 at frame 597: holes 0, rim-vs-core 0.65, rim-vs-outside 0.30, heterogeneity 0.17; core [0.782, 0.138, 0.072, 0.649] rim [0.428, 0.279, 0.257, 0.154]
  - track 17 at frame 403: holes 0, rim-vs-core 0.66, rim-vs-outside 0.34, heterogeneity 0.17; core [0.824, 0.089, 0.049, 0.655] rim [0.459, 0.308, 0.241, 0.194]
  - track 274 at frame 992: holes 0, rim-vs-core 0.64, rim-vs-outside 0.28, heterogeneity 0.17; core [0.761, 0.108, 0.082, 0.565] rim [0.394, 0.316, 0.276, 0.126]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 175 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.769, rim/outside 16.5 (aggregate of 175 individuals; 1/175 membrane-like individually; rim level 0.686)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.9, rim/outside 0.773 (aggregate of 175 individuals; 0/175 membrane-like individually; rim level 0.476)
  - radial vorticity (signed): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 1 (aggregate of 175 individuals; 0/175 membrane-like individually; rim level 0.486)
  - radial eating: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.716, rim/outside 27.1 (aggregate of 175 individuals; 5/175 membrane-like individually; rim level 0.529)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #63 (t=1488, R_eq 4.85): none; #106 (t=1791, R_eq 3.95): none; #17 (t=1209, R_eq 4.98): none; #274 (t=2976, R_eq 5.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 175 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
