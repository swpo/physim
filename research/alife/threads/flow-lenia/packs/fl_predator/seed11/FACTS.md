# Evidence pack: fl_predator (seed 11)

- world: `../../../worlds/fl_predator/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_forager (prey and predator both use glider rule C2_r202); mutation: two glider species with their own rules; predator matter converts prey matter it overlaps (mass-conserving), is drawn up a blurred prey field and decays to food; prey eat food
- run: 301 frames x 40 steps x dt 0.2 = time 2400; grid [128, 128]; wall 266s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_predator/world.py --out threads/flow-lenia/packs/fl_predator/seed11 --frames 300 --seeds 11`
- segmentation: matter > 0.07 of robust range [0.0, 2.2569], min area 6 px

## Measurements
- components: final 16, mean 14.6, max 23; occupancy final 0.13
- tracks: 1401; persistent (alive >= 50% of run): 0; longest 22 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [6, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 18, 17], H1 [10, 7, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.712/time; max body lengths 11.6
- replication (lineage window K = 20 frames = time 160, default): splits 521, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 452, merge/split ratio 0.868, nucleations 26
- channel total drift (end/start - 1): [4.1862, -1.0, -0.5548]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1209 at frame 270: holes 0, rim-vs-core 0.46, rim-vs-outside 0.05, heterogeneity 0.11; core [0.522, 0.0, 0.035] rim [0.058, 0.0, 0.024]
  - track 5 at frame 13: holes 0, rim-vs-core 0.26, rim-vs-outside 0.35, heterogeneity 0.22; core [0.54, 0.025, 0.348] rim [0.313, 0.154, 0.333]
  - track 13 at frame 25: holes 0, rim-vs-core 0.42, rim-vs-outside 0.10, heterogeneity 0.15; core [0.501, 0.126, 0.167] rim [0.086, 0.105, 0.208]
  - track 38 at frame 38: holes 0, rim-vs-core 0.45, rim-vs-outside 0.04, heterogeneity 0.12; core [0.477, 0.003, 0.122] rim [0.031, 0.005, 0.152]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 102 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial prey: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 18.6 (aggregate of 102 individuals; 30/102 membrane-like individually; rim level 0.461)
  - radial predator: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 1.1 (aggregate of 102 individuals; 4/102 membrane-like individually; rim level 0.0251)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 0.931 (aggregate of 102 individuals; 0/102 membrane-like individually; rim level 0.0516)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1209 (t=2160, R_eq 5.84): none; #5 (t=104, R_eq 6.63): ['predator']; #13 (t=200, R_eq 5.41): ['prey']; #38 (t=304, R_eq 5.38): ['prey']
- species `prey` (channels ['prey'], own threshold): components final 18, mean 22.8, max 37; tracks 2948, persistent 0; splits 486, persistent splits 0 (K=20), max generation 0, merges 423, merge/split 0.87; moving tracks 8
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.3, max 3; tracks 12, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
