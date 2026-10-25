# Evidence pack: membrane-evo (seed 52)

- world: `../../world_twin.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 92s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_twin.py --out collective/contrib/c17-mevo-wip/twin/seed52 --seeds 52 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7301], min area 6 px

## Measurements
- components: final 16, mean 11.5, max 17; occupancy final 0.26
- tracks: 85; persistent (alive >= 50% of run): 3; longest 121 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.51 (1 = constant size)
- enclosures: components with a hole mean 10.58, final 16; holes at thresholds 0.2/0.35/0.5 final [6, 16, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 16, 16], H1 [16, 16, 9]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00308/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 5000, default): splits 34, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.8185, None, 0.0423, -0.2231]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 101: holes 1, rim-vs-core 0.47, rim-vs-outside 0.74, heterogeneity 0.22; core [0.0, 0.898, 0.662, 0.466] rim [0.0, 0.48, 0.557, 0.648]
  - track 32 at frame 97: holes 1, rim-vs-core 0.44, rim-vs-outside 0.71, heterogeneity 0.22; core [0.866, 0.0, 0.703, 0.513] rim [0.46, 0.0, 0.568, 0.611]
  - track 30 at frame 91: holes 1, rim-vs-core 0.41, rim-vs-outside 0.70, heterogeneity 0.21; core [0.857, 0.0, 0.677, 0.555] rim [0.479, 0.0, 0.555, 0.64]
  - track 55 at frame 129: holes 1, rim-vs-core 0.34, rim-vs-outside 0.76, heterogeneity 0.20; core [0.84, 0.0, 0.603, 0.45] rim [0.551, 0.0, 0.576, 0.627]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 8.92 (aggregate of 76 individuals; 9/76 membrane-like individually; rim level 0.456)
  - radial K2: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 7.72 (aggregate of 76 individuals; 6/76 membrane-like individually; rim level 0.173)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.48, rim/outside 6.41 (aggregate of 76 individuals; 56/76 membrane-like individually; rim level 0.504)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 5.94, rim/outside 4.41 (aggregate of 76 individuals; 67/76 membrane-like individually; rim level 0.487)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #20 (t=25250, R_eq 9.9, ring): ['membrane (wall)']; #32 (t=24250, R_eq 8.2, ring): ['L link', 'membrane (wall)']; #30 (t=22750, R_eq 9.41, ring): ['K1', 'L link', 'membrane (wall)']; #55 (t=32250, R_eq 10.26, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 68 of 76 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
