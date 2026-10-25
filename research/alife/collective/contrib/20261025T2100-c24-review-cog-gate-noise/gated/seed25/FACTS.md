# Evidence pack: lcn-cog (seed 25)

- world: `../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 106s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/20261025T2100-c24-review-cog-gate-noise/gated/seed25 --seeds 25 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 0, mean 1.7, max 23; occupancy final 0.00
- tracks: 79; persistent (alive >= 50% of run): 0; longest 22 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.98, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 100, default): splits 22, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 0.273, nucleations 2
- channel total drift (end/start - 1): [-1.0, -1.0, 0.4978, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 22: holes 4, rim-vs-core 0.68, rim-vs-outside 0.60, heterogeneity 0.29; core [0.833, 0.479, 0.207, 0.382] rim [0.219, 0.758, 0.307, 0.322]
  - track 40 at frame 16: holes 0, rim-vs-core 0.67, rim-vs-outside 0.45, heterogeneity 0.29; core [0.77, 0.41, 0.162, 0.5] rim [0.2, 0.757, 0.141, 0.481]
  - track 4 at frame 12: holes 0, rim-vs-core 0.61, rim-vs-outside 0.50, heterogeneity 0.29; core [0.715, 0.347, 0.136, 0.541] rim [0.263, 0.762, 0.098, 0.562]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 4 components >= 12 px at frames [17]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.472, rim/outside 33.9 (aggregate of 4 individuals; 1/4 membrane-like individually; rim level 0.33)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 4.57 (aggregate of 4 individuals; 1/4 membrane-like individually; rim level 0.704)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.67, rim/outside 0.834 (aggregate of 4 individuals; 0/4 membrane-like individually; rim level 0.402)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 1.3 (aggregate of 4 individuals; 0/4 membrane-like individually; rim level 0.659)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #38 (t=110, R_eq 8.63): none; #40 (t=80, R_eq 8.16): none; #4 (t=60, R_eq 8.08): none; #0 (t=15, R_eq 97.36): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
