# Evidence pack: lcn-cog (seed 6)

- world: `../../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 53s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/wip-c22/rev_cog/ungated/seed6 --seeds 6 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 12, mean 12.0, max 23; occupancy final 0.08
- tracks: 92; persistent (alive >= 50% of run): 12; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.30 (1 = constant size)
- enclosures: components with a hole mean 8.83, final 11; holes at thresholds 0.2/0.35/0.5 final [0, 27, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 12, 12], H1 [31, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 100, default): splits 21, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 12, merge/split ratio 0.571, nucleations 6
- channel total drift (end/start - 1): [-0.9412, -0.866, 0.4462, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 55: holes 1, rim-vs-core 0.70, rim-vs-outside 0.48, heterogeneity 0.24; core [0.862, 0.482, 0.909, 0.046] rim [0.209, 0.732, 0.917, 0.038]
  - track 12 at frame 55: holes 0, rim-vs-core 0.63, rim-vs-outside 0.49, heterogeneity 0.24; core [0.846, 0.436, 0.894, 0.048] rim [0.273, 0.701, 0.902, 0.042]
  - track 24 at frame 55: holes 1, rim-vs-core 0.75, rim-vs-outside 0.47, heterogeneity 0.24; core [0.853, 0.419, 0.89, 0.05] rim [0.184, 0.752, 0.897, 0.042]
  - track 47 at frame 56: holes 2, rim-vs-core 0.69, rim-vs-outside 0.48, heterogeneity 0.24; core [0.779, 0.417, 0.911, 0.053] rim [0.186, 0.777, 0.92, 0.046]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.214, rim/outside 7.91 (aggregate of 79 individuals; 2/79 membrane-like individually; rim level 0.158)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.21, rim/outside 18.2 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.902)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.954 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.747)
  - radial W: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.979, rim/outside 1.25 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.213)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=275, R_eq 8.88): none; #12 (t=275, R_eq 8.92): none; #24 (t=275, R_eq 8.83): none; #47 (t=280, R_eq 8.72): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
