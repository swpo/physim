# Evidence pack: flow-lenia-digestion-ecology-thetaB (seed 1)

- world: `../world_th.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 606s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fus/world_th.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fus/th13 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0021, 1.8846], min area 6 px

## Measurements
- components: final 20, mean 24.5, max 94; occupancy final 0.13
- tracks: 2493; persistent (alive >= 50% of run): 0; longest 90 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 17, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 22, 19], H1 [17, 2, 0]
- motion: 32 long-lived tracks moved >= 1 body length; max speed 0.941/time; max body lengths 12.7
- replication (lineage window K = 20 frames = time 100, default): splits 793, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 773, merge/split ratio 0.975, nucleations 245
- channel total drift (end/start - 1): [-0.2156, None, -0.0704, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1919 at frame 479: holes 0, rim-vs-core 0.40, rim-vs-outside 0.14, heterogeneity 0.08; core [0.002, 0.548, 0.954, 0.034] rim [0.003, 0.146, 0.95, 0.022]
  - track 38 at frame 50: holes 0, rim-vs-core 0.57, rim-vs-outside 0.15, heterogeneity 0.12; core [0.598, 0.0, 0.181, 0.004] rim [0.089, 0.003, 0.43, 0.003]
  - track 1811 at frame 449: holes 0, rim-vs-core 0.50, rim-vs-outside 0.12, heterogeneity 0.08; core [0.003, 0.628, 0.942, 0.042] rim [0.004, 0.126, 0.938, 0.027]
  - track 2164 at frame 534: holes 0, rim-vs-core 0.41, rim-vs-outside 0.15, heterogeneity 0.08; core [0.003, 0.558, 0.937, 0.053] rim [0.005, 0.146, 0.931, 0.034]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 133 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 8.22 (aggregate of 133 individuals; 24/133 membrane-like individually; rim level 0.238)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.13, rim/outside 11 (aggregate of 133 individuals; 37/133 membrane-like individually; rim level 0.287)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.4, rim/outside 0.935 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.738)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.71, rim/outside 3.31 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.0992)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1919 (t=2395, R_eq 5.89): ['predator B']; #38 (t=250, R_eq 3.91): none; #1811 (t=2245, R_eq 4.37): none; #2164 (t=2670, R_eq 5.86): ['predator B']
- species `prey` (channels ['prey A'], own threshold): components final 14, mean 14.8, max 52; tracks 809, persistent 0; splits 251, persistent splits 4 (K=20), max generation 2, merges 230, merge/split 0.916; moving tracks 139
- species `predator` (channels ['predator B'], own threshold): components final 13, mean 13.1, max 22; tracks 81, persistent 11; splits 14, persistent splits 2 (K=20), max generation 1, merges 22, merge/split 1.57; moving tracks 20

## Warnings
- radial: 2 of 133 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
