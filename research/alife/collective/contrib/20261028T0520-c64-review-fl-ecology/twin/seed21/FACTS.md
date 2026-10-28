# Evidence pack: flow-lenia-digestion-ecology (seed 21)

- world: `../../world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 313s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0520-c64-review-fl-ecology/world.py --out collective/contrib/20261028T0520-c64-review-fl-ecology/twin/seed21 --seeds 21 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0003, 1.8378], min area 6 px

## Measurements
- components: final 19, mean 17.4, max 61; occupancy final 0.09
- tracks: 1589; persistent (alive >= 50% of run): 0; longest 48 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 9, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 20, 20], H1 [10, 4, 0]
- motion: 96 long-lived tracks moved >= 1 body length; max speed 0.956/time; max body lengths 24.4
- replication (lineage window K = 20 frames = time 100, default): splits 521, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 549, merge/split ratio 1.05, nucleations 61
- channel total drift (end/start - 1): [0.0, None, -0.0852, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 327 at frame 131: holes 0, rim-vs-core 0.53, rim-vs-outside 0.14, heterogeneity 0.13; core [0.588, 0.0, 0.33, 0.0] rim [0.099, 0.0, 0.53, 0.0]
  - track 340 at frame 136: holes 0, rim-vs-core 0.59, rim-vs-outside 0.10, heterogeneity 0.13; core [0.623, 0.0, 0.368, 0.0] rim [0.066, 0.0, 0.552, 0.0]
  - track 172 at frame 71: holes 0, rim-vs-core 0.56, rim-vs-outside 0.12, heterogeneity 0.13; core [0.626, 0.0, 0.471, 0.0] rim [0.095, 0.0, 0.644, 0.0]
  - track 1116 at frame 434: holes 0, rim-vs-core 0.50, rim-vs-outside 0.12, heterogeneity 0.13; core [0.548, 0.0, 0.351, 0.0] rim [0.09, 0.0, 0.543, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 99 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 27.2 (aggregate of 99 individuals; 25/99 membrane-like individually; rim level 0.511)
  - radial predator B: flat profile (no radial structure; level 0; aggregate of 99 individuals)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.1, rim/outside 0.832 (aggregate of 99 individuals; 0/99 membrane-like individually; rim level 0.631)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 99 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #327 (t=655, R_eq 5.01): none; #340 (t=680, R_eq 4.37): none; #172 (t=355, R_eq 4.26): none; #1116 (t=2170, R_eq 5.78): ['prey A']
- species `prey` (channels ['prey A'], own threshold): components final 20, mean 18.4, max 54; tracks 1517, persistent 0; splits 486, persistent splits 0 (K=20), max generation 0, merges 471, merge/split 0.969; moving tracks 133
- species `predator` (channels ['predator B'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- radial: 1 of 99 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
