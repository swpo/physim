# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../c62work/world_fleco.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 401 frames x 25 steps x dt 0.2 = time 2000; grid [160, 160]; wall 412s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/c62work/world_fleco.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fl4/lk1 --seeds 1 --size 160 160 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0021, 2.1758], min area 6 px

## Measurements
- components: final 32, mean 28.6, max 38; occupancy final 0.14
- tracks: 2879; persistent (alive >= 50% of run): 0; longest 49 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.17, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 5, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [55, 39, 28], H1 [13, 1, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.882/time; max body lengths 9.7
- replication (lineage window K = 20 frames = time 100, default): splits 1035, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 969, merge/split ratio 0.936, nucleations 80
- channel total drift (end/start - 1): [-0.0688, None, -0.0776, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1175 at frame 198: holes 0, rim-vs-core 0.50, rim-vs-outside 0.09, heterogeneity 0.09; core [0.002, 0.594, 0.923, 0.026] rim [0.003, 0.095, 0.92, 0.016]
  - track 872 at frame 158: holes 0, rim-vs-core 0.39, rim-vs-outside 0.08, heterogeneity 0.09; core [0.001, 0.491, 0.884, 0.011] rim [0.001, 0.101, 0.877, 0.007]
  - track 2631 at frame 387: holes 0, rim-vs-core 0.49, rim-vs-outside 0.04, heterogeneity 0.09; core [0.001, 0.538, 0.955, 0.012] rim [0.001, 0.05, 0.95, 0.007]
  - track 125 at frame 50: holes 0, rim-vs-core 0.69, rim-vs-outside 0.18, heterogeneity 0.12; core [0.782, 0.0, 0.227, 0.007] rim [0.131, 0.001, 0.443, 0.008]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 176 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 8.36 (aggregate of 176 individuals; 22/176 membrane-like individually; rim level 0.197)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.951, rim/outside 10.9 (aggregate of 176 individuals; 43/176 membrane-like individually; rim level 0.253)
  - radial food: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.35, rim/outside 0.938 (aggregate of 176 individuals; 0/176 membrane-like individually; rim level 0.75)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.77, rim/outside 2.71 (aggregate of 176 individuals; 2/176 membrane-like individually; rim level 0.0688)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1175 (t=990, R_eq 4.07): none; #872 (t=790, R_eq 4.69): none; #2631 (t=1935, R_eq 4.98): ['predator B']; #125 (t=250, R_eq 3.39): none
- species `prey` (channels ['prey A'], own threshold): components final 20, mean 16.0, max 21; tracks 759, persistent 0; splits 259, persistent splits 0 (K=20), max generation 0, merges 212, merge/split 0.819; moving tracks 94
- species `predator` (channels ['predator B'], own threshold): components final 25, mean 22.0, max 28; tracks 1061, persistent 0; splits 364, persistent splits 8 (K=20), max generation 3, merges 303, merge/split 0.832; moving tracks 128

## Warnings
- radial: 2 of 176 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
