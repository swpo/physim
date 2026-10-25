# Evidence pack: fch-micelle-chemoton-2k (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0936-c02-micelle-chemoton-sighting/world.py; mutation: two catalyst kinds K1, K2 that share the precursor and differ only in amphiphile yield (r2 = rr * r)
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [128, 128]; wall 1109s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds/world.py --out collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds/pack_k0.003/seed0 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1186, 2.9924], min area 6 px

## Measurements
- components: final 103, mean 93.8, max 103; occupancy final 0.49
- tracks: 273; persistent (alive >= 50% of run): 97; longest 195 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.20 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [103, 103, 103], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0205/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 80, default): splits 100, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 3, merges 34, merge/split ratio 0.34, nucleations 23
- channel total drift (end/start - 1): [1.7026, 3.4535, 0.9644, -0.756]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 43 at frame 104: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.08; core [0.602, 0.002, 0.0, 0.207] rim [0.155, 0.0, 0.0, 0.201]
  - track 51 at frame 104: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.08; core [0.61, 0.001, 0.0, 0.239] rim [0.164, 0.0, 0.0, 0.233]
  - track 69 at frame 104: holes 0, rim-vs-core 0.52, rim-vs-outside 0.19, heterogeneity 0.16; core [0.662, 0.32, 0.0, 0.063] rim [0.25, 0.011, 0.0, 0.137]
  - track 208 at frame 119: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.08; core [0.604, 0.001, 0.001, 0.211] rim [0.154, 0.0, 0.0, 0.207]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 596 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.504, rim/outside 2.71 (aggregate of 596 individuals; 1/596 membrane-like individually; rim level 0.471)
  - radial catalyst K1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.062, rim/outside 1 (aggregate of 596 individuals; 2/596 membrane-like individually; rim level 0.0047)
  - radial catalyst K2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.102, rim/outside 1.01 (aggregate of 596 individuals; 1/596 membrane-like individually; rim level 0.0035)
  - radial precursor Pp: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 1.02 (aggregate of 596 individuals; 0/596 membrane-like individually; rim level 0.201)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #43 (t=416, R_eq 5.05): none; #51 (t=416, R_eq 5.01): none; #69 (t=416, R_eq 4.98): none; #208 (t=476, R_eq 5.05): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
