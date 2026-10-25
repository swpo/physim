# Evidence pack: neural-field-dep (seed 0)

- world: `../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 100 steps x dt 0.05 (--dt; world META dt 0.1) = time 1000; grid [128, 128]; wall 17s; status ok
- command: `python -m labkit.run /tmp/c20nfd/world.py --out /tmp/c20nfd/pack_dt2 --seeds 0 --spf 100 --dt 0.05 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 29, mean 39.8, max 69; occupancy final 0.09
- tracks: 821; persistent (alive >= 50% of run): 0; longest 86 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 29], H1 [0, 0, 0]
- motion: 115 long-lived tracks moved >= 1 body length; max speed 0.599/time; max body lengths 31.1
- replication (lineage window K = 20 frames = time 100, default): splits 325, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 6, merges 97, merge/split ratio 0.298, nucleations 7
- channel total drift (end/start - 1): [-1.0, None, -0.6226, -0.175]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 500 at frame 131: holes 0, rim-vs-core 0.25, rim-vs-outside 0.83, heterogeneity 0.17; core [0.936, 0.571, 1.0, 0.335] rim [0.708, 0.506, 0.925, 0.339]
  - track 511 at frame 136: holes 0, rim-vs-core 0.30, rim-vs-outside 0.83, heterogeneity 0.17; core [0.885, 0.52, 1.0, 0.233] rim [0.648, 0.434, 0.855, 0.313]
  - track 497 at frame 123: holes 0, rim-vs-core 0.29, rim-vs-outside 0.79, heterogeneity 0.16; core [0.855, 0.514, 1.0, 0.153] rim [0.641, 0.451, 0.847, 0.257]
  - track 732 at frame 183: holes 0, rim-vs-core 0.24, rim-vs-outside 0.90, heterogeneity 0.15; core [0.931, 0.574, 1.0, 0.33] rim [0.717, 0.522, 0.947, 0.393]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 222 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 2.94 (aggregate of 222 individuals; 0/222 membrane-like individually; rim level 0.705)
  - radial adaptation a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 2 (aggregate of 222 individuals; 5/222 membrane-like individually; rim level 0.549)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.831, rim/outside 26.3 (aggregate of 222 individuals; 1/222 membrane-like individually; rim level 0.805)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.47, rim/outside 0.874 (aggregate of 222 individuals; 7/222 membrane-like individually; rim level 0.42)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #500 (t=655, R_eq 2.99): ['synaptic resource r']; #511 (t=680, R_eq 3.29): none; #497 (t=615, R_eq 3.29): none; #732 (t=915, R_eq 3.09): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.05 only relabels time (world META dt 0.1): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 1 of 222 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
