# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 318s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim3/twin/seed1 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0002, 1.8344], min area 6 px

## Measurements
- components: final 17, mean 17.8, max 58; occupancy final 0.09
- tracks: 1642; persistent (alive >= 50% of run): 0; longest 46 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 9, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 19, 19], H1 [9, 3, 0]
- motion: 100 long-lived tracks moved >= 1 body length; max speed 0.972/time; max body lengths 21.0
- replication (lineage window K = 20 frames = time 100, default): splits 543, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 573, merge/split ratio 1.05, nucleations 58
- channel total drift (end/start - 1): [0.0, None, -0.0817, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 647 at frame 257: holes 0, rim-vs-core 0.35, rim-vs-outside 0.42, heterogeneity 0.15; core [0.655, 0.0, 0.218, 0.0] rim [0.334, 0.0, 0.363, 0.0]
  - track 1260 at frame 489: holes 0, rim-vs-core 0.48, rim-vs-outside 0.31, heterogeneity 0.14; core [0.625, 0.0, 0.147, 0.0] rim [0.219, 0.0, 0.401, 0.0]
  - track 918 at frame 368: holes 0, rim-vs-core 0.48, rim-vs-outside 0.27, heterogeneity 0.15; core [0.631, 0.0, 0.178, 0.0] rim [0.204, 0.0, 0.39, 0.0]
  - track 838 at frame 328: holes 0, rim-vs-core 0.54, rim-vs-outside 0.12, heterogeneity 0.13; core [0.562, 0.0, 0.348, 0.0] rim [0.073, 0.0, 0.568, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 101 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 24.4 (aggregate of 101 individuals; 24/101 membrane-like individually; rim level 0.514)
  - radial predator B: flat profile (no radial structure; level 0; aggregate of 101 individuals)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.99, rim/outside 0.827 (aggregate of 101 individuals; 0/101 membrane-like individually; rim level 0.627)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 101 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #647 (t=1285, R_eq 7.44): none; #1260 (t=2445, R_eq 6.36): none; #918 (t=1840, R_eq 8.48): none; #838 (t=1640, R_eq 5.59): ['prey A']
- species `prey` (channels ['prey A'], own threshold): components final 19, mean 18.8, max 51; tracks 1532, persistent 0; splits 500, persistent splits 1 (K=20), max generation 1, merges 488, merge/split 0.976; moving tracks 143
- species `predator` (channels ['predator B'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
