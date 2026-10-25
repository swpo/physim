# Evidence pack: crawler-divide (seed 3)

- world: `../../../../contrib/20261025T0849-c04-crawler-divide-forks/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 282s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0849-c04-crawler-divide-forks/world.py --out collective/work_c05/rev_cf/cut/seed3 --seeds 3 --frames 240 --no-movie`
- segmentation: matter > 0.26 of robust range [-0.0, 0.9461], min area 6 px

## Measurements
- components: final 12, mean 8.7, max 12; occupancy final 0.19
- tracks: 32; persistent (alive >= 50% of run): 11; longest 215 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.93 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 12], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 2.7/time; max body lengths 14.1
- replication (lineage window K = 20 frames = time 50, default): splits 13, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 4, merges 3, merge/split ratio 0.231, nucleations 3
- channel total drift (end/start - 1): [3.6391, -0.4882, None, -0.6225]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 133: holes 0, rim-vs-core 0.46, rim-vs-outside 0.31, heterogeneity 0.10; core [0.814, 0.149, 0.415, 0.287] rim [0.407, 0.168, 0.208, 0.323]
  - track 10 at frame 145: holes 0, rim-vs-core 0.46, rim-vs-outside 0.31, heterogeneity 0.10; core [0.814, 0.145, 0.409, 0.268] rim [0.41, 0.165, 0.206, 0.305]
  - track 13 at frame 147: holes 0, rim-vs-core 0.42, rim-vs-outside 0.29, heterogeneity 0.09; core [0.813, 0.139, 0.308, 0.223] rim [0.422, 0.158, 0.16, 0.252]
  - track 16 at frame 149: holes 0, rim-vs-core 0.40, rim-vs-outside 0.38, heterogeneity 0.10; core [0.834, 0.138, 0.418, 0.261] rim [0.476, 0.164, 0.239, 0.284]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.785, rim/outside 21.1 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.623)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.37, rim/outside 5.57 (aggregate of 59 individuals; 55/59 membrane-like individually; rim level 0.231)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 28.8 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.34)
  - radial n (nutrient): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.2, rim/outside 0.932 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.336)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #5 (t=332.5, R_eq 17.38): ['|P| (actin polarization)']; #10 (t=362.5, R_eq 17.33): ['|P| (actin polarization)']; #13 (t=367.5, R_eq 16.24): ['|P| (actin polarization)']; #16 (t=372.5, R_eq 17.36): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
