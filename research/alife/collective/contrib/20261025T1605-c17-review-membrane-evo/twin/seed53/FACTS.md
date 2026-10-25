# Evidence pack: membrane-evo (seed 53)

- world: `../../world_twin.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 91s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_twin.py --out collective/contrib/c17-mevo-wip/twin/seed53 --seeds 53 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7267], min area 6 px

## Measurements
- components: final 12, mean 11.3, max 16; occupancy final 0.27
- tracks: 84; persistent (alive >= 50% of run): 2; longest 103 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.68 (1 = constant size)
- enclosures: components with a hole mean 10.61, final 12; holes at thresholds 0.2/0.35/0.5 final [6, 13, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 12, 12], H1 [13, 13, 12]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00179/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 5000, default): splits 34, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.631, None, 0.1112, -0.2253]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 43 at frame 109: holes 1, rim-vs-core 0.44, rim-vs-outside 0.75, heterogeneity 0.21; core [0.884, 0.0, 0.629, 0.348] rim [0.53, 0.0, 0.562, 0.602]
  - track 49 at frame 114: holes 1, rim-vs-core 0.38, rim-vs-outside 0.74, heterogeneity 0.22; core [0.851, 0.0, 0.729, 0.474] rim [0.521, 0.0, 0.594, 0.597]
  - track 30 at frame 78: holes 1, rim-vs-core 0.35, rim-vs-outside 0.68, heterogeneity 0.20; core [0.824, 0.0, 0.654, 0.547] rim [0.495, 0.0, 0.565, 0.644]
  - track 65 at frame 137: holes 1, rim-vs-core 0.36, rim-vs-outside 0.76, heterogeneity 0.20; core [0.821, 0.0, 0.552, 0.392] rim [0.539, 0.0, 0.553, 0.614]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 70 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 7.19 (aggregate of 70 individuals; 10/70 membrane-like individually; rim level 0.514)
  - radial K2: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 4.55 (aggregate of 70 individuals; 0/70 membrane-like individually; rim level 0.0597)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 4.92 (aggregate of 70 individuals; 45/70 membrane-like individually; rim level 0.455)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.61, rim/outside 3.59 (aggregate of 70 individuals; 60/70 membrane-like individually; rim level 0.446)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #43 (t=27250, R_eq 11.28, ring): ['membrane (wall)']; #49 (t=28500, R_eq 9.22, ring): ['membrane (wall)']; #30 (t=19500, R_eq 9.8, ring): ['L link', 'membrane (wall)']; #65 (t=34250, R_eq 10.82, ring): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 59 of 70 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
