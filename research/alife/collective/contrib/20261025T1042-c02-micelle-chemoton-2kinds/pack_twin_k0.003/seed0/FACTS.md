# Evidence pack: fch-micelle-chemoton-2k-twin (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds/world_twin.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0936-c02-micelle-chemoton-sighting/world.py; mutation: two catalyst kinds K1, K2 that share the precursor and differ only in amphiphile yield (r2 = rr * r)
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [128, 128]; wall 1109s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds/world_twin.py --out collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds/pack_twin_k0.003/seed0 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1172, 2.9936], min area 6 px

## Measurements
- components: final 102, mean 91.7, max 102; occupancy final 0.49
- tracks: 244; persistent (alive >= 50% of run): 96; longest 195 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.26 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [102, 102, 102], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0129/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 80, default): splits 95, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 3, merges 21, merge/split ratio 0.221, nucleations 23
- channel total drift (end/start - 1): [1.705, 3.3296, 1.4906, -0.7867]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 39 at frame 104: holes 0, rim-vs-core 0.44, rim-vs-outside 0.10, heterogeneity 0.07; core [0.603, 0.001, 0.0, 0.203] rim [0.16, 0.0, 0.0, 0.197]
  - track 41 at frame 104: holes 0, rim-vs-core 0.50, rim-vs-outside 0.09, heterogeneity 0.16; core [0.595, 0.0, 0.225, 0.074] rim [0.149, 0.0, 0.001, 0.125]
  - track 47 at frame 104: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.08; core [0.611, 0.001, 0.0, 0.219] rim [0.166, 0.0, 0.0, 0.213]
  - track 208 at frame 131: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.07; core [0.6, 0.001, 0.001, 0.178] rim [0.153, 0.0, 0.0, 0.171]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 581 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.504, rim/outside 2.99 (aggregate of 581 individuals; 0/581 membrane-like individually; rim level 0.475)
  - radial catalyst K1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.056, rim/outside 1.09 (aggregate of 581 individuals; 0/581 membrane-like individually; rim level 0.0047)
  - radial catalyst K2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.082, rim/outside 1.02 (aggregate of 581 individuals; 0/581 membrane-like individually; rim level 0.0034)
  - radial precursor Pp: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 1.02 (aggregate of 581 individuals; 0/581 membrane-like individually; rim level 0.171)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #39 (t=416, R_eq 4.95): none; #41 (t=416, R_eq 5.17): none; #47 (t=416, R_eq 5.01): none; #208 (t=524, R_eq 5.08): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
