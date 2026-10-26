# Evidence pack: fl_morph257 (seed 6)

- world: `../../../../../../threads/flow-lenia/worlds/fl_morph257/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_forager; mutation: rule_seed 257 (two coexisting morphs: orange rings, cyan crescents) in the forager food world; 20x20 patch
- run: 301 frames x 20 steps x dt 0.2 = time 1200; grid [128, 128]; wall 86s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_morph257/world.py --out collective/contrib/20261025T2325-c23-review-flmorph/rerun/seed6 --seeds 6 --frames 300 --spf 20 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0, 1.8486], min area 6 px

## Measurements
- components: final 13, mean 10.5, max 15; occupancy final 0.16
- tracks: 410; persistent (alive >= 50% of run): 0; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.38, final 1; holes at thresholds 0.2/0.35/0.5 final [19, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [53, 28, 16], H1 [30, 12, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.408/time; max body lengths 3.8
- replication (lineage window K = 20 frames = time 80, default): splits 142, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 136, merge/split ratio 0.958, nucleations 1
- channel total drift (end/start - 1): [4.1124, 0.5509, -0.579]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 236 at frame 229: holes 1, rim-vs-core 0.05, rim-vs-outside 0.33, heterogeneity 0.19; core [0.287, 0.039, 0.021] rim [0.322, 0.066, 0.033]
  - track 78 at frame 106: holes 0, rim-vs-core 0.05, rim-vs-outside 0.35, heterogeneity 0.12; core [0.378, 0.0, 0.064] rim [0.346, 0.0, 0.101]
  - track 176 at frame 179: holes 0, rim-vs-core 0.10, rim-vs-outside 0.32, heterogeneity 0.13; core [0.415, 0.0, 0.05] rim [0.32, 0.0, 0.057]
  - track 289 at frame 222: holes 0, rim-vs-core 0.06, rim-vs-outside 0.33, heterogeneity 0.12; core [0.388, 0.0, 0.045] rim [0.332, 0.0, 0.042]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 65 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 3.29 (aggregate of 65 individuals; 14/65 membrane-like individually; rim level 0.214)
  - radial A1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.01, rim/outside 7.07 (aggregate of 65 individuals; 37/65 membrane-like individually; rim level 0.269)  MEMBRANE-LIKE
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.81, rim/outside 0.742 (aggregate of 65 individuals; 1/65 membrane-like individually; rim level 0.101)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #236 (t=916, R_eq 12.46, ring): ['A0']; #78 (t=424, R_eq 6.91): ['A1']; #176 (t=716, R_eq 6.6): none; #289 (t=888, R_eq 7.16): ['A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 65 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
