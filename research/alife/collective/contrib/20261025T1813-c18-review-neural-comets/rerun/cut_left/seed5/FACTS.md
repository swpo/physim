# Evidence pack: neural-field-dep-fork (seed 5)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev5/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev5/cut_left --seeds 5 6 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 10, mean 28.6, max 70; occupancy final 0.05
- tracks: 599; persistent (alive >= 50% of run): 0; longest 91 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 78 long-lived tracks moved >= 1 body length; max speed 0.591/time; max body lengths 32.5
- replication (lineage window K = 20 frames = time 100, default): splits 242, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 3, merges 60, merge/split ratio 0.248, nucleations 5
- channel total drift (end/start - 1): [-1.0, None, -0.796, -0.2588]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 554 at frame 156: holes 0, rim-vs-core 0.28, rim-vs-outside 0.89, heterogeneity 0.19; core [0.954, 0.598, 1.0, 0.541] rim [0.709, 0.478, 0.936, 0.521]
  - track 568 at frame 160: holes 0, rim-vs-core 0.32, rim-vs-outside 0.83, heterogeneity 0.17; core [0.921, 0.638, 1.0, 0.451] rim [0.661, 0.531, 0.862, 0.485]
  - track 573 at frame 160: holes 0, rim-vs-core 0.18, rim-vs-outside 1.02, heterogeneity 0.14; core [0.95, 0.494, 1.0, 0.516] rim [0.776, 0.453, 0.959, 0.503]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 144 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.782, rim/outside 2.86 (aggregate of 144 individuals; 0/144 membrane-like individually; rim level 0.688)
  - radial adaptation a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 2.02 (aggregate of 144 individuals; 4/144 membrane-like individually; rim level 0.565)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 24.3 (aggregate of 144 individuals; 1/144 membrane-like individually; rim level 0.778)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.25, rim/outside 0.929 (aggregate of 144 individuals; 1/144 membrane-like individually; rim level 0.546)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #554 (t=780, R_eq 3.19): ['synaptic resource r']; #568 (t=800, R_eq 3.48): none; #573 (t=800, R_eq 8.23): none; #594 (t=875, R_eq 7.23): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 144 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
