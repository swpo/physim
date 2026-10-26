# Evidence pack: phoretic-colloids (seed 0)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 115s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33-nuc/world.py --out collective/contrib/wip-c33-nuc/pack_off --seeds 0 1 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.4545], min area 6 px

## Measurements
- components: final 7, mean 9.7, max 17; occupancy final 0.03
- tracks: 203; persistent (alive >= 50% of run): 5; longest 589 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 12, 5], H1 [0, 0, 0]
- motion: 38 long-lived tracks moved >= 1 body length; max speed 0.532/time; max body lengths 8.6
- replication (lineage window K = 20 frames = time 10, default): splits 10, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 3, merges 21, merge/split ratio 2.1, nucleations 162
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 26 at frame 397: holes 0, rim-vs-core 0.19, rim-vs-outside 0.21, heterogeneity 0.09; core [0.741, 0.085, 0.325] rim [0.624, 0.228, 0.303]
  - track 5 at frame 323: holes 0, rim-vs-core 0.25, rim-vs-outside 0.19, heterogeneity 0.12; core [0.813, 0.124, 0.466] rim [0.621, 0.272, 0.41]
  - track 192 at frame 787: holes 0, rim-vs-core 0.11, rim-vs-outside 0.19, heterogeneity 0.07; core [0.747, 0.03, 0.399] rim [0.647, 0.076, 0.373]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 54 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.89, rim/outside 9.81 (aggregate of 54 individuals; 3/54 membrane-like individually; rim level 0.701)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 7.43 (aggregate of 54 individuals; 33/54 membrane-like individually; rim level 0.382)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.827, rim/outside 2.28 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.528)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #26 (t=198.5, R_eq 2.11): ['B density']; #5 (t=161.5, R_eq 3.24): ['B density']; #74 (t=212, R_eq 2.33): ['B density']; #192 (t=393.5, R_eq 2.33): ['B density']

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
