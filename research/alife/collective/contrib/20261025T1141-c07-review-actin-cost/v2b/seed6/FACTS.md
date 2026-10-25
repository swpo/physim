# Evidence pack: crawler-divide (seed 6)

- world: `../../../20261025T1044-c04-crawler-actin-cost-negative/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 287s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1044-c04-crawler-actin-cost-negative/world.py --out collective/contrib/_c07rev23/v2b/seed6 --seeds 6 --frames 240 --no-movie`
- segmentation: matter > 0.26 of robust range [-0.0, 0.9707], min area 6 px

## Measurements
- components: final 2, mean 5.7, max 11; occupancy final 0.03
- tracks: 55; persistent (alive >= 50% of run): 3; longest 149 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 279.44 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.151/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 50, default): splits 24, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 9, merge/split ratio 0.375, nucleations 0
- channel total drift (end/start - 1): [-0.334, -0.8207, None, -0.2108]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 48 at frame 167: holes 0, rim-vs-core 0.48, rim-vs-outside 0.56, heterogeneity 0.12; core [0.907, 0.305, 0.203, 0.022] rim [0.484, 0.506, 0.108, 0.078]
  - track 50 at frame 167: holes 0, rim-vs-core 0.25, rim-vs-outside 0.63, heterogeneity 0.13; core [0.894, 0.345, 0.215, 0.041] rim [0.658, 0.396, 0.158, 0.069]
  - track 37 at frame 145: holes 0, rim-vs-core 0.48, rim-vs-outside 0.54, heterogeneity 0.12; core [0.905, 0.298, 0.209, 0.001] rim [0.482, 0.494, 0.111, 0.024]
  - track 46 at frame 151: holes 0, rim-vs-core 0.47, rim-vs-outside 0.55, heterogeneity 0.12; core [0.89, 0.322, 0.175, 0.028] rim [0.477, 0.517, 0.094, 0.084]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 34 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 15.3 (aggregate of 34 individuals; 2/34 membrane-like individually; rim level 0.766)
  - radial |P| (actin polarization): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.78, rim/outside 14.5 (aggregate of 34 individuals; 33/34 membrane-like individually; rim level 0.547)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 9.55 (aggregate of 34 individuals; 2/34 membrane-like individually; rim level 0.188)
  - radial n (nutrient): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.99, rim/outside 0.859 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.279)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #48 (t=417.5, R_eq 23.8): ['|P| (actin polarization)']; #50 (t=417.5, R_eq 25.02): ['|P| (actin polarization)']; #37 (t=362.5, R_eq 23.44): ['|P| (actin polarization)']; #46 (t=377.5, R_eq 22.23): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
