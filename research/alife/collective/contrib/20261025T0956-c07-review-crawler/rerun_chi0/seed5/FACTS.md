# Evidence pack: crawler-divide (seed 5)

- world: `../../../20261025T0828-c04-crawler-divide-claim/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 301s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0828-c04-crawler-divide-claim/world.py --out collective/contrib/_c07rev14/rerun_chi0/seed5 --seeds 5 --frames 240 --threshold 0.25 --no-movie`
- segmentation: matter > 0.33 of robust range [-0.0, 0.7617], min area 6 px

## Measurements
- components: final 22, mean 17.2, max 22; occupancy final 0.21
- tracks: 42; persistent (alive >= 50% of run): 22; longest 207 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.87 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 22, 22], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 1.68/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 50, default): splits 20, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 5, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [3.1804, 1.7581, None, -0.7025]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 137: holes 0, rim-vs-core 0.31, rim-vs-outside 0.47, heterogeneity 0.11; core [0.807, 0.351, 0.55, 0.049] rim [0.597, 0.521, 0.407, 0.058]
  - track 13 at frame 139: holes 0, rim-vs-core 0.41, rim-vs-outside 0.35, heterogeneity 0.11; core [0.805, 0.386, 0.471, 0.036] rim [0.514, 0.61, 0.301, 0.049]
  - track 15 at frame 145: holes 0, rim-vs-core 0.38, rim-vs-outside 0.31, heterogeneity 0.10; core [0.793, 0.393, 0.329, 0.025] rim [0.514, 0.615, 0.213, 0.036]
  - track 32 at frame 159: holes 0, rim-vs-core 0.22, rim-vs-outside 0.22, heterogeneity 0.07; core [0.674, 0.375, 0.0, 0.024] rim [0.528, 0.535, 0.0, 0.027]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 116 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 9.18 (aggregate of 116 individuals; 0/116 membrane-like individually; rim level 0.674)
  - radial |P| (actin polarization): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.59, rim/outside 4.42 (aggregate of 116 individuals; 115/116 membrane-like individually; rim level 0.611)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 7.35 (aggregate of 116 individuals; 0/116 membrane-like individually; rim level 0.196)
  - radial n (nutrient): peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.2, rim/outside 0.958 (aggregate of 116 individuals; 0/116 membrane-like individually; rim level 0.172)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #11 (t=342.5, R_eq 20.81): ['|P| (actin polarization)']; #13 (t=347.5, R_eq 19.81): ['|P| (actin polarization)']; #15 (t=362.5, R_eq 18.33): ['|P| (actin polarization)']; #32 (t=397.5, R_eq 13.61): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
