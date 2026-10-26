# Evidence pack: lcn-cog (seed 25)

- world: `../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 107s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/20261025T2100-c24-review-cog-gate-noise/ungated/seed25 --seeds 25 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 16, mean 15.6, max 26; occupancy final 0.11
- tracks: 79; persistent (alive >= 50% of run): 16; longest 93 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.31 (1 = constant size)
- enclosures: components with a hole mean 12.49, final 14; holes at thresholds 0.2/0.35/0.5 final [0, 33, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 16, 16], H1 [50, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 100, default): splits 21, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 7, merge/split ratio 0.333, nucleations 3
- channel total drift (end/start - 1): [-0.921, -0.819, 0.4255, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 54: holes 3, rim-vs-core 0.53, rim-vs-outside 0.53, heterogeneity 0.24; core [0.731, 0.451, 0.875, 0.049] rim [0.278, 0.731, 0.882, 0.043]
  - track 9 at frame 55: holes 2, rim-vs-core 0.75, rim-vs-outside 0.53, heterogeneity 0.24; core [0.827, 0.405, 0.878, 0.062] rim [0.181, 0.784, 0.892, 0.046]
  - track 18 at frame 55: holes 2, rim-vs-core 0.66, rim-vs-outside 0.54, heterogeneity 0.24; core [0.787, 0.455, 0.841, 0.049] rim [0.202, 0.761, 0.849, 0.041]
  - track 19 at frame 55: holes 2, rim-vs-core 0.65, rim-vs-outside 0.50, heterogeneity 0.24; core [0.756, 0.468, 0.816, 0.05] rim [0.182, 0.765, 0.825, 0.043]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 100 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.155, rim/outside 8.67 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.117)
  - radial A1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.27, rim/outside 26.7 (aggregate of 100 individuals; 1/100 membrane-like individually; rim level 0.938)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.963 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.763)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.958, rim/outside 1.27 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.174)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=270, R_eq 8.85): none; #9 (t=275, R_eq 8.85): none; #18 (t=275, R_eq 8.92): none; #19 (t=275, R_eq 8.92): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 100 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
