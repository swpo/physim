# Evidence pack: flow-lenia-digestion-ecology (seed 3)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 317s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim3/twin/seed3 --seeds 3 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0003, 1.8311], min area 6 px

## Measurements
- components: final 16, mean 17.3, max 58; occupancy final 0.08
- tracks: 1594; persistent (alive >= 50% of run): 0; longest 58 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 9, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 21, 17], H1 [13, 3, 0]
- motion: 84 long-lived tracks moved >= 1 body length; max speed 0.939/time; max body lengths 20.1
- replication (lineage window K = 20 frames = time 100, default): splits 526, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 564, merge/split ratio 1.07, nucleations 60
- channel total drift (end/start - 1): [0.0, None, -0.0855, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 503 at frame 232: holes 0, rim-vs-core 0.39, rim-vs-outside 0.43, heterogeneity 0.15; core [0.667, 0.0, 0.132, 0.0] rim [0.355, 0.0, 0.366, 0.0]
  - track 1268 at frame 504: holes 0, rim-vs-core 0.51, rim-vs-outside 0.30, heterogeneity 0.15; core [0.661, 0.0, 0.179, 0.0] rim [0.215, 0.0, 0.416, 0.0]
  - track 397 at frame 176: holes 0, rim-vs-core 0.52, rim-vs-outside 0.30, heterogeneity 0.14; core [0.678, 0.0, 0.145, 0.0] rim [0.217, 0.0, 0.376, 0.0]
  - track 1216 at frame 484: holes 0, rim-vs-core 0.50, rim-vs-outside 0.29, heterogeneity 0.15; core [0.66, 0.0, 0.2, 0.0] rim [0.21, 0.0, 0.423, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 95 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 23 (aggregate of 95 individuals; 31/95 membrane-like individually; rim level 0.522)
  - radial predator B: flat profile (no radial structure; level 0; aggregate of 95 individuals)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 3.06, rim/outside 0.839 (aggregate of 95 individuals; 0/95 membrane-like individually; rim level 0.638)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 95 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #503 (t=1160, R_eq 6.48): ['prey A']; #1268 (t=2520, R_eq 6.75): none; #397 (t=880, R_eq 6.41): none; #1216 (t=2420, R_eq 6.91): none
- species `prey` (channels ['prey A'], own threshold): components final 17, mean 18.1, max 50; tracks 1451, persistent 0; splits 465, persistent splits 0 (K=20), max generation 0, merges 462, merge/split 0.994; moving tracks 119
- species `predator` (channels ['predator B'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
