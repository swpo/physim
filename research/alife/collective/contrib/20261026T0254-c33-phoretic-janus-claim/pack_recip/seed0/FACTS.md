# Evidence pack: phoretic-colloids (seed 0)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 57s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33/world.py --out collective/contrib/wip-c33/pack_recip --seeds 0 1 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8185], min area 6 px

## Measurements
- components: final 19, mean 24.6, max 40; occupancy final 0.07
- tracks: 130; persistent (alive >= 50% of run): 17; longest 373 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 20, 18], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.243/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 10, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 30, merge/split ratio 30, nucleations 98
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 215: holes 0, rim-vs-core 0.24, rim-vs-outside 0.27, heterogeneity 0.11; core [0.742, 0.439, 0.477] rim [0.521, 0.399, 0.405]
  - track 30 at frame 222: holes 0, rim-vs-core 0.32, rim-vs-outside 0.34, heterogeneity 0.14; core [0.796, 0.587, 0.67] rim [0.587, 0.381, 0.544]
  - track 34 at frame 222: holes 0, rim-vs-core 0.26, rim-vs-outside 0.35, heterogeneity 0.13; core [0.71, 0.791, 0.466] rim [0.52, 0.616, 0.414]
  - track 38 at frame 222: holes 0, rim-vs-core 0.26, rim-vs-outside 0.32, heterogeneity 0.16; core [0.802, 0.412, 0.532] rim [0.557, 0.389, 0.448]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 135 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.829, rim/outside 22.1 (aggregate of 135 individuals; 0/135 membrane-like individually; rim level 0.715)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 17.3 (aggregate of 135 individuals; 23/135 membrane-like individually; rim level 0.537)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 2.82 (aggregate of 135 individuals; 0/135 membrane-like individually; rim level 0.612)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=107.5, R_eq 2.93): none; #30 (t=111, R_eq 3.91): none; #34 (t=111, R_eq 2.59): none; #38 (t=111, R_eq 3.24): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
