# Evidence pack: cips-layered-lownoise (seed 5)

- world: `../../../20261026T1626-c44-cips-lownoise-gen4-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 251 frames x 1000 steps x dt 0.1 = time 25000; grid [192, 192]; wall 1588s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1626-c44-cips-lownoise-gen4-claim/world.py --out collective/contrib/20261026T2233-c47-review-gen4-cut/rerun/seed5 --seeds 5 --frames 250 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0211, 0.9759], min area 6 px

## Measurements
- components: final 18, mean 12.9, max 18; occupancy final 0.09
- tracks: 32; persistent (alive >= 50% of run): 10; longest 212 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.54 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.00391/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 14, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 4
- channel total drift (end/start - 1): [-0.0, -0.5821, 0.6273, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 145: holes 0, rim-vs-core 0.53, rim-vs-outside 0.63, heterogeneity 0.16; core [0.985, 0.94, 0.045, 0.082] rim [0.788, 0.704, 0.228, 0.472]
  - track 8 at frame 145: holes 0, rim-vs-core 0.56, rim-vs-outside 0.63, heterogeneity 0.17; core [0.988, 0.948, 0.06, 0.078] rim [0.777, 0.699, 0.247, 0.496]
  - track 12 at frame 168: holes 0, rim-vs-core 0.54, rim-vs-outside 0.63, heterogeneity 0.16; core [0.988, 0.95, 0.06, 0.078] rim [0.787, 0.706, 0.244, 0.472]
  - track 24 at frame 189: holes 0, rim-vs-core 0.55, rim-vs-outside 0.63, heterogeneity 0.16; core [0.987, 0.946, 0.057, 0.077] rim [0.782, 0.7, 0.241, 0.484]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 84 components >= 12 px at frames [42, 84, 126, 166, 208, 250]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 36 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.899)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 12.7 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.848)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 22, rim/outside 0.66 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.5)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 5.28, rim/outside 23.8 (aggregate of 84 individuals; 77/84 membrane-like individually; rim level 0.633)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #6 (t=14500, R_eq 7.96): ['s']; #8 (t=14500, R_eq 7.53): ['s']; #12 (t=16800, R_eq 7.48): ['s']; #24 (t=18900, R_eq 7.59): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
