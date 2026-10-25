# Evidence pack: lcn-cog (seed 7)

- world: `../../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 54s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/wip-c22/rev_cog/gated/seed7 --seeds 7 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 0, mean 2.1, max 28; occupancy final 0.00
- tracks: 101; persistent (alive >= 50% of run): 0; longest 19 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.23, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 100, default): splits 24, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 9, merge/split ratio 0.375, nucleations 4
- channel total drift (end/start - 1): [-1.0, -1.0, 0.5003, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 19: holes 4, rim-vs-core 0.66, rim-vs-outside 0.52, heterogeneity 0.29; core [0.832, 0.501, 0.236, 0.338] rim [0.22, 0.749, 0.303, 0.347]
  - track 27 at frame 14: holes 2, rim-vs-core 0.38, rim-vs-outside 0.53, heterogeneity 0.31; core [0.758, 0.489, 0.027, 0.746] rim [0.416, 0.625, 0.089, 0.663]
  - track 58 at frame 14: holes 0, rim-vs-core 1.02, rim-vs-outside 0.51, heterogeneity 0.29; core [0.875, 0.312, 0.158, 0.49] rim [0.047, 0.895, 0.104, 0.538]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [17]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.64, rim/outside 8.6 (aggregate of 6 individuals; 2/6 membrane-like individually; rim level 0.281)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.34, rim/outside 6.39 (aggregate of 6 individuals; 3/6 membrane-like individually; rim level 0.566)
  - radial F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 6.15, rim/outside 0.61 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.277)
  - radial W: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 1.38 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.77)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #33 (t=95, R_eq 8.23): none; #86 (t=100, R_eq 6.91, ring): none; #27 (t=70, R_eq 10.7, ring): ['A1']; #58 (t=70, R_eq 7.82): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 6 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
