# Evidence pack: neural-field-dep (seed 11)

- world: `../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run scratch/c14/rev_nc/world.py --out scratch/c14/rev_nc/pack_kd0 --seeds 11 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 10, mean 17.8, max 72; occupancy final 0.31
- tracks: 1223; persistent (alive >= 50% of run): 0; longest 41 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.585/time; max body lengths 12.3
- replication (lineage window K = 20 frames = time 100, default): splits 424, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 352, merge/split ratio 0.83, nucleations 3
- channel total drift (end/start - 1): [-1.0, None, 0.3749, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 251 at frame 34: holes 0, rim-vs-core 0.26, rim-vs-outside 0.92, heterogeneity 0.12; core [0.906, 0.545, 1.0, 0.0] rim [0.667, 0.479, 0.933, 0.0]
  - track 67 at frame 18: holes 0, rim-vs-core 0.24, rim-vs-outside 0.93, heterogeneity 0.12; core [0.918, 0.549, 1.0, 0.0] rim [0.694, 0.502, 0.945, 0.0]
  - track 204 at frame 27: holes 0, rim-vs-core 0.18, rim-vs-outside 1.04, heterogeneity 0.11; core [0.967, 0.521, 1.0, 0.0] rim [0.792, 0.495, 0.979, 0.0]
  - track 247 at frame 27: holes 0, rim-vs-core 0.19, rim-vs-outside 1.04, heterogeneity 0.12; core [0.966, 0.514, 1.0, 0.0] rim [0.779, 0.494, 0.964, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.9, rim/outside 1.55 (aggregate of 78 individuals; 5/78 membrane-like individually; rim level 0.526)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 1.2 (aggregate of 78 individuals; 2/78 membrane-like individually; rim level 0.465)
  - radial firing f(u): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 2.26 (aggregate of 78 individuals; 13/78 membrane-like individually; rim level 0.516)
  - radial synaptic resource r: flat profile (no radial structure; level 0; aggregate of 78 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #251 (t=170, R_eq 4.55): none; #67 (t=90, R_eq 5.26): none; #204 (t=135, R_eq 6.53): none; #247 (t=135, R_eq 9.18, ring): ['activity u', 'firing f(u)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 35 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
