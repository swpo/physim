# Evidence pack: active-model-h (seed 0)

- world: `../../world.py`, family `active-model-h`
- parent: None; mutation: -
- run: 161 frames x 250 steps x dt 0.05 = time 2000; grid [128, 128]; wall 668s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1225-c12-active-model-h-sighting/world.py --out collective/contrib/20261025T1225-c12-active-model-h-sighting/pack --seeds 0 1 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.22 of robust range [0.0583, 2.0337], min area 6 px

## Measurements
- components: final 63, mean 60.1, max 98; occupancy final 0.38
- tracks: 183; persistent (alive >= 50% of run): 68; longest 130 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.43 (1 = constant size)
- enclosures: components with a hole mean 0.18, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [66, 66, 65], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 250, default): splits 59, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 19, merge/split ratio 0.322, nucleations 0
- channel total drift (end/start - 1): [-0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 95: holes 0, rim-vs-core 0.47, rim-vs-outside 0.21, heterogeneity 0.21; core [0.81, 0.299] rim [0.343, 0.38]
  - track 4 at frame 97: holes 0, rim-vs-core 0.48, rim-vs-outside 0.22, heterogeneity 0.19; core [0.814, 0.221] rim [0.343, 0.302]
  - track 6 at frame 97: holes 0, rim-vs-core 0.48, rim-vs-outside 0.22, heterogeneity 0.21; core [0.823, 0.311] rim [0.349, 0.411]
  - track 154 at frame 106: holes 0, rim-vs-core 0.42, rim-vs-outside 0.25, heterogeneity 0.20; core [0.807, 0.256] rim [0.393, 0.313]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 391 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi + 1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.73, rim/outside 5.07 (aggregate of 391 individuals; 0/391 membrane-like individually; rim level 0.677)
  - radial flow speed |u|: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 1.36 (aggregate of 391 individuals; 137/391 membrane-like individually; rim level 0.431)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=1187.5, R_eq 5.44): none; #4 (t=1212.5, R_eq 5.61): none; #6 (t=1212.5, R_eq 5.75): ['flow speed |u|']; #154 (t=1325, R_eq 4.95): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- radial: for 1 of 391 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
