# Evidence pack: fch-protocell (seed 7)

- world: `../world_dt2.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0745-c03-fch-vesicles/world.py; mutation: add a solute made by the bilayer, excluded from it by chi c u (barrier), decaying everywhere
- run: 101 frames x 800 steps x dt 0.01 = time 800; grid [128, 128]; wall 498s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev2/world_dt2.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev2/dt2 --seeds 7 --frames 100 --no-movie`
- segmentation: matter > 0.25 of robust range [0.106, 1.6727], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 5; occupancy final 0.16
- tracks: 5; persistent (alive >= 50% of run): 1; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 437.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 1, 1], H1 [1, 1, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 160, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 50: holes 0, rim-vs-core 0.37, rim-vs-outside 0.74, heterogeneity 0.23; core [0.765, 0.502] rim [0.735, 0.134]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 93.4 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.954)
  - radial solute c: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 2.1 (aggregate of 6 individuals; 3/6 membrane-like individually; rim level 0.664)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): solute c
- membrane-like channels per top track at mid-life: #1 (t=400, R_eq 28.88): ['solute c']; #0 (t=0, R_eq 1.38): none; #2 (t=0, R_eq 1.38): none; #3 (t=0, R_eq 1.49): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
