# Evidence pack: fch-micelle-chemoton-2k-twin (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds/world_twin.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0936-c02-micelle-chemoton-sighting/world.py; mutation: two catalyst kinds K1, K2 that share the precursor and differ only in amphiphile yield (r2 = rr * r)
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [128, 128]; wall 831s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds/world_twin.py --out collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds/pack_twin_k0.0015/seed0 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1191, 2.9872], min area 6 px

## Measurements
- components: final 1, mean 28.7, max 95; occupancy final 0.98
- tracks: 525; persistent (alive >= 50% of run): 0; longest 93 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.82, final 1; holes at thresholds 0.2/0.35/0.5 final [40, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [41, 15, 13], H1 [33, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 80, default): splits 173, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 1, merges 148, merge/split ratio 0.855, nucleations 23
- channel total drift (end/start - 1): [3.4155, 2.2708, 0.4758, -0.5927]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 219 at frame 71: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.08; core [0.609, 0.001, 0.001, 0.254] rim [0.158, 0.0, 0.0, 0.248]
  - track 182 at frame 57: holes 0, rim-vs-core 0.45, rim-vs-outside 0.09, heterogeneity 0.08; core [0.601, 0.003, 0.0, 0.195] rim [0.152, 0.0, 0.0, 0.188]
  - track 179 at frame 57: holes 0, rim-vs-core 0.44, rim-vs-outside 0.09, heterogeneity 0.08; core [0.599, 0.002, 0.002, 0.199] rim [0.154, 0.0, 0.0, 0.193]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 140 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.507, rim/outside 1.67 (aggregate of 140 individuals; 0/140 membrane-like individually; rim level 0.439)
  - radial catalyst K1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.084, rim/outside 0.762 (aggregate of 140 individuals; 6/140 membrane-like individually; rim level 0.0063)
  - radial catalyst K2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.123, rim/outside 0.751 (aggregate of 140 individuals; 6/140 membrane-like individually; rim level 0.0044)
  - radial precursor Pp: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 1.06 (aggregate of 140 individuals; 0/140 membrane-like individually; rim level 0.181)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #219 (t=284, R_eq 5.14): none; #524 (t=640, R_eq 69.56): none; #182 (t=228, R_eq 5.08): none; #179 (t=228, R_eq 5.11): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 5 of 140 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
