# Evidence pack: active-gel-fed-comets (seed 7)

- world: `../../../../contrib/20261025T1016-c09-active-gel-comets-claim/world_starve.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 46s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1016-c09-active-gel-comets-claim/world_starve.py --out collective/work_c05/rev_gel/world_starve/seed7 --seeds 7 --frames 200 --no-movie`
- segmentation: matter > 0.13 of robust range [0.0, 7.901], min area 6 px

## Measurements
- components: final 0, mean 9.1, max 46; occupancy final 0.00
- tracks: 94; persistent (alive >= 50% of run): 3; longest 111 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.22 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 29 long-lived tracks moved >= 1 body length; max speed 0.534/time; max body lengths 6.1
- replication (lineage window K = 20 frames = time 20, default): splits 8, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 28, merge/split ratio 3.5, nucleations 55
- channel total drift (end/start - 1): [-0.9999, -0.7713, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 74 at frame 71: holes 0, rim-vs-core 0.25, rim-vs-outside 0.24, heterogeneity 0.06; core [0.694, 0.581, 0.351] rim [0.444, 0.542, 0.37]
  - track 73 at frame 71: holes 0, rim-vs-core 0.32, rim-vs-outside 0.23, heterogeneity 0.08; core [0.733, 0.71, 0.325] rim [0.42, 0.659, 0.348]
  - track 86 at frame 94: holes 0, rim-vs-core 0.28, rim-vs-outside 0.24, heterogeneity 0.06; core [0.718, 0.583, 0.36] rim [0.438, 0.546, 0.381]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 31 components >= 12 px at frames [34, 67, 101]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.671, rim/outside 15 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.651)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 1.26 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.725)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 0.871 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.335)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #72 (t=71, R_eq 1.78): none; #74 (t=71, R_eq 2.03): none; #73 (t=71, R_eq 2.26): none; #86 (t=94, R_eq 2.11): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
