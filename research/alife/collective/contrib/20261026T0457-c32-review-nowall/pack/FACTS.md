# Evidence pack: phoretic-colloids (seed 2)

- world: `../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 76s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0457-c32-review-nowall/world.py --out collective/contrib/20261026T0457-c32-review-nowall/pack --seeds 2 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8051], min area 6 px

## Measurements
- components: final 12, mean 14.6, max 26; occupancy final 0.05
- tracks: 353; persistent (alive >= 50% of run): 0; longest 339 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 12, 10], H1 [0, 0, 0]
- motion: 65 long-lived tracks moved >= 1 body length; max speed 0.54/time; max body lengths 6.7
- replication (lineage window K = 20 frames = time 10, default): splits 34, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 4, merges 45, merge/split ratio 1.32, nucleations 240
- channel total drift (end/start - 1): [0.5886, -0.205, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 225 at frame 518: holes 0, rim-vs-core 0.31, rim-vs-outside 0.32, heterogeneity 0.17; core [0.876, 0.198, 0.674] rim [0.616, 0.087, 0.544]
  - track 46 at frame 249: holes 0, rim-vs-core 0.21, rim-vs-outside 0.29, heterogeneity 0.05; core [0.841, 0.0, 0.426] rim [0.635, 0.0, 0.374]
  - track 117 at frame 343: holes 0, rim-vs-core 0.19, rim-vs-outside 0.24, heterogeneity 0.10; core [0.767, 0.142, 0.381] rim [0.586, 0.117, 0.34]
  - track 339 at frame 766: holes 0, rim-vs-core 0.20, rim-vs-outside 0.22, heterogeneity 0.11; core [0.776, 0.137, 0.465] rim [0.587, 0.108, 0.421]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.856, rim/outside 14.5 (aggregate of 77 individuals; 2/77 membrane-like individually; rim level 0.689)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 10.8 (aggregate of 77 individuals; 33/77 membrane-like individually; rim level 0.267)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.833, rim/outside 2.24 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.573)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #225 (t=259, R_eq 4.37): ['B density']; #46 (t=124.5, R_eq 2.88): none; #117 (t=171.5, R_eq 2.52): ['B density']; #339 (t=383, R_eq 2.82): ['B density']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
