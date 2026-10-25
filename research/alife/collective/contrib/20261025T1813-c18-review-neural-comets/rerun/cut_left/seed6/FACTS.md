# Evidence pack: neural-field-dep-fork (seed 6)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev5/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev5/cut_left --seeds 5 6 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 9, mean 28.6, max 64; occupancy final 0.03
- tracks: 668; persistent (alive >= 50% of run): 0; longest 61 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 84 long-lived tracks moved >= 1 body length; max speed 0.587/time; max body lengths 19.9
- replication (lineage window K = 20 frames = time 100, default): splits 259, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 75, merge/split ratio 0.29, nucleations 11
- channel total drift (end/start - 1): [1.0, None, -0.8718, -0.2518]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 129 at frame 37: holes 0, rim-vs-core 0.26, rim-vs-outside 0.92, heterogeneity 0.16; core [0.938, 0.491, 1.0, 0.507] rim [0.693, 0.459, 0.918, 0.533]
  - track 203 at frame 42: holes 0, rim-vs-core 0.21, rim-vs-outside 0.89, heterogeneity 0.15; core [0.863, 0.466, 1.0, 0.467] rim [0.683, 0.462, 0.9, 0.498]
  - track 184 at frame 37: holes 0, rim-vs-core 0.30, rim-vs-outside 0.81, heterogeneity 0.17; core [0.943, 0.552, 1.0, 0.494] rim [0.693, 0.463, 0.873, 0.537]
  - track 602 at frame 166: holes 0, rim-vs-core 0.25, rim-vs-outside 0.81, heterogeneity 0.14; core [0.929, 0.654, 1.0, 0.472] rim [0.72, 0.553, 0.95, 0.534]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 140 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 2.92 (aggregate of 140 individuals; 0/140 membrane-like individually; rim level 0.698)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.898, rim/outside 2.07 (aggregate of 140 individuals; 4/140 membrane-like individually; rim level 0.574)
  - radial firing f(u): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 22.5 (aggregate of 140 individuals; 1/140 membrane-like individually; rim level 0.782)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.22, rim/outside 0.92 (aggregate of 140 individuals; 0/140 membrane-like individually; rim level 0.55)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #129 (t=185, R_eq 3.74): ['adaptation a']; #203 (t=210, R_eq 4.69): none; #184 (t=185, R_eq 3.48): none; #602 (t=830, R_eq 3.04): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 140 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
