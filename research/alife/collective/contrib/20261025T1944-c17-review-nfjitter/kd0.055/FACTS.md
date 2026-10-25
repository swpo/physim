# Evidence pack: neural-field-dep (seed 7)

- world: `../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 30 steps x dt 0.1 = time 600; grid [128, 128]; wall 3s; status ok
- command: `python -m labkit.run world.py --out kd0.055 --seeds 7 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 35, mean 41.5, max 69; occupancy final 0.09
- tracks: 574; persistent (alive >= 50% of run): 3; longest 138 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.77 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 36, 36], H1 [0, 0, 0]
- motion: 143 long-lived tracks moved >= 1 body length; max speed 0.597/time; max body lengths 29.2
- replication (lineage window K = 20 frames = time 60, default): splits 218, persistent splits 37 (0 more failed only because the siblings re-merged within K), max generation 4, merges 81, merge/split ratio 0.372, nucleations 7
- channel total drift (end/start - 1): [1.0, None, -0.5599, -0.1877]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 298 at frame 106: holes 0, rim-vs-core 0.21, rim-vs-outside 0.86, heterogeneity 0.16; core [0.894, 0.467, 1.0, 0.382] rim [0.694, 0.457, 0.93, 0.397]
  - track 386 at frame 141: holes 0, rim-vs-core 0.28, rim-vs-outside 0.85, heterogeneity 0.16; core [0.913, 0.641, 1.0, 0.234] rim [0.692, 0.524, 0.922, 0.324]
  - track 316 at frame 106: holes 0, rim-vs-core 0.29, rim-vs-outside 0.83, heterogeneity 0.15; core [0.858, 0.54, 1.0, 0.238] rim [0.638, 0.45, 0.866, 0.318]
  - track 516 at frame 176: holes 0, rim-vs-core 0.24, rim-vs-outside 0.81, heterogeneity 0.14; core [0.855, 0.583, 1.0, 0.244] rim [0.67, 0.484, 0.92, 0.329]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 226 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 3.04 (aggregate of 226 individuals; 0/226 membrane-like individually; rim level 0.716)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 1.97 (aggregate of 226 individuals; 10/226 membrane-like individually; rim level 0.546)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.869, rim/outside 34.6 (aggregate of 226 individuals; 0/226 membrane-like individually; rim level 0.843)
  - radial synaptic resource r: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.855 (aggregate of 226 individuals; 7/226 membrane-like individually; rim level 0.416)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #298 (t=318, R_eq 4.37): none; #386 (t=423, R_eq 2.71): none; #316 (t=318, R_eq 2.65): none; #516 (t=528, R_eq 2.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 226 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
