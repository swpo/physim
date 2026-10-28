# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 650s; status ok
- command: `python -m labkit.run /tmp/claude-0/ar/world.py --out /tmp/claude-0/ar/rep4n/seed1 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0016, 2.2039], min area 6 px

## Measurements
- components: final 36, mean 38.7, max 101; occupancy final 0.12
- tracks: 3113; persistent (alive >= 50% of run): 0; longest 122 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 5, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [44, 38, 37], H1 [9, 1, 0]
- motion: 226 long-lived tracks moved >= 1 body length; max speed 1.03/time; max body lengths 20.6
- replication (lineage window K = 20 frames = time 100, default): splits 1008, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1026, merge/split ratio 1.02, nucleations 259
- channel total drift (end/start - 1): [-0.3109, None, -0.0664, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 960 at frame 187: holes 0, rim-vs-core 0.41, rim-vs-outside 0.09, heterogeneity 0.07; core [0.002, 0.513, 0.896, 0.029] rim [0.003, 0.104, 0.89, 0.019]
  - track 959 at frame 176: holes 0, rim-vs-core 0.57, rim-vs-outside 0.08, heterogeneity 0.10; core [0.006, 0.645, 0.917, 0.07] rim [0.008, 0.078, 0.914, 0.044]
  - track 1317 at frame 242: holes 0, rim-vs-core 0.46, rim-vs-outside 0.05, heterogeneity 0.07; core [0.005, 0.525, 0.931, 0.043] rim [0.006, 0.063, 0.929, 0.026]
  - track 2287 at frame 434: holes 0, rim-vs-core 0.35, rim-vs-outside 0.28, heterogeneity 0.08; core [0.007, 0.642, 0.916, 0.074] rim [0.009, 0.29, 0.913, 0.052]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 218 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.811, rim/outside 6.26 (aggregate of 218 individuals; 17/218 membrane-like individually; rim level 0.14)
  - radial predator B: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.696, rim/outside 19.8 (aggregate of 218 individuals; 31/218 membrane-like individually; rim level 0.335)
  - radial food: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.25, rim/outside 0.964 (aggregate of 218 individuals; 0/218 membrane-like individually; rim level 0.781)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.721, rim/outside 2.56 (aggregate of 218 individuals; 3/218 membrane-like individually; rim level 0.1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #960 (t=935, R_eq 3.78): none; #959 (t=880, R_eq 3.7): none; #1317 (t=1210, R_eq 3.52): none; #2287 (t=2170, R_eq 3.19): none
- species `prey` (channels ['prey A'], own threshold): components final 14, mean 14.4, max 52; tracks 699, persistent 0; splits 198, persistent splits 3 (K=20), max generation 2, merges 196, merge/split 0.99; moving tracks 156
- species `predator` (channels ['predator B'], own threshold): components final 27, mean 28.1, max 40; tracks 201, persistent 23; splits 13, persistent splits 1 (K=20), max generation 1, merges 21, merge/split 1.61; moving tracks 66

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
