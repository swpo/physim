# Evidence pack: fch-micelle-chemoton (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0936-c02-micelle-chemoton-sighting/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0810-c01-fch-uptake-cargo/world.py; mutation: global amphiphile feed replaced by amphiphile made by a partitioning autocatalyst K from a fed precursor; amphiphile decays
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [128, 128]; wall 536s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0936-c02-micelle-chemoton-sighting/world.py --out collective/contrib/20261025T0936-c02-micelle-chemoton-sighting/pack/seed0 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1189, 2.9798], min area 6 px

## Measurements
- components: final 54, mean 39.3, max 56; occupancy final 0.34
- tracks: 239; persistent (alive >= 50% of run): 28; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 14.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [67, 67, 67], H1 [1, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0133/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 80, default): splits 80, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 42, merge/split ratio 0.525, nucleations 23
- channel total drift (end/start - 1): [0.9621, 9.4514, -0.5211]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 0, rim-vs-core 0.17, rim-vs-outside 0.43, heterogeneity 0.26; core [0.552, 0.258, 0.123] rim [0.392, 0.238, 0.188]
  - track 4 at frame 101: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.10; core [0.607, 0.0, 0.779] rim [0.16, 0.0, 0.778]
  - track 5 at frame 101: holes 0, rim-vs-core 0.45, rim-vs-outside 0.11, heterogeneity 0.10; core [0.625, 0.0, 0.777] rim [0.174, 0.0, 0.778]
  - track 103 at frame 171: holes 0, rim-vs-core 0.51, rim-vs-outside 0.09, heterogeneity 0.22; core [0.599, 0.233, 0.051] rim [0.147, 0.001, 0.121]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 249 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.511, rim/outside 4.72 (aggregate of 249 individuals; 2/249 membrane-like individually; rim level 0.473)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.081, rim/outside 1.08 (aggregate of 249 individuals; 5/249 membrane-like individually; rim level 0.0117)
  - radial precursor Pp: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.13, rim/outside 0.984 (aggregate of 249 individuals; 0/249 membrane-like individually; rim level 0.501)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=404, R_eq 5.11): none; #4 (t=404, R_eq 4.95): none; #5 (t=404, R_eq 4.92): none; #103 (t=684, R_eq 5.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 249 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
