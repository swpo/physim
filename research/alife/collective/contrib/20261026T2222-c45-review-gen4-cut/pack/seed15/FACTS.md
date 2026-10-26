# Evidence pack: cips-layered-lownoise (seed 15)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261026T1626-c44-cips-lownoise-gen4-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 151 frames x 1000 steps x dt 0.1 = time 15000; grid [192, 192]; wall 780s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1626-c44-cips-lownoise-gen4-claim/world.py --out /tmp/claude-0/gc/pack/seed15 --seeds 15 --frames 150 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0208, 0.9755], min area 6 px

## Measurements
- components: final 15, mean 9.6, max 15; occupancy final 0.08
- tracks: 26; persistent (alive >= 50% of run): 4; longest 114 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.64 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 15, 15], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00391/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 11, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 4
- channel total drift (end/start - 1): [-0.0, -0.6021, 0.6488, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 93: holes 0, rim-vs-core 0.58, rim-vs-outside 0.60, heterogeneity 0.17; core [0.981, 0.939, 0.047, 0.078] rim [0.765, 0.699, 0.226, 0.531]
  - track 11 at frame 87: holes 0, rim-vs-core 0.56, rim-vs-outside 0.60, heterogeneity 0.17; core [0.976, 0.925, 0.056, 0.073] rim [0.766, 0.707, 0.219, 0.515]
  - track 12 at frame 112: holes 0, rim-vs-core 0.56, rim-vs-outside 0.60, heterogeneity 0.16; core [0.974, 0.92, 0.051, 0.074] rim [0.764, 0.704, 0.209, 0.515]
  - track 13 at frame 112: holes 0, rim-vs-core 0.54, rim-vs-outside 0.63, heterogeneity 0.16; core [0.99, 0.964, 0.058, 0.077] rim [0.79, 0.723, 0.24, 0.474]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.866, rim/outside 28 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.835)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 11.6 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.816)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 20.1, rim/outside 0.645 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.489)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 3.84, rim/outside 16 (aggregate of 62 individuals; 56/62 membrane-like individually; rim level 0.494)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #6 (t=9300, R_eq 8.31): ['s']; #11 (t=8700, R_eq 8.63): ['s']; #12 (t=11200, R_eq 9.03): ['s']; #13 (t=11200, R_eq 7.29): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
