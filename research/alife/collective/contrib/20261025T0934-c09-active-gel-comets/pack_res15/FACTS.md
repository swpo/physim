# Evidence pack: active-gel (seed 0)

- world: `../world_res15.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 151 frames x 100 steps x dt 0.01 = time 150; grid [192, 192]; wall 66s; status ok
- command: `python -m labkit.run /tmp/claude-0/c09/ag/ag1/world_res15.py --out /tmp/claude-0/c09/ag/ag1/pack_res15 --seeds 0 --frames 150 --no-movie`
- segmentation: matter > 0.27 of robust range [0.131, 10.5734], min area 6 px

## Measurements
- components: final 45, mean 46.0, max 83; occupancy final 0.10
- tracks: 247; persistent (alive >= 50% of run): 29; longest 143 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 46, 31], H1 [0, 0, 0]
- motion: 53 long-lived tracks moved >= 1 body length; max speed 0.671/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 20, default): splits 26, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 86, merge/split ratio 3.31, nucleations 109
- channel total drift (end/start - 1): [-0.0001, 0.0001]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 79: holes 0, rim-vs-core 0.39, rim-vs-outside 0.21, heterogeneity 0.17; core [0.76, 0.944] rim [0.412, 0.766]
  - track 9 at frame 79: holes 0, rim-vs-core 0.38, rim-vs-outside 0.20, heterogeneity 0.19; core [0.731, 0.856] rim [0.395, 0.685]
  - track 45 at frame 81: holes 0, rim-vs-core 0.23, rim-vs-outside 0.20, heterogeneity 0.15; core [0.632, 0.678] rim [0.419, 0.585]
  - track 225 at frame 136: holes 0, rim-vs-core 0.41, rim-vs-outside 0.19, heterogeneity 0.20; core [0.784, 0.599] rim [0.397, 0.468]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 283 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.648, rim/outside 10 (aggregate of 283 individuals; 2/283 membrane-like individually; rim level 0.543)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.833, rim/outside 2.72 (aggregate of 283 individuals; 0/283 membrane-like individually; rim level 0.665)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=79, R_eq 4.58): none; #9 (t=79, R_eq 5.05): none; #45 (t=81, R_eq 5.97): none; #225 (t=136, R_eq 4.37): none

## Warnings
- radial: 3 of 283 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
