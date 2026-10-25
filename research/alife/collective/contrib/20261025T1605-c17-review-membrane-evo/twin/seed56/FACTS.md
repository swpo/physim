# Evidence pack: membrane-evo (seed 56)

- world: `../../world_twin.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 92s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_twin.py --out collective/contrib/c17-mevo-wip/twin/seed56 --seeds 56 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.727], min area 6 px

## Measurements
- components: final 12, mean 11.6, max 25; occupancy final 0.24
- tracks: 101; persistent (alive >= 50% of run): 4; longest 113 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.05 (1 = constant size)
- enclosures: components with a hole mean 10.70, final 11; holes at thresholds 0.2/0.35/0.5 final [9, 11, 11]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 12, 12], H1 [12, 11, 8]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00248/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 5000, default): splits 35, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 6, merges 4, merge/split ratio 0.114, nucleations 0
- channel total drift (end/start - 1): [-0.7345, None, 0.0394, -0.1348]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 50 at frame 105: holes 1, rim-vs-core 0.42, rim-vs-outside 0.68, heterogeneity 0.21; core [0.852, 0.0, 0.719, 0.576] rim [0.468, 0.0, 0.558, 0.614]
  - track 60 at frame 113: holes 1, rim-vs-core 0.42, rim-vs-outside 0.81, heterogeneity 0.22; core [0.834, 0.0, 0.568, 0.287] rim [0.548, 0.0, 0.607, 0.597]
  - track 52 at frame 99: holes 1, rim-vs-core 0.37, rim-vs-outside 0.68, heterogeneity 0.21; core [0.806, 0.0, 0.68, 0.573] rim [0.465, 0.0, 0.548, 0.62]
  - track 87 at frame 144: holes 1, rim-vs-core 0.44, rim-vs-outside 0.71, heterogeneity 0.22; core [0.844, 0.0, 0.735, 0.508] rim [0.455, 0.0, 0.568, 0.607]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 8.95 (aggregate of 77 individuals; 17/77 membrane-like individually; rim level 0.527)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.3, rim/outside 5.66 (aggregate of 77 individuals; 4/77 membrane-like individually; rim level 0.0763)
  - radial L link: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 5.76 (aggregate of 77 individuals; 59/77 membrane-like individually; rim level 0.475)
  - radial membrane (wall): peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 5.99, rim/outside 3.98 (aggregate of 77 individuals; 73/77 membrane-like individually; rim level 0.477)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #50 (t=26250, R_eq 9.39, ring): ['K1', 'L link', 'membrane (wall)']; #60 (t=28250, R_eq 10.7): none; #52 (t=24750, R_eq 9.71, ring): ['K1', 'L link', 'membrane (wall)']; #87 (t=36000, R_eq 8.88, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 73 of 77 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
