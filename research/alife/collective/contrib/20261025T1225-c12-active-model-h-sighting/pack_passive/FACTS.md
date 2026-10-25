# Evidence pack: active-model-h (seed 0)

- world: `../world.py`, family `active-model-h`
- parent: None; mutation: -
- run: 161 frames x 250 steps x dt 0.05 = time 2000; grid [128, 128]; wall 562s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1225-c12-active-model-h-sighting/world.py --out collective/contrib/20261025T1225-c12-active-model-h-sighting/pack_passive --seeds 0 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.23 of robust range [0.0402, 2.0385], min area 6 px

## Measurements
- components: final 37, mean 42.9, max 89; occupancy final 0.35
- tracks: 201; persistent (alive >= 50% of run): 21; longest 127 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.60 (1 = constant size)
- enclosures: components with a hole mean 0.17, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 37, 37], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.0142/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 250, default): splits 51, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 53, merge/split ratio 1.04, nucleations 0
- channel total drift (end/start - 1): [-0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 97: holes 0, rim-vs-core 0.48, rim-vs-outside 0.20, heterogeneity 0.15; core [0.818, 0.233] rim [0.343, 0.233]
  - track 35 at frame 99: holes 0, rim-vs-core 0.44, rim-vs-outside 0.21, heterogeneity 0.13; core [0.798, 0.326] rim [0.36, 0.316]
  - track 64 at frame 101: holes 0, rim-vs-core 0.23, rim-vs-outside 0.42, heterogeneity 0.14; core [0.796, 0.229] rim [0.563, 0.229]
  - track 7 at frame 93: holes 0, rim-vs-core 0.47, rim-vs-outside 0.20, heterogeneity 0.14; core [0.806, 0.243] rim [0.332, 0.24]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 269 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi + 1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 7.53 (aggregate of 269 individuals; 1/269 membrane-like individually; rim level 0.761)
  - radial flow speed |u|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.992, rim/outside 1.07 (aggregate of 269 individuals; 4/269 membrane-like individually; rim level 0.193)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=1212.5, R_eq 5.67): none; #35 (t=1237.5, R_eq 4.85): none; #64 (t=1262.5, R_eq 5.75): none; #7 (t=1162.5, R_eq 5.41): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- radial: for 1 of 269 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
