# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 647s; status ok
- command: `python -m labkit.run /tmp/claude-0/ar/world.py --out /tmp/claude-0/ar/rep4/seed1 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0016, 2.1897], min area 6 px

## Measurements
- components: final 28, mean 28.7, max 95; occupancy final 0.13
- tracks: 2565; persistent (alive >= 50% of run): 0; longest 112 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [4, 9, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 30, 28], H1 [19, 3, 0]
- motion: 167 long-lived tracks moved >= 1 body length; max speed 0.921/time; max body lengths 15.2
- replication (lineage window K = 20 frames = time 100, default): splits 825, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 840, merge/split ratio 1.02, nucleations 194
- channel total drift (end/start - 1): [-0.2316, None, -0.0701, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1492 at frame 348: holes 0, rim-vs-core 0.40, rim-vs-outside 0.19, heterogeneity 0.09; core [0.001, 0.593, 0.966, 0.033] rim [0.003, 0.19, 0.961, 0.021]
  - track 618 at frame 121: holes 0, rim-vs-core 0.53, rim-vs-outside 0.09, heterogeneity 0.09; core [0.003, 0.623, 0.935, 0.038] rim [0.004, 0.094, 0.933, 0.023]
  - track 573 at frame 106: holes 0, rim-vs-core 0.51, rim-vs-outside 0.11, heterogeneity 0.09; core [0.005, 0.623, 0.93, 0.059] rim [0.007, 0.114, 0.927, 0.037]
  - track 2393 at frame 575: holes 0, rim-vs-core 0.16, rim-vs-outside 0.36, heterogeneity 0.09; core [0.005, 0.52, 0.913, 0.071] rim [0.006, 0.365, 0.911, 0.059]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 160 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 8.94 (aggregate of 160 individuals; 28/160 membrane-like individually; rim level 0.212)
  - radial predator B: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 17.3 (aggregate of 160 individuals; 38/160 membrane-like individually; rim level 0.315)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 0.937 (aggregate of 160 individuals; 0/160 membrane-like individually; rim level 0.751)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 3.2 (aggregate of 160 individuals; 0/160 membrane-like individually; rim level 0.0964)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1492 (t=1740, R_eq 7.05): none; #618 (t=605, R_eq 3.91): none; #573 (t=530, R_eq 3.78): none; #2393 (t=2875, R_eq 6.43): ['predator B']
- species `prey` (channels ['prey A'], own threshold): components final 16, mean 14.7, max 52; tracks 838, persistent 0; splits 252, persistent splits 3 (K=20), max generation 2, merges 222, merge/split 0.881; moving tracks 134
- species `predator` (channels ['predator B'], own threshold): components final 16, mean 17.9, max 29; tracks 107, persistent 15; splits 17, persistent splits 1 (K=20), max generation 1, merges 27, merge/split 1.59; moving tracks 46

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
