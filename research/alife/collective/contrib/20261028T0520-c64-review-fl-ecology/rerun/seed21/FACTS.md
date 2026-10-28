# Evidence pack: flow-lenia-digestion-ecology (seed 21)

- world: `../../../20261028T0344-c62-flow-lenia-ecology-s-claim/world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 609s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0344-c62-flow-lenia-ecology-s-claim/world.py --out collective/contrib/20261028T0520-c64-review-fl-ecology/rerun/seed21 --seeds 21 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0018, 2.1858], min area 6 px

## Measurements
- components: final 32, mean 29.8, max 91; occupancy final 0.13
- tracks: 3948; persistent (alive >= 50% of run): 0; longest 55 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 6, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [58, 40, 33], H1 [16, 5, 0]
- motion: 67 long-lived tracks moved >= 1 body length; max speed 0.927/time; max body lengths 14.0
- replication (lineage window K = 20 frames = time 100, default): splits 1337, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1334, merge/split ratio 0.998, nucleations 176
- channel total drift (end/start - 1): [-0.2922, None, -0.0656, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 459 at frame 86: holes 0, rim-vs-core 0.38, rim-vs-outside 0.18, heterogeneity 0.12; core [0.014, 0.539, 0.848, 0.243] rim [0.016, 0.172, 0.854, 0.154]
  - track 58 at frame 40: holes 0, rim-vs-core 0.43, rim-vs-outside 0.13, heterogeneity 0.08; core [0.53, 0.001, 0.415, 0.006] rim [0.126, 0.001, 0.552, 0.005]
  - track 355 at frame 71: holes 0, rim-vs-core 0.45, rim-vs-outside 0.08, heterogeneity 0.09; core [0.002, 0.54, 0.891, 0.038] rim [0.004, 0.085, 0.871, 0.025]
  - track 1882 at frame 323: holes 0, rim-vs-core 0.38, rim-vs-outside 0.15, heterogeneity 0.08; core [0.003, 0.538, 0.926, 0.047] rim [0.005, 0.156, 0.921, 0.031]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 174 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.973, rim/outside 8.02 (aggregate of 174 individuals; 29/174 membrane-like individually; rim level 0.194)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 13.6 (aggregate of 174 individuals; 46/174 membrane-like individually; rim level 0.289)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.31, rim/outside 0.946 (aggregate of 174 individuals; 0/174 membrane-like individually; rim level 0.756)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 2.72 (aggregate of 174 individuals; 3/174 membrane-like individually; rim level 0.112)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #459 (t=430, R_eq 6.68): ['predator B']; #58 (t=200, R_eq 3.09): none; #355 (t=355, R_eq 4.37): none; #1882 (t=1615, R_eq 4.85): none
- species `prey` (channels ['prey A'], own threshold): components final 12, mean 14.8, max 54; tracks 750, persistent 0; splits 222, persistent splits 5 (K=20), max generation 4, merges 204, merge/split 0.919; moving tracks 141
- species `predator` (channels ['predator B'], own threshold): components final 26, mean 22.2, max 30; tracks 1951, persistent 0; splits 637, persistent splits 2 (K=20), max generation 1, merges 558, merge/split 0.876; moving tracks 165

## Warnings
- radial: 2 of 174 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
