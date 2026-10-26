# Evidence pack: ringswim-dl2 (seed 2)

- world: `../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 311s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0434-c29-kernel-ring-seed2/world.py --out collective/contrib/20261026T0434-c29-kernel-ring-seed2/pack --seeds 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5887], min area 6 px

## Measurements
- components: final 295, mean 198.2, max 295; occupancy final 0.38
- tracks: 1354; persistent (alive >= 50% of run): 118; longest 158 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.55 (1 = constant size)
- enclosures: components with a hole mean 0.33, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [295, 295, 295], H1 [0, 0, 0]
- motion: 112 long-lived tracks moved >= 1 body length; max speed 0.0361/time; max body lengths 3.8
- replication (lineage window K = 20 frames = time 1000, default): splits 545, persistent splits 228 (1 more failed only because the siblings re-merged within K), max generation 6, merges 105, merge/split ratio 0.193, nucleations 6
- channel total drift (end/start - 1): [-0.5581, -0.7067, 0.4258, 0.4768]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 595 at frame 123: holes 0, rim-vs-core 0.77, rim-vs-outside 0.52, heterogeneity 0.20; core [0.212, 0.826, 0.853, 0.892] rim [0.355, 0.317, 0.424, 0.536]
  - track 610 at frame 123: holes 0, rim-vs-core 0.58, rim-vs-outside 0.58, heterogeneity 0.16; core [0.131, 0.762, 0.744, 0.907] rim [0.259, 0.395, 0.449, 0.588]
  - track 635 at frame 124: holes 0, rim-vs-core 0.64, rim-vs-outside 0.49, heterogeneity 0.17; core [0.128, 0.72, 0.711, 0.893] rim [0.262, 0.348, 0.395, 0.496]
  - track 1235 at frame 158: holes 0, rim-vs-core 0.57, rim-vs-outside 0.55, heterogeneity 0.16; core [0.109, 0.729, 0.682, 0.888] rim [0.253, 0.378, 0.418, 0.553]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1308 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 6.39, rim/outside 0.942 (aggregate of 1308 individuals; 0/1308 membrane-like individually; rim level 0.393)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 9.55 (aggregate of 1308 individuals; 2/1308 membrane-like individually; rim level 0.706)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.58, rim/outside 8.86 (aggregate of 1308 individuals; 943/1308 membrane-like individually; rim level 0.795)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 7.62 (aggregate of 1308 individuals; 4/1308 membrane-like individually; rim level 0.919)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #595 (t=6150, R_eq 4.26): none; #610 (t=6150, R_eq 5.23): none; #635 (t=6200, R_eq 5.23): ['L link']; #1235 (t=7900, R_eq 5.59): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
