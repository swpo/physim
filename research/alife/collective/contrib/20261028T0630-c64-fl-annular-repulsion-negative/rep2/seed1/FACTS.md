# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 630s; status ok
- command: `python -m labkit.run /tmp/claude-0/ar/world.py --out /tmp/claude-0/ar/rep2/seed1 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0018, 2.1618], min area 6 px

## Measurements
- components: final 31, mean 28.2, max 94; occupancy final 0.13
- tracks: 3067; persistent (alive >= 50% of run): 0; longest 99 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 10, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 30, 21], H1 [16, 2, 0]
- motion: 95 long-lived tracks moved >= 1 body length; max speed 0.914/time; max body lengths 18.6
- replication (lineage window K = 20 frames = time 100, default): splits 1015, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1018, merge/split ratio 1, nucleations 191
- channel total drift (end/start - 1): [-0.226, None, -0.0708, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2334 at frame 484: holes 0, rim-vs-core 0.57, rim-vs-outside 0.05, heterogeneity 0.10; core [0.014, 0.61, 0.863, 0.138] rim [0.018, 0.042, 0.862, 0.077]
  - track 1422 at frame 282: holes 0, rim-vs-core 0.30, rim-vs-outside 0.29, heterogeneity 0.10; core [0.008, 0.59, 0.905, 0.089] rim [0.01, 0.291, 0.902, 0.072]
  - track 2659 at frame 529: holes 0, rim-vs-core 0.53, rim-vs-outside 0.06, heterogeneity 0.11; core [0.025, 0.558, 0.808, 0.26] rim [0.03, 0.041, 0.813, 0.139]
  - track 644 at frame 111: holes 0, rim-vs-core 0.52, rim-vs-outside 0.05, heterogeneity 0.08; core [0.004, 0.568, 0.931, 0.047] rim [0.006, 0.05, 0.928, 0.028]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 164 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 8.94 (aggregate of 164 individuals; 25/164 membrane-like individually; rim level 0.213)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 14.6 (aggregate of 164 individuals; 47/164 membrane-like individually; rim level 0.305)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.32, rim/outside 0.938 (aggregate of 164 individuals; 0/164 membrane-like individually; rim level 0.745)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.766, rim/outside 3.83 (aggregate of 164 individuals; 1/164 membrane-like individually; rim level 0.0992)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2334 (t=2420, R_eq 4.11): none; #1422 (t=1410, R_eq 4.22): none; #2659 (t=2645, R_eq 4.58): none; #644 (t=555, R_eq 4.62): none
- species `prey` (channels ['prey A'], own threshold): components final 11, mean 14.8, max 52; tracks 799, persistent 0; splits 252, persistent splits 3 (K=20), max generation 3, merges 216, merge/split 0.857; moving tracks 137
- species `predator` (channels ['predator B'], own threshold): components final 21, mean 18.6, max 26; tracks 1046, persistent 0; splits 323, persistent splits 5 (K=20), max generation 3, merges 310, merge/split 0.96; moving tracks 167

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
