# Evidence pack: cips-fuel-turnover (seed 1)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1100-c40-cips-layered-divide-claim; mutation: c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 1040s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/1b1a770d-5b2c-5e4e-abc5-f6c6c2737e43/scratchpad/fpd/world.py --out /tmp/claude-0/-home-user-physim/1b1a770d-5b2c-5e4e-abc5-f6c6c2737e43/scratchpad/fpd/pack/seed1 --seeds 1 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0222, 0.9753], min area 6 px

## Measurements
- components: final 15, mean 10.6, max 15; occupancy final 0.08
- tracks: 23; persistent (alive >= 50% of run): 10; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.19 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00307/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 2000, default): splits 8, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [-0.0221, 0.5166, -0.0841, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.42, rim-vs-outside 0.69, heterogeneity 0.17; core [0.971, 0.909, 0.059, 0.077] rim [0.813, 0.757, 0.176, 0.421]
  - track 5 at frame 62: holes 0, rim-vs-core 0.58, rim-vs-outside 0.62, heterogeneity 0.17; core [0.987, 0.949, 0.05, 0.08] rim [0.771, 0.7, 0.235, 0.517]
  - track 7 at frame 78: holes 0, rim-vs-core 0.57, rim-vs-outside 0.61, heterogeneity 0.16; core [0.982, 0.937, 0.044, 0.079] rim [0.774, 0.7, 0.225, 0.517]
  - track 17 at frame 104: holes 0, rim-vs-core 0.35, rim-vs-outside 0.78, heterogeneity 0.16; core [0.985, 0.945, 0.05, 0.082] rim [0.854, 0.794, 0.159, 0.351]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.898, rim/outside 33.9 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.871)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 12.7 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.837)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 22.8, rim/outside 0.644 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.489)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.2, rim/outside 19.4 (aggregate of 67 individuals; 61/67 membrane-like individually; rim level 0.517)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #0 (t=6100, R_eq 8.69): ['s']; #5 (t=6200, R_eq 7.65): ['s']; #7 (t=7800, R_eq 8.14): ['s']; #17 (t=10400, R_eq 7.8): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
