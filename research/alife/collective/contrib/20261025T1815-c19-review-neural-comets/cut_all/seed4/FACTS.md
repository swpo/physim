# Evidence pack: neural-field-dep-fork (seed 4)

- world: `../../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 6s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1815-c19-review-neural-comets/cut_all/seed4 --seeds 4 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 24.0, max 73; occupancy final 0.00
- tracks: 562; persistent (alive >= 50% of run): 0; longest 58 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [51, 28, 5], H1 [48, 6, 0]
- motion: 57 long-lived tracks moved >= 1 body length; max speed 0.593/time; max body lengths 25.4
- replication (lineage window K = 20 frames = time 100, default): splits 219, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 49, merge/split ratio 0.224, nucleations 9
- channel total drift (end/start - 1): [-1.0, None, -0.9986, -0.3538]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 373 at frame 76: holes 0, rim-vs-core 0.23, rim-vs-outside 0.86, heterogeneity 0.16; core [0.916, 0.6, 1.0, 0.445] rim [0.722, 0.528, 0.92, 0.507]
  - track 450 at frame 92: holes 0, rim-vs-core 0.24, rim-vs-outside 0.85, heterogeneity 0.13; core [0.931, 0.623, 1.0, 0.363] rim [0.722, 0.502, 0.972, 0.396]
  - track 376 at frame 72: holes 0, rim-vs-core 0.29, rim-vs-outside 0.78, heterogeneity 0.17; core [0.928, 0.512, 1.0, 0.468] rim [0.674, 0.457, 0.867, 0.485]
  - track 528 at frame 108: holes 0, rim-vs-core 0.18, rim-vs-outside 0.84, heterogeneity 0.11; core [0.852, 0.468, 1.0, 0.227] rim [0.678, 0.463, 0.956, 0.226]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 115 components >= 12 px at frames [34, 67, 101]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 3.29 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.733)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.852, rim/outside 2.03 (aggregate of 115 individuals; 2/115 membrane-like individually; rim level 0.553)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.881, rim/outside 31.4 (aggregate of 115 individuals; 1/115 membrane-like individually; rim level 0.835)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.25, rim/outside 0.924 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.541)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #373 (t=380, R_eq 3.48): none; #450 (t=460, R_eq 2.65): none; #376 (t=360, R_eq 3.66): none; #528 (t=540, R_eq 2.33): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 115 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
