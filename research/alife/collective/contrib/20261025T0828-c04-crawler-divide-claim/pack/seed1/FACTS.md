# Evidence pack: crawler (seed 1)

- world: `../../crawler.py`, family `phase-field`
- parent: None; mutation: Ziebert-Aranson crawling cell, body-wise area constraint
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 224s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/crawler.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/K1 --seeds 1 2 --frames 240 --threshold 0.25 --no-movie`
- segmentation: matter > 0.33 of robust range [-0.0, 0.75], min area 6 px

## Measurements
- components: final 15, mean 10.2, max 15; occupancy final 0.19
- tracks: 39; persistent (alive >= 50% of run): 10; longest 157 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 174.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 2.84/time; max body lengths 7.9
- replication (lineage window K = 20 frames = time 50, default): splits 15, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 4, merges 3, merge/split ratio 0.2, nucleations 5
- channel total drift (end/start - 1): [2.9338, 0.9671, None, -0.6074]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 163: holes 0, rim-vs-core 0.34, rim-vs-outside 0.47, heterogeneity 0.10; core [0.723, 0.175, 0.727, 0.209] rim [0.508, 0.321, 0.511, 0.232]
  - track 22 at frame 165: holes 0, rim-vs-core 0.32, rim-vs-outside 0.41, heterogeneity 0.08; core [0.734, 0.174, 0.617, 0.191] rim [0.508, 0.303, 0.427, 0.212]
  - track 24 at frame 167: holes 0, rim-vs-core 0.23, rim-vs-outside 0.54, heterogeneity 0.09; core [0.729, 0.159, 0.677, 0.175] rim [0.577, 0.259, 0.536, 0.196]
  - track 28 at frame 171: holes 0, rim-vs-core 0.34, rim-vs-outside 0.46, heterogeneity 0.09; core [0.729, 0.168, 0.715, 0.185] rim [0.508, 0.302, 0.498, 0.204]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 68 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 17.8 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.683)
  - radial |P| (actin polarization): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.07, rim/outside 6.18 (aggregate of 68 individuals; 68/68 membrane-like individually; rim level 0.347)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 31 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.452)
  - radial n (nutrient): peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.942 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.298)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #19 (t=407.5, R_eq 19.17): ['|P| (actin polarization)']; #22 (t=412.5, R_eq 18.26): ['|P| (actin polarization)']; #24 (t=417.5, R_eq 18.8): ['|P| (actin polarization)']; #28 (t=427.5, R_eq 18.77): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
