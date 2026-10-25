# Evidence pack: membrane-evo (seed 33)

- world: `../../../../../threads/autopoiesis/worlds/membrane_evo/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 97s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo/world.py --out collective/contrib/20261025T1355-c09-review-membrane-evo/membrane_evo/seed33 --seeds 33 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7252], min area 6 px

## Measurements
- components: final 18, mean 10.8, max 18; occupancy final 0.27
- tracks: 88; persistent (alive >= 50% of run): 2; longest 116 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.10 (1 = constant size)
- enclosures: components with a hole mean 10.11, final 14; holes at thresholds 0.2/0.35/0.5 final [3, 14, 18]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 18, 18], H1 [18, 18, 13]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00382/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 5000, default): splits 37, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 5, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.7547, None, 0.0529, -0.1765]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 35 at frame 104: holes 1, rim-vs-core 0.40, rim-vs-outside 0.78, heterogeneity 0.22; core [0.0, 1.0, 0.605, 0.42] rim [0.0, 0.65, 0.578, 0.605]
  - track 34 at frame 91: holes 1, rim-vs-core 0.32, rim-vs-outside 0.71, heterogeneity 0.20; core [0.806, 0.0, 0.635, 0.544] rim [0.507, 0.0, 0.563, 0.646]
  - track 47 at frame 121: holes 1, rim-vs-core 0.29, rim-vs-outside 0.76, heterogeneity 0.21; core [0.811, 0.0, 0.613, 0.485] rim [0.549, 0.0, 0.573, 0.603]
  - track 70 at frame 144: holes 1, rim-vs-core 0.31, rim-vs-outside 0.77, heterogeneity 0.21; core [0.829, 0.0, 0.636, 0.496] rim [0.545, 0.0, 0.579, 0.599]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 73 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 8.86 (aggregate of 73 individuals; 14/73 membrane-like individually; rim level 0.549)
  - radial K2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.943, rim/outside 4.84 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.0706)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 6.05 (aggregate of 73 individuals; 54/73 membrane-like individually; rim level 0.507)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 5.34, rim/outside 4.35 (aggregate of 73 individuals; 65/73 membrane-like individually; rim level 0.499)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #35 (t=26000, R_eq 10.65, ring): ['L link', 'membrane (wall)']; #34 (t=22750, R_eq 9.37, ring): ['L link', 'membrane (wall)']; #47 (t=30250, R_eq 10.12, ring): ['L link', 'membrane (wall)']; #70 (t=36000, R_eq 10.01, ring): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 65 of 73 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
