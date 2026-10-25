# Evidence pack: neural-field-dep-fork (seed 5)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 4s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev5/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev5/fed --seeds 5 6 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 37, mean 38.0, max 70; occupancy final 0.09
- tracks: 818; persistent (alive >= 50% of run): 0; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 38, 38], H1 [0, 0, 0]
- motion: 106 long-lived tracks moved >= 1 body length; max speed 0.582/time; max body lengths 27.4
- replication (lineage window K = 20 frames = time 100, default): splits 338, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 87, merge/split ratio 0.257, nucleations 6
- channel total drift (end/start - 1): [-1.0, None, -0.6023, -0.1786]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 596 at frame 160: holes 0, rim-vs-core 0.19, rim-vs-outside 0.85, heterogeneity 0.14; core [0.848, 0.558, 1.0, 0.144] rim [0.682, 0.515, 0.93, 0.193]
  - track 568 at frame 146: holes 0, rim-vs-core 0.29, rim-vs-outside 0.91, heterogeneity 0.18; core [0.933, 0.572, 1.0, 0.422] rim [0.677, 0.494, 0.902, 0.485]
  - track 193 at frame 39: holes 0, rim-vs-core 0.31, rim-vs-outside 0.84, heterogeneity 0.18; core [0.887, 0.599, 1.0, 0.298] rim [0.655, 0.47, 0.873, 0.382]
  - track 572 at frame 134: holes 0, rim-vs-core 0.27, rim-vs-outside 0.86, heterogeneity 0.17; core [0.92, 0.455, 1.0, 0.246] rim [0.682, 0.405, 0.928, 0.343]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 213 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 2.9 (aggregate of 213 individuals; 0/213 membrane-like individually; rim level 0.701)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 2 (aggregate of 213 individuals; 5/213 membrane-like individually; rim level 0.562)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 26.5 (aggregate of 213 individuals; 2/213 membrane-like individually; rim level 0.807)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.53, rim/outside 0.881 (aggregate of 213 individuals; 10/213 membrane-like individually; rim level 0.435)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #596 (t=800, R_eq 3.24): none; #568 (t=730, R_eq 3.61): none; #193 (t=195, R_eq 3.19): none; #572 (t=670, R_eq 3.39): ['synaptic resource r']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 213 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
