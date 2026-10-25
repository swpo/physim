# Evidence pack: crawler-divide (seed 5)

- world: `../../../20261025T0828-c04-crawler-divide-claim/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 305s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0828-c04-crawler-divide-claim/world.py --out collective/contrib/_c07rev14/rerun/seed5 --seeds 5 --frames 240 --threshold 0.25 --no-movie`
- segmentation: matter > 0.33 of robust range [-0.0, 0.7548], min area 6 px

## Measurements
- components: final 13, mean 5.9, max 13; occupancy final 0.20
- tracks: 27; persistent (alive >= 50% of run): 3; longest 217 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.21 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 13], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 2.09/time; max body lengths 34.7
- replication (lineage window K = 20 frames = time 50, default): splits 12, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 5, merges 0, merge/split ratio 0, nucleations 2
- channel total drift (end/start - 1): [2.6958, 1.1568, None, -0.4669]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 133: holes 0, rim-vs-core 0.35, rim-vs-outside 0.55, heterogeneity 0.18; core [0.843, 0.475, 0.624, 0.413] rim [0.589, 0.615, 0.423, 0.435]
  - track 6 at frame 115: holes 0, rim-vs-core 0.34, rim-vs-outside 0.64, heterogeneity 0.18; core [0.832, 0.427, 0.682, 0.516] rim [0.611, 0.612, 0.497, 0.539]
  - track 3 at frame 103: holes 0, rim-vs-core 0.30, rim-vs-outside 0.65, heterogeneity 0.17; core [0.812, 0.337, 0.783, 0.533] rim [0.634, 0.498, 0.609, 0.543]
  - track 16 at frame 220: holes 0, rim-vs-core 0.31, rim-vs-outside 0.47, heterogeneity 0.08; core [0.675, 0.135, 0.763, 0.024] rim [0.49, 0.263, 0.553, 0.053]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 43 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.833, rim/outside 15.1 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.638)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.44, rim/outside 5.12 (aggregate of 43 individuals; 42/43 membrane-like individually; rim level 0.33)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.839, rim/outside 35.8 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.551)
  - radial n (nutrient): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.19, rim/outside 0.924 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.297)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #4 (t=332.5, R_eq 17.32): ['|P| (actin polarization)']; #6 (t=287.5, R_eq 18.08): ['|P| (actin polarization)']; #3 (t=257.5, R_eq 18.3): ['|P| (actin polarization)']; #16 (t=550, R_eq 19.05): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
