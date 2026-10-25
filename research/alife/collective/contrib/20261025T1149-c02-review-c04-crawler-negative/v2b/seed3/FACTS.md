# run with WORLD_P='{"okclip":1,"bV":1,"shed":0,"kup":0.05,"n0":0.5,"capdev":0.3,"kact":0.1}'
# Evidence pack: crawler-divide (seed 3)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1044-c04-crawler-actin-cost-negative/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 366s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1044-c04-crawler-actin-cost-negative/world.py --out collective/contrib/20261025T1149-c02-review-c04-crawler-negative/v2b/seed3 --seeds 3 --frames 240 --no-movie`
- segmentation: matter > 0.26 of robust range [-0.0, 0.9694], min area 6 px

## Measurements
- components: final 2, mean 5.3, max 9; occupancy final 0.02
- tracks: 59; persistent (alive >= 50% of run): 3; longest 157 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 193.62 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 2], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.726/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 50, default): splits 25, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 8, merge/split ratio 0.32, nucleations 0
- channel total drift (end/start - 1): [-0.6304, -0.8884, None, -0.1959]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 163: holes 0, rim-vs-core 0.49, rim-vs-outside 0.54, heterogeneity 0.12; core [0.916, 0.278, 0.22, 0.021] rim [0.486, 0.475, 0.116, 0.08]
  - track 45 at frame 167: holes 0, rim-vs-core 0.47, rim-vs-outside 0.55, heterogeneity 0.12; core [0.905, 0.296, 0.186, 0.032] rim [0.491, 0.486, 0.101, 0.084]
  - track 23 at frame 139: holes 0, rim-vs-core 0.48, rim-vs-outside 0.52, heterogeneity 0.12; core [0.9, 0.278, 0.207, 0.019] rim [0.476, 0.472, 0.109, 0.066]
  - track 49 at frame 163: holes 0, rim-vs-core 0.25, rim-vs-outside 0.57, heterogeneity 0.11; core [0.838, 0.363, 0.15, 0.068] rim [0.604, 0.433, 0.108, 0.105]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 33 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.844, rim/outside 12.5 (aggregate of 33 individuals; 0/33 membrane-like individually; rim level 0.71)
  - radial |P| (actin polarization): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.37, rim/outside 12 (aggregate of 33 individuals; 30/33 membrane-like individually; rim level 0.498)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 6.98 (aggregate of 33 individuals; 0/33 membrane-like individually; rim level 0.165)
  - radial n (nutrient): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.79, rim/outside 0.862 (aggregate of 33 individuals; 0/33 membrane-like individually; rim level 0.284)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #38 (t=407.5, R_eq 25.01): ['|P| (actin polarization)']; #45 (t=417.5, R_eq 23.07): ['|P| (actin polarization)']; #23 (t=347.5, R_eq 24.09): ['|P| (actin polarization)']; #49 (t=407.5, R_eq 21.52): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
