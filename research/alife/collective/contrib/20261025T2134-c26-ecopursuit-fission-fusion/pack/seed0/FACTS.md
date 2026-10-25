# Evidence pack: eco-pursuit (seed 0)

- world: `../../world.py`, family `chemotaxis`
- parent: threads/chemotaxis-motility/worlds/evopursuit; mutation: all prey B (B0=1, m=0), species tracking, food- and prey-removal forks
- run: 201 frames x 240 steps x dt 0.05 = time 2400; grid [160, 160]; wall 360s; status ok
- command: `python -m labkit.run collective/contrib/_c26work/ep/world.py --out collective/contrib/_c26work/ep/pack --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9029], min area 6 px

## Measurements
- components: final 34, mean 30.5, max 40; occupancy final 0.06
- tracks: 2770; persistent (alive >= 50% of run): 0; longest 16 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 33, 27], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 8.9
- replication (lineage window K = 20 frames = time 240, default): splits 68, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 68, merge/split ratio 1, nucleations 2568
- channel total drift (end/start - 1): [None, 0.3287, 0.7494, -0.0905]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 936 at frame 77: holes 0, rim-vs-core 0.50, rim-vs-outside 0.63, heterogeneity 0.26; core [0.045, 0.44, 0.908, 0.254] rim [0.114, 0.66, 0.459, 0.269]
  - track 2298 at frame 176: holes 0, rim-vs-core 0.39, rim-vs-outside 0.36, heterogeneity 0.34; core [0.599, 0.77, 0.647, 0.039] rim [0.487, 0.567, 0.373, 0.193]
  - track 725 at frame 61: holes 0, rim-vs-core 0.25, rim-vs-outside 0.51, heterogeneity 0.31; core [0.2, 0.583, 0.7, 0.057] rim [0.163, 0.457, 0.546, 0.204]
  - track 836 at frame 69: holes 0, rim-vs-core 0.47, rim-vs-outside 0.43, heterogeneity 0.18; core [0.163, 0.914, 0.641, 0.145] rim [0.121, 0.691, 0.263, 0.305]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 189 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial preyA: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 5.19 (aggregate of 189 individuals; 14/189 membrane-like individually; rim level 0.226)
  - radial preyB: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 6.86 (aggregate of 189 individuals; 16/189 membrane-like individually; rim level 0.603)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.57, rim/outside 10.2 (aggregate of 189 individuals; 2/189 membrane-like individually; rim level 0.412)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.32, rim/outside 0.757 (aggregate of 189 individuals; 0/189 membrane-like individually; rim level 0.545)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #936 (t=924, R_eq 7): ['preyB']; #2298 (t=2112, R_eq 5.81): none; #725 (t=732, R_eq 6.38): none; #836 (t=828, R_eq 3.66): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 35, mean 32.2, max 40; tracks 2419, persistent 0; splits 86, persistent splits 0 (K=20), max generation 0, merges 89, merge/split 1.03; moving tracks 1
- species `predator` (channels ['predator'], own threshold): components final 32, mean 23.6, max 32; tracks 2747, persistent 0; splits 6, persistent splits 0 (K=20), max generation 0, merges 25, merge/split 4.17; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 189 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
