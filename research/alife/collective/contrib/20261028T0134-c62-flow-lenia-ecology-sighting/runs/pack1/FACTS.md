# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../c62work/world_fleco.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 401 frames x 25 steps x dt 0.2 = time 2000; grid [160, 160]; wall 489s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/c62work/world_fleco.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fl2/pack1 --seeds 1 --size 160 160 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0032, 1.9722], min area 6 px

## Measurements
- components: final 10, mean 17.2, max 31; occupancy final 0.13
- tracks: 1505; persistent (alive >= 50% of run): 0; longest 53 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.03, final 2; holes at thresholds 0.2/0.35/0.5 final [3, 7, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 14, 6], H1 [9, 2, 0]
- motion: 38 long-lived tracks moved >= 1 body length; max speed 0.939/time; max body lengths 14.4
- replication (lineage window K = 20 frames = time 100, default): splits 526, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 464, merge/split ratio 0.882, nucleations 71
- channel total drift (end/start - 1): [-0.0851, None, -0.0762, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 52 at frame 54: holes 0, rim-vs-core 0.55, rim-vs-outside 0.14, heterogeneity 0.12; core [0.598, 0.001, 0.311, 0.007] rim [0.091, 0.006, 0.529, 0.005]
  - track 1296 at frame 356: holes 0, rim-vs-core 0.46, rim-vs-outside 0.12, heterogeneity 0.10; core [0.507, 0.001, 0.392, 0.005] rim [0.087, 0.004, 0.577, 0.004]
  - track 928 at frame 242: holes 0, rim-vs-core 0.54, rim-vs-outside 0.24, heterogeneity 0.15; core [0.664, 0.001, 0.131, 0.008] rim [0.158, 0.008, 0.335, 0.006]
  - track 104 at frame 61: holes 0, rim-vs-core 0.48, rim-vs-outside 0.09, heterogeneity 0.07; core [0.002, 0.582, 0.968, 0.017] rim [0.003, 0.1, 0.967, 0.011]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 92 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 9.91 (aggregate of 92 individuals; 19/92 membrane-like individually; rim level 0.291)
  - radial predator B: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 5.19 (aggregate of 92 individuals; 22/92 membrane-like individually; rim level 0.184)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.64, rim/outside 0.904 (aggregate of 92 individuals; 0/92 membrane-like individually; rim level 0.705)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 3.94 (aggregate of 92 individuals; 2/92 membrane-like individually; rim level 0.0817)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #52 (t=270, R_eq 3.74): none; #1296 (t=1780, R_eq 3.87): none; #928 (t=1210, R_eq 6.77): ['predator B']; #104 (t=305, R_eq 4.11): none
- species `prey` (channels ['prey A'], own threshold): components final 15, mean 15.4, max 20; tracks 675, persistent 0; splits 217, persistent splits 0 (K=20), max generation 0, merges 198, merge/split 0.912; moving tracks 77
- species `predator` (channels ['predator B'], own threshold): components final 7, mean 7.3, max 13; tracks 553, persistent 1; splits 178, persistent splits 0 (K=20), max generation 0, merges 175, merge/split 0.983; moving tracks 23

## Warnings
- radial: 1 of 92 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
