# Evidence pack: lcn-cog (seed 1)

- world: `../../world_res.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [288, 288]; wall 240s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/cog/world_res.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/cog/pack_r15 --seeds 0 1 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 6, mean 10.9, max 37; occupancy final 0.04
- tracks: 244; persistent (alive >= 50% of run): 10; longest 190 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.33 (1 = constant size)
- enclosures: components with a hole mean 8.67, final 6; holes at thresholds 0.2/0.35/0.5 final [1, 35, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 6, 6], H1 [32, 8, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0164/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 100, default): splits 49, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 27, merge/split ratio 0.551, nucleations 12
- channel total drift (end/start - 1): [-0.9714, -0.9325, 0.4732, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 32 at frame 106: holes 6, rim-vs-core 0.71, rim-vs-outside 0.59, heterogeneity 0.24; core [0.932, 0.547, 0.847, 0.041] rim [0.25, 0.742, 0.856, 0.032]
  - track 54 at frame 108: holes 7, rim-vs-core 0.78, rim-vs-outside 0.60, heterogeneity 0.24; core [0.974, 0.525, 0.885, 0.036] rim [0.232, 0.757, 0.895, 0.026]
  - track 103 at frame 108: holes 7, rim-vs-core 0.73, rim-vs-outside 0.60, heterogeneity 0.24; core [0.95, 0.516, 0.817, 0.048] rim [0.254, 0.742, 0.827, 0.039]
  - track 234 at frame 170: holes 7, rim-vs-core 0.76, rim-vs-outside 0.61, heterogeneity 0.23; core [0.964, 0.562, 0.918, 0.048] rim [0.233, 0.76, 0.926, 0.038]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 60 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.141, rim/outside 4.47 (aggregate of 60 individuals; 1/60 membrane-like individually; rim level 0.102)
  - radial A1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.19, rim/outside 10.5 (aggregate of 60 individuals; 1/60 membrane-like individually; rim level 0.892)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.983 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.826)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.903, rim/outside 1.32 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.0835)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #32 (t=530, R_eq 13.13): none; #54 (t=540, R_eq 13.12): none; #103 (t=540, R_eq 12.77): none; #234 (t=850, R_eq 13.07): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
