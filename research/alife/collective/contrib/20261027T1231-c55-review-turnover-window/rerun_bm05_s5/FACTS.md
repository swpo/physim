# Evidence pack: cips-gene (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T2334-c48-cips-turnover-window/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1100-c40-cips-layered-divide-claim; mutation: c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 832s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261026T2334-c48-cips-turnover-window/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/turn/pack_bm05 --seeds 5 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0206, 0.9764], min area 6 px

## Measurements
- components: final 11, mean 8.0, max 11; occupancy final 0.08
- tracks: 16; persistent (alive >= 50% of run): 9; longest 98 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00274/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 2000, default): splits 5, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [0.0062, 0.5064, -0.0826, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 52: holes 0, rim-vs-core 0.56, rim-vs-outside 1.17, heterogeneity 0.11; core [0.985, 0.953, 0.043, 0.087, 0.999, 0.0] rim [0.778, 0.706, 0.23, 0.502, 0.999, 0.0]
  - track 5 at frame 53: holes 0, rim-vs-core 0.57, rim-vs-outside 1.15, heterogeneity 0.11; core [0.983, 0.947, 0.063, 0.078, 1.0, 0.0] rim [0.771, 0.707, 0.238, 0.51, 0.999, 0.0]
  - track 2 at frame 41: holes 0, rim-vs-core 0.33, rim-vs-outside 1.32, heterogeneity 0.10; core [0.986, 0.907, 0.001, 0.067, 0.0, 1.0] rim [0.855, 0.758, 0.081, 0.316, 0.0, 0.999]
  - track 6 at frame 69: holes 0, rim-vs-core 0.53, rim-vs-outside 1.15, heterogeneity 0.11; core [0.988, 0.958, 0.059, 0.079, 1.0, 0.0] rim [0.79, 0.721, 0.239, 0.474, 0.999, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 51 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.866, rim/outside 24.2 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.833)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 11.3 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.808)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 17.7, rim/outside 0.674 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.51)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.24, rim/outside 17.9 (aggregate of 51 individuals; 42/51 membrane-like individually; rim level 0.541)  MEMBRANE-LIKE
  - radial g1: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.927, rim/outside 54 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.778)
  - radial g2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.559, rim/outside 4.36 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.074)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #4 (t=5200, R_eq 8.08): ['s']; #5 (t=5300, R_eq 7.72): ['s']; #2 (t=4100, R_eq 14.65): none; #6 (t=6900, R_eq 7.53): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
