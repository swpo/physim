# Evidence pack: flow-lenia-digestion-ecology-dt (seed 21)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261028T0326-c62-flow-lenia-ecology-robustness/world_dt.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 50 steps x dt 0.1 (--dt; world META dt 0.2) = time 3000; grid [160, 160]; wall 1292s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0326-c62-flow-lenia-ecology-robustness/world_dt.py --out /tmp/claude-0/dt/dthalf/seed21 --seeds 21 --size 160 160 --frames 600 --spf 50 --dt 0.1 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0036, 1.9359], min area 6 px

## Measurements
- components: final 32, mean 31.1, max 44; occupancy final 0.13
- tracks: 5305; persistent (alive >= 50% of run): 0; longest 46 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 7, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [54, 41, 36], H1 [17, 5, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.999/time; max body lengths 20.9
- replication (lineage window K = 20 frames = time 100, default): splits 1915, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1926, merge/split ratio 1.01, nucleations 64
- channel total drift (end/start - 1): [-0.3211, None, -0.0657, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1894 at frame 237: holes 0, rim-vs-core 0.56, rim-vs-outside 0.05, heterogeneity 0.10; core [0.008, 0.609, 0.81, 0.105] rim [0.009, 0.051, 0.812, 0.075]
  - track 3637 at frame 424: holes 0, rim-vs-core 0.51, rim-vs-outside 0.05, heterogeneity 0.09; core [0.007, 0.57, 0.696, 0.07] rim [0.008, 0.059, 0.703, 0.043]
  - track 1382 at frame 176: holes 0, rim-vs-core 0.21, rim-vs-outside 0.28, heterogeneity 0.09; core [0.005, 0.518, 0.921, 0.051] rim [0.005, 0.304, 0.921, 0.043]
  - track 3447 at frame 403: holes 0, rim-vs-core 0.52, rim-vs-outside 0.02, heterogeneity 0.08; core [0.004, 0.544, 0.918, 0.04] rim [0.005, 0.02, 0.915, 0.024]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 191 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.17, rim/outside 9.09 (aggregate of 191 individuals; 34/191 membrane-like individually; rim level 0.212)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.927, rim/outside 13.6 (aggregate of 191 individuals; 39/191 membrane-like individually; rim level 0.301)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.27, rim/outside 0.953 (aggregate of 191 individuals; 0/191 membrane-like individually; rim level 0.75)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.729, rim/outside 2.24 (aggregate of 191 individuals; 4/191 membrane-like individually; rim level 0.0907)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1894 (t=1185, R_eq 4.3): none; #3637 (t=2120, R_eq 4.82): none; #1382 (t=880, R_eq 3.78): none; #3447 (t=2015, R_eq 3.43): none
- species `prey` (channels ['prey A'], own threshold): components final 13, mean 14.3, max 26; tracks 803, persistent 0; splits 276, persistent splits 3 (K=20), max generation 2, merges 172, merge/split 0.623; moving tracks 139
- species `predator` (channels ['predator B'], own threshold): components final 29, mean 26.4, max 33; tracks 1878, persistent 0; splits 553, persistent splits 14 (K=20), max generation 4, merges 351, merge/split 0.635; moving tracks 203

## Warnings
- --dt 0.1 only relabels time (world META dt 0.2): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 4 of 191 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
