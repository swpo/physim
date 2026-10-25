# Evidence pack: eco-lenia2 (seed 0)

- world: `../../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 308s; status ok
- command: `python -m labkit.run collective/contrib/_c26work/le/world.py --out collective/contrib/_c26work/le/pack_sep --seeds 0 1 --frames 500 --spf 20 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.998], min area 6 px

## Measurements
- components: final 41, mean 41.9, max 66; occupancy final 0.28
- tracks: 1105; persistent (alive >= 50% of run): 20; longest 443 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.30 (1 = constant size)
- enclosures: components with a hole mean 1.23, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [60, 40, 29], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.164/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 40, default): splits 253, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 4, merges 253, merge/split ratio 1, nucleations 352
- channel total drift (end/start - 1): [19.5417, 13.9072, 9.6512, 6.7978, 6.2275, 7.3649, -0.1131]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 482 at frame 282: holes 0, rim-vs-core 0.61, rim-vs-outside 0.68, heterogeneity 0.39; core [0.841, 0.676, 0.393, 0.783, 0.829, 0.739, 0.759] rim [0.605, 0.766, 0.188, 0.523, 0.473, 0.479, 0.787]
  - track 527 at frame 286: holes 0, rim-vs-core 0.43, rim-vs-outside 0.59, heterogeneity 0.42; core [0.536, 0.394, 0.376, 0.536, 0.345, 0.569, 0.796] rim [0.505, 0.592, 0.049, 0.504, 0.535, 0.515, 0.81]
  - track 652 at frame 294: holes 0, rim-vs-core 0.62, rim-vs-outside 0.93, heterogeneity 0.36; core [0.904, 0.803, 0.353, 0.906, 0.594, 0.987, 0.742] rim [0.646, 0.801, 0.164, 0.505, 0.721, 0.667, 0.771]
  - track 996 at frame 429: holes 0, rim-vs-core 0.31, rim-vs-outside 0.56, heterogeneity 0.42; core [0.56, 0.462, 0.335, 0.489, 0.368, 0.509, 0.76] rim [0.524, 0.609, 0.111, 0.492, 0.521, 0.51, 0.782]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 246 components >= 12 px at frames [84, 168, 252, 332, 416, 500]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.634, rim/outside 9.06 (aggregate of 246 individuals; 6/246 membrane-like individually; rim level 0.424)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.913, rim/outside 4.24 (aggregate of 246 individuals; 49/246 membrane-like individually; rim level 0.489)
  - radial A2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.781, rim/outside 2.65 (aggregate of 246 individuals; 89/246 membrane-like individually; rim level 0.249)
  - radial B0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.775, rim/outside 6.57 (aggregate of 246 individuals; 16/246 membrane-like individually; rim level 0.552)
  - radial B1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.873, rim/outside 3.44 (aggregate of 246 individuals; 57/246 membrane-like individually; rim level 0.528)
  - radial B2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 5.2 (aggregate of 246 individuals; 30/246 membrane-like individually; rim level 0.537)
  - radial F: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 0.975 (aggregate of 246 individuals; 0/246 membrane-like individually; rim level 0.728)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #482 (t=564, R_eq 7.25): none; #527 (t=572, R_eq 8.27): ['A2']; #652 (t=588, R_eq 7.11): ['B1']; #996 (t=858, R_eq 8.29): ['A2']
- species `A` (channels ['A0'], own threshold): components final 31, mean 27.6, max 33; tracks 214, persistent 30; splits 70, persistent splits 17 (K=20), max generation 3, merges 43, merge/split 0.614; moving tracks 3
- species `B` (channels ['B0'], own threshold): components final 47, mean 54.5, max 95; tracks 2073, persistent 31; splits 413, persistent splits 3 (K=20), max generation 1, merges 349, merge/split 0.845; moving tracks 3

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 246 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
