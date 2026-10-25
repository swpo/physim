# Evidence pack: fch-pchemoton-kablate (seed 5)

- world: `../../world_kablate.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 373s; status ok
- command: `python -m labkit.run collective/contrib/c17-kb-wip/world_kablate.py --out collective/contrib/c17-kb-wip/kb05/seed5 --seeds 5 --no-movie`
- segmentation: matter > 0.39 of robust range [-0.0208, 1.5865], min area 6 px

## Measurements
- components: final 6, mean 6.0, max 6; occupancy final 0.04
- tracks: 6; persistent (alive >= 50% of run): 6; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.72 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 12, 6], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 6
- channel total drift (end/start - 1): [-0.5502, 1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.24, rim-vs-outside 0.31, heterogeneity 0.06; core [0.854, 1.0, 0.0] rim [0.609, 1.0, 0.0]
  - track 1 at frame 101: holes 0, rim-vs-core 0.27, rim-vs-outside 0.27, heterogeneity 0.06; core [0.844, 1.0, 0.0] rim [0.57, 1.0, 0.0]
  - track 2 at frame 101: holes 0, rim-vs-core 0.28, rim-vs-outside 0.27, heterogeneity 0.06; core [0.847, 1.0, 0.0] rim [0.565, 1.0, 0.0]
  - track 3 at frame 101: holes 0, rim-vs-core 0.29, rim-vs-outside 0.30, heterogeneity 0.06; core [0.883, 1.0, 0.0] rim [0.597, 1.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 36 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.553, rim/outside 4.55 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.412)
  - radial precursor P: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.982)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.986, rim/outside 1 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.0007)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 9.61): none; #1 (t=303, R_eq 9.59): none; #2 (t=303, R_eq 9.8): none; #3 (t=303, R_eq 8.06): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
