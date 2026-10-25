# Evidence pack: crawler-divide (seed 3)

- world: `../../20261025T0828-c04-crawler-divide-claim/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 254s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0828-c04-crawler-divide-claim/world.py --out collective/contrib/20261025T0932-c01-review-crawler-divide/chi0 --seeds 3 --frames 240 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.0, 0.7761], min area 6 px

## Measurements
- components: final 18, mean 13.9, max 18; occupancy final 0.18
- tracks: 34; persistent (alive >= 50% of run): 18; longest 211 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 27.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 1.75/time; max body lengths 5.2
- replication (lineage window K = 20 frames = time 50, default): splits 16, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 5, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [2.5121, 1.2963, None, -0.6605]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 135: holes 0, rim-vs-core 0.35, rim-vs-outside 0.31, heterogeneity 0.09; core [0.757, 0.336, 0.356, 0.101] rim [0.495, 0.54, 0.233, 0.117]
  - track 11 at frame 141: holes 0, rim-vs-core 0.35, rim-vs-outside 0.31, heterogeneity 0.09; core [0.749, 0.322, 0.383, 0.072] rim [0.492, 0.526, 0.252, 0.088]
  - track 13 at frame 145: holes 0, rim-vs-core 0.36, rim-vs-outside 0.32, heterogeneity 0.09; core [0.752, 0.321, 0.415, 0.052] rim [0.492, 0.522, 0.272, 0.069]
  - track 32 at frame 179: holes 0, rim-vs-core 0.11, rim-vs-outside 0.29, heterogeneity 0.06; core [0.638, 0.363, 0.0, 0.03] rim [0.549, 0.424, 0.0, 0.033]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 92 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.813, rim/outside 13.3 (aggregate of 92 individuals; 0/92 membrane-like individually; rim level 0.656)
  - radial |P| (actin polarization): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.51, rim/outside 5.85 (aggregate of 92 individuals; 92/92 membrane-like individually; rim level 0.544)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.827, rim/outside 10.1 (aggregate of 92 individuals; 0/92 membrane-like individually; rim level 0.197)
  - radial n (nutrient): peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.24, rim/outside 0.939 (aggregate of 92 individuals; 0/92 membrane-like individually; rim level 0.182)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #7 (t=337.5, R_eq 19.01): ['|P| (actin polarization)']; #11 (t=352.5, R_eq 19.42): ['|P| (actin polarization)']; #13 (t=362.5, R_eq 19.81): ['|P| (actin polarization)']; #32 (t=447.5, R_eq 14.23): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
