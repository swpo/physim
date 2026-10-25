# Evidence pack: crawler-divide (seed 3)

- world: `../../../../contrib/20261025T0849-c04-crawler-divide-forks/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 280s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0849-c04-crawler-divide-forks/world.py --out collective/work_c05/rev_cf/starve/seed3 --seeds 3 --frames 240 --no-movie`
- segmentation: matter > 0.30 of robust range [-0.0, 0.8225], min area 6 px

## Measurements
- components: final 11, mean 8.7, max 11; occupancy final 0.09
- tracks: 30; persistent (alive >= 50% of run): 11; longest 215 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.78 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 2.7/time; max body lengths 17.0
- replication (lineage window K = 20 frames = time 50, default): splits 12, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 4, merges 3, merge/split ratio 0.25, nucleations 3
- channel total drift (end/start - 1): [1.1403, -0.6063, None, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 133: holes 0, rim-vs-core 0.38, rim-vs-outside 0.21, heterogeneity 0.06; core [0.815, 0.128, 0.0, 0.0] rim [0.436, 0.138, 0.0, 0.0]
  - track 10 at frame 145: holes 0, rim-vs-core 0.38, rim-vs-outside 0.22, heterogeneity 0.06; core [0.824, 0.13, 0.0, 0.0] rim [0.444, 0.14, 0.0, 0.0]
  - track 13 at frame 147: holes 0, rim-vs-core 0.38, rim-vs-outside 0.22, heterogeneity 0.06; core [0.823, 0.131, 0.0, 0.0] rim [0.441, 0.139, 0.0, 0.0]
  - track 16 at frame 149: holes 0, rim-vs-core 0.32, rim-vs-outside 0.30, heterogeneity 0.06; core [0.847, 0.125, 0.0, 0.0] rim [0.525, 0.142, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 58 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.774, rim/outside 19.8 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.654)
  - radial |P| (actin polarization): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.25, rim/outside 5.58 (aggregate of 58 individuals; 55/58 membrane-like individually; rim level 0.241)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.836, rim/outside 15.6 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.225)
  - radial n (nutrient): peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.989 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.199)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #5 (t=332.5, R_eq 13.23): ['|P| (actin polarization)']; #10 (t=362.5, R_eq 13.1): ['|P| (actin polarization)']; #13 (t=367.5, R_eq 13.06): ['|P| (actin polarization)']; #16 (t=372.5, R_eq 13.11): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
