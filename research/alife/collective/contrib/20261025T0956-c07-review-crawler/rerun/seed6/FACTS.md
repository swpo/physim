# Evidence pack: crawler-divide (seed 6)

- world: `../../../20261025T0828-c04-crawler-divide-claim/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 307s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0828-c04-crawler-divide-claim/world.py --out collective/contrib/_c07rev14/rerun/seed6 --seeds 6 --frames 240 --threshold 0.25 --no-movie`
- segmentation: matter > 0.34 of robust range [-0.0, 0.7347], min area 6 px

## Measurements
- components: final 13, mean 8.2, max 14; occupancy final 0.19
- tracks: 29; persistent (alive >= 50% of run): 7; longest 204 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.11 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 13], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 1.72/time; max body lengths 16.0
- replication (lineage window K = 20 frames = time 50, default): splits 13, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.077, nucleations 1
- channel total drift (end/start - 1): [2.6357, 0.9197, None, -0.5486]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 139: holes 0, rim-vs-core 0.32, rim-vs-outside 0.37, heterogeneity 0.12; core [0.749, 0.292, 0.515, 0.326] rim [0.525, 0.467, 0.361, 0.344]
  - track 8 at frame 139: holes 0, rim-vs-core 0.27, rim-vs-outside 0.37, heterogeneity 0.09; core [0.667, 0.161, 0.514, 0.297] rim [0.505, 0.327, 0.389, 0.319]
  - track 11 at frame 141: holes 0, rim-vs-core 0.36, rim-vs-outside 0.46, heterogeneity 0.15; core [0.811, 0.362, 0.617, 0.317] rim [0.558, 0.531, 0.422, 0.335]
  - track 21 at frame 212: holes 0, rim-vs-core 0.30, rim-vs-outside 0.27, heterogeneity 0.07; core [0.749, 0.194, 0.36, 0.037] rim [0.505, 0.311, 0.243, 0.058]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 56 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.827, rim/outside 15.4 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.682)
  - radial |P| (actin polarization): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.87, rim/outside 5.57 (aggregate of 56 individuals; 56/56 membrane-like individually; rim level 0.357)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.839, rim/outside 29.9 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.52)
  - radial n (nutrient): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.16, rim/outside 0.935 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.302)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #7 (t=347.5, R_eq 17.64): ['|P| (actin polarization)']; #8 (t=347.5, R_eq 18.34): ['|P| (actin polarization)']; #11 (t=352.5, R_eq 17.94): ['|P| (actin polarization)']; #21 (t=530, R_eq 16.74): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
