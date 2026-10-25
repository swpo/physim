# Evidence pack: crawler (seed 2)

- world: `../../crawler.py`, family `phase-field`
- parent: None; mutation: Ziebert-Aranson crawling cell, body-wise area constraint
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 214s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/crawler.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/K1 --seeds 1 2 --frames 240 --threshold 0.25 --no-movie`
- segmentation: matter > 0.34 of robust range [-0.0, 0.7335], min area 6 px

## Measurements
- components: final 14, mean 10.1, max 14; occupancy final 0.19
- tracks: 34; persistent (alive >= 50% of run): 12; longest 205 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 32.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 14, 14], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 2.69/time; max body lengths 11.4
- replication (lineage window K = 20 frames = time 50, default): splits 14, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.071, nucleations 4
- channel total drift (end/start - 1): [2.7911, 0.8555, None, -0.6098]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 139: holes 0, rim-vs-core 0.31, rim-vs-outside 0.38, heterogeneity 0.08; core [0.723, 0.188, 0.558, 0.268] rim [0.504, 0.325, 0.389, 0.289]
  - track 9 at frame 139: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.08; core [0.671, 0.16, 0.522, 0.311] rim [0.495, 0.313, 0.385, 0.332]
  - track 17 at frame 157: holes 0, rim-vs-core 0.33, rim-vs-outside 0.45, heterogeneity 0.11; core [0.73, 0.178, 0.733, 0.199] rim [0.516, 0.293, 0.518, 0.216]
  - track 19 at frame 157: holes 0, rim-vs-core 0.17, rim-vs-outside 0.61, heterogeneity 0.10; core [0.727, 0.211, 0.726, 0.2] rim [0.614, 0.26, 0.613, 0.21]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 68 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 17.7 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.687)
  - radial |P| (actin polarization): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.11, rim/outside 6.15 (aggregate of 68 individuals; 67/68 membrane-like individually; rim level 0.358)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.806, rim/outside 30.9 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.438)
  - radial n (nutrient): peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.944 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.303)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #8 (t=347.5, R_eq 18.31): ['|P| (actin polarization)']; #9 (t=347.5, R_eq 18.7): ['|P| (actin polarization)']; #17 (t=392.5, R_eq 19.41): ['|P| (actin polarization)']; #19 (t=392.5, R_eq 19.1): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
