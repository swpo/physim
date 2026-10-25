# Evidence pack: active-model-h (seed 3)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1240-c12-amh-turnover-static/world.py`, family `active-model-h`
- parent: None; mutation: -
- run: 151 frames x 200 steps x dt 0.05 = time 1500; grid [128, 128]; wall 327s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1240-c12-amh-turnover-static/world.py --out /tmp/claude-0/c11rev29/e0.003 --seeds 3 --frames 150 --no-movie`
- segmentation: matter > 0.19 of robust range [0.1726, 1.9161], min area 6 px

## Measurements
- components: final 90, mean 41.7, max 96; occupancy final 0.38
- tracks: 176; persistent (alive >= 50% of run): 17; longest 93 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.65 (1 = constant size)
- enclosures: components with a hole mean 0.31, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [91, 91, 90], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 200, default): splits 65, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.031, nucleations 0
- channel total drift (end/start - 1): [-0.0004, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 105: holes 0, rim-vs-core 0.49, rim-vs-outside 0.19, heterogeneity 0.25; core [0.775, 0.386] rim [0.286, 0.42]
  - track 4 at frame 108: holes 0, rim-vs-core 0.47, rim-vs-outside 0.20, heterogeneity 0.25; core [0.765, 0.556] rim [0.3, 0.586]
  - track 6 at frame 110: holes 0, rim-vs-core 0.50, rim-vs-outside 0.21, heterogeneity 0.25; core [0.776, 0.397] rim [0.302, 0.562]
  - track 91 at frame 120: holes 0, rim-vs-core 0.34, rim-vs-outside 0.16, heterogeneity 0.19; core [0.614, 0.295] rim [0.279, 0.347]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 297 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi + 1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.65, rim/outside 5.33 (aggregate of 297 individuals; 1/297 membrane-like individually; rim level 0.59)
  - radial flow speed |u|: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 1.47 (aggregate of 297 individuals; 149/297 membrane-like individually; rim level 0.441)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=1050, R_eq 5.23): ['flow speed |u|']; #4 (t=1080, R_eq 4.85): none; #6 (t=1100, R_eq 4.85): ['flow speed |u|']; #91 (t=1200, R_eq 3.43): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- radial: for 3 of 297 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
