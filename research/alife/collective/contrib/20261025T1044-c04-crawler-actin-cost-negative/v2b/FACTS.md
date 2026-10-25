# Evidence pack: crawler-divide (seed 1)

- world: `../cdiv2.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 219s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv2.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/v2b --seeds 1 --frames 240 --no-movie`
- segmentation: matter > 0.26 of robust range [-0.0, 0.9689], min area 6 px

## Measurements
- components: final 3, mean 5.0, max 10; occupancy final 0.11
- tracks: 46; persistent (alive >= 50% of run): 4; longest 146 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.41 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.871/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 50, default): splits 19, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 7, merge/split ratio 0.368, nucleations 0
- channel total drift (end/start - 1): [1.9169, -0.4635, None, -0.2756]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 35 at frame 167: holes 0, rim-vs-core 0.29, rim-vs-outside 0.68, heterogeneity 0.13; core [0.923, 0.283, 0.229, 0.028] rim [0.674, 0.405, 0.167, 0.076]
  - track 33 at frame 159: holes 0, rim-vs-core 0.47, rim-vs-outside 0.54, heterogeneity 0.11; core [0.903, 0.297, 0.179, 0.005] rim [0.483, 0.49, 0.095, 0.05]
  - track 43 at frame 177: holes 0, rim-vs-core 0.50, rim-vs-outside 0.58, heterogeneity 0.13; core [0.877, 0.238, 0.259, 0.024] rim [0.487, 0.526, 0.144, 0.095]
  - track 44 at frame 177: holes 0, rim-vs-core 0.50, rim-vs-outside 0.60, heterogeneity 0.13; core [0.933, 0.245, 0.239, 0.014] rim [0.517, 0.495, 0.132, 0.083]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 31 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 13.7 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.765)
  - radial |P| (actin polarization): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.99, rim/outside 12.8 (aggregate of 31 individuals; 29/31 membrane-like individually; rim level 0.528)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.855, rim/outside 7.68 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.181)
  - radial n (nutrient): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.25, rim/outside 0.827 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.29)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #35 (t=417.5, R_eq 26.62): ['|P| (actin polarization)']; #33 (t=397.5, R_eq 23.39): ['|P| (actin polarization)']; #43 (t=442.5, R_eq 26.58): ['|P| (actin polarization)']; #44 (t=442.5, R_eq 26.92): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
