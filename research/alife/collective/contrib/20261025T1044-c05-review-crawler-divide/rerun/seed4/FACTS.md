# Evidence pack: crawler-divide (seed 4)

- world: `../../../../contrib/20261025T0828-c04-crawler-divide-claim/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 295s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0828-c04-crawler-divide-claim/world.py --out collective/work_c05/rev_cd/rerun/seed4 --seeds 4 --frames 240 --no-movie`
- segmentation: matter > 0.33 of robust range [-0.0, 0.7554], min area 6 px

## Measurements
- components: final 18, mean 10.8, max 18; occupancy final 0.21
- tracks: 43; persistent (alive >= 50% of run): 2; longest 141 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.82 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 2.74/time; max body lengths 10.1
- replication (lineage window K = 20 frames = time 50, default): splits 18, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 6, merges 3, merge/split ratio 0.167, nucleations 3
- channel total drift (end/start - 1): [3.3182, 1.1383, None, -0.6317]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 171: holes 0, rim-vs-core 0.35, rim-vs-outside 0.44, heterogeneity 0.09; core [0.739, 0.185, 0.693, 0.2] rim [0.502, 0.318, 0.471, 0.221]
  - track 23 at frame 175: holes 0, rim-vs-core 0.31, rim-vs-outside 0.41, heterogeneity 0.09; core [0.77, 0.213, 0.613, 0.185] rim [0.542, 0.33, 0.432, 0.201]
  - track 25 at frame 182: holes 0, rim-vs-core 0.42, rim-vs-outside 0.55, heterogeneity 0.10; core [0.768, 0.184, 0.913, 0.148] rim [0.509, 0.314, 0.615, 0.17]
  - track 41 at frame 214: holes 0, rim-vs-core 0.28, rim-vs-outside 0.18, heterogeneity 0.06; core [0.739, 0.232, 0.0, 0.047] rim [0.481, 0.332, 0.0, 0.057]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 73 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 14.5 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.674)
  - radial |P| (actin polarization): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.97, rim/outside 5.53 (aggregate of 73 individuals; 70/73 membrane-like individually; rim level 0.342)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 18.8 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.4)
  - radial n (nutrient): peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 0.945 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.272)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #20 (t=427.5, R_eq 18.74): ['|P| (actin polarization)']; #23 (t=437.5, R_eq 17.83): ['|P| (actin polarization)']; #25 (t=455, R_eq 19.67): ['|P| (actin polarization)']; #41 (t=535, R_eq 13.97): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
