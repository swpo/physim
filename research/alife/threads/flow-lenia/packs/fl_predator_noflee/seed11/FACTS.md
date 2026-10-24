# Evidence pack: fl_predator_noflee (seed 11)

- world: `../../../worlds/fl_predator_noflee/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_predator; mutation: ablation arm: noflee (otherwise identical to fl_predator)
- run: 301 frames x 40 steps x dt 0.2 = time 2400; grid [128, 128]; wall 262s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_predator_noflee/world.py --out threads/flow-lenia/packs/fl_predator_noflee/seed11 --frames 300 --seeds 11`
- segmentation: matter > 0.10 of robust range [0.0, 1.5329], min area 6 px

## Measurements
- components: final 0, mean 1.4, max 9; occupancy final 0.00
- tracks: 49; persistent (alive >= 50% of run): 0; longest 56 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.341/time; max body lengths 4.9
- replication (lineage window K = 20 frames = time 160, default): splits 16, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 10, merge/split ratio 0.625, nucleations 3
- channel total drift (end/start - 1): [-1.0, -1.0, 0.3417]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 26 at frame 50: holes 0, rim-vs-core 0.49, rim-vs-outside 0.41, heterogeneity 0.29; core [0.478, 0.882, 0.663] rim [0.0, 0.826, 0.772]
  - track 28 at frame 38: holes 0, rim-vs-core 0.27, rim-vs-outside 0.65, heterogeneity 0.13; core [0.928, 0.0, 0.0] rim [0.658, 0.0, 0.016]
  - track 35 at frame 48: holes 0, rim-vs-core 0.42, rim-vs-outside 0.12, heterogeneity 0.27; core [0.413, 0.871, 0.688] rim [0.0, 0.871, 0.757]
  - track 19 at frame 28: holes 0, rim-vs-core 0.33, rim-vs-outside 0.63, heterogeneity 0.13; core [0.967, 0.0, 0.001] rim [0.642, 0.0, 0.024]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [50]):
  - radial prey: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.676, rim/outside 14.3 (aggregate of 6 individuals; 1/6 membrane-like individually; rim level 0.525)
  - radial predator: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.39, rim/outside 11.3 (aggregate of 6 individuals; 3/6 membrane-like individually; rim level 0.595)
  - radial food: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.64, rim/outside 1.24 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.425)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #26 (t=400, R_eq 5.94): ['predator']; #28 (t=304, R_eq 7.38): none; #35 (t=384, R_eq 5.53): ['predator']; #19 (t=224, R_eq 6.33): none
- species `prey` (channels ['prey'], own threshold): components final 0, mean 1.1, max 8; tracks 22, persistent 0; splits 7, persistent splits 2 (K=20), max generation 1, merges 1, merge/split 0.143; moving tracks 6
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.7, max 5; tracks 29, persistent 0; splits 4, persistent splits 0 (K=20), max generation 0, merges 5, merge/split 1.25; moving tracks 1

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
