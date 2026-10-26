# Evidence pack: active-nematic-rodsource (seed 4)

- world: `../../../20261026T0300-c34-swimdivide/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 405s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0300-c34-swimdivide/world.py --out collective/contrib/20261026T0331-c30-review-swimdivide/rerun_zeta1 --seeds 3 4 --frames 200 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8081, 0.5816], min area 6 px

## Measurements
- components: final 29, mean 23.1, max 32; occupancy final 0.05
- tracks: 124; persistent (alive >= 50% of run): 10; longest 153 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 29], H1 [0, 0, 0]
- motion: 55 long-lived tracks moved >= 1 body length; max speed 0.107/time; max body lengths 5.7
- replication (lineage window K = 20 frames = time 100, default): splits 48, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 4, merges 16, merge/split ratio 0.333, nucleations 12
- channel total drift (end/start - 1): [-0.5085, -0.5476, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 103: holes 0, rim-vs-core 0.40, rim-vs-outside 0.29, heterogeneity 0.13; core [0.94, 0.594, 0.432] rim [0.751, 0.409, 0.728]
  - track 18 at frame 99: holes 0, rim-vs-core 0.44, rim-vs-outside 0.38, heterogeneity 0.14; core [0.976, 0.909, 0.31] rim [0.808, 0.651, 0.621]
  - track 20 at frame 97: holes 0, rim-vs-core 0.52, rim-vs-outside 0.35, heterogeneity 0.17; core [0.945, 0.887, 0.405] rim [0.734, 0.583, 0.768]
  - track 75 at frame 171: holes 0, rim-vs-core 0.44, rim-vs-outside 0.34, heterogeneity 0.16; core [0.958, 0.789, 0.375] rim [0.778, 0.545, 0.695]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 153 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.831, rim/outside 4.55 (aggregate of 153 individuals; 0/153 membrane-like individually; rim level 0.8)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.765, rim/outside 7.83 (aggregate of 153 individuals; 0/153 membrane-like individually; rim level 0.674)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.81, rim/outside 2.83 (aggregate of 153 individuals; 129/153 membrane-like individually; rim level 0.629)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #21 (t=515, R_eq 2.46): ['surfactant s']; #18 (t=495, R_eq 2.65): ['surfactant s']; #20 (t=485, R_eq 2.88): ['surfactant s']; #75 (t=855, R_eq 2.65): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
