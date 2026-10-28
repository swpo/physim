# Evidence pack: flow-lenia-digestion-ecology (seed 3)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 610s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim3/noise/seed3 --seeds 3 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.07 of robust range [0.002, 2.1649], min area 6 px

## Measurements
- components: final 28, mean 29.8, max 105; occupancy final 0.13
- tracks: 3942; persistent (alive >= 50% of run): 0; longest 65 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 7, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 32, 24], H1 [10, 1, 0]
- motion: 51 long-lived tracks moved >= 1 body length; max speed 0.923/time; max body lengths 12.3
- replication (lineage window K = 20 frames = time 100, default): splits 1336, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1324, merge/split ratio 0.991, nucleations 191
- channel total drift (end/start - 1): [-0.2839, None, -0.0685, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 141 at frame 55: holes 0, rim-vs-core 0.43, rim-vs-outside 0.09, heterogeneity 0.08; core [0.001, 0.551, 0.949, 0.013] rim [0.001, 0.121, 0.946, 0.009]
  - track 288 at frame 61: holes 0, rim-vs-core 0.39, rim-vs-outside 0.07, heterogeneity 0.07; core [0.001, 0.473, 0.973, 0.017] rim [0.001, 0.085, 0.969, 0.013]
  - track 397 at frame 71: holes 0, rim-vs-core 0.51, rim-vs-outside 0.09, heterogeneity 0.08; core [0.003, 0.614, 0.926, 0.043] rim [0.004, 0.102, 0.92, 0.028]
  - track 569 at frame 106: holes 0, rim-vs-core 0.41, rim-vs-outside 0.10, heterogeneity 0.08; core [0.002, 0.513, 0.962, 0.027] rim [0.002, 0.105, 0.959, 0.019]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 181 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 8.39 (aggregate of 181 individuals; 28/181 membrane-like individually; rim level 0.201)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 11.8 (aggregate of 181 individuals; 47/181 membrane-like individually; rim level 0.291)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.27, rim/outside 0.943 (aggregate of 181 individuals; 0/181 membrane-like individually; rim level 0.759)
  - radial digestion q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 2.39 (aggregate of 181 individuals; 3/181 membrane-like individually; rim level 0.102)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #141 (t=275, R_eq 4.37): none; #288 (t=305, R_eq 5.61): ['predator B']; #397 (t=355, R_eq 3.83): none; #569 (t=530, R_eq 5.94, ring): ['predator B']
- species `prey` (channels ['prey A'], own threshold): components final 14, mean 14.3, max 50; tracks 690, persistent 0; splits 209, persistent splits 5 (K=20), max generation 4, merges 199, merge/split 0.952; moving tracks 145
- species `predator` (channels ['predator B'], own threshold): components final 25, mean 23.2, max 29; tracks 1766, persistent 0; splits 585, persistent splits 9 (K=20), max generation 3, merges 484, merge/split 0.827; moving tracks 188

## Warnings
- radial: 3 of 181 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
