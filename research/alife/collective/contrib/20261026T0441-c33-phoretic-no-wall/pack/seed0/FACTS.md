# Evidence pack: phoretic-colloids (seed 0)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 115s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33-nuc/world.py --out collective/contrib/wip-c33-nuc/pack --seeds 0 1 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7379], min area 6 px

## Measurements
- components: final 15, mean 14.7, max 25; occupancy final 0.05
- tracks: 312; persistent (alive >= 50% of run): 1; longest 567 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 15, 12], H1 [0, 0, 0]
- motion: 65 long-lived tracks moved >= 1 body length; max speed 0.643/time; max body lengths 9.5
- replication (lineage window K = 20 frames = time 10, default): splits 27, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 6, merges 45, merge/split ratio 1.67, nucleations 213
- channel total drift (end/start - 1): [0.58, -0.375, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 114 at frame 477: holes 0, rim-vs-core 0.24, rim-vs-outside 0.26, heterogeneity 0.16; core [0.782, 0.191, 0.386] rim [0.55, 0.254, 0.345]
  - track 165 at frame 511: holes 0, rim-vs-core 0.24, rim-vs-outside 0.31, heterogeneity 0.06; core [0.924, 0.0, 0.503] rim [0.691, 0.0, 0.432]
  - track 160 at frame 464: holes 0, rim-vs-core 0.39, rim-vs-outside 0.33, heterogeneity 0.19; core [0.921, 0.206, 0.849] rim [0.579, 0.208, 0.655]
  - track 302 at frame 793: holes 0, rim-vs-core 0.33, rim-vs-outside 0.25, heterogeneity 0.26; core [0.768, 0.306, 0.795] rim [0.481, 0.25, 0.635]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 16.1 (aggregate of 79 individuals; 3/79 membrane-like individually; rim level 0.706)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.649, rim/outside 8.52 (aggregate of 79 individuals; 25/79 membrane-like individually; rim level 0.204)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 2.28 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.568)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #114 (t=238.5, R_eq 2.52): ['B density']; #165 (t=255.5, R_eq 3.19): none; #160 (t=232, R_eq 5.05): ['B density']; #302 (t=396.5, R_eq 5.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
