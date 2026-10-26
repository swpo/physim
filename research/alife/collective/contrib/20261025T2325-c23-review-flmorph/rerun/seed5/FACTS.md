# Evidence pack: fl_morph257 (seed 5)

- world: `../../../../../../threads/flow-lenia/worlds/fl_morph257/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_forager; mutation: rule_seed 257 (two coexisting morphs: orange rings, cyan crescents) in the forager food world; 20x20 patch
- run: 301 frames x 20 steps x dt 0.2 = time 1200; grid [128, 128]; wall 86s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_morph257/world.py --out collective/contrib/20261025T2325-c23-review-flmorph/rerun/seed5 --seeds 5 --frames 300 --spf 20 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0, 1.8582], min area 6 px

## Measurements
- components: final 13, mean 8.3, max 13; occupancy final 0.15
- tracks: 307; persistent (alive >= 50% of run): 2; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.63 (1 = constant size)
- enclosures: components with a hole mean 1.63, final 2; holes at thresholds 0.2/0.35/0.5 final [17, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 16, 11], H1 [17, 5, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.201/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 80, default): splits 105, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 99, merge/split ratio 0.943, nucleations 0
- channel total drift (end/start - 1): [3.6735, 0.8071, -0.5318]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 116: holes 2, rim-vs-core 0.33, rim-vs-outside 0.25, heterogeneity 0.21; core [0.471, 0.257, 0.121] rim [0.234, 0.03, 0.144]
  - track 107 at frame 161: holes 0, rim-vs-core 0.47, rim-vs-outside 0.08, heterogeneity 0.11; core [0.0, 0.54, 0.048] rim [0.0, 0.075, 0.064]
  - track 71 at frame 129: holes 0, rim-vs-core 0.14, rim-vs-outside 0.30, heterogeneity 0.13; core [0.435, 0.0, 0.076] rim [0.297, 0.0, 0.111]
  - track 202 at frame 242: holes 0, rim-vs-core 0.46, rim-vs-outside 0.11, heterogeneity 0.11; core [0.0, 0.565, 0.009] rim [0.0, 0.109, 0.025]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 56 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 3.31 (aggregate of 56 individuals; 16/56 membrane-like individually; rim level 0.177)
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.44, rim/outside 11.7 (aggregate of 56 individuals; 26/56 membrane-like individually; rim level 0.344)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.84, rim/outside 0.72 (aggregate of 56 individuals; 1/56 membrane-like individually; rim level 0.131)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=464, R_eq 9.42): ['A0']; #107 (t=644, R_eq 5.84): ['A1']; #71 (t=516, R_eq 8.06): ['A1']; #202 (t=968, R_eq 5.64): ['A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 56 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
