# Evidence pack: fch-uptake-micelles (seed 11)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0810-c01-fch-uptake-cargo/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: solute supplied uniformly (kp0 everywhere) instead of made by the amphiphile; partitioning chi=-3 concentrates it in the micelles
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [128, 128]; wall 245s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0810-c01-fch-uptake-cargo/world.py --out /tmp/claude-0/c11rev/rerun --seeds 11 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1163, 2.9937], min area 6 px

## Measurements
- components: final 83, mean 53.1, max 83; occupancy final 0.41
- tracks: 151; persistent (alive >= 50% of run): 43; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.44 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [83, 83, 83], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0139/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 80, default): splits 63, persistent splits 45 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.016, nucleations 20
- channel total drift (end/start - 1): [1.3255, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 101: holes 0, rim-vs-core 0.18, rim-vs-outside 0.35, heterogeneity 0.28; core [0.57, 0.13] rim [0.39, 0.144]
  - track 5 at frame 101: holes 0, rim-vs-core 0.24, rim-vs-outside 0.32, heterogeneity 0.29; core [0.579, 0.2] rim [0.359, 0.113]
  - track 11 at frame 101: holes 0, rim-vs-core 0.49, rim-vs-outside 0.10, heterogeneity 0.27; core [0.613, 0.192] rim [0.166, 0.001]
  - track 123 at frame 180: holes 0, rim-vs-core 0.46, rim-vs-outside 0.10, heterogeneity 0.21; core [0.611, 0.091] rim [0.159, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 348 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.515, rim/outside 6.64 (aggregate of 348 individuals; 4/348 membrane-like individually; rim level 0.481)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.036, rim/outside 1.97 (aggregate of 348 individuals; 4/348 membrane-like individually; rim level 0.0145)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=404, R_eq 5.01): none; #5 (t=404, R_eq 5.08): none; #11 (t=404, R_eq 5.08): none; #123 (t=720, R_eq 5.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
