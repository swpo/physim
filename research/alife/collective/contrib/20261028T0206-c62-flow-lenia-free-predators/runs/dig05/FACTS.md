# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../c62work/world_fleco.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 401 frames x 25 steps x dt 0.2 = time 2000; grid [160, 160]; wall 419s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/c62work/world_fleco.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fl5/dig05 --seeds 1 --size 160 160 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0025, 2.1582], min area 6 px

## Measurements
- components: final 32, mean 27.4, max 37; occupancy final 0.15
- tracks: 2730; persistent (alive >= 50% of run): 0; longest 32 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [5, 11, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [53, 35, 31], H1 [18, 6, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.909/time; max body lengths 11.5
- replication (lineage window K = 20 frames = time 100, default): splits 951, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 938, merge/split ratio 0.986, nucleations 79
- channel total drift (end/start - 1): [-0.1074, None, -0.0759, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 752 at frame 138: holes 0, rim-vs-core 0.61, rim-vs-outside 0.04, heterogeneity 0.09; core [0.002, 0.652, 0.941, 0.043] rim [0.004, 0.045, 0.937, 0.027]
  - track 298 at frame 77: holes 0, rim-vs-core 0.51, rim-vs-outside 0.16, heterogeneity 0.10; core [0.618, 0.0, 0.321, 0.008] rim [0.143, 0.0, 0.499, 0.009]
  - track 309 at frame 77: holes 0, rim-vs-core 0.35, rim-vs-outside 0.10, heterogeneity 0.08; core [0.435, 0.0, 0.429, 0.003] rim [0.116, 0.0, 0.565, 0.003]
  - track 1695 at frame 262: holes 0, rim-vs-core 0.43, rim-vs-outside 0.10, heterogeneity 0.09; core [0.502, 0.0, 0.475, 0.007] rim [0.094, 0.001, 0.606, 0.007]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 187 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 7.91 (aggregate of 187 individuals; 21/187 membrane-like individually; rim level 0.216)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 10.4 (aggregate of 187 individuals; 44/187 membrane-like individually; rim level 0.264)
  - radial food: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.42, rim/outside 0.941 (aggregate of 187 individuals; 0/187 membrane-like individually; rim level 0.75)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.687, rim/outside 2.92 (aggregate of 187 individuals; 3/187 membrane-like individually; rim level 0.0919)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #752 (t=690, R_eq 4.11): none; #298 (t=385, R_eq 3.19): none; #309 (t=385, R_eq 3.29): none; #1695 (t=1310, R_eq 2.99): none
- species `prey` (channels ['prey A'], own threshold): components final 17, mean 15.9, max 22; tracks 696, persistent 0; splits 195, persistent splits 2 (K=20), max generation 1, merges 176, merge/split 0.903; moving tracks 105
- species `predator` (channels ['predator B'], own threshold): components final 23, mean 19.3, max 26; tracks 1286, persistent 0; splits 397, persistent splits 3 (K=20), max generation 2, merges 388, merge/split 0.977; moving tracks 92

## Warnings
- radial: 2 of 187 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
