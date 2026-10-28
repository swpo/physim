# Evidence pack: flow-lenia-digestion-ecology (seed 21)

- world: `../ctrl_world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 401 frames x 25 steps x dt 0.2 = time 2000; grid [160, 160]; wall 420s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0520-c63-review-flow-lenia-ecology/ctrl_world.py --out collective/contrib/20261028T0520-c63-review-flow-lenia-ecology/ctrl_film --seeds 21 --size 160 160 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0015, 2.1283], min area 6 px

## Measurements
- components: final 28, mean 30.8, max 91; occupancy final 0.12
- tracks: 2266; persistent (alive >= 50% of run): 0; longest 68 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.12, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 5, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 34, 29], H1 [12, 2, 0]
- motion: 63 long-lived tracks moved >= 1 body length; max speed 0.927/time; max body lengths 12.5
- replication (lineage window K = 20 frames = time 100, default): splits 733, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 754, merge/split ratio 1.03, nucleations 165
- channel total drift (end/start - 1): [-0.3474, None, -0.0625, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1531 at frame 299: holes 0, rim-vs-core 0.39, rim-vs-outside 0.11, heterogeneity 0.09; core [0.004, 0.496, 0.935, 0.103] rim [0.006, 0.112, 0.928, 0.066]
  - track 459 at frame 87: holes 0, rim-vs-core 0.35, rim-vs-outside 0.23, heterogeneity 0.12; core [0.012, 0.522, 0.859, 0.374] rim [0.016, 0.198, 0.859, 0.25]
  - track 1384 at frame 266: holes 0, rim-vs-core 0.49, rim-vs-outside 0.15, heterogeneity 0.11; core [0.541, 0.016, 0.249, 0.004] rim [0.112, 0.007, 0.48, 0.005]
  - track 1755 at frame 329: holes 0, rim-vs-core 0.50, rim-vs-outside 0.07, heterogeneity 0.09; core [0.005, 0.571, 0.93, 0.105] rim [0.007, 0.07, 0.926, 0.07]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 181 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 8.02 (aggregate of 181 individuals; 27/181 membrane-like individually; rim level 0.186)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 12.9 (aggregate of 181 individuals; 40/181 membrane-like individually; rim level 0.301)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.31, rim/outside 0.944 (aggregate of 181 individuals; 0/181 membrane-like individually; rim level 0.768)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.772, rim/outside 3.13 (aggregate of 181 individuals; 0/181 membrane-like individually; rim level 0.119)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1531 (t=1495, R_eq 5.97): ['predator B']; #459 (t=435, R_eq 6.68): ['predator B']; #1384 (t=1330, R_eq 3.74): none; #1755 (t=1645, R_eq 5.89): none
- species `prey` (channels ['prey A'], own threshold): components final 11, mean 15.6, max 54; tracks 436, persistent 0; splits 113, persistent splits 5 (K=20), max generation 3, merges 114, merge/split 1.01; moving tracks 97
- species `predator` (channels ['predator B'], own threshold): components final 27, mean 21.4, max 29; tracks 1047, persistent 0; splits 351, persistent splits 3 (K=20), max generation 2, merges 293, merge/split 0.835; moving tracks 118

## Warnings
- radial: 3 of 181 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
