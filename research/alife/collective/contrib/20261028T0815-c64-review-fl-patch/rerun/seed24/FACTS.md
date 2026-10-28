# Evidence pack: flow-lenia-digestion-ecology (seed 24)

- world: `../../../20261028T0303-c62-flow-lenia-ecology-claim/world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 649s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py --out collective/contrib/20261028T0815-c64-review-fl-patch/rerun/seed24 --seeds 24 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0027, 2.1665], min area 6 px

## Measurements
- components: final 32, mean 28.2, max 39; occupancy final 0.13
- tracks: 3720; persistent (alive >= 50% of run): 0; longest 67 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 36, 31], H1 [7, 0, 0]
- motion: 56 long-lived tracks moved >= 1 body length; max speed 0.928/time; max body lengths 12.9
- replication (lineage window K = 20 frames = time 100, default): splits 1303, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1273, merge/split ratio 0.977, nucleations 66
- channel total drift (end/start - 1): [-0.2379, None, -0.0665, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2366 at frame 434: holes 0, rim-vs-core 0.44, rim-vs-outside 0.14, heterogeneity 0.10; core [0.504, 0.0, 0.297, 0.006] rim [0.119, 0.002, 0.506, 0.006]
  - track 152 at frame 66: holes 0, rim-vs-core 0.39, rim-vs-outside 0.16, heterogeneity 0.08; core [0.004, 0.552, 0.931, 0.065] rim [0.006, 0.167, 0.927, 0.043]
  - track 1403 at frame 267: holes 0, rim-vs-core 0.61, rim-vs-outside 0.06, heterogeneity 0.11; core [0.016, 0.652, 0.832, 0.192] rim [0.02, 0.052, 0.831, 0.113]
  - track 408 at frame 106: holes 0, rim-vs-core 0.50, rim-vs-outside 0.04, heterogeneity 0.09; core [0.004, 0.56, 0.942, 0.043] rim [0.005, 0.059, 0.941, 0.027]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 171 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 8.25 (aggregate of 171 individuals; 27/171 membrane-like individually; rim level 0.182)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 15.5 (aggregate of 171 individuals; 54/171 membrane-like individually; rim level 0.305)
  - radial food: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.29, rim/outside 0.942 (aggregate of 171 individuals; 0/171 membrane-like individually; rim level 0.764)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.721, rim/outside 3.18 (aggregate of 171 individuals; 2/171 membrane-like individually; rim level 0.0903)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2366 (t=2170, R_eq 3.74): none; #152 (t=330, R_eq 4.75): ['predator B']; #1403 (t=1335, R_eq 4.15): none; #408 (t=530, R_eq 3.43): none
- species `prey` (channels ['prey A'], own threshold): components final 14, mean 13.1, max 19; tracks 732, persistent 0; splits 245, persistent splits 4 (K=20), max generation 3, merges 206, merge/split 0.841; moving tracks 135
- species `predator` (channels ['predator B'], own threshold): components final 27, mean 23.1, max 30; tracks 1783, persistent 0; splits 610, persistent splits 5 (K=20), max generation 2, merges 479, merge/split 0.785; moving tracks 194

## Warnings
- radial: 1 of 171 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
