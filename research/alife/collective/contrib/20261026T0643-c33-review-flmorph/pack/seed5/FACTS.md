# Evidence pack: fl_morph257 (seed 5)

- world: `../../../../../threads/flow-lenia/worlds/fl_morph257/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_forager; mutation: rule_seed 257 (two coexisting morphs: orange rings, cyan crescents) in the forager food world; 20x20 patch
- run: 201 frames x 10 steps x dt 0.2 = time 400; grid [128, 128]; wall 49s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_morph257/world.py --out collective/contrib/wip-c33-fl/pack --seeds 5 6 --frames 200 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0, 1.7983], min area 6 px

## Measurements
- components: final 9, mean 7.2, max 10; occupancy final 0.10
- tracks: 160; persistent (alive >= 50% of run): 1; longest 165 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.73 (1 = constant size)
- enclosures: components with a hole mean 0.41, final 0; holes at thresholds 0.2/0.35/0.5 final [15, 6, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 12, 9], H1 [19, 7, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.21/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 40, default): splits 57, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 50, merge/split ratio 0.877, nucleations 0
- channel total drift (end/start - 1): [1.7683, 0.5502, -0.2748]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 119: holes 0, rim-vs-core 0.17, rim-vs-outside 0.25, heterogeneity 0.23; core [0.358, 0.158, 0.038] rim [0.215, 0.093, 0.102]
  - track 87 at frame 155: holes 0, rim-vs-core 0.17, rim-vs-outside 0.31, heterogeneity 0.15; core [0.459, 0.0, 0.078] rim [0.304, 0.0, 0.136]
  - track 14 at frame 55: holes 0, rim-vs-core 0.47, rim-vs-outside 0.12, heterogeneity 0.15; core [0.566, 0.0, 0.211] rim [0.1, 0.0, 0.293]
  - track 35 at frame 87: holes 0, rim-vs-core 0.44, rim-vs-outside 0.10, heterogeneity 0.13; core [0.54, 0.0, 0.03] rim [0.099, 0.0, 0.058]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 44 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 6.95 (aggregate of 44 individuals; 13/44 membrane-like individually; rim level 0.251)
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.7, rim/outside 7.46 (aggregate of 44 individuals; 25/44 membrane-like individually; rim level 0.266)  MEMBRANE-LIKE
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.52, rim/outside 0.671 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.215)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #25 (t=238, R_eq 8.41): ['A1']; #87 (t=310, R_eq 7.11): ['A1']; #14 (t=110, R_eq 5.78): none; #35 (t=174, R_eq 5.11): ['A0']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 44 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
