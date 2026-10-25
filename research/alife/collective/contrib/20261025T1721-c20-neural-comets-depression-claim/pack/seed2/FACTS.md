# Evidence pack: neural-field-dep (seed 2)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run /tmp/c20nfd/world.py --out /tmp/c20nfd/pack --seeds 0 1 2 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 30, mean 40.1, max 74; occupancy final 0.08
- tracks: 770; persistent (alive >= 50% of run): 2; longest 129 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 30], H1 [0, 0, 0]
- motion: 112 long-lived tracks moved >= 1 body length; max speed 0.575/time; max body lengths 58.0
- replication (lineage window K = 20 frames = time 100, default): splits 302, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 4, merges 86, merge/split ratio 0.285, nucleations 7
- channel total drift (end/start - 1): [-1.0, None, -0.6703, -0.1744]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 133 at frame 71: holes 0, rim-vs-core 0.29, rim-vs-outside 0.83, heterogeneity 0.17; core [0.91, 0.588, 1.0, 0.223] rim [0.667, 0.487, 0.881, 0.252]
  - track 172 at frame 64: holes 0, rim-vs-core 0.23, rim-vs-outside 0.90, heterogeneity 0.16; core [0.838, 0.679, 1.0, 0.132] rim [0.778, 0.508, 0.95, 0.271]
  - track 177 at frame 55: holes 0, rim-vs-core 0.26, rim-vs-outside 0.92, heterogeneity 0.16; core [0.945, 0.558, 1.0, 0.384] rim [0.689, 0.535, 0.939, 0.407]
  - track 615 at frame 153: holes 0, rim-vs-core 0.31, rim-vs-outside 0.85, heterogeneity 0.17; core [0.912, 0.489, 1.0, 0.239] rim [0.653, 0.385, 0.884, 0.318]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 221 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 2.96 (aggregate of 221 individuals; 0/221 membrane-like individually; rim level 0.702)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 1.93 (aggregate of 221 individuals; 5/221 membrane-like individually; rim level 0.539)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.845, rim/outside 25.8 (aggregate of 221 individuals; 3/221 membrane-like individually; rim level 0.808)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.49, rim/outside 0.898 (aggregate of 221 individuals; 3/221 membrane-like individually; rim level 0.424)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #133 (t=355, R_eq 3.04): none; #172 (t=320, R_eq 3.24): none; #177 (t=275, R_eq 3.39): none; #615 (t=765, R_eq 3.34): ['adaptation a']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 221 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
