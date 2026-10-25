# Evidence pack: neural-field-dep-fork (seed 4)

- world: `../../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1815-c19-review-neural-comets/fed/seed4 --seeds 4 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 38, mean 40.3, max 73; occupancy final 0.09
- tracks: 862; persistent (alive >= 50% of run): 0; longest 62 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 38, 38], H1 [0, 0, 0]
- motion: 109 long-lived tracks moved >= 1 body length; max speed 0.591/time; max body lengths 26.2
- replication (lineage window K = 20 frames = time 100, default): splits 350, persistent splits 28 (0 more failed only because the siblings re-merged within K), max generation 4, merges 86, merge/split ratio 0.246, nucleations 9
- channel total drift (end/start - 1): [-1.0, None, -0.6096, -0.1825]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 441 at frame 94: holes 0, rim-vs-core 0.23, rim-vs-outside 0.89, heterogeneity 0.16; core [0.921, 0.52, 1.0, 0.428] rim [0.705, 0.49, 0.94, 0.453]
  - track 373 at frame 76: holes 0, rim-vs-core 0.23, rim-vs-outside 0.86, heterogeneity 0.16; core [0.895, 0.593, 1.0, 0.286] rim [0.71, 0.526, 0.92, 0.366]
  - track 561 at frame 136: holes 0, rim-vs-core 0.30, rim-vs-outside 0.91, heterogeneity 0.18; core [0.927, 0.59, 1.0, 0.488] rim [0.659, 0.501, 0.902, 0.535]
  - track 683 at frame 173: holes 0, rim-vs-core 0.14, rim-vs-outside 0.85, heterogeneity 0.16; core [0.86, 0.578, 1.0, 0.258] rim [0.759, 0.583, 0.933, 0.194]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 216 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 2.95 (aggregate of 216 individuals; 1/216 membrane-like individually; rim level 0.702)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 1.98 (aggregate of 216 individuals; 4/216 membrane-like individually; rim level 0.55)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 26.1 (aggregate of 216 individuals; 3/216 membrane-like individually; rim level 0.801)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 0.855 (aggregate of 216 individuals; 9/216 membrane-like individually; rim level 0.419)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #441 (t=470, R_eq 4.3): none; #373 (t=380, R_eq 3.48): none; #561 (t=680, R_eq 3.19): none; #683 (t=865, R_eq 2.99): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 216 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
