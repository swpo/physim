# Evidence pack: flow-lenia-digestion-ecology-dt (seed 22)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261028T0326-c62-flow-lenia-ecology-robustness/world_dt.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 50 steps x dt 0.1 (--dt; world META dt 0.2) = time 3000; grid [160, 160]; wall 1274s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0326-c62-flow-lenia-ecology-robustness/world_dt.py --out /tmp/claude-0/dt/dthalf/seed22 --seeds 22 --size 160 160 --frames 600 --spf 50 --dt 0.1 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0034, 1.9337], min area 6 px

## Measurements
- components: final 29, mean 31.3, max 41; occupancy final 0.13
- tracks: 5438; persistent (alive >= 50% of run): 0; longest 34 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 39, 28], H1 [5, 1, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 1.02/time; max body lengths 13.3
- replication (lineage window K = 20 frames = time 100, default): splits 1964, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1942, merge/split ratio 0.989, nucleations 73
- channel total drift (end/start - 1): [-0.2816, None, -0.0685, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1793 at frame 222: holes 0, rim-vs-core 0.54, rim-vs-outside 0.08, heterogeneity 0.09; core [0.005, 0.629, 0.931, 0.066] rim [0.006, 0.09, 0.93, 0.04]
  - track 3814 at frame 439: holes 0, rim-vs-core 0.53, rim-vs-outside 0.03, heterogeneity 0.08; core [0.003, 0.582, 0.938, 0.041] rim [0.004, 0.055, 0.936, 0.026]
  - track 2713 at frame 323: holes 0, rim-vs-core 0.43, rim-vs-outside 0.24, heterogeneity 0.09; core [0.005, 0.675, 0.922, 0.046] rim [0.006, 0.25, 0.918, 0.043]
  - track 3339 at frame 388: holes 0, rim-vs-core 0.55, rim-vs-outside 0.08, heterogeneity 0.09; core [0.004, 0.634, 0.913, 0.063] rim [0.006, 0.089, 0.909, 0.038]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 193 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 8.88 (aggregate of 193 individuals; 22/193 membrane-like individually; rim level 0.198)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 13 (aggregate of 193 individuals; 45/193 membrane-like individually; rim level 0.296)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 0.943 (aggregate of 193 individuals; 0/193 membrane-like individually; rim level 0.74)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.837, rim/outside 2.26 (aggregate of 193 individuals; 2/193 membrane-like individually; rim level 0.107)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1793 (t=1110, R_eq 4.07): none; #3814 (t=2195, R_eq 3.43): none; #2713 (t=1615, R_eq 4.3): none; #3339 (t=1940, R_eq 4.3): none
- species `prey` (channels ['prey A'], own threshold): components final 17, mean 14.6, max 28; tracks 864, persistent 0; splits 309, persistent splits 5 (K=20), max generation 4, merges 174, merge/split 0.563; moving tracks 137
- species `predator` (channels ['predator B'], own threshold): components final 28, mean 26.8, max 33; tracks 1790, persistent 0; splits 519, persistent splits 15 (K=20), max generation 3, merges 328, merge/split 0.632; moving tracks 217

## Warnings
- --dt 0.1 only relabels time (world META dt 0.2): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 1 of 193 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
