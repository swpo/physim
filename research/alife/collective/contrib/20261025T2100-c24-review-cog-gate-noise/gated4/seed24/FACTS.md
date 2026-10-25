# Evidence pack: lcn-cog (seed 24)

- world: `../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 105s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/20261025T2100-c24-review-cog-gate-noise/gated4/seed24 --seeds 24 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 2, mean 2.9, max 16; occupancy final 0.01
- tracks: 70; persistent (alive >= 50% of run): 2; longest 88 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.17 (1 = constant size)
- enclosures: components with a hole mean 2.11, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [4, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 100, default): splits 18, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 0.222, nucleations 0
- channel total drift (end/start - 1): [-0.9901, -0.9774, 0.4916, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 37 at frame 57: holes 1, rim-vs-core 0.48, rim-vs-outside 0.54, heterogeneity 0.27; core [0.651, 0.452, 0.597, 0.074] rim [0.268, 0.727, 0.708, 0.058]
  - track 45 at frame 57: holes 0, rim-vs-core 0.75, rim-vs-outside 0.46, heterogeneity 0.27; core [0.748, 0.385, 0.607, 0.069] rim [0.135, 0.805, 0.736, 0.056]
  - track 27 at frame 16: holes 4, rim-vs-core 0.55, rim-vs-outside 0.61, heterogeneity 0.31; core [0.726, 0.029, 0.0, 0.824] rim [0.475, 0.495, 0.073, 0.706]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 16 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.213, rim/outside 15.4 (aggregate of 16 individuals; 3/16 membrane-like individually; rim level 0.144)
  - radial A1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 60 (aggregate of 16 individuals; 3/16 membrane-like individually; rim level 0.856)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.9, rim/outside 0.909 (aggregate of 16 individuals; 0/16 membrane-like individually; rim level 0.705)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.46 (aggregate of 16 individuals; 0/16 membrane-like individually; rim level 0.327)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #37 (t=285, R_eq 8.96): none; #45 (t=285, R_eq 8.72): none; #27 (t=80, R_eq 17.01, ring): ['A0', 'A1']; #0 (t=20, R_eq 96.8): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 16 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
