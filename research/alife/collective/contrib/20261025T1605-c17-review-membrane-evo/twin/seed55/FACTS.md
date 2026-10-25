# Evidence pack: membrane-evo (seed 55)

- world: `../../world_twin.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 93s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_twin.py --out collective/contrib/c17-mevo-wip/twin/seed55 --seeds 55 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7287], min area 6 px

## Measurements
- components: final 14, mean 11.2, max 22; occupancy final 0.29
- tracks: 103; persistent (alive >= 50% of run): 2; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.66 (1 = constant size)
- enclosures: components with a hole mean 10.47, final 13; holes at thresholds 0.2/0.35/0.5 final [7, 14, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 14, 14], H1 [16, 16, 11]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0046/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 5000, default): splits 39, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.026, nucleations 0
- channel total drift (end/start - 1): [-0.7444, None, 0.1333, -0.0066]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 67 at frame 114: holes 1, rim-vs-core 0.33, rim-vs-outside 0.75, heterogeneity 0.20; core [0.847, 0.0, 0.635, 0.49] rim [0.552, 0.0, 0.579, 0.625]
  - track 71 at frame 118: holes 1, rim-vs-core 0.48, rim-vs-outside 0.71, heterogeneity 0.23; core [0.0, 0.975, 0.691, 0.53] rim [0.0, 0.522, 0.559, 0.622]
  - track 64 at frame 104: holes 1, rim-vs-core 0.47, rim-vs-outside 0.77, heterogeneity 0.23; core [0.878, 0.0, 0.706, 0.474] rim [0.446, 0.0, 0.585, 0.63]
  - track 93 at frame 144: holes 1, rim-vs-core 0.45, rim-vs-outside 0.77, heterogeneity 0.22; core [0.0, 1.0, 0.696, 0.382] rim [0.0, 0.623, 0.596, 0.6]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 8.65 (aggregate of 75 individuals; 16/75 membrane-like individually; rim level 0.488)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 7.32 (aggregate of 75 individuals; 2/75 membrane-like individually; rim level 0.125)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 6.09 (aggregate of 75 individuals; 56/75 membrane-like individually; rim level 0.492)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.85, rim/outside 4.25 (aggregate of 75 individuals; 67/75 membrane-like individually; rim level 0.481)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #67 (t=28500, R_eq 10.43, ring): ['L link', 'membrane (wall)']; #71 (t=29500, R_eq 8.48, ring): ['L link', 'membrane (wall)']; #64 (t=26000, R_eq 7.46, ring): ['L link', 'membrane (wall)']; #93 (t=36000, R_eq 11.27, ring): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 67 of 75 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
