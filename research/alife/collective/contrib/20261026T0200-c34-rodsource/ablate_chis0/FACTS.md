# Evidence pack: active-nematic-rodsource (seed 0)

- world: `../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5
- run: 121 frames x 100 steps x dt 0.05 = time 600; grid [128, 128]; wall 201s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0200-c34-rodsource/world.py --out collective/contrib/20261026T0200-c34-rodsource/ablate_chis0 --seeds 0 --frames 120 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8162, 0.6147], min area 6 px

## Measurements
- components: final 19, mean 14.1, max 20; occupancy final 0.05
- tracks: 43; persistent (alive >= 50% of run): 11; longest 90 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 19, 19], H1 [0, 0, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.0797/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 100, default): splits 16, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.125, nucleations 9
- channel total drift (end/start - 1): [-0.504, -0.5879, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 76: holes 0, rim-vs-core 0.38, rim-vs-outside 0.36, heterogeneity 0.13; core [0.945, 0.881, 0.896] rim [0.735, 0.584, 0.775]
  - track 13 at frame 76: holes 0, rim-vs-core 0.34, rim-vs-outside 0.38, heterogeneity 0.11; core [0.96, 0.873, 0.874] rim [0.774, 0.614, 0.762]
  - track 15 at frame 78: holes 0, rim-vs-core 0.36, rim-vs-outside 0.41, heterogeneity 0.12; core [0.971, 0.95, 0.861] rim [0.778, 0.674, 0.739]
  - track 23 at frame 87: holes 0, rim-vs-core 0.37, rim-vs-outside 0.43, heterogeneity 0.12; core [0.974, 0.969, 0.875] rim [0.765, 0.694, 0.741]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 94 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 4.99 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.774)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.763, rim/outside 8.29 (aggregate of 94 individuals; 2/94 membrane-like individually; rim level 0.642)
  - radial surfactant s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 2.26 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.815)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=380, R_eq 3.09): none; #13 (t=380, R_eq 2.65): none; #15 (t=390, R_eq 3.04): none; #23 (t=435, R_eq 3.24): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
