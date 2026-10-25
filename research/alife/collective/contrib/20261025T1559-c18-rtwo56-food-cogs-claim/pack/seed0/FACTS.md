# Evidence pack: lcn-cog (seed 0)

- world: `../../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [192, 192]; wall 109s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/cog/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/cog/pack --seeds 0 1 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 14, mean 13.6, max 18; occupancy final 0.09
- tracks: 62; persistent (alive >= 50% of run): 14; longest 192 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.27 (1 = constant size)
- enclosures: components with a hole mean 11.97, final 14; holes at thresholds 0.2/0.35/0.5 final [1, 31, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 14, 14], H1 [37, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 100, default): splits 15, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio 0.333, nucleations 6
- channel total drift (end/start - 1): [-0.9312, -0.8423, 0.4369, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 106: holes 0, rim-vs-core 0.66, rim-vs-outside 0.46, heterogeneity 0.24; core [0.775, 0.44, 0.89, 0.039] rim [0.193, 0.749, 0.898, 0.03]
  - track 25 at frame 106: holes 2, rim-vs-core 0.72, rim-vs-outside 0.51, heterogeneity 0.24; core [0.841, 0.453, 0.879, 0.039] rim [0.193, 0.755, 0.888, 0.031]
  - track 26 at frame 106: holes 2, rim-vs-core 0.73, rim-vs-outside 0.50, heterogeneity 0.24; core [0.838, 0.441, 0.87, 0.038] rim [0.179, 0.759, 0.878, 0.03]
  - track 30 at frame 106: holes 2, rim-vs-core 0.76, rim-vs-outside 0.47, heterogeneity 0.24; core [0.89, 0.402, 0.86, 0.053] rim [0.208, 0.742, 0.868, 0.042]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 84 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.179, rim/outside 8.23 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.136)
  - radial A1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.27, rim/outside 22.1 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.945)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.984 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.88)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.892, rim/outside 1.59 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.0614)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=530, R_eq 8.81): none; #25 (t=530, R_eq 8.88): none; #26 (t=530, R_eq 8.87): none; #30 (t=530, R_eq 8.54): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
