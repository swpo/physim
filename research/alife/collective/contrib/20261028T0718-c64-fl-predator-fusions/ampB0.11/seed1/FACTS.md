# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 655s; status ok
- command: `python -m labkit.run /tmp/claude-0/pd/world.py --out /tmp/claude-0/pd/b0.11/seed1 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0018, 1.9457], min area 6 px

## Measurements
- components: final 25, mean 23.3, max 58; occupancy final 0.11
- tracks: 2352; persistent (alive >= 50% of run): 0; longest 158 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.24, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 9, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 26, 24], H1 [12, 5, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 0.951/time; max body lengths 15.1
- replication (lineage window K = 20 frames = time 100, default): splits 755, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 757, merge/split ratio 1, nucleations 203
- channel total drift (end/start - 1): [-0.1955, None, -0.0724, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1133 at frame 348: holes 0, rim-vs-core 0.47, rim-vs-outside 0.05, heterogeneity 0.10; core [0.001, 0.532, 0.868, 0.027] rim [0.002, 0.06, 0.845, 0.019]
  - track 407 at frame 141: holes 0, rim-vs-core 0.41, rim-vs-outside 0.11, heterogeneity 0.08; core [0.002, 0.53, 0.956, 0.044] rim [0.003, 0.124, 0.951, 0.028]
  - track 1218 at frame 343: holes 0, rim-vs-core 0.41, rim-vs-outside 0.21, heterogeneity 0.10; core [0.007, 0.62, 0.914, 0.097] rim [0.008, 0.207, 0.915, 0.067]
  - track 2164 at frame 580: holes 0, rim-vs-core 0.54, rim-vs-outside 0.04, heterogeneity 0.09; core [0.005, 0.581, 0.92, 0.075] rim [0.007, 0.043, 0.917, 0.044]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 132 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 13.2 (aggregate of 132 individuals; 25/132 membrane-like individually; rim level 0.282)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.25, rim/outside 11.1 (aggregate of 132 individuals; 32/132 membrane-like individually; rim level 0.226)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.62, rim/outside 0.91 (aggregate of 132 individuals; 0/132 membrane-like individually; rim level 0.725)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 3.83 (aggregate of 132 individuals; 0/132 membrane-like individually; rim level 0.103)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1133 (t=1740, R_eq 4.72): ['predator B']; #407 (t=705, R_eq 5.08): ['predator B']; #1218 (t=1715, R_eq 3.57): none; #2164 (t=2900, R_eq 4.03): none
- species `prey` (channels ['prey A'], own threshold): components final 15, mean 15.9, max 52; tracks 990, persistent 0; splits 322, persistent splits 0 (K=20), max generation 0, merges 294, merge/split 0.913; moving tracks 146
- species `predator` (channels ['predator B'], own threshold): components final 15, mean 10.8, max 15; tracks 422, persistent 7; splits 138, persistent splits 4 (K=20), max generation 2, merges 127, merge/split 0.92; moving tracks 25

## Warnings
- radial: 6 of 132 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
