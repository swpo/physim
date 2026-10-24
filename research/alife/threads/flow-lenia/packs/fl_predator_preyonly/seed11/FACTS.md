# Evidence pack: fl_predator_preyonly (seed 11)

- world: `../../../worlds/fl_predator_preyonly/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_predator; mutation: ablation arm: preyonly (otherwise identical to fl_predator)
- run: 301 frames x 40 steps x dt 0.2 = time 2400; grid [128, 128]; wall 268s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_predator_preyonly/world.py --out threads/flow-lenia/packs/fl_predator_preyonly/seed11 --frames 300 --seeds 11`
- segmentation: matter > 0.07 of robust range [0.0, 2.2284], min area 6 px

## Measurements
- components: final 9, mean 12.6, max 19; occupancy final 0.10
- tracks: 978; persistent (alive >= 50% of run): 0; longest 34 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [6, 3, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 13, 9], H1 [12, 6, 1]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.594/time; max body lengths 12.1
- replication (lineage window K = 20 frames = time 160, default): splits 353, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 321, merge/split ratio 0.909, nucleations 13
- channel total drift (end/start - 1): [3.219, None, -0.5565]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 97 at frame 86: holes 0, rim-vs-core 0.27, rim-vs-outside 0.26, heterogeneity 0.11; core [0.533, 0.0, 0.045] rim [0.263, 0.0, 0.055]
  - track 4 at frame 18: holes 0, rim-vs-core 0.40, rim-vs-outside 0.23, heterogeneity 0.16; core [0.58, 0.0, 0.344] rim [0.197, 0.0, 0.462]
  - track 2 at frame 15: holes 0, rim-vs-core 0.42, rim-vs-outside 0.09, heterogeneity 0.15; core [0.475, 0.0, 0.343] rim [0.067, 0.0, 0.438]
  - track 6 at frame 15: holes 0, rim-vs-core 0.41, rim-vs-outside 0.23, heterogeneity 0.15; core [0.613, 0.0, 0.297] rim [0.209, 0.0, 0.367]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 69 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial prey: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 30.5 (aggregate of 69 individuals; 27/69 membrane-like individually; rim level 0.468)
  - radial predator: flat profile (no radial structure; level 0; aggregate of 69 individuals)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.22, rim/outside 0.88 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.0626)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #97 (t=688, R_eq 7.29): none; #4 (t=144, R_eq 7.4): none; #2 (t=120, R_eq 5.89): ['prey']; #6 (t=120, R_eq 7.14): ['prey']
- species `prey` (channels ['prey'], own threshold): components final 11, mean 18.6, max 30; tracks 2343, persistent 0; splits 401, persistent splits 0 (K=20), max generation 0, merges 364, merge/split 0.908; moving tracks 10
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 69 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
