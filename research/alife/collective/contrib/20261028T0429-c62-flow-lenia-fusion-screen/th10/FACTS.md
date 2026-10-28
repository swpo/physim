# Evidence pack: flow-lenia-digestion-ecology-thetaB (seed 1)

- world: `../world_th.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 612s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fus/world_th.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fus/th10 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0021, 1.8289], min area 6 px

## Measurements
- components: final 24, mean 24.8, max 94; occupancy final 0.14
- tracks: 2287; persistent (alive >= 50% of run): 0; longest 88 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 18, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 29, 23], H1 [17, 8, 1]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.942/time; max body lengths 13.5
- replication (lineage window K = 20 frames = time 100, default): splits 728, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 733, merge/split ratio 1.01, nucleations 213
- channel total drift (end/start - 1): [-0.2141, None, -0.071, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 951 at frame 237: holes 0, rim-vs-core 0.53, rim-vs-outside 0.09, heterogeneity 0.09; core [0.007, 0.627, 0.91, 0.065] rim [0.009, 0.093, 0.906, 0.04]
  - track 1239 at frame 313: holes 0, rim-vs-core 0.35, rim-vs-outside 0.31, heterogeneity 0.08; core [0.004, 0.664, 0.904, 0.071] rim [0.007, 0.315, 0.891, 0.05]
  - track 2081 at frame 565: holes 0, rim-vs-core 0.41, rim-vs-outside 0.28, heterogeneity 0.08; core [0.002, 0.694, 0.963, 0.036] rim [0.003, 0.284, 0.959, 0.025]
  - track 1024 at frame 252: holes 0, rim-vs-core 0.36, rim-vs-outside 0.29, heterogeneity 0.08; core [0.003, 0.658, 0.929, 0.057] rim [0.006, 0.295, 0.919, 0.039]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 135 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.907, rim/outside 6.71 (aggregate of 135 individuals; 25/135 membrane-like individually; rim level 0.188)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.19, rim/outside 14.3 (aggregate of 135 individuals; 46/135 membrane-like individually; rim level 0.376)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 0.941 (aggregate of 135 individuals; 0/135 membrane-like individually; rim level 0.741)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.77, rim/outside 3.87 (aggregate of 135 individuals; 1/135 membrane-like individually; rim level 0.117)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #951 (t=1185, R_eq 4.41): none; #1239 (t=1565, R_eq 7.07): none; #2081 (t=2825, R_eq 6.31): ['predator B']; #1024 (t=1260, R_eq 6.28): ['predator B']
- species `prey` (channels ['prey A'], own threshold): components final 13, mean 14.0, max 52; tracks 811, persistent 0; splits 256, persistent splits 6 (K=20), max generation 4, merges 218, merge/split 0.852; moving tracks 124
- species `predator` (channels ['predator B'], own threshold): components final 12, mean 14.8, max 21; tracks 51, persistent 14; splits 0, persistent splits 0 (K=20), max generation 0, merges 11, merge/split n/a; moving tracks 18

## Warnings
- radial: 1 of 135 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
