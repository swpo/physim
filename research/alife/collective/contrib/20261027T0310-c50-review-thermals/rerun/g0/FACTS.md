# Evidence pack: reacting-thermals (seed 11)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 54s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out /tmp/claude-0/th/g0 --seeds 11 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7598], min area 6 px

## Measurements
- components: final 18, mean 10.1, max 39; occupancy final 0.02
- tracks: 124; persistent (alive >= 50% of run): 5; longest 554 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 17], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.0386/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 20, default): splits 38, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 6, merge/split ratio 0.158, nucleations 9
- channel total drift (end/start - 1): [-0.9285, -0.17, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 99 at frame 328: holes 0, rim-vs-core 0.18, rim-vs-outside 0.63, heterogeneity 0.06; core [0.968, 0.055, 0.0, 1.0] rim [0.81, 0.114, 0.0, 0.929]
  - track 101 at frame 328: holes 0, rim-vs-core 0.14, rim-vs-outside 0.54, heterogeneity 0.05; core [0.924, 0.037, 0.0, 0.94] rim [0.805, 0.106, 0.0, 0.918]
  - track 90 at frame 242: holes 0, rim-vs-core 0.21, rim-vs-outside 0.61, heterogeneity 0.05; core [0.947, 0.054, 0.0, 0.985] rim [0.772, 0.123, 0.0, 0.898]
  - track 112 at frame 545: holes 0, rim-vs-core 0.26, rim-vs-outside 0.66, heterogeneity 0.07; core [0.983, 0.059, 0.0, 0.999] rim [0.768, 0.133, 0.0, 0.884]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 18.8 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.853)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.71, rim/outside 0.623 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.24)
  - radial vorticity: flat profile (no radial structure; level 0; aggregate of 62 individuals)
  - radial burn r: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 59 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.922)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #99 (t=328, R_eq 2.33): none; #101 (t=328, R_eq 2.52): none; #90 (t=242, R_eq 2.52): none; #112 (t=545, R_eq 2.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
