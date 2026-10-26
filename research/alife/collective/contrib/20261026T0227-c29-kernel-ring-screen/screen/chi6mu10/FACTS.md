# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 77s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/chi6mu10 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5856], min area 6 px

## Measurements
- components: final 76, mean 55.5, max 76; occupancy final 0.38
- tracks: 303; persistent (alive >= 50% of run): 58; longest 171 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.04 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [76, 76, 76], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.0209/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 1000, default): splits 120, persistent splits 60 (0 more failed only because the siblings re-merged within K), max generation 4, merges 21, merge/split ratio 0.175, nucleations 0
- channel total drift (end/start - 1): [-0.5679, -0.6982, 0.4383, 0.3368]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 123 at frame 116: holes 0, rim-vs-core 0.59, rim-vs-outside 0.55, heterogeneity 0.16; core [0.121, 0.755, 0.697, 0.889] rim [0.26, 0.386, 0.401, 0.569]
  - track 173 at frame 124: holes 0, rim-vs-core 0.39, rim-vs-outside 0.77, heterogeneity 0.17; core [0.134, 0.735, 0.709, 0.895] rim [0.204, 0.524, 0.493, 0.664]
  - track 177 at frame 124: holes 0, rim-vs-core 0.70, rim-vs-outside 0.53, heterogeneity 0.18; core [0.141, 0.76, 0.741, 0.912] rim [0.264, 0.347, 0.36, 0.521]
  - track 253 at frame 139: holes 0, rim-vs-core 0.58, rim-vs-outside 0.58, heterogeneity 0.17; core [0.125, 0.775, 0.724, 0.893] rim [0.253, 0.399, 0.42, 0.59]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 371 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 5.65, rim/outside 0.959 (aggregate of 371 individuals; 0/371 membrane-like individually; rim level 0.38)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 9.73 (aggregate of 371 individuals; 0/371 membrane-like individually; rim level 0.722)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.7, rim/outside 9.47 (aggregate of 371 individuals; 296/371 membrane-like individually; rim level 0.822)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 7.34 (aggregate of 371 individuals; 1/371 membrane-like individually; rim level 0.929)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #123 (t=5800, R_eq 5.41): ['L link']; #173 (t=6200, R_eq 5.41): ['L link']; #177 (t=6200, R_eq 5.7): none; #253 (t=6950, R_eq 5.08): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
