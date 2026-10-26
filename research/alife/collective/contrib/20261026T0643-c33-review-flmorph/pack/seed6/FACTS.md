# Evidence pack: fl_morph257 (seed 6)

- world: `../../../../../threads/flow-lenia/worlds/fl_morph257/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_forager; mutation: rule_seed 257 (two coexisting morphs: orange rings, cyan crescents) in the forager food world; 20x20 patch
- run: 201 frames x 10 steps x dt 0.2 = time 400; grid [128, 128]; wall 38s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_morph257/world.py --out collective/contrib/wip-c33-fl/pack --seeds 5 6 --frames 200 --no-movie`
- segmentation: matter > 0.09 of robust range [0.0, 1.7514], min area 6 px

## Measurements
- components: final 7, mean 6.9, max 11; occupancy final 0.11
- tracks: 180; persistent (alive >= 50% of run): 1; longest 101 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.81 (1 = constant size)
- enclosures: components with a hole mean 1.02, final 2; holes at thresholds 0.2/0.35/0.5 final [14, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 14, 11], H1 [21, 8, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.473/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 40, default): splits 61, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 57, merge/split ratio 0.934, nucleations 0
- channel total drift (end/start - 1): [2.2867, 0.5341, -0.3497]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 55: holes 0, rim-vs-core 0.54, rim-vs-outside 0.08, heterogeneity 0.15; core [0.602, 0.0, 0.173] rim [0.064, 0.0, 0.246]
  - track 108 at frame 161: holes 0, rim-vs-core 0.15, rim-vs-outside 0.31, heterogeneity 0.14; core [0.449, 0.0, 0.083] rim [0.304, 0.0, 0.129]
  - track 98 at frame 145: holes 0, rim-vs-core 0.11, rim-vs-outside 0.38, heterogeneity 0.15; core [0.0, 0.468, 0.026] rim [0.0, 0.379, 0.082]
  - track 107 at frame 148: holes 0, rim-vs-core 0.20, rim-vs-outside 0.36, heterogeneity 0.16; core [0.514, 0.0, 0.137] rim [0.331, 0.0, 0.219]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 6.85 (aggregate of 40 individuals; 13/40 membrane-like individually; rim level 0.272)
  - radial A1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.64, rim/outside 5.6 (aggregate of 40 individuals; 22/40 membrane-like individually; rim level 0.208)  MEMBRANE-LIKE
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.53, rim/outside 0.681 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.269)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #2 (t=110, R_eq 4.37): ['A0']; #108 (t=322, R_eq 6.53): ['A1']; #98 (t=290, R_eq 6.1): ['A1']; #107 (t=296, R_eq 7.31): ['A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 40 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
