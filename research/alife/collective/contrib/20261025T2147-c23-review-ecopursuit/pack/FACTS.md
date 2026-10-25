# Evidence pack: eco-pursuit (seed 3)

- world: `../../../20261025T2134-c26-ecopursuit-fission-fusion/world.py`, family `chemotaxis`
- parent: threads/chemotaxis-motility/worlds/evopursuit; mutation: all prey B (B0=1, m=0), species tracking, food- and prey-removal forks
- run: 201 frames x 240 steps x dt 0.05 = time 2400; grid [160, 160]; wall 311s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2134-c26-ecopursuit-fission-fusion/world.py --out collective/contrib/20261025T2147-c23-review-ecopursuit/pack --seeds 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9025], min area 6 px

## Measurements
- components: final 38, mean 30.6, max 41; occupancy final 0.07
- tracks: 2822; persistent (alive >= 50% of run): 0; longest 19 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 36, 24], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 10.4
- replication (lineage window K = 20 frames = time 240, default): splits 66, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 66, merge/split ratio 1, nucleations 2627
- channel total drift (end/start - 1): [None, 0.4062, 0.8576, -0.0968]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1695 at frame 133: holes 0, rim-vs-core 0.42, rim-vs-outside 0.48, heterogeneity 0.28; core [0.109, 0.343, 0.883, 0.067] rim [0.154, 0.449, 0.518, 0.242]
  - track 695 at frame 61: holes 0, rim-vs-core 0.31, rim-vs-outside 0.26, heterogeneity 0.31; core [0.338, 0.441, 0.722, 0.245] rim [0.369, 0.456, 0.45, 0.394]
  - track 532 at frame 49: holes 0, rim-vs-core 0.45, rim-vs-outside 0.46, heterogeneity 0.25; core [0.699, 0.941, 0.589, 0.063] rim [0.535, 0.692, 0.297, 0.228]
  - track 724 at frame 61: holes 0, rim-vs-core 0.46, rim-vs-outside 0.32, heterogeneity 0.32; core [0.586, 0.743, 0.691, 0.062] rim [0.382, 0.522, 0.389, 0.238]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 190 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial preyA: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 4.76 (aggregate of 190 individuals; 21/190 membrane-like individually; rim level 0.168)
  - radial preyB: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.835, rim/outside 6.95 (aggregate of 190 individuals; 23/190 membrane-like individually; rim level 0.589)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.589, rim/outside 10 (aggregate of 190 individuals; 4/190 membrane-like individually; rim level 0.426)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.39, rim/outside 0.76 (aggregate of 190 individuals; 0/190 membrane-like individually; rim level 0.55)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1695 (t=1596, R_eq 6.26): ['preyA', 'preyB']; #695 (t=732, R_eq 4.58): none; #532 (t=588, R_eq 3.95): none; #724 (t=732, R_eq 5.23): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 38, mean 32.4, max 42; tracks 2485, persistent 0; splits 90, persistent splits 0 (K=20), max generation 0, merges 91, merge/split 1.01; moving tracks 2
- species `predator` (channels ['predator'], own threshold): components final 24, mean 24.6, max 32; tracks 2941, persistent 0; splits 10, persistent splits 0 (K=20), max generation 0, merges 25, merge/split 2.5; moving tracks 2

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 190 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
