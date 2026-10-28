# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../c62work/world_fleco.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 401 frames x 25 steps x dt 0.2 = time 2000; grid [160, 160]; wall 417s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/c62work/world_fleco.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fl5/noise1 --seeds 1 --size 160 160 --frames 400 --no-movie`
- segmentation: matter > 0.05 of robust range [0.0015, 2.7888], min area 6 px

## Measurements
- components: final 31, mean 28.8, max 89; occupancy final 0.41
- tracks: 7325; persistent (alive >= 50% of run): 0; longest 15 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.68, final 4; holes at thresholds 0.2/0.35/0.5 final [33, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [97, 57, 25], H1 [38, 5, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 4.3
- replication (lineage window K = 20 frames = time 100, default): splits 2858, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2863, merge/split ratio 1, nucleations 94
- channel total drift (end/start - 1): [-0.1675, None, -0.1771, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5516 at frame 303: holes 0, rim-vs-core 0.34, rim-vs-outside 0.16, heterogeneity 0.08; core [0.008, 0.497, 0.855, 0.032] rim [0.011, 0.162, 0.842, 0.021]
  - track 1185 at frame 67: holes 0, rim-vs-core 0.42, rim-vs-outside 0.12, heterogeneity 0.08; core [0.01, 0.541, 0.848, 0.043] rim [0.012, 0.121, 0.837, 0.028]
  - track 4561 at frame 249: holes 0, rim-vs-core 0.48, rim-vs-outside 0.07, heterogeneity 0.10; core [0.498, 0.001, 0.394, 0.002] rim [0.046, 0.003, 0.547, 0.002]
  - track 4589 at frame 249: holes 0, rim-vs-core 0.44, rim-vs-outside 0.07, heterogeneity 0.08; core [0.006, 0.502, 0.875, 0.027] rim [0.009, 0.067, 0.86, 0.018]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 158 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial prey A: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.852, rim/outside 3.13 (aggregate of 158 individuals; 33/158 membrane-like individually; rim level 0.172)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 3.82 (aggregate of 158 individuals; 24/158 membrane-like individually; rim level 0.189)
  - radial food: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.31, rim/outside 0.981 (aggregate of 158 individuals; 0/158 membrane-like individually; rim level 0.65)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.536, rim/outside 1.83 (aggregate of 158 individuals; 10/158 membrane-like individually; rim level 0.0808)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5516 (t=1515, R_eq 7.07): ['predator B']; #1185 (t=335, R_eq 4.92): none; #4561 (t=1245, R_eq 4.41): none; #4589 (t=1245, R_eq 4.92): none
- species `prey` (channels ['prey A'], own threshold): components final 36, mean 38.8, max 84; tracks 4018, persistent 0; splits 1184, persistent splits 0 (K=20), max generation 0, merges 1166, merge/split 0.985; moving tracks 35
- species `predator` (channels ['predator B'], own threshold): components final 63, mean 55.8, max 85; tracks 8003, persistent 0; splits 1942, persistent splits 0 (K=20), max generation 0, merges 2412, merge/split 1.24; moving tracks 27

## Warnings
- radial: 9 of 158 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
