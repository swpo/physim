# Evidence pack: active-nematic-marangoni-ladder (seed 100)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 848s; status ok
- command: `python -m labkit.run /tmp/claude-0/ld/world.py --out /tmp/claude-0/ld/runs/twin/seed100 --seeds 100 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8284, 0.5769], min area 6 px

## Measurements
- components: final 18, mean 20.8, max 28; occupancy final 0.06
- tracks: 279; persistent (alive >= 50% of run): 0; longest 140 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 18, 17], H1 [1, 0, 0]
- motion: 134 long-lived tracks moved >= 1 body length; max speed 0.389/time; max body lengths 11.3
- replication (lineage window K = 20 frames = time 100, default): splits 123, persistent splits 51 (0 more failed only because the siblings re-merged within K), max generation 7, merges 19, merge/split ratio 0.154, nucleations 14
- channel total drift (end/start - 1): [-0.5173, -0.5967, -0.189, 3.6709, 6.3605]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 174 at frame 319: holes 0, rim-vs-core 0.63, rim-vs-outside 0.40, heterogeneity 0.13; core [0.966, 0.918, 0.018, 0.359, 0.014] rim [0.771, 0.587, 0.06, 0.859, 0.04]
  - track 101 at frame 195: holes 0, rim-vs-core 0.48, rim-vs-outside 0.31, heterogeneity 0.10; core [0.917, 0.603, 0.541, 0.0, 0.03] rim [0.739, 0.434, 0.947, 0.001, 0.06]
  - track 150 at frame 269: holes 0, rim-vs-core 0.58, rim-vs-outside 0.37, heterogeneity 0.12; core [0.947, 0.855, 0.018, 0.001, 0.415] rim [0.757, 0.55, 0.047, 0.002, 0.866]
  - track 258 at frame 387: holes 0, rim-vs-core 0.41, rim-vs-outside 0.47, heterogeneity 0.11; core [0.93, 0.902, 0.004, 0.423, 0.01] rim [0.766, 0.681, 0.009, 0.732, 0.022]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 126 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 4.03 (aggregate of 126 individuals; 0/126 membrane-like individually; rim level 0.673)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.772, rim/outside 7.26 (aggregate of 126 individuals; 10/126 membrane-like individually; rim level 0.514)
  - radial s0 (mar 20): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 2.67 (aggregate of 126 individuals; 34/126 membrane-like individually; rim level 0.14)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 2.82 (aggregate of 126 individuals; 24/126 membrane-like individually; rim level 0.154)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 3.1 (aggregate of 126 individuals; 42/126 membrane-like individually; rim level 0.39)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #174 (t=1595, R_eq 3.29): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #101 (t=975, R_eq 4.82): none; #150 (t=1345, R_eq 3.66): ['s0 (mar 20)', 's2 (mar 60)']; #258 (t=1935, R_eq 4.15): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 126 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
