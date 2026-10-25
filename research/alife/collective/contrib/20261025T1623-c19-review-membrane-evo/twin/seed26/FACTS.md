# Evidence pack: membrane-evo (seed 26)

- world: `../../../../../threads/autopoiesis/worlds/membrane_evo/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 105s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo/world.py --out collective/contrib/20261025T1623-c19-review-membrane-evo/twin/seed26 --seeds 26 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7314], min area 6 px

## Measurements
- components: final 17, mean 11.4, max 23; occupancy final 0.28
- tracks: 104; persistent (alive >= 50% of run): 2; longest 106 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 25.40 (1 = constant size)
- enclosures: components with a hole mean 10.42, final 16; holes at thresholds 0.2/0.35/0.5 final [6, 16, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 17, 17], H1 [17, 16, 13]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00252/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 5000, default): splits 38, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 4, merges 2, merge/split ratio 0.053, nucleations 0
- channel total drift (end/start - 1): [-0.7688, None, 0.1146, -0.1431]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 46 at frame 108: holes 0, rim-vs-core 0.76, rim-vs-outside 1.03, heterogeneity 0.24; core [0.924, 0.0, 0.734, 0.272] rim [0.402, 0.0, 0.717, 0.824]
  - track 52 at frame 102: holes 1, rim-vs-core 0.40, rim-vs-outside 0.68, heterogeneity 0.21; core [0.83, 0.0, 0.671, 0.57] rim [0.451, 0.0, 0.539, 0.619]
  - track 61 at frame 105: holes 1, rim-vs-core 0.42, rim-vs-outside 0.72, heterogeneity 0.22; core [0.0, 0.923, 0.697, 0.559] rim [0.0, 0.532, 0.559, 0.623]
  - track 83 at frame 140: holes 1, rim-vs-core 0.35, rim-vs-outside 0.71, heterogeneity 0.20; core [0.851, 0.0, 0.63, 0.479] rim [0.534, 0.0, 0.55, 0.617]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 7.68 (aggregate of 75 individuals; 7/75 membrane-like individually; rim level 0.387)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 7.42 (aggregate of 75 individuals; 6/75 membrane-like individually; rim level 0.247)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 5.58 (aggregate of 75 individuals; 53/75 membrane-like individually; rim level 0.505)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.52, rim/outside 4.03 (aggregate of 75 individuals; 69/75 membrane-like individually; rim level 0.494)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #46 (t=27000, R_eq 6.72): ['L link', 'membrane (wall)']; #52 (t=25500, R_eq 9.1, ring): ['L link', 'membrane (wall)']; #61 (t=26250, R_eq 9.15, ring): ['L link', 'membrane (wall)']; #83 (t=35000, R_eq 11.55): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 62 of 75 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
