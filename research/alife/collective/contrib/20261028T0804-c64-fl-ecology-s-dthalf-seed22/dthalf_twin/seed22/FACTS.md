# Evidence pack: flow-lenia-digestion-ecology-dt (seed 22)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261028T0326-c62-flow-lenia-ecology-robustness/world_dt.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 50 steps x dt 0.1 (--dt; world META dt 0.2) = time 3000; grid [160, 160]; wall 657s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0326-c62-flow-lenia-ecology-robustness/world_dt.py --out /tmp/claude-0/dt/dthalf_twin/seed22 --seeds 22 --size 160 160 --frames 600 --spf 50 --dt 0.1 --no-movie`
- segmentation: matter > 0.09 of robust range [0.0011, 1.6825], min area 6 px

## Measurements
- components: final 23, mean 19.7, max 29; occupancy final 0.08
- tracks: 2642; persistent (alive >= 50% of run): 0; longest 40 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 23, 23], H1 [4, 1, 0]
- motion: 50 long-lived tracks moved >= 1 body length; max speed 1.15/time; max body lengths 21.7
- replication (lineage window K = 20 frames = time 100, default): splits 924, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 917, merge/split ratio 0.992, nucleations 30
- channel total drift (end/start - 1): [0.0, None, -0.0919, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1327 at frame 333: holes 0, rim-vs-core 0.55, rim-vs-outside 0.11, heterogeneity 0.14; core [0.585, 0.0, 0.29, 0.0] rim [0.081, 0.0, 0.507, 0.0]
  - track 1294 at frame 318: holes 0, rim-vs-core 0.54, rim-vs-outside 0.13, heterogeneity 0.14; core [0.573, 0.0, 0.256, 0.0] rim [0.091, 0.0, 0.499, 0.0]
  - track 2448 at frame 570: holes 0, rim-vs-core 0.57, rim-vs-outside 0.11, heterogeneity 0.15; core [0.608, 0.0, 0.342, 0.0] rim [0.078, 0.0, 0.566, 0.0]
  - track 1872 at frame 444: holes 0, rim-vs-core 0.56, rim-vs-outside 0.11, heterogeneity 0.14; core [0.585, 0.0, 0.249, 0.0] rim [0.065, 0.0, 0.466, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 133 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.19, rim/outside 29.8 (aggregate of 133 individuals; 43/133 membrane-like individually; rim level 0.58)
  - radial predator B: flat profile (no radial structure; level 0; aggregate of 133 individuals)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.9, rim/outside 0.869 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.617)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 133 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1327 (t=1665, R_eq 5.11): ['prey A']; #1294 (t=1590, R_eq 5.94): ['prey A']; #2448 (t=2850, R_eq 5.01): none; #1872 (t=2220, R_eq 5.11): ['prey A']
- species `prey` (channels ['prey A'], own threshold): components final 23, mean 21.1, max 28; tracks 1889, persistent 0; splits 678, persistent splits 7 (K=20), max generation 6, merges 348, merge/split 0.513; moving tracks 108
- species `predator` (channels ['predator B'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- --dt 0.1 only relabels time (world META dt 0.2): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
