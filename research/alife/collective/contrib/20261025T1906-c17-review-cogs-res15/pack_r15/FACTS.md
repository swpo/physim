# Evidence pack: lcn-cog (seed 3)

- world: `../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [288, 288]; wall 270s; status ok
- command: `python -m labkit.run world.py --out pack_r15 --seeds 3 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 10, mean 10.2, max 33; occupancy final 0.06
- tracks: 196; persistent (alive >= 50% of run): 9; longest 191 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.24 (1 = constant size)
- enclosures: components with a hole mean 9.00, final 9; holes at thresholds 0.2/0.35/0.5 final [4, 52, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 11, 9], H1 [48, 9, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 100, default): splits 38, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 22, merge/split ratio 0.579, nucleations 23
- channel total drift (end/start - 1): [-0.9571, -0.8998, 0.4609, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 44 at frame 106: holes 6, rim-vs-core 0.74, rim-vs-outside 0.61, heterogeneity 0.23; core [0.962, 0.615, 0.908, 0.035] rim [0.237, 0.761, 0.918, 0.025]
  - track 59 at frame 106: holes 9, rim-vs-core 0.75, rim-vs-outside 0.60, heterogeneity 0.23; core [0.963, 0.584, 0.913, 0.04] rim [0.237, 0.756, 0.923, 0.029]
  - track 118 at frame 108: holes 6, rim-vs-core 0.75, rim-vs-outside 0.61, heterogeneity 0.23; core [0.966, 0.575, 0.908, 0.038] rim [0.238, 0.759, 0.918, 0.029]
  - track 131 at frame 109: holes 4, rim-vs-core 0.68, rim-vs-outside 0.60, heterogeneity 0.23; core [0.95, 0.667, 0.874, 0.04] rim [0.268, 0.732, 0.883, 0.031]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 55 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.136, rim/outside 9.21 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.106)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.31, rim/outside 20.5 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.97)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.985 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.879)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 1.43 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.0621)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #44 (t=530, R_eq 13.04): none; #59 (t=530, R_eq 13.09): none; #118 (t=540, R_eq 13.1): none; #131 (t=545, R_eq 12.87): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
