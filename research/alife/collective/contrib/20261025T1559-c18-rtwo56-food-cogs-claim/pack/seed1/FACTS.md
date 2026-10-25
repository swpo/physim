# Evidence pack: lcn-cog (seed 1)

- world: `../../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [192, 192]; wall 104s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/cog/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/cog/pack --seeds 0 1 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 11, mean 11.4, max 23; occupancy final 0.07
- tracks: 102; persistent (alive >= 50% of run): 11; longest 192 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.43 (1 = constant size)
- enclosures: components with a hole mean 9.03, final 10; holes at thresholds 0.2/0.35/0.5 final [0, 22, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 11, 11], H1 [28, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 100, default): splits 28, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 19, merge/split ratio 0.679, nucleations 4
- channel total drift (end/start - 1): [-0.9459, -0.8759, 0.4505, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 106: holes 2, rim-vs-core 0.76, rim-vs-outside 0.47, heterogeneity 0.24; core [0.906, 0.439, 0.888, 0.039] rim [0.204, 0.742, 0.897, 0.031]
  - track 28 at frame 106: holes 5, rim-vs-core 0.78, rim-vs-outside 0.50, heterogeneity 0.24; core [0.884, 0.387, 0.896, 0.041] rim [0.204, 0.767, 0.903, 0.033]
  - track 56 at frame 106: holes 1, rim-vs-core 0.76, rim-vs-outside 0.48, heterogeneity 0.24; core [0.905, 0.439, 0.919, 0.036] rim [0.203, 0.734, 0.927, 0.027]
  - track 60 at frame 108: holes 0, rim-vs-core 0.73, rim-vs-outside 0.49, heterogeneity 0.24; core [0.742, 0.387, 0.874, 0.046] rim [0.146, 0.802, 0.88, 0.038]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 69 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.134, rim/outside 9.93 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.098)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 24.2 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.948)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.98 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.88)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.925, rim/outside 1.56 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.0786)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=530, R_eq 8.72): none; #28 (t=530, R_eq 8.72): none; #56 (t=530, R_eq 8.92): none; #60 (t=540, R_eq 8.87): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
