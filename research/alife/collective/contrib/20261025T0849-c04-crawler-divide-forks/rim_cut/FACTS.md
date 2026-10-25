# Evidence pack: crawler-divide (seed 1)

- world: `../cdiv.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 228s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cut --seeds 1 --frames 240 --no-movie`
- segmentation: matter > 0.27 of robust range [-0.0, 0.9429], min area 6 px

## Measurements
- components: final 12, mean 9.4, max 13; occupancy final 0.18
- tracks: 33; persistent (alive >= 50% of run): 12; longest 164 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 144.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 2.84/time; max body lengths 7.2
- replication (lineage window K = 20 frames = time 50, default): splits 13, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 4, merges 3, merge/split ratio 0.231, nucleations 3
- channel total drift (end/start - 1): [3.3911, -0.4973, None, -0.6211]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 159: holes 0, rim-vs-core 0.53, rim-vs-outside 0.44, heterogeneity 0.12; core [0.858, 0.133, 0.683, 0.212] rim [0.446, 0.162, 0.354, 0.251]
  - track 19 at frame 163: holes 0, rim-vs-core 0.50, rim-vs-outside 0.35, heterogeneity 0.11; core [0.827, 0.13, 0.555, 0.136] rim [0.411, 0.145, 0.276, 0.166]
  - track 22 at frame 165: holes 0, rim-vs-core 0.50, rim-vs-outside 0.35, heterogeneity 0.11; core [0.826, 0.132, 0.552, 0.158] rim [0.413, 0.149, 0.276, 0.189]
  - track 28 at frame 171: holes 0, rim-vs-core 0.57, rim-vs-outside 0.48, heterogeneity 0.13; core [0.863, 0.122, 0.794, 0.151] rim [0.446, 0.15, 0.41, 0.189]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 23.2 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.621)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.57, rim/outside 5.66 (aggregate of 62 individuals; 62/62 membrane-like individually; rim level 0.227)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 33.6 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.376)
  - radial n (nutrient): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.19, rim/outside 0.934 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.333)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #18 (t=397.5, R_eq 18.18): ['|P| (actin polarization)']; #19 (t=407.5, R_eq 17.24): ['|P| (actin polarization)']; #22 (t=412.5, R_eq 17.24): ['|P| (actin polarization)']; #28 (t=427.5, R_eq 18.72): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
