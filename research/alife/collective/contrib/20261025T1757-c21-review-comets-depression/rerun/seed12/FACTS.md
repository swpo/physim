# Evidence pack: neural-field-dep (seed 12)

- world: `../../../20261025T1721-c20-neural-comets-depression-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 30 steps x dt 0.1 = time 600; grid [128, 128]; wall 3s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1721-c20-neural-comets-depression-claim/world.py --out collective/contrib/20261025T1757-c21-review-comets-depression/rerun --seeds 11 12 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 40, mean 43.4, max 75; occupancy final 0.10
- tracks: 667; persistent (alive >= 50% of run): 0; longest 91 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 40], H1 [0, 0, 0]
- motion: 155 long-lived tracks moved >= 1 body length; max speed 0.586/time; max body lengths 19.4
- replication (lineage window K = 20 frames = time 60, default): splits 262, persistent splits 33 (0 more failed only because the siblings re-merged within K), max generation 5, merges 75, merge/split ratio 0.286, nucleations 1
- channel total drift (end/start - 1): [-1.0, None, -0.5667, -0.1892]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 466 at frame 153: holes 0, rim-vs-core 0.33, rim-vs-outside 0.88, heterogeneity 0.16; core [0.908, 0.713, 1.0, 0.187] rim [0.748, 0.488, 0.925, 0.343]
  - track 206 at frame 57: holes 0, rim-vs-core 0.24, rim-vs-outside 0.82, heterogeneity 0.16; core [0.877, 0.555, 1.0, 0.398] rim [0.678, 0.488, 0.901, 0.441]
  - track 495 at frame 161: holes 0, rim-vs-core 0.24, rim-vs-outside 0.83, heterogeneity 0.16; core [0.863, 0.527, 1.0, 0.25] rim [0.68, 0.447, 0.881, 0.313]
  - track 608 at frame 187: holes 0, rim-vs-core 0.27, rim-vs-outside 0.95, heterogeneity 0.17; core [0.948, 0.569, 1.0, 0.438] rim [0.697, 0.504, 0.962, 0.497]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 250 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.804, rim/outside 2.95 (aggregate of 250 individuals; 0/250 membrane-like individually; rim level 0.71)
  - radial adaptation a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.856, rim/outside 1.91 (aggregate of 250 individuals; 13/250 membrane-like individually; rim level 0.534)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 29.6 (aggregate of 250 individuals; 2/250 membrane-like individually; rim level 0.827)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.5, rim/outside 0.876 (aggregate of 250 individuals; 9/250 membrane-like individually; rim level 0.406)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #466 (t=459, R_eq 3.19): none; #206 (t=171, R_eq 4.65): none; #495 (t=483, R_eq 3.83): none; #608 (t=561, R_eq 3.61): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 250 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
