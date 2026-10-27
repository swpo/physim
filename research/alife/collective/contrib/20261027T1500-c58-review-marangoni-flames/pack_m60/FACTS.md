# Evidence pack: marangoni-flames (seed 4)

- world: `../../20261027T0319-c51-marangoni-flames-negative/world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 53s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0319-c51-marangoni-flames-negative/world.py --out collective/contrib/20261027T1500-c58-review-marangoni-flames/pack_m60 --seeds 4 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.11 of robust range [0.0, 2.261], min area 6 px

## Measurements
- components: final 32, mean 31.3, max 47; occupancy final 0.02
- tracks: 122; persistent (alive >= 50% of run): 32; longest 601 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 9.64 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 32, 30], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00648/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 20, default): splits 34, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 0.088, nucleations 17
- channel total drift (end/start - 1): [-0.9029, -0.2833, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 303: holes 0, rim-vs-core 0.94, rim-vs-outside 0.50, heterogeneity 0.27; core [0.989, 0.208, 0.802, 1.0] rim [0.318, 0.235, 0.605, 0.366]
  - track 11 at frame 303: holes 0, rim-vs-core 0.94, rim-vs-outside 0.50, heterogeneity 0.27; core [0.981, 0.204, 0.804, 0.995] rim [0.316, 0.232, 0.599, 0.362]
  - track 14 at frame 303: holes 0, rim-vs-core 0.60, rim-vs-outside 0.74, heterogeneity 0.23; core [0.926, 0.17, 0.625, 0.938] rim [0.49, 0.191, 0.681, 0.532]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 144 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.536, rim/outside 41.5 (aggregate of 144 individuals; 0/144 membrane-like individually; rim level 0.531)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.59, rim/outside 1.02 (aggregate of 144 individuals; 0/144 membrane-like individually; rim level 0.389)
  - radial |u|: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.05, rim/outside 9.05 (aggregate of 144 individuals; 143/144 membrane-like individually; rim level 0.858)  MEMBRANE-LIKE
  - radial burn r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.698, rim/outside 70.5 (aggregate of 144 individuals; 0/144 membrane-like individually; rim level 0.695)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |u| (peak at rho=0.45, outside the peak band)
- membrane-like channels per top track at mid-life: #7 (t=303, R_eq 2.03): ['|u|']; #11 (t=303, R_eq 2.03): ['|u|']; #14 (t=303, R_eq 1.87): ['|u|']; #91 (t=308, R_eq 1.78): ['|u|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
