# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 73s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/chi5mu10kd12 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5843], min area 6 px

## Measurements
- components: final 74, mean 36.9, max 74; occupancy final 0.36
- tracks: 401; persistent (alive >= 50% of run): 2; longest 105 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.47 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [74, 74, 74], H1 [0, 0, 0]
- motion: 33 long-lived tracks moved >= 1 body length; max speed 0.0341/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 1000, default): splits 147, persistent splits 61 (0 more failed only because the siblings re-merged within K), max generation 7, merges 41, merge/split ratio 0.279, nucleations 0
- channel total drift (end/start - 1): [-0.5431, -0.7227, 0.386, 0.2549]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 169 at frame 118: holes 0, rim-vs-core 0.56, rim-vs-outside 0.35, heterogeneity 0.14; core [0.13, 0.606, 0.658, 0.915] rim [0.254, 0.402, 0.451, 0.448]
  - track 257 at frame 151: holes 0, rim-vs-core 0.72, rim-vs-outside 0.55, heterogeneity 0.20; core [0.162, 0.812, 0.776, 0.871] rim [0.331, 0.314, 0.4, 0.549]
  - track 283 at frame 156: holes 0, rim-vs-core 0.60, rim-vs-outside 0.47, heterogeneity 0.16; core [0.149, 0.706, 0.755, 0.914] rim [0.274, 0.387, 0.453, 0.532]
  - track 352 at frame 171: holes 0, rim-vs-core 0.46, rim-vs-outside 0.69, heterogeneity 0.17; core [0.116, 0.767, 0.724, 0.883] rim [0.241, 0.448, 0.517, 0.651]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 252 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.33, rim/outside 0.902 (aggregate of 252 individuals; 0/252 membrane-like individually; rim level 0.414)
  - radial K catalyst: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 12 (aggregate of 252 individuals; 0/252 membrane-like individually; rim level 0.692)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 10.6 (aggregate of 252 individuals; 161/252 membrane-like individually; rim level 0.789)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 10 (aggregate of 252 individuals; 0/252 membrane-like individually; rim level 0.906)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #169 (t=5900, R_eq 5.97): none; #257 (t=7550, R_eq 4.95): ['L link']; #283 (t=7800, R_eq 5.11): none; #352 (t=8550, R_eq 4.92): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
