# Evidence pack: lcn-cog (seed 6)

- world: `../../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 57s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/wip-c22/rev_cog/slowD/seed6 --seeds 6 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 3, mean 4.6, max 24; occupancy final 0.02
- tracks: 69; persistent (alive >= 50% of run): 4; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.96 (1 = constant size)
- enclosures: components with a hole mean 2.72, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 5, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [8, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 100, default): splits 15, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 0.4, nucleations 3
- channel total drift (end/start - 1): [-0.9853, -0.9664, 0.4868, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 55: holes 1, rim-vs-core 0.69, rim-vs-outside 0.58, heterogeneity 0.28; core [0.731, 0.42, 0.357, 0.066] rim [0.16, 0.798, 0.429, 0.054]
  - track 52 at frame 56: holes 2, rim-vs-core 0.80, rim-vs-outside 0.55, heterogeneity 0.27; core [0.94, 0.442, 0.296, 0.079] rim [0.215, 0.746, 0.454, 0.057]
  - track 57 at frame 57: holes 3, rim-vs-core 0.80, rim-vs-outside 0.55, heterogeneity 0.28; core [0.941, 0.451, 0.281, 0.074] rim [0.216, 0.744, 0.462, 0.06]
  - track 51 at frame 40: holes 1, rim-vs-core 0.88, rim-vs-outside 0.59, heterogeneity 0.29; core [0.724, 0.381, 0.355, 0.111] rim [0.035, 0.922, 0.412, 0.104]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 27 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.215, rim/outside 17.4 (aggregate of 27 individuals; 1/27 membrane-like individually; rim level 0.164)
  - radial A1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.26, rim/outside 49.7 (aggregate of 27 individuals; 2/27 membrane-like individually; rim level 0.892)
  - radial F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 4.13, rim/outside 0.847 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.604)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.53 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.246)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=275, R_eq 8.94): none; #52 (t=280, R_eq 8.76): none; #57 (t=285, R_eq 8.74): none; #51 (t=200, R_eq 8.43): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 27 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
