# Evidence pack: neural-field-dep-fork (seed 6)

- world: `../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1943-c19-review-comets-jitter/kd0.045 --seeds 6 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 44, mean 44.8, max 67; occupancy final 0.11
- tracks: 917; persistent (alive >= 50% of run): 0; longest 82 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [44, 44, 44], H1 [0, 0, 0]
- motion: 133 long-lived tracks moved >= 1 body length; max speed 0.602/time; max body lengths 32.5
- replication (lineage window K = 20 frames = time 100, default): splits 362, persistent splits 28 (0 more failed only because the siblings re-merged within K), max generation 4, merges 125, merge/split ratio 0.345, nucleations 10
- channel total drift (end/start - 1): [1.0, None, -0.4625, -0.1963]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 675 at frame 160: holes 0, rim-vs-core 0.30, rim-vs-outside 0.98, heterogeneity 0.16; core [0.91, 0.369, 1.0, 0.549] rim [0.785, 0.582, 0.969, 0.385]
  - track 709 at frame 166: holes 0, rim-vs-core 0.29, rim-vs-outside 0.89, heterogeneity 0.17; core [0.91, 0.55, 1.0, 0.375] rim [0.644, 0.506, 0.897, 0.389]
  - track 725 at frame 168: holes 0, rim-vs-core 0.24, rim-vs-outside 0.91, heterogeneity 0.16; core [0.833, 0.671, 0.999, 0.277] rim [0.745, 0.492, 0.947, 0.405]
  - track 856 at frame 185: holes 0, rim-vs-core 0.19, rim-vs-outside 0.93, heterogeneity 0.16; core [0.91, 0.518, 1.0, 0.437] rim [0.729, 0.495, 0.954, 0.451]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 264 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 3 (aggregate of 264 individuals; 0/264 membrane-like individually; rim level 0.71)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.896, rim/outside 1.94 (aggregate of 264 individuals; 10/264 membrane-like individually; rim level 0.545)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.85, rim/outside 32.5 (aggregate of 264 individuals; 0/264 membrane-like individually; rim level 0.824)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.45, rim/outside 0.897 (aggregate of 264 individuals; 10/264 membrane-like individually; rim level 0.402)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #675 (t=800, R_eq 3.48): none; #709 (t=830, R_eq 3.87): none; #725 (t=840, R_eq 3.74): none; #856 (t=925, R_eq 5.47): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 264 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
