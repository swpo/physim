# Evidence pack: ringswim-dl2 (seed 9)

- world: `../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 61 frames x 50 steps x dt 1.0 = time 3000; grid [256, 256]; wall 88s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27n/world.py --out collective/contrib/wip-c27n/pack_chi0 --seeds 9 --frames 60 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.4924], min area 6 px

## Measurements
- components: final 0, mean 10.3, max 119; occupancy final 0.00
- tracks: 217; persistent (alive >= 50% of run): 0; longest 20 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.52, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 1000, default): splits 39, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 7, merge/split ratio 0.179, nucleations 1
- channel total drift (end/start - 1): [-0.0, -1.0, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 10: holes 0, rim-vs-core 0.60, rim-vs-outside 0.49, heterogeneity 0.16; core [0.088, 0.69, 0.675, 0.866] rim [0.319, 0.278, 0.502, 0.541]
  - track 91 at frame 10: holes 0, rim-vs-core 0.75, rim-vs-outside 0.54, heterogeneity 0.21; core [0.163, 0.759, 0.806, 0.885] rim [0.396, 0.224, 0.464, 0.556]
  - track 27 at frame 9: holes 0, rim-vs-core 0.82, rim-vs-outside 0.54, heterogeneity 0.22; core [0.127, 0.808, 0.785, 0.836] rim [0.394, 0.202, 0.39, 0.545]
  - track 57 at frame 10: holes 0, rim-vs-core 0.63, rim-vs-outside 0.54, heterogeneity 0.18; core [0.082, 0.714, 0.669, 0.821] rim [0.337, 0.258, 0.459, 0.547]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 11 components >= 12 px at frames [10]):
  - radial S: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 46.3, rim/outside 0.766 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.57)
  - radial K catalyst: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 70.9 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.723)
  - radial L link: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 60.9 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.698)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.21, rim/outside 83.7 (aggregate of 11 individuals; 11/11 membrane-like individually; rim level 1)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #11 (t=500, R_eq 5.47): ['membrane (wall)']; #91 (t=500, R_eq 4.55): ['membrane (wall)']; #27 (t=450, R_eq 4.98): ['membrane (wall)']; #57 (t=500, R_eq 5.92): ['membrane (wall)']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
