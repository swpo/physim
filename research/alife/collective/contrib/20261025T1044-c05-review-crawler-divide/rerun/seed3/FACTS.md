# Evidence pack: crawler-divide (seed 3)

- world: `../../../../contrib/20261025T0828-c04-crawler-divide-claim/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 294s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0828-c04-crawler-divide-claim/world.py --out collective/work_c05/rev_cd/rerun/seed3 --seeds 3 --frames 240 --no-movie`
- segmentation: matter > 0.34 of robust range [-0.0, 0.7417], min area 6 px

## Measurements
- components: final 15, mean 10.2, max 15; occupancy final 0.19
- tracks: 38; persistent (alive >= 50% of run): 8; longest 187 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.65 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 2.7/time; max body lengths 14.9
- replication (lineage window K = 20 frames = time 50, default): splits 16, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 5, merges 3, merge/split ratio 0.188, nucleations 3
- channel total drift (end/start - 1): [2.8223, 0.9231, None, -0.6071]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 147: holes 0, rim-vs-core 0.27, rim-vs-outside 0.27, heterogeneity 0.07; core [0.684, 0.177, 0.38, 0.223] rim [0.482, 0.305, 0.267, 0.243]
  - track 16 at frame 149: holes 0, rim-vs-core 0.16, rim-vs-outside 0.50, heterogeneity 0.08; core [0.656, 0.155, 0.615, 0.257] rim [0.556, 0.238, 0.521, 0.266]
  - track 19 at frame 157: holes 0, rim-vs-core 0.33, rim-vs-outside 0.44, heterogeneity 0.09; core [0.725, 0.167, 0.678, 0.186] rim [0.503, 0.299, 0.47, 0.209]
  - track 30 at frame 186: holes 0, rim-vs-core 0.36, rim-vs-outside 0.36, heterogeneity 0.09; core [0.774, 0.206, 0.604, 0.099] rim [0.502, 0.32, 0.392, 0.12]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 69 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 17.1 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.694)
  - radial |P| (actin polarization): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.9, rim/outside 5.94 (aggregate of 69 individuals; 67/69 membrane-like individually; rim level 0.351)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 28.1 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.419)
  - radial n (nutrient): peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.16, rim/outside 0.942 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.288)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #13 (t=367.5, R_eq 17.44): ['|P| (actin polarization)']; #16 (t=372.5, R_eq 19.38): ['|P| (actin polarization)']; #19 (t=392.5, R_eq 19.02): ['|P| (actin polarization)']; #30 (t=465, R_eq 17.95): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
