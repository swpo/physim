# Evidence pack: flow-lenia-digestion-ecology (seed 22)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261028T0344-c62-flow-lenia-ecology-s-claim/world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 337s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0344-c62-flow-lenia-ecology-s-claim/world.py --out /tmp/claude-0/ar/twinlow/seed22 --seeds 22 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0003, 1.7862], min area 6 px

## Measurements
- components: final 15, mean 15.5, max 48; occupancy final 0.07
- tracks: 1125; persistent (alive >= 50% of run): 0; longest 72 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 16, 15], H1 [8, 1, 0]
- motion: 97 long-lived tracks moved >= 1 body length; max speed 0.982/time; max body lengths 23.3
- replication (lineage window K = 20 frames = time 100, default): splits 360, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 384, merge/split ratio 1.07, nucleations 48
- channel total drift (end/start - 1): [0.0, None, -0.0691, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 45: holes 0, rim-vs-core 0.55, rim-vs-outside 0.17, heterogeneity 0.12; core [0.624, 0.0, 0.26, 0.0] rim [0.127, 0.0, 0.489, 0.0]
  - track 33 at frame 45: holes 0, rim-vs-core 0.44, rim-vs-outside 0.12, heterogeneity 0.09; core [0.538, 0.0, 0.415, 0.0] rim [0.122, 0.0, 0.556, 0.0]
  - track 42 at frame 50: holes 0, rim-vs-core 0.52, rim-vs-outside 0.18, heterogeneity 0.10; core [0.661, 0.0, 0.311, 0.0] rim [0.173, 0.0, 0.495, 0.0]
  - track 44 at frame 50: holes 0, rim-vs-core 0.44, rim-vs-outside 0.12, heterogeneity 0.09; core [0.54, 0.0, 0.416, 0.0] rim [0.126, 0.0, 0.565, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 87 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 29.6 (aggregate of 87 individuals; 24/87 membrane-like individually; rim level 0.547)
  - radial predator B: flat profile (no radial structure; level 0; aggregate of 87 individuals)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.56, rim/outside 0.833 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.635)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 87 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=225, R_eq 3.74): none; #33 (t=225, R_eq 3.14): none; #42 (t=250, R_eq 3.24): none; #44 (t=250, R_eq 3.19): none
- species `prey` (channels ['prey A'], own threshold): components final 16, mean 15.9, max 44; tracks 1030, persistent 0; splits 340, persistent splits 2 (K=20), max generation 2, merges 318, merge/split 0.935; moving tracks 131
- species `predator` (channels ['predator B'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
