# Evidence pack: fch-micelle-chemoton (seed 1)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0936-c02-micelle-chemoton-sighting/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0810-c01-fch-uptake-cargo/world.py; mutation: global amphiphile feed replaced by amphiphile made by a partitioning autocatalyst K from a fed precursor; amphiphile decays
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [128, 128]; wall 534s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0936-c02-micelle-chemoton-sighting/world.py --out collective/contrib/20261025T0936-c02-micelle-chemoton-sighting/pack/seed1 --seeds 1 --frames 200 --no-movie`
- segmentation: matter > 0.17 of robust range [0.0295, 2.8463], min area 6 px

## Measurements
- components: final 31, mean 30.5, max 31; occupancy final 0.06
- tracks: 45; persistent (alive >= 50% of run): 31; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 31], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 80, default): splits 13, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 18
- channel total drift (end/start - 1): [-0.6538, -1.0, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 0.43, rim-vs-outside 0.14, heterogeneity 0.09; core [0.667, 0.0, 0.973] rim [0.242, 0.0, 0.973]
  - track 7 at frame 101: holes 0, rim-vs-core 0.42, rim-vs-outside 0.15, heterogeneity 0.09; core [0.677, 0.0, 0.973] rim [0.253, 0.0, 0.973]
  - track 10 at frame 101: holes 0, rim-vs-core 0.42, rim-vs-outside 0.15, heterogeneity 0.09; core [0.677, 0.0, 0.973] rim [0.253, 0.0, 0.973]
  - track 33 at frame 104: holes 0, rim-vs-core 0.42, rim-vs-outside 0.14, heterogeneity 0.09; core [0.657, 0.0, 0.973] rim [0.237, 0.0, 0.973]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 186 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.511, rim/outside 18.1 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.473)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.881, rim/outside 1 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0)
  - radial precursor Pp: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 1 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.909)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=404, R_eq 3.78): none; #7 (t=404, R_eq 3.78): none; #10 (t=404, R_eq 3.78): none; #33 (t=416, R_eq 3.83): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
