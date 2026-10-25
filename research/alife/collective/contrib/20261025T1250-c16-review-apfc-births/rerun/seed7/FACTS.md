# Evidence pack: apfc (seed 7)

- world: `../world.py`, family `active-pfc`
- parent: new class (Menzel & Loewen 2013 active phase-field crystal); mutation: none (benchmark model)
- run: 121 frames x 50 steps x dt 0.1 = time 600; grid [128, 128]; wall 35s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1250-c16-review-apfc-births/world.py --out collective/contrib/20261025T1250-c16-review-apfc-births/rerun --seeds 7 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 0.5922], min area 6 px

## Measurements
- components: final 10, mean 10.2, max 13; occupancy final 0.16
- tracks: 104; persistent (alive >= 50% of run): 0; longest 50 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 11, 9], H1 [0, 0, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.296/time; max body lengths 7.2
- replication (lineage window K = 20 frames = time 100, default): splits 31, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 32, merge/split ratio 1.03, nucleations 10
- channel total drift (end/start - 1): [-0.6577, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 27: holes 0, rim-vs-core 0.59, rim-vs-outside 0.15, heterogeneity 0.27; core [0.726, 0.395, 0.651] rim [0.434, 0.049, 0.275]
  - track 8 at frame 27: holes 0, rim-vs-core 0.57, rim-vs-outside 0.15, heterogeneity 0.27; core [0.723, 0.386, 0.634] rim [0.429, 0.045, 0.283]
  - track 37 at frame 71: holes 0, rim-vs-core 0.58, rim-vs-outside 0.17, heterogeneity 0.26; core [0.731, 0.425, 0.672] rim [0.459, 0.052, 0.321]
  - track 20 at frame 40: holes 0, rim-vs-core 0.58, rim-vs-outside 0.17, heterogeneity 0.27; core [0.737, 0.399, 0.647] rim [0.442, 0.05, 0.295]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial crystal amplitude (smoothed (phi - mean)^2): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.741, rim/outside 9.26 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.652)
  - radial density phi: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.41, rim/outside 1.44 (aggregate of 62 individuals; 13/62 membrane-like individually; rim level 0.252)
  - radial |P|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 9.95 (aggregate of 62 individuals; 4/62 membrane-like individually; rim level 0.548)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=135, R_eq 5.53): none; #8 (t=135, R_eq 5.56): none; #37 (t=355, R_eq 5.29): none; #20 (t=200, R_eq 5.53): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
