# Evidence pack: cips-fuel-turnover (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1100-c40-cips-layered-divide-claim; mutation: c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 1023s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/1b1a770d-5b2c-5e4e-abc5-f6c6c2737e43/scratchpad/fpd/world.py --out /tmp/claude-0/-home-user-physim/1b1a770d-5b2c-5e4e-abc5-f6c6c2737e43/scratchpad/fpd/pack_const/seed0 --seeds 0 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0213, 0.9747], min area 6 px

## Measurements
- components: final 16, mean 11.8, max 16; occupancy final 0.09
- tracks: 25; persistent (alive >= 50% of run): 10; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.11 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00344/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 9, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [0.0, 0.6273, -0.0988, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 62: holes 0, rim-vs-core 0.60, rim-vs-outside 0.58, heterogeneity 0.17; core [0.976, 0.923, 0.054, 0.082] rim [0.753, 0.688, 0.234, 0.549]
  - track 8 at frame 78: holes 0, rim-vs-core 0.61, rim-vs-outside 0.62, heterogeneity 0.17; core [0.985, 0.946, 0.061, 0.081] rim [0.756, 0.689, 0.249, 0.548]
  - track 9 at frame 78: holes 0, rim-vs-core 0.56, rim-vs-outside 0.60, heterogeneity 0.16; core [0.978, 0.926, 0.059, 0.074] rim [0.765, 0.698, 0.231, 0.51]
  - track 19 at frame 101: holes 0, rim-vs-core 0.57, rim-vs-outside 0.62, heterogeneity 0.17; core [0.988, 0.953, 0.063, 0.079] rim [0.772, 0.703, 0.248, 0.508]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 40.6 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.888)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.881, rim/outside 13.9 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.847)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 26.8, rim/outside 0.652 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.491)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.37, rim/outside 20.7 (aggregate of 77 individuals; 73/77 membrane-like individually; rim level 0.485)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #0 (t=6200, R_eq 8.74): ['s']; #8 (t=7800, R_eq 8.02): ['s']; #9 (t=7800, R_eq 8.74): ['s']; #19 (t=10100, R_eq 7.78): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
