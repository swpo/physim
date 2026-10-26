# Evidence pack: cips-fuel-turnover (seed 1)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1100-c40-cips-layered-divide-claim; mutation: c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 997s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/1b1a770d-5b2c-5e4e-abc5-f6c6c2737e43/scratchpad/fpd/world.py --out /tmp/claude-0/-home-user-physim/1b1a770d-5b2c-5e4e-abc5-f6c6c2737e43/scratchpad/fpd/pack_const/seed1 --seeds 1 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0208, 0.9754], min area 6 px

## Measurements
- components: final 16, mean 11.7, max 16; occupancy final 0.09
- tracks: 25; persistent (alive >= 50% of run): 12; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.92 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00306/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 9, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [0.0, 0.6245, -0.098, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 62: holes 0, rim-vs-core 0.53, rim-vs-outside 0.64, heterogeneity 0.16; core [0.989, 0.954, 0.056, 0.077] rim [0.789, 0.711, 0.233, 0.464]
  - track 9 at frame 77: holes 0, rim-vs-core 0.56, rim-vs-outside 0.62, heterogeneity 0.16; core [0.985, 0.945, 0.053, 0.08] rim [0.778, 0.702, 0.233, 0.496]
  - track 10 at frame 77: holes 0, rim-vs-core 0.43, rim-vs-outside 0.67, heterogeneity 0.16; core [0.968, 0.902, 0.059, 0.078] rim [0.809, 0.753, 0.18, 0.423]
  - track 19 at frame 100: holes 0, rim-vs-core 0.37, rim-vs-outside 0.76, heterogeneity 0.17; core [0.985, 0.948, 0.051, 0.084] rim [0.843, 0.783, 0.172, 0.364]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.893, rim/outside 35.1 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.872)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.873, rim/outside 12.8 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.835)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 23.2, rim/outside 0.654 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.486)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.39, rim/outside 18.8 (aggregate of 76 individuals; 71/76 membrane-like individually; rim level 0.504)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #5 (t=6200, R_eq 7.57): ['s']; #9 (t=7700, R_eq 7.96): ['s']; #10 (t=7700, R_eq 9.39): ['s']; #19 (t=10000, R_eq 8.12): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
