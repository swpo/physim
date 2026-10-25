# Evidence pack: active-gel-fed-comets (seed 7)

- world: `../../../../contrib/20261025T1034-c09-active-gel-no-division/world_z45.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 301 frames x 100 steps x dt 0.01 = time 300; grid [128, 128]; wall 67s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1034-c09-active-gel-no-division/world_z45.py --out collective/work_c05/rev_gn/z45_ks03/seed7 --seeds 7 --frames 300 --no-movie`
- segmentation: matter > 0.25 of robust range [0.0612, 3.8144], min area 6 px

## Measurements
- components: final 11, mean 8.0, max 57; occupancy final 0.02
- tracks: 107; persistent (alive >= 50% of run): 3; longest 210 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.38/time; max body lengths 9.7
- replication (lineage window K = 20 frames = time 20, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 32, merge/split ratio 16, nucleations 72
- channel total drift (end/start - 1): [-0.7442, -0.6809, -0.4325]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 96 at frame 197: holes 0, rim-vs-core 0.35, rim-vs-outside 0.30, heterogeneity 0.10; core [0.964, 0.458, 0.064] rim [0.621, 0.385, 0.109]
  - track 97 at frame 199: holes 0, rim-vs-core 0.34, rim-vs-outside 0.32, heterogeneity 0.09; core [0.995, 0.491, 0.067] rim [0.667, 0.409, 0.109]
  - track 98 at frame 199: holes 0, rim-vs-core 0.34, rim-vs-outside 0.31, heterogeneity 0.10; core [0.974, 0.454, 0.066] rim [0.643, 0.394, 0.107]
  - track 99 at frame 232: holes 0, rim-vs-core 0.34, rim-vs-outside 0.31, heterogeneity 0.10; core [0.97, 0.475, 0.066] rim [0.639, 0.415, 0.107]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.841, rim/outside 8.91 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.834)
  - radial regulator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 1.63 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.451)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.45, rim/outside 0.709 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.166)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #96 (t=197, R_eq 2.88): none; #97 (t=199, R_eq 2.71): none; #98 (t=199, R_eq 2.82): none; #99 (t=232, R_eq 2.82): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
