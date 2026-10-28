# Evidence pack: flow-lenia-digestion-ecology-dt (seed 1)

- world: `../../world_dt.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 50 steps x dt 0.2 = time 6000; grid [160, 160]; wall 1224s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim2/world_dt.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim2/dthalf/seed1 --seeds 1 --size 160 160 --frames 600 --spf 50 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0037, 1.9296], min area 6 px

## Measurements
- components: final 30, mean 28.7, max 38; occupancy final 0.12
- tracks: 4549; persistent (alive >= 50% of run): 0; longest 50 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 36, 29], H1 [4, 0, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.526/time; max body lengths 14.1
- replication (lineage window K = 20 frames = time 200, default): splits 1657, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1630, merge/split ratio 0.984, nucleations 21
- channel total drift (end/start - 1): [-0.3386, None, -0.0615, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 549 at frame 116: holes 0, rim-vs-core 0.43, rim-vs-outside 0.09, heterogeneity 0.09; core [0.003, 0.532, 0.896, 0.042] rim [0.004, 0.103, 0.889, 0.027]
  - track 507 at frame 111: holes 0, rim-vs-core 0.53, rim-vs-outside 0.04, heterogeneity 0.08; core [0.004, 0.58, 0.935, 0.044] rim [0.005, 0.048, 0.935, 0.027]
  - track 1345 at frame 212: holes 0, rim-vs-core 0.39, rim-vs-outside 0.19, heterogeneity 0.09; core [0.004, 0.593, 0.922, 0.071] rim [0.005, 0.202, 0.922, 0.048]
  - track 421 at frame 91: holes 0, rim-vs-core 0.56, rim-vs-outside 0.05, heterogeneity 0.09; core [0.006, 0.626, 0.923, 0.076] rim [0.007, 0.066, 0.921, 0.046]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 179 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 8.79 (aggregate of 179 individuals; 35/179 membrane-like individually; rim level 0.21)
  - radial predator B: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 12.2 (aggregate of 179 individuals; 35/179 membrane-like individually; rim level 0.294)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.29, rim/outside 0.949 (aggregate of 179 individuals; 0/179 membrane-like individually; rim level 0.75)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.755, rim/outside 2.54 (aggregate of 179 individuals; 1/179 membrane-like individually; rim level 0.0967)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #549 (t=1160, R_eq 4.62): none; #507 (t=1110, R_eq 3.34): none; #1345 (t=2120, R_eq 6.82): none; #421 (t=910, R_eq 3.78): none
- species `prey` (channels ['prey A'], own threshold): components final 14, mean 14.0, max 21; tracks 853, persistent 0; splits 314, persistent splits 7 (K=20), max generation 4, merges 175, merge/split 0.557; moving tracks 126
- species `predator` (channels ['predator B'], own threshold): components final 25, mean 24.7, max 32; tracks 1665, persistent 0; splits 504, persistent splits 17 (K=20), max generation 4, merges 342, merge/split 0.679; moving tracks 182

## Warnings
- radial: 3 of 179 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
