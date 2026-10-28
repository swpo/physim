# Evidence pack: flow-lenia-digestion-ecology (seed 5)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 612s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim2/pack/seed5 --seeds 5 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0027, 2.1685], min area 6 px

## Measurements
- components: final 27, mean 27.2, max 39; occupancy final 0.12
- tracks: 3447; persistent (alive >= 50% of run): 0; longest 45 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [5, 7, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [48, 34, 26], H1 [14, 2, 0]
- motion: 60 long-lived tracks moved >= 1 body length; max speed 0.954/time; max body lengths 12.6
- replication (lineage window K = 20 frames = time 100, default): splits 1222, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1197, merge/split ratio 0.98, nucleations 60
- channel total drift (end/start - 1): [-0.2423, None, -0.0661, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1984 at frame 368: holes 0, rim-vs-core 0.53, rim-vs-outside 0.09, heterogeneity 0.09; core [0.005, 0.626, 0.922, 0.063] rim [0.007, 0.097, 0.919, 0.038]
  - track 1331 at frame 247: holes 0, rim-vs-core 0.42, rim-vs-outside 0.12, heterogeneity 0.08; core [0.003, 0.56, 0.86, 0.04] rim [0.004, 0.139, 0.847, 0.028]
  - track 199 at frame 66: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.07; core [0.003, 0.57, 0.945, 0.038] rim [0.004, 0.118, 0.941, 0.024]
  - track 455 at frame 111: holes 0, rim-vs-core 0.52, rim-vs-outside 0.05, heterogeneity 0.09; core [0.007, 0.572, 0.895, 0.103] rim [0.008, 0.05, 0.893, 0.066]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 167 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 9.88 (aggregate of 167 individuals; 31/167 membrane-like individually; rim level 0.21)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.956, rim/outside 15.8 (aggregate of 167 individuals; 42/167 membrane-like individually; rim level 0.287)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.32, rim/outside 0.944 (aggregate of 167 individuals; 0/167 membrane-like individually; rim level 0.776)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.779, rim/outside 2.98 (aggregate of 167 individuals; 1/167 membrane-like individually; rim level 0.08)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1984 (t=1840, R_eq 3.99): none; #1331 (t=1235, R_eq 3.87): none; #199 (t=330, R_eq 3.83): none; #455 (t=555, R_eq 4.75): none
- species `prey` (channels ['prey A'], own threshold): components final 13, mean 12.5, max 22; tracks 656, persistent 0; splits 216, persistent splits 3 (K=20), max generation 3, merges 182, merge/split 0.843; moving tracks 130
- species `predator` (channels ['predator B'], own threshold): components final 24, mean 22.4, max 29; tracks 1687, persistent 0; splits 562, persistent splits 14 (K=20), max generation 4, merges 474, merge/split 0.843; moving tracks 171

## Warnings
- radial: 2 of 167 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
