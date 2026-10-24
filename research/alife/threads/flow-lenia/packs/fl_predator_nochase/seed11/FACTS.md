# Evidence pack: fl_predator_nochase (seed 11)

- world: `../../../worlds/fl_predator_nochase/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_predator; mutation: ablation arm: nochase (otherwise identical to fl_predator)
- run: 301 frames x 40 steps x dt 0.2 = time 2400; grid [128, 128]; wall 263s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_predator_nochase/world.py --out threads/flow-lenia/packs/fl_predator_nochase/seed11 --frames 300 --seeds 11`
- segmentation: matter > 0.07 of robust range [0.0, 2.2595], min area 6 px

## Measurements
- components: final 11, mean 13.5, max 23; occupancy final 0.13
- tracks: 1170; persistent (alive >= 50% of run): 0; longest 23 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.15, final 0; holes at thresholds 0.2/0.35/0.5 final [5, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 16, 14], H1 [11, 6, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.617/time; max body lengths 9.6
- replication (lineage window K = 20 frames = time 160, default): splits 429, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 387, merge/split ratio 0.902, nucleations 23
- channel total drift (end/start - 1): [4.2197, -1.0, -0.5606]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 10: holes 0, rim-vs-core 0.19, rim-vs-outside 0.46, heterogeneity 0.13; core [0.0, 1.0, 0.883] rim [0.0, 0.882, 0.727]
  - track 5 at frame 13: holes 0, rim-vs-core 0.34, rim-vs-outside 0.27, heterogeneity 0.16; core [0.546, 0.003, 0.318] rim [0.223, 0.003, 0.428]
  - track 18 at frame 35: holes 0, rim-vs-core 0.40, rim-vs-outside 0.18, heterogeneity 0.20; core [0.561, 0.233, 0.196] rim [0.166, 0.26, 0.272]
  - track 34 at frame 48: holes 0, rim-vs-core 0.43, rim-vs-outside 0.06, heterogeneity 0.12; core [0.485, 0.089, 0.108] rim [0.058, 0.089, 0.125]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial prey: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 24.2 (aggregate of 81 individuals; 26/81 membrane-like individually; rim level 0.454)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.995, rim/outside 1 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.0026)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.2, rim/outside 0.91 (aggregate of 81 individuals; 1/81 membrane-like individually; rim level 0.0419)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=80, R_eq 4.37): none; #5 (t=104, R_eq 6.7): none; #18 (t=280, R_eq 8.2): none; #34 (t=384, R_eq 5.41): ['prey']
- species `prey` (channels ['prey'], own threshold): components final 15, mean 22.3, max 36; tracks 2946, persistent 0; splits 516, persistent splits 0 (K=20), max generation 0, merges 495, merge/split 0.959; moving tracks 13
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.2, max 3; tracks 6, persistent 0; splits 2, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 81 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
