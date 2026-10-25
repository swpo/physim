# Evidence pack: lcn-cog (seed 7)

- world: `../../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 121 frames x 50 steps x dt 0.1 = time 600; grid [96, 96]; wall 17s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1721-c13-review-cog-no-fission/world.py --out collective/contrib/20261025T1721-c13-review-cog-no-fission/rerun/seed7 --seeds 7 --spf 50 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 3, mean 3.0, max 6; occupancy final 0.08
- tracks: 30; persistent (alive >= 50% of run): 3; longest 105 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.37 (1 = constant size)
- enclosures: components with a hole mean 2.68, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 6, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [8, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 100, default): splits 10, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio 0.5, nucleations 1
- channel total drift (end/start - 1): [-0.9414, -0.8643, 0.4479, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 69: holes 2, rim-vs-core 0.70, rim-vs-outside 0.50, heterogeneity 0.24; core [0.85, 0.475, 0.93, 0.037] rim [0.2, 0.744, 0.938, 0.03]
  - track 27 at frame 69: holes 1, rim-vs-core 0.57, rim-vs-outside 0.52, heterogeneity 0.24; core [0.65, 0.306, 0.942, 0.035] rim [0.286, 0.749, 0.945, 0.031]
  - track 29 at frame 69: holes 1, rim-vs-core 0.66, rim-vs-outside 0.48, heterogeneity 0.24; core [0.881, 0.524, 0.93, 0.037] rim [0.249, 0.702, 0.936, 0.03]
  - track 4 at frame 12: holes 1, rim-vs-core 0.36, rim-vs-outside 0.49, heterogeneity 0.27; core [0.753, 0.585, 0.012, 0.821] rim [0.4, 0.631, 0.046, 0.791]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 18 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial A0: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.069, rim/outside 5.7 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.047)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 88.5 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.97)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.966 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.855)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.943, rim/outside 1.45 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.144)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #23 (t=345, R_eq 8.87): none; #27 (t=345, R_eq 8.96): none; #29 (t=345, R_eq 8.94): none; #4 (t=60, R_eq 12.37, ring): ['A1']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
