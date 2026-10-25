# Evidence pack: lcn-cog (seed 6)

- world: `../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [192, 192]; wall 115s; status ok
- command: `python -m labkit.run world.py --out pack --seeds 6 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 12, mean 12.0, max 23; occupancy final 0.08
- tracks: 92; persistent (alive >= 50% of run): 12; longest 192 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.30 (1 = constant size)
- enclosures: components with a hole mean 9.62, final 10; holes at thresholds 0.2/0.35/0.5 final [0, 23, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 12, 12], H1 [27, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 100, default): splits 21, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 12, merge/split ratio 0.571, nucleations 6
- channel total drift (end/start - 1): [-0.9412, -0.866, 0.4467, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 106: holes 2, rim-vs-core 0.70, rim-vs-outside 0.47, heterogeneity 0.24; core [0.824, 0.456, 0.931, 0.036] rim [0.189, 0.748, 0.939, 0.028]
  - track 12 at frame 106: holes 0, rim-vs-core 0.65, rim-vs-outside 0.48, heterogeneity 0.24; core [0.841, 0.423, 0.916, 0.036] rim [0.256, 0.713, 0.924, 0.029]
  - track 24 at frame 106: holes 3, rim-vs-core 0.67, rim-vs-outside 0.48, heterogeneity 0.24; core [0.822, 0.484, 0.91, 0.041] rim [0.197, 0.731, 0.918, 0.032]
  - track 47 at frame 106: holes 2, rim-vs-core 0.66, rim-vs-outside 0.50, heterogeneity 0.24; core [0.704, 0.427, 0.941, 0.037] rim [0.158, 0.799, 0.948, 0.03]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 72 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.168, rim/outside 9.39 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.126)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.24, rim/outside 25 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.93)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.983 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.892)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 1.55 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.0672)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=530, R_eq 8.87): none; #12 (t=530, R_eq 8.96): none; #24 (t=530, R_eq 8.88): none; #47 (t=530, R_eq 8.81): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
