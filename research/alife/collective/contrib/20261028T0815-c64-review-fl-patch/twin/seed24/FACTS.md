# Evidence pack: flow-lenia-digestion-ecology (seed 24)

- world: `../../../20261028T0303-c62-flow-lenia-ecology-claim/world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 355s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py --out collective/contrib/20261028T0815-c64-review-fl-patch/twin/seed24 --seeds 24 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0003, 1.8238], min area 6 px

## Measurements
- components: final 14, mean 15.4, max 20; occupancy final 0.08
- tracks: 1465; persistent (alive >= 50% of run): 0; longest 48 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 6, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 17, 14], H1 [8, 1, 0]
- motion: 94 long-lived tracks moved >= 1 body length; max speed 0.938/time; max body lengths 19.6
- replication (lineage window K = 20 frames = time 100, default): splits 506, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 492, merge/split ratio 0.972, nucleations 2
- channel total drift (end/start - 1): [-0.0, None, -0.0817, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 437 at frame 202: holes 0, rim-vs-core 0.36, rim-vs-outside 0.32, heterogeneity 0.14; core [0.587, 0.0, 0.308, 0.0] rim [0.255, 0.0, 0.445, 0.0]
  - track 637 at frame 277: holes 0, rim-vs-core 0.48, rim-vs-outside 0.35, heterogeneity 0.15; core [0.679, 0.0, 0.151, 0.0] rim [0.269, 0.0, 0.393, 0.0]
  - track 652 at frame 277: holes 0, rim-vs-core 0.42, rim-vs-outside 0.40, heterogeneity 0.15; core [0.689, 0.0, 0.159, 0.0] rim [0.335, 0.0, 0.384, 0.0]
  - track 487 at frame 222: holes 0, rim-vs-core 0.47, rim-vs-outside 0.27, heterogeneity 0.15; core [0.645, 0.0, 0.194, 0.0] rim [0.221, 0.0, 0.402, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 95 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 25.7 (aggregate of 95 individuals; 26/95 membrane-like individually; rim level 0.511)
  - radial predator B: flat profile (no radial structure; level 0; aggregate of 95 individuals)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.97, rim/outside 0.837 (aggregate of 95 individuals; 0/95 membrane-like individually; rim level 0.629)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 95 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #437 (t=1010, R_eq 5.2): ['prey A']; #637 (t=1385, R_eq 6.46): none; #652 (t=1385, R_eq 7.63): none; #487 (t=1110, R_eq 7.88): none
- species `prey` (channels ['prey A'], own threshold): components final 17, mean 16.6, max 21; tracks 1398, persistent 0; splits 498, persistent splits 3 (K=20), max generation 3, merges 431, merge/split 0.865; moving tracks 128
- species `predator` (channels ['predator B'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- radial: 1 of 95 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
