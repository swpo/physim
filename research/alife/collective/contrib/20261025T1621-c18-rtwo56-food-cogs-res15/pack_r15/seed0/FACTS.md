# Evidence pack: lcn-cog (seed 0)

- world: `../../world_res.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [288, 288]; wall 265s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/cog/world_res.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/cog/pack_r15 --seeds 0 1 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 3, mean 6.5, max 37; occupancy final 0.02
- tracks: 294; persistent (alive >= 50% of run): 4; longest 182 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.36 (1 = constant size)
- enclosures: components with a hole mean 5.33, final 3; holes at thresholds 0.2/0.35/0.5 final [2, 18, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 3, 3], H1 [16, 2, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 100, default): splits 75, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 40, merge/split ratio 0.533, nucleations 16
- channel total drift (end/start - 1): [-0.9864, -0.9671, 0.4861, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 187 at frame 111: holes 7, rim-vs-core 0.72, rim-vs-outside 0.61, heterogeneity 0.23; core [0.94, 0.574, 0.889, 0.036] rim [0.244, 0.751, 0.898, 0.027]
  - track 261 at frame 119: holes 6, rim-vs-core 0.74, rim-vs-outside 0.62, heterogeneity 0.23; core [0.962, 0.615, 0.904, 0.038] rim [0.239, 0.759, 0.912, 0.029]
  - track 288 at frame 123: holes 5, rim-vs-core 0.76, rim-vs-outside 0.62, heterogeneity 0.23; core [0.986, 0.608, 0.904, 0.034] rim [0.237, 0.759, 0.913, 0.025]
  - track 240 at frame 81: holes 6, rim-vs-core 0.73, rim-vs-outside 0.60, heterogeneity 0.23; core [0.951, 0.577, 0.858, 0.04] rim [0.238, 0.751, 0.868, 0.031]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 34 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.128, rim/outside 4.71 (aggregate of 34 individuals; 1/34 membrane-like individually; rim level 0.0932)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.23, rim/outside 22.2 (aggregate of 34 individuals; 1/34 membrane-like individually; rim level 0.904)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.968 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.806)
  - radial W: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 1.48 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.127)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #187 (t=555, R_eq 13.24): none; #261 (t=595, R_eq 13.04): none; #288 (t=615, R_eq 12.99): none; #240 (t=405, R_eq 13.17): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
