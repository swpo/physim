# Evidence pack: membrane-evo (seed 4)

- world: `../../worlds/membrane_evo/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 92s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo/world.py --out threads/autopoiesis/packs/membrane_evo_twin --seeds 4 --frames 160 --spf 250`
- segmentation: matter > 0.35 of robust range [0.0, 1.727], min area 6 px

## Measurements
- components: final 15, mean 10.4, max 16; occupancy final 0.27
- tracks: 83; persistent (alive >= 50% of run): 0; longest 80 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 9.60, final 14; holes at thresholds 0.2/0.35/0.5 final [5, 15, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 15, 15], H1 [16, 15, 9]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00295/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 5000, default): splits 30, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.033, nucleations 1
- channel total drift (end/start - 1): [-0.7323, None, 0.0625, -0.2827]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 47 at frame 121: holes 1, rim-vs-core 0.33, rim-vs-outside 0.75, heterogeneity 0.21; core [0.0, 0.897, 0.659, 0.583] rim [0.0, 0.584, 0.568, 0.616]
  - track 23 at frame 77: holes 1, rim-vs-core 0.34, rim-vs-outside 0.73, heterogeneity 0.20; core [0.834, 0.0, 0.661, 0.554] rim [0.517, 0.0, 0.567, 0.631]
  - track 53 at frame 122: holes 1, rim-vs-core 0.31, rim-vs-outside 0.75, heterogeneity 0.21; core [0.815, 0.0, 0.642, 0.521] rim [0.525, 0.0, 0.562, 0.609]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 7.67 (aggregate of 67 individuals; 9/67 membrane-like individually; rim level 0.434)
  - radial K2: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 6.68 (aggregate of 67 individuals; 2/67 membrane-like individually; rim level 0.177)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 5.37 (aggregate of 67 individuals; 41/67 membrane-like individually; rim level 0.482)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.74, rim/outside 3.63 (aggregate of 67 individuals; 57/67 membrane-like individually; rim level 0.435)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #47 (t=30250, R_eq 11.04, ring): ['K2', 'L link', 'membrane (wall)']; #48 (t=30250, R_eq 11.33, ring): ['membrane (wall)']; #23 (t=19250, R_eq 8.96, ring): ['L link', 'membrane (wall)']; #53 (t=30500, R_eq 10.84, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 55 of 67 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
