# Evidence pack: membrane-evo (seed 24)

- world: `../../../../../threads/autopoiesis/worlds/membrane_evo/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 106s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo/world.py --out collective/contrib/20261025T1623-c19-review-membrane-evo/twin/seed24 --seeds 24 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7274], min area 6 px

## Measurements
- components: final 16, mean 11.2, max 19; occupancy final 0.26
- tracks: 102; persistent (alive >= 50% of run): 1; longest 109 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.54 (1 = constant size)
- enclosures: components with a hole mean 10.29, final 14; holes at thresholds 0.2/0.35/0.5 final [7, 14, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 16, 16], H1 [16, 15, 9]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0032/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 5000, default): splits 39, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 5, merges 1, merge/split ratio 0.026, nucleations 1
- channel total drift (end/start - 1): [-0.8225, None, 0.049, -0.2443]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 106: holes 1, rim-vs-core 0.39, rim-vs-outside 0.69, heterogeneity 0.21; core [0.865, 0.0, 0.673, 0.536] rim [0.5, 0.0, 0.568, 0.633]
  - track 41 at frame 95: holes 1, rim-vs-core 0.38, rim-vs-outside 0.69, heterogeneity 0.21; core [0.838, 0.0, 0.696, 0.536] rim [0.497, 0.0, 0.573, 0.633]
  - track 31 at frame 79: holes 1, rim-vs-core 0.37, rim-vs-outside 0.76, heterogeneity 0.20; core [0.845, 0.0, 0.595, 0.433] rim [0.531, 0.0, 0.55, 0.618]
  - track 69 at frame 133: holes 1, rim-vs-core 0.43, rim-vs-outside 0.69, heterogeneity 0.22; core [0.0, 0.91, 0.672, 0.582] rim [0.0, 0.5, 0.545, 0.621]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 9.2 (aggregate of 76 individuals; 12/76 membrane-like individually; rim level 0.426)
  - radial K2: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 7.88 (aggregate of 76 individuals; 5/76 membrane-like individually; rim level 0.21)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 6.33 (aggregate of 76 individuals; 56/76 membrane-like individually; rim level 0.508)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 5.53, rim/outside 4.36 (aggregate of 76 individuals; 72/76 membrane-like individually; rim level 0.499)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #38 (t=26500, R_eq 9.52, ring): ['L link', 'membrane (wall)']; #41 (t=23750, R_eq 9.87, ring): ['L link', 'membrane (wall)']; #31 (t=19750, R_eq 10.14, ring): ['L link', 'membrane (wall)']; #69 (t=33250, R_eq 8.81, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 68 of 76 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
