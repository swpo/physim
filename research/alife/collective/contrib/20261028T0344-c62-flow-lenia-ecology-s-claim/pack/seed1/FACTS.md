# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 614s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim3/noise/seed1 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.07 of robust range [0.002, 2.1501], min area 6 px

## Measurements
- components: final 31, mean 30.2, max 94; occupancy final 0.13
- tracks: 4123; persistent (alive >= 50% of run): 0; longest 68 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [4, 5, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 33, 24], H1 [12, 1, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.932/time; max body lengths 14.6
- replication (lineage window K = 20 frames = time 100, default): splits 1383, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1423, merge/split ratio 1.03, nucleations 191
- channel total drift (end/start - 1): [-0.2773, None, -0.0672, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 405 at frame 86: holes 0, rim-vs-core 0.34, rim-vs-outside 0.20, heterogeneity 0.08; core [0.005, 0.554, 0.891, 0.049] rim [0.006, 0.217, 0.889, 0.034]
  - track 409 at frame 81: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.08; core [0.002, 0.555, 0.946, 0.031] rim [0.003, 0.104, 0.941, 0.019]
  - track 53 at frame 35: holes 0, rim-vs-core 0.39, rim-vs-outside 0.11, heterogeneity 0.07; core [0.481, 0.0, 0.481, 0.008] rim [0.112, 0.0, 0.593, 0.009]
  - track 441 at frame 81: holes 0, rim-vs-core 0.59, rim-vs-outside 0.08, heterogeneity 0.10; core [0.006, 0.675, 0.904, 0.076] rim [0.008, 0.081, 0.901, 0.048]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 171 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 7.76 (aggregate of 171 individuals; 27/171 membrane-like individually; rim level 0.178)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.955, rim/outside 13.3 (aggregate of 171 individuals; 41/171 membrane-like individually; rim level 0.295)
  - radial food: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 0.942 (aggregate of 171 individuals; 0/171 membrane-like individually; rim level 0.758)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.685, rim/outside 2.81 (aggregate of 171 individuals; 3/171 membrane-like individually; rim level 0.0949)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #405 (t=430, R_eq 3.78): none; #409 (t=405, R_eq 4.55): none; #53 (t=175, R_eq 2.82): none; #441 (t=405, R_eq 3.87): none
- species `prey` (channels ['prey A'], own threshold): components final 12, mean 15.2, max 52; tracks 768, persistent 0; splits 237, persistent splits 8 (K=20), max generation 5, merges 210, merge/split 0.886; moving tracks 149
- species `predator` (channels ['predator B'], own threshold): components final 26, mean 23.2, max 31; tracks 1927, persistent 0; splits 643, persistent splits 9 (K=20), max generation 3, merges 530, merge/split 0.824; moving tracks 166

## Warnings
- radial: 1 of 171 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
