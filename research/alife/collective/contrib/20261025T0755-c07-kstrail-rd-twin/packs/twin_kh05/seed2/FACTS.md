# Evidence pack: rdtrail (seed 2)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/_c07wip/world.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 25s; status ok
- command: `python -m labkit.run collective/contrib/_c07wip/world.py --out /tmp/claude-0/c07/pk_matched --seeds 0 1 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9933], min area 6 px

## Measurements
- components: final 21, mean 11.2, max 21; occupancy final 0.29
- tracks: 57; persistent (alive >= 50% of run): 3; longest 113 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.41 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 21, 21], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 60, default): splits 24, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 4, merges 3, merge/split ratio 0.125, nucleations 0
- channel total drift (end/start - 1): [6.916, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 145: holes 0, rim-vs-core 0.51, rim-vs-outside 0.43, heterogeneity 0.17; core [0.879, 0.649, 0.788] rim [0.536, 0.446, 0.466]
  - track 27 at frame 150: holes 0, rim-vs-core 0.59, rim-vs-outside 0.45, heterogeneity 0.19; core [0.906, 0.749, 0.836] rim [0.538, 0.499, 0.448]
  - track 29 at frame 150: holes 0, rim-vs-core 0.53, rim-vs-outside 0.46, heterogeneity 0.18; core [0.887, 0.695, 0.833] rim [0.539, 0.494, 0.494]
  - track 43 at frame 176: holes 0, rim-vs-core 0.25, rim-vs-outside 0.56, heterogeneity 0.16; core [0.814, 0.627, 0.809] rim [0.632, 0.546, 0.652]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 9.22 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.697)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 3.22 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.572)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.758, rim/outside 6.2 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.674)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #24 (t=435, R_eq 14.42): none; #27 (t=450, R_eq 16.68): none; #29 (t=450, R_eq 14.92): none; #43 (t=528, R_eq 12.64): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
