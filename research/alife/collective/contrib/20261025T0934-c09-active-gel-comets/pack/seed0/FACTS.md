# Evidence pack: active-gel (seed 0)

- world: `../../world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 151 frames x 100 steps x dt 0.01 = time 150; grid [128, 128]; wall 31s; status ok
- command: `python -m labkit.run /tmp/claude-0/c09/ag/ag1/world.py --out /tmp/claude-0/c09/ag/ag1/pack2 --seeds 0 1 --frames 150 --no-movie`
- segmentation: matter > 0.28 of robust range [0.1115, 10.3297], min area 6 px

## Measurements
- components: final 49, mean 48.6, max 75; occupancy final 0.10
- tracks: 173; persistent (alive >= 50% of run): 41; longest 143 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [53, 50, 46], H1 [0, 0, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 0.346/time; max body lengths 4.7
- replication (lineage window K = 20 frames = time 20, default): splits 19, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 52, merge/split ratio 2.74, nucleations 84
- channel total drift (end/start - 1): [-0.0003, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 79: holes 0, rim-vs-core 0.47, rim-vs-outside 0.28, heterogeneity 0.21; core [0.843, 0.818] rim [0.423, 0.599]
  - track 8 at frame 79: holes 0, rim-vs-core 0.38, rim-vs-outside 0.28, heterogeneity 0.17; core [0.784, 0.772] rim [0.442, 0.604]
  - track 12 at frame 79: holes 0, rim-vs-core 0.45, rim-vs-outside 0.30, heterogeneity 0.18; core [0.803, 0.918] rim [0.411, 0.688]
  - track 117 at frame 97: holes 0, rim-vs-core 0.33, rim-vs-outside 0.27, heterogeneity 0.15; core [0.75, 0.788] rim [0.459, 0.643]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 303 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial generator a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.644, rim/outside 11.1 (aggregate of 303 individuals; 0/303 membrane-like individually; rim level 0.566)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.835, rim/outside 2.98 (aggregate of 303 individuals; 0/303 membrane-like individually; rim level 0.7)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=79, R_eq 3.14): none; #8 (t=79, R_eq 3.14): none; #12 (t=79, R_eq 3.24): none; #117 (t=97, R_eq 3.39): none

## Warnings
- radial: 1 of 303 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
