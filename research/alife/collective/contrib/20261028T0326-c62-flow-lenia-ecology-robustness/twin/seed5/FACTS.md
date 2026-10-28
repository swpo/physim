# Evidence pack: flow-lenia-digestion-ecology (seed 5)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 327s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim2/twin/seed5 --seeds 5 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0003, 1.8293], min area 6 px

## Measurements
- components: final 9, mean 16.1, max 22; occupancy final 0.08
- tracks: 1563; persistent (alive >= 50% of run): 0; longest 53 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 7, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 15, 9], H1 [11, 3, 0]
- motion: 81 long-lived tracks moved >= 1 body length; max speed 0.948/time; max body lengths 20.5
- replication (lineage window K = 20 frames = time 100, default): splits 545, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 538, merge/split ratio 0.987, nucleations 3
- channel total drift (end/start - 1): [-0.0, None, -0.0777, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 138 at frame 86: holes 0, rim-vs-core 0.28, rim-vs-outside 0.39, heterogeneity 0.14; core [0.572, 0.0, 0.251, 0.0] rim [0.316, 0.0, 0.364, 0.0]
  - track 887 at frame 338: holes 0, rim-vs-core 0.53, rim-vs-outside 0.10, heterogeneity 0.13; core [0.543, 0.0, 0.405, 0.0] rim [0.062, 0.0, 0.617, 0.0]
  - track 1272 at frame 489: holes 0, rim-vs-core 0.40, rim-vs-outside 0.36, heterogeneity 0.14; core [0.628, 0.0, 0.126, 0.0] rim [0.306, 0.0, 0.361, 0.0]
  - track 1052 at frame 408: holes 0, rim-vs-core 0.59, rim-vs-outside 0.12, heterogeneity 0.15; core [0.591, 0.0, 0.236, 0.0] rim [0.059, 0.0, 0.497, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 97 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 33.2 (aggregate of 97 individuals; 28/97 membrane-like individually; rim level 0.509)
  - radial predator B: flat profile (no radial structure; level 0; aggregate of 97 individuals)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.18, rim/outside 0.835 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.646)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 97 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #138 (t=430, R_eq 5.75): ['prey A']; #887 (t=1690, R_eq 5.35): none; #1272 (t=2445, R_eq 7.82): none; #1052 (t=2040, R_eq 5.92): none
- species `prey` (channels ['prey A'], own threshold): components final 13, mean 17.4, max 22; tracks 1439, persistent 0; splits 510, persistent splits 0 (K=20), max generation 0, merges 439, merge/split 0.861; moving tracks 135
- species `predator` (channels ['predator B'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
