# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 820s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim/world.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim/pack/seed1 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0027, 2.1397], min area 6 px

## Measurements
- components: final 26, mean 27.8, max 37; occupancy final 0.12
- tracks: 3617; persistent (alive >= 50% of run): 0; longest 54 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 5, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [45, 32, 16], H1 [8, 2, 0]
- motion: 66 long-lived tracks moved >= 1 body length; max speed 0.9/time; max body lengths 22.8
- replication (lineage window K = 20 frames = time 100, default): splits 1255, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1219, merge/split ratio 0.971, nucleations 60
- channel total drift (end/start - 1): [-0.3222, None, -0.062, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3032 at frame 529: holes 0, rim-vs-core 0.49, rim-vs-outside 0.10, heterogeneity 0.09; core [0.004, 0.591, 0.936, 0.049] rim [0.005, 0.106, 0.933, 0.03]
  - track 1937 at frame 343: holes 0, rim-vs-core 0.52, rim-vs-outside 0.09, heterogeneity 0.08; core [0.002, 0.622, 0.962, 0.031] rim [0.003, 0.1, 0.96, 0.019]
  - track 2864 at frame 499: holes 0, rim-vs-core 0.52, rim-vs-outside 0.06, heterogeneity 0.08; core [0.006, 0.577, 0.91, 0.051] rim [0.008, 0.057, 0.907, 0.031]
  - track 413 at frame 101: holes 0, rim-vs-core 0.59, rim-vs-outside 0.10, heterogeneity 0.15; core [0.606, 0.001, 0.284, 0.005] rim [0.061, 0.008, 0.513, 0.004]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 166 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 7.27 (aggregate of 166 individuals; 24/166 membrane-like individually; rim level 0.168)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 14.9 (aggregate of 166 individuals; 46/166 membrane-like individually; rim level 0.318)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.26, rim/outside 0.953 (aggregate of 166 individuals; 0/166 membrane-like individually; rim level 0.775)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.761, rim/outside 3.06 (aggregate of 166 individuals; 2/166 membrane-like individually; rim level 0.0994)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3032 (t=2645, R_eq 3.99): none; #1937 (t=1715, R_eq 4.07): none; #2864 (t=2495, R_eq 3.19): none; #413 (t=505, R_eq 4.95): none
- species `prey` (channels ['prey A'], own threshold): components final 12, mean 12.5, max 19; tracks 755, persistent 0; splits 255, persistent splits 4 (K=20), max generation 3, merges 217, merge/split 0.851; moving tracks 121
- species `predator` (channels ['predator B'], own threshold): components final 24, mean 22.9, max 31; tracks 1740, persistent 0; splits 603, persistent splits 9 (K=20), max generation 5, merges 475, merge/split 0.788; moving tracks 192

## Warnings
- radial: 2 of 166 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
