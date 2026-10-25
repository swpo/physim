# Evidence pack: active-model-h (seed 3)

- world: `../../../20261025T1240-c12-amh-turnover-static/world.py`, family `active-model-h`
- parent: None; mutation: -
- run: 151 frames x 200 steps x dt 0.05 = time 1500; grid [128, 128]; wall 330s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1240-c12-amh-turnover-static/world.py --out collective/contrib/20261025T1406-c09-review-amh/e1zm1/seed3 --seeds 3 --frames 150 --spf 200 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1073, 1.9933], min area 6 px

## Measurements
- components: final 80, mean 54.3, max 97; occupancy final 0.38
- tracks: 171; persistent (alive >= 50% of run): 73; longest 109 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.71 (1 = constant size)
- enclosures: components with a hole mean 0.21, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [82, 82, 80], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 200, default): splits 55, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 4, merges 7, merge/split ratio 0.127, nucleations 0
- channel total drift (end/start - 1): [-0.0003, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 96: holes 0, rim-vs-core 0.49, rim-vs-outside 0.21, heterogeneity 0.21; core [0.804, 0.313] rim [0.321, 0.363]
  - track 4 at frame 100: holes 0, rim-vs-core 0.48, rim-vs-outside 0.21, heterogeneity 0.24; core [0.79, 0.55] rim [0.315, 0.537]
  - track 5 at frame 100: holes 0, rim-vs-core 0.47, rim-vs-outside 0.19, heterogeneity 0.25; core [0.787, 0.741] rim [0.318, 0.669]
  - track 160 at frame 113: holes 0, rim-vs-core 0.47, rim-vs-outside 0.20, heterogeneity 0.25; core [0.793, 0.593] rim [0.325, 0.564]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 360 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi + 1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.698, rim/outside 5.48 (aggregate of 360 individuals; 0/360 membrane-like individually; rim level 0.648)
  - radial flow speed |u|: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.52, rim/outside 1.44 (aggregate of 360 individuals; 139/360 membrane-like individually; rim level 0.433)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=960, R_eq 5.29): none; #4 (t=1000, R_eq 5.14): none; #5 (t=1000, R_eq 4.98): none; #160 (t=1130, R_eq 5.11): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- radial: for 2 of 360 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
