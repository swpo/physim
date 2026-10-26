# Evidence pack: ringswim-dl2 (seed 3)

- world: `../../code/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 278s; status ok
- command: `python -m labkit.run /tmp/claude-0/c28sd/code/world.py --out /tmp/claude-0/c28sd/kpack --seeds 3 4 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.562], min area 6 px

## Measurements
- components: final 70, mean 71.2, max 118; occupancy final 0.16
- tracks: 1045; persistent (alive >= 50% of run): 1; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.12 (1 = constant size)
- enclosures: components with a hole mean 0.26, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [78, 70, 69], H1 [51, 5, 0]
- motion: 181 long-lived tracks moved >= 1 body length; max speed 0.0307/time; max body lengths 4.2
- replication (lineage window K = 20 frames = time 1000, default): splits 455, persistent splits 119 (0 more failed only because the siblings re-merged within K), max generation 7, merges 9, merge/split ratio 0.02, nucleations 0
- channel total drift (end/start - 1): [-0.2685, -0.8675, -0.2909, -0.486]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 228 at frame 79: holes 0, rim-vs-core 0.66, rim-vs-outside 0.55, heterogeneity 0.20; core [0.178, 0.787, 0.799, 0.831] rim [0.399, 0.321, 0.53, 0.517]
  - track 653 at frame 150: holes 0, rim-vs-core 0.30, rim-vs-outside 0.91, heterogeneity 0.16; core [0.067, 0.72, 0.614, 0.846] rim [0.265, 0.542, 0.671, 0.722]
  - track 641 at frame 145: holes 0, rim-vs-core 0.62, rim-vs-outside 0.45, heterogeneity 0.19; core [0.176, 0.755, 0.782, 0.855] rim [0.346, 0.35, 0.549, 0.478]
  - track 897 at frame 183: holes 0, rim-vs-core 0.36, rim-vs-outside 0.92, heterogeneity 0.16; core [0.073, 0.772, 0.658, 0.799] rim [0.261, 0.477, 0.642, 0.706]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 423 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 9.12, rim/outside 0.827 (aggregate of 423 individuals; 0/423 membrane-like individually; rim level 0.551)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.936, rim/outside 12.7 (aggregate of 423 individuals; 6/423 membrane-like individually; rim level 0.71)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 8.9 (aggregate of 423 individuals; 189/423 membrane-like individually; rim level 0.776)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 13.2 (aggregate of 423 individuals; 164/423 membrane-like individually; rim level 0.847)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #228 (t=3950, R_eq 5.84): ['L link', 'membrane (wall)']; #653 (t=7500, R_eq 7.82): none; #641 (t=7250, R_eq 5.97): none; #897 (t=9150, R_eq 6.46): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 423 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
