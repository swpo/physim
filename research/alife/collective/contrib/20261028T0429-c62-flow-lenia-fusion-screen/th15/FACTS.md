# Evidence pack: flow-lenia-digestion-ecology-thetaB (seed 1)

- world: `../world_th.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 609s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fus/world_th.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fus/th15 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.002, 1.9733], min area 6 px

## Measurements
- components: final 19, mean 26.1, max 94; occupancy final 0.12
- tracks: 2623; persistent (alive >= 50% of run): 0; longest 95 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.12, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 12, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 20, 12], H1 [8, 0, 0]
- motion: 56 long-lived tracks moved >= 1 body length; max speed 0.948/time; max body lengths 15.1
- replication (lineage window K = 20 frames = time 100, default): splits 845, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 862, merge/split ratio 1.02, nucleations 207
- channel total drift (end/start - 1): [-0.2667, None, -0.069, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1380 at frame 348: holes 0, rim-vs-core 0.53, rim-vs-outside 0.07, heterogeneity 0.09; core [0.008, 0.603, 0.906, 0.064] rim [0.01, 0.076, 0.904, 0.04]
  - track 588 at frame 121: holes 0, rim-vs-core 0.53, rim-vs-outside 0.05, heterogeneity 0.09; core [0.008, 0.578, 0.901, 0.061] rim [0.01, 0.048, 0.899, 0.038]
  - track 864 at frame 187: holes 0, rim-vs-core 0.53, rim-vs-outside 0.11, heterogeneity 0.09; core [0.003, 0.643, 0.929, 0.044] rim [0.005, 0.109, 0.925, 0.028]
  - track 2055 at frame 499: holes 0, rim-vs-core 0.43, rim-vs-outside 0.12, heterogeneity 0.08; core [0.006, 0.546, 0.917, 0.067] rim [0.008, 0.117, 0.908, 0.043]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 139 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 8 (aggregate of 139 individuals; 26/139 membrane-like individually; rim level 0.197)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 13.1 (aggregate of 139 individuals; 24/139 membrane-like individually; rim level 0.286)
  - radial food: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.32, rim/outside 0.946 (aggregate of 139 individuals; 0/139 membrane-like individually; rim level 0.75)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.773, rim/outside 3.65 (aggregate of 139 individuals; 1/139 membrane-like individually; rim level 0.106)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1380 (t=1740, R_eq 3.52): none; #588 (t=605, R_eq 3.61): none; #864 (t=935, R_eq 4.3): none; #2055 (t=2495, R_eq 5.53): ['predator B']
- species `prey` (channels ['prey A'], own threshold): components final 12, mean 13.8, max 52; tracks 718, persistent 0; splits 222, persistent splits 5 (K=20), max generation 4, merges 186, merge/split 0.838; moving tracks 136
- species `predator` (channels ['predator B'], own threshold): components final 13, mean 17.8, max 23; tracks 601, persistent 2; splits 197, persistent splits 12 (K=20), max generation 5, merges 190, merge/split 0.964; moving tracks 76

## Warnings
- radial: 4 of 139 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
