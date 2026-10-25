# Evidence pack: crawler-divide (seed 3)

- world: `../../20261025T0908-c04-crawler-divide-confound/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 269s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0908-c04-crawler-divide-confound/world.py --out collective/contrib/20261025T1055-c01-review-crawler-confound/bV_starve --seeds 3 --frames 240 --no-movie`
- segmentation: matter > 0.29 of robust range [-0.0, 0.8672], min area 6 px

## Measurements
- components: final 14, mean 11.4, max 14; occupancy final 0.10
- tracks: 32; persistent (alive >= 50% of run): 14; longest 195 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.40 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 14, 14], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 1.46/time; max body lengths 5.5
- replication (lineage window K = 20 frames = time 50, default): splits 14, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.071, nucleations 1
- channel total drift (end/start - 1): [1.3038, -1.0, None, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 143: holes 0, rim-vs-core 0.37, rim-vs-outside 0.23, heterogeneity 0.05; core [0.806, 0.0, 0.0, 0.0] rim [0.431, 0.0, 0.0, 0.0]
  - track 17 at frame 147: holes 0, rim-vs-core 0.38, rim-vs-outside 0.23, heterogeneity 0.05; core [0.807, 0.0, 0.0, 0.0] rim [0.43, 0.0, 0.0, 0.0]
  - track 19 at frame 157: holes 0, rim-vs-core 0.37, rim-vs-outside 0.24, heterogeneity 0.06; core [0.816, 0.0, 0.0, 0.0] rim [0.443, 0.0, 0.0, 0.0]
  - track 25 at frame 159: holes 0, rim-vs-core 0.38, rim-vs-outside 0.22, heterogeneity 0.05; core [0.807, 0.0, 0.0, 0.0] rim [0.428, 0.0, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.752, rim/outside 22.1 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.701)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.91, rim/outside 8.38 (aggregate of 76 individuals; 33/76 membrane-like individually; rim level 0.182)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 13.3 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.252)
  - radial n (nutrient): peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 0.98 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.198)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #14 (t=357.5, R_eq 11.97): none; #17 (t=367.5, R_eq 11.98): none; #19 (t=392.5, R_eq 12.09): none; #25 (t=397.5, R_eq 12.05): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
