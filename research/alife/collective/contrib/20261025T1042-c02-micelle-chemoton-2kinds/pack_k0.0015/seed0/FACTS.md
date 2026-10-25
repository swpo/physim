# Evidence pack: fch-micelle-chemoton-2k (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0936-c02-micelle-chemoton-sighting/world.py; mutation: two catalyst kinds K1, K2 that share the precursor and differ only in amphiphile yield (r2 = rr * r)
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [128, 128]; wall 837s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds/world.py --out collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds/pack_k0.0015/seed0 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1205, 2.9901], min area 6 px

## Measurements
- components: final 1, mean 23.7, max 98; occupancy final 1.00
- tracks: 523; persistent (alive >= 50% of run): 1; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.25 (1 = constant size)
- enclosures: components with a hole mean 0.84, final 0; holes at thresholds 0.2/0.35/0.5 final [106, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 20, 12], H1 [33, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 80, default): splits 177, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 133, merge/split ratio 0.751, nucleations 23
- channel total drift (end/start - 1): [3.7173, 1.8967, 0.0389, -0.588]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 522 at frame 141: holes 63, rim-vs-core 0.28, rim-vs-outside 0.38, heterogeneity 0.13; core [0.279, 0.0, 0.053, 0.217] rim [0.433, 0.008, 0.006, 0.446]
  - track 80 at frame 44: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.08; core [0.604, 0.001, 0.0, 0.285] rim [0.154, 0.0, 0.0, 0.278]
  - track 93 at frame 40: holes 0, rim-vs-core 0.44, rim-vs-outside 0.11, heterogeneity 0.08; core [0.615, 0.001, 0.0, 0.295] rim [0.17, 0.0, 0.0, 0.29]
  - track 122 at frame 44: holes 0, rim-vs-core 0.45, rim-vs-outside 0.08, heterogeneity 0.08; core [0.598, 0.003, 0.0, 0.243] rim [0.147, 0.0, 0.0, 0.239]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 135 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.509, rim/outside 1.55 (aggregate of 135 individuals; 0/135 membrane-like individually; rim level 0.457)
  - radial catalyst K1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.059, rim/outside 0.518 (aggregate of 135 individuals; 0/135 membrane-like individually; rim level 0.0049)
  - radial catalyst K2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.136, rim/outside 0.767 (aggregate of 135 individuals; 3/135 membrane-like individually; rim level 0.0041)
  - radial precursor Pp: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 1.08 (aggregate of 135 individuals; 0/135 membrane-like individually; rim level 0.182)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #522 (t=564, R_eq 70.35): none; #80 (t=176, R_eq 5.14): none; #93 (t=160, R_eq 5.05): none; #122 (t=176, R_eq 5.2): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 135 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 5 of 135 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
