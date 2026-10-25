# Evidence pack: active-gel (seed 1)

- world: `../../world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 151 frames x 100 steps x dt 0.01 = time 150; grid [128, 128]; wall 27s; status ok
- command: `python -m labkit.run /tmp/claude-0/c09/ag/ag1/world.py --out /tmp/claude-0/c09/ag/ag1/pack2 --seeds 0 1 --frames 150 --no-movie`
- segmentation: matter > 0.28 of robust range [0.1032, 10.3295], min area 6 px

## Measurements
- components: final 48, mean 45.3, max 77; occupancy final 0.10
- tracks: 239; persistent (alive >= 50% of run): 22; longest 143 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.20 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [52, 49, 39], H1 [0, 0, 0]
- motion: 57 long-lived tracks moved >= 1 body length; max speed 0.325/time; max body lengths 4.6
- replication (lineage window K = 20 frames = time 20, default): splits 36, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 77, merge/split ratio 2.14, nucleations 93
- channel total drift (end/start - 1): [0.0005, 0.0004]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 79: holes 0, rim-vs-core 0.44, rim-vs-outside 0.25, heterogeneity 0.22; core [0.845, 0.621] rim [0.419, 0.512]
  - track 11 at frame 79: holes 0, rim-vs-core 0.43, rim-vs-outside 0.29, heterogeneity 0.20; core [0.827, 0.788] rim [0.443, 0.594]
  - track 17 at frame 79: holes 0, rim-vs-core 0.46, rim-vs-outside 0.28, heterogeneity 0.21; core [0.837, 0.808] rim [0.419, 0.624]
  - track 196 at frame 130: holes 0, rim-vs-core 0.36, rim-vs-outside 0.29, heterogeneity 0.15; core [0.784, 0.81] rim [0.465, 0.653]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 277 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial generator a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.645, rim/outside 8.46 (aggregate of 277 individuals; 1/277 membrane-like individually; rim level 0.529)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.847, rim/outside 2.54 (aggregate of 277 individuals; 1/277 membrane-like individually; rim level 0.664)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=79, R_eq 3.66): none; #11 (t=79, R_eq 3.24): none; #17 (t=79, R_eq 3.34): none; #196 (t=130, R_eq 3.04): none

## Warnings
- radial: 1 of 277 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
