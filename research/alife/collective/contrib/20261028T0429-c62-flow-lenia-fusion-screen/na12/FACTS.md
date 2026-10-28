# Evidence pack: flow-lenia-digestion-ecology-thetaB (seed 1)

- world: `../world_th.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 607s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fus/world_th.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fus/na12 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0023, 1.9561], min area 6 px

## Measurements
- components: final 16, mean 19.0, max 69; occupancy final 0.10
- tracks: 1566; persistent (alive >= 50% of run): 0; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.20, final 2; holes at thresholds 0.2/0.35/0.5 final [3, 7, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 18, 17], H1 [14, 4, 2]
- motion: 76 long-lived tracks moved >= 1 body length; max speed 0.975/time; max body lengths 20.8
- replication (lineage window K = 20 frames = time 100, default): splits 480, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 500, merge/split ratio 1.04, nucleations 154
- channel total drift (end/start - 1): [-0.2286, None, -0.0574, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 706 at frame 237: holes 0, rim-vs-core 0.54, rim-vs-outside 0.21, heterogeneity 0.08; core [0.001, 0.761, 0.973, 0.028] rim [0.001, 0.218, 0.972, 0.021]
  - track 598 at frame 197: holes 0, rim-vs-core 0.37, rim-vs-outside 0.12, heterogeneity 0.08; core [0.003, 0.501, 0.959, 0.054] rim [0.004, 0.128, 0.955, 0.035]
  - track 1454 at frame 570: holes 0, rim-vs-core 0.46, rim-vs-outside 0.05, heterogeneity 0.09; core [0.002, 0.516, 0.963, 0.028] rim [0.002, 0.06, 0.962, 0.018]
  - track 361 at frame 106: holes 0, rim-vs-core 0.38, rim-vs-outside 0.14, heterogeneity 0.08; core [0.002, 0.528, 0.936, 0.047] rim [0.003, 0.147, 0.928, 0.031]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 99 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 15 (aggregate of 99 individuals; 26/99 membrane-like individually; rim level 0.296)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.36, rim/outside 10.4 (aggregate of 99 individuals; 31/99 membrane-like individually; rim level 0.23)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.61, rim/outside 0.894 (aggregate of 99 individuals; 0/99 membrane-like individually; rim level 0.714)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.729, rim/outside 4.43 (aggregate of 99 individuals; 3/99 membrane-like individually; rim level 0.109)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #706 (t=1185, R_eq 6.28, ring): ['predator B']; #598 (t=985, R_eq 5.7): ['predator B']; #1454 (t=2850, R_eq 4.51): ['predator B']; #361 (t=530, R_eq 5.11): none
- species `prey` (channels ['prey A'], own threshold): components final 10, mean 12.9, max 41; tracks 630, persistent 0; splits 204, persistent splits 2 (K=20), max generation 1, merges 176, merge/split 0.863; moving tracks 132
- species `predator` (channels ['predator B'], own threshold): components final 8, mean 9.1, max 15; tracks 898, persistent 5; splits 309, persistent splits 0 (K=20), max generation 0, merges 297, merge/split 0.961; moving tracks 20

## Warnings
- radial: 5 of 99 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
