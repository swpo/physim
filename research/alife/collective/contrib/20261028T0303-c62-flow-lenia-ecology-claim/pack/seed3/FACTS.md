# Evidence pack: flow-lenia-digestion-ecology (seed 3)

- world: `../../world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 821s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim/world.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim/pack/seed3 --seeds 3 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0025, 2.1454], min area 6 px

## Measurements
- components: final 29, mean 27.9, max 37; occupancy final 0.13
- tracks: 3786; persistent (alive >= 50% of run): 0; longest 62 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [5, 5, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [56, 35, 30], H1 [11, 4, 0]
- motion: 54 long-lived tracks moved >= 1 body length; max speed 0.926/time; max body lengths 12.1
- replication (lineage window K = 20 frames = time 100, default): splits 1322, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1281, merge/split ratio 0.969, nucleations 63
- channel total drift (end/start - 1): [-0.2307, None, -0.0661, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2940 at frame 499: holes 0, rim-vs-core 0.61, rim-vs-outside 0.05, heterogeneity 0.09; core [0.004, 0.662, 0.925, 0.041] rim [0.004, 0.05, 0.92, 0.026]
  - track 2954 at frame 504: holes 0, rim-vs-core 0.43, rim-vs-outside 0.11, heterogeneity 0.08; core [0.004, 0.558, 0.935, 0.055] rim [0.006, 0.125, 0.933, 0.035]
  - track 2219 at frame 378: holes 0, rim-vs-core 0.56, rim-vs-outside 0.07, heterogeneity 0.09; core [0.005, 0.624, 0.892, 0.093] rim [0.007, 0.066, 0.886, 0.057]
  - track 3105 at frame 519: holes 0, rim-vs-core 0.59, rim-vs-outside 0.04, heterogeneity 0.10; core [0.014, 0.626, 0.859, 0.163] rim [0.017, 0.041, 0.858, 0.091]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 174 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.967, rim/outside 8.56 (aggregate of 174 individuals; 23/174 membrane-like individually; rim level 0.199)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 12.9 (aggregate of 174 individuals; 44/174 membrane-like individually; rim level 0.288)
  - radial food: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 0.942 (aggregate of 174 individuals; 0/174 membrane-like individually; rim level 0.771)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.776, rim/outside 2.53 (aggregate of 174 individuals; 1/174 membrane-like individually; rim level 0.0966)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2940 (t=2495, R_eq 2.88): none; #2954 (t=2520, R_eq 3.78): none; #2219 (t=1890, R_eq 4.37): none; #3105 (t=2595, R_eq 4.15): none
- species `prey` (channels ['prey A'], own threshold): components final 16, mean 13.1, max 18; tracks 854, persistent 0; splits 298, persistent splits 5 (K=20), max generation 2, merges 249, merge/split 0.836; moving tracks 111
- species `predator` (channels ['predator B'], own threshold): components final 24, mean 22.6, max 29; tracks 1639, persistent 0; splits 555, persistent splits 8 (K=20), max generation 3, merges 448, merge/split 0.807; moving tracks 187

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
