# Evidence pack: phoretic-colloids (seed 2)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 73s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0422-c32-review-phor-divide/world.py --out collective/contrib/20261026T0422-c32-review-phor-divide/tpack --seeds 2 3 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.697], min area 6 px

## Measurements
- components: final 16, mean 16.6, max 26; occupancy final 0.05
- tracks: 325; persistent (alive >= 50% of run): 3; longest 466 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 18, 11], H1 [0, 0, 0]
- motion: 58 long-lived tracks moved >= 1 body length; max speed 0.403/time; max body lengths 9.3
- replication (lineage window K = 20 frames = time 10, default): splits 17, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 3, merges 33, merge/split ratio 1.94, nucleations 259
- channel total drift (end/start - 1): [0.5257, 0.135, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 184 at frame 571: holes 0, rim-vs-core 0.23, rim-vs-outside 0.28, heterogeneity 0.05; core [0.885, 0.0, 0.37] rim [0.656, 0.0, 0.33]
  - track 206 at frame 592: holes 0, rim-vs-core 0.19, rim-vs-outside 0.31, heterogeneity 0.05; core [0.862, 0.0, 0.456] rim [0.687, 0.0, 0.39]
  - track 208 at frame 592: holes 0, rim-vs-core 0.29, rim-vs-outside 0.27, heterogeneity 0.16; core [0.838, 0.104, 0.503] rim [0.572, 0.171, 0.424]
  - track 277 at frame 746: holes 0, rim-vs-core 0.24, rim-vs-outside 0.25, heterogeneity 0.19; core [0.759, 0.269, 0.441] rim [0.536, 0.339, 0.385]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 90 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.829, rim/outside 14.2 (aggregate of 90 individuals; 1/90 membrane-like individually; rim level 0.675)
  - radial B density: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.962, rim/outside 9.84 (aggregate of 90 individuals; 36/90 membrane-like individually; rim level 0.307)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.831, rim/outside 2.5 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.55)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #184 (t=285.5, R_eq 2.26): none; #206 (t=296, R_eq 2.82): none; #208 (t=296, R_eq 3.29): ['B density']; #277 (t=373, R_eq 2.65): ['B density']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
