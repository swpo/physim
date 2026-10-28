# Evidence pack: flow-lenia-digestion-ecology (seed 21)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261028T0344-c62-flow-lenia-ecology-s-claim/world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 334s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0344-c62-flow-lenia-ecology-s-claim/world.py --out /tmp/claude-0/ar/twinlow/seed21 --seeds 21 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0003, 1.7999], min area 6 px

## Measurements
- components: final 13, mean 15.2, max 48; occupancy final 0.07
- tracks: 1084; persistent (alive >= 50% of run): 0; longest 102 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 10, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 15, 13], H1 [11, 4, 0]
- motion: 104 long-lived tracks moved >= 1 body length; max speed 0.941/time; max body lengths 23.7
- replication (lineage window K = 20 frames = time 100, default): splits 349, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 376, merge/split ratio 1.08, nucleations 48
- channel total drift (end/start - 1): [0.0, None, -0.0679, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 61: holes 0, rim-vs-core 0.62, rim-vs-outside 0.14, heterogeneity 0.13; core [0.672, 0.0, 0.286, 0.0] rim [0.085, 0.0, 0.494, 0.0]
  - track 8 at frame 45: holes 0, rim-vs-core 0.56, rim-vs-outside 0.17, heterogeneity 0.12; core [0.636, 0.0, 0.245, 0.0] rim [0.124, 0.0, 0.472, 0.0]
  - track 224 at frame 136: holes 0, rim-vs-core 0.29, rim-vs-outside 0.44, heterogeneity 0.14; core [0.631, 0.0, 0.165, 0.0] rim [0.363, 0.0, 0.28, 0.0]
  - track 825 at frame 494: holes 0, rim-vs-core 0.55, rim-vs-outside 0.11, heterogeneity 0.14; core [0.546, 0.0, 0.276, 0.0] rim [0.052, 0.0, 0.521, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 27.6 (aggregate of 85 individuals; 24/85 membrane-like individually; rim level 0.535)
  - radial predator B: flat profile (no radial structure; level 0; aggregate of 85 individuals)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.54, rim/outside 0.832 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.637)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 85 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #22 (t=305, R_eq 3.87): none; #8 (t=225, R_eq 3.74): none; #224 (t=680, R_eq 7.4): none; #825 (t=2470, R_eq 5.64): ['prey A']
- species `prey` (channels ['prey A'], own threshold): components final 14, mean 15.7, max 45; tracks 1000, persistent 0; splits 331, persistent splits 3 (K=20), max generation 3, merges 312, merge/split 0.943; moving tracks 137
- species `predator` (channels ['predator B'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
