# Evidence pack: lcn-cog (seed 4)

- world: `../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 76s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/20261025T1921-c19-cog-gate-from-noise/gated/seed4 --seeds 4 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 2, mean 4.1, max 19; occupancy final 0.01
- tracks: 101; persistent (alive >= 50% of run): 2; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.14 (1 = constant size)
- enclosures: components with a hole mean 3.24, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 5, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [5, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.36/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 100, default): splits 30, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 12, merge/split ratio 0.4, nucleations 3
- channel total drift (end/start - 1): [-0.9902, -0.9773, 0.4906, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 55: holes 1, rim-vs-core 0.71, rim-vs-outside 0.55, heterogeneity 0.27; core [0.8, 0.43, 0.529, 0.076] rim [0.179, 0.759, 0.592, 0.059]
  - track 43 at frame 56: holes 3, rim-vs-core 0.75, rim-vs-outside 0.51, heterogeneity 0.28; core [0.888, 0.439, 0.484, 0.078] rim [0.208, 0.734, 0.6, 0.057]
  - track 67 at frame 27: holes 3, rim-vs-core 0.40, rim-vs-outside 0.54, heterogeneity 0.34; core [0.686, 0.372, 0.137, 0.561] rim [0.389, 0.63, 0.201, 0.562]
  - track 94 at frame 50: holes 2, rim-vs-core 0.40, rim-vs-outside 0.53, heterogeneity 0.36; core [0.719, 0.435, 0.218, 0.417] rim [0.381, 0.621, 0.306, 0.414]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 21 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.4, rim/outside 9.41 (aggregate of 21 individuals; 5/21 membrane-like individually; rim level 0.234)
  - radial A1: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 23 (aggregate of 21 individuals; 7/21 membrane-like individually; rim level 0.804)  MEMBRANE-LIKE
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.8, rim/outside 0.858 (aggregate of 21 individuals; 0/21 membrane-like individually; rim level 0.668)
  - radial W: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside 1.62 (aggregate of 21 individuals; 0/21 membrane-like individually; rim level 0.383)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #15 (t=275, R_eq 8.96): none; #43 (t=280, R_eq 8.74): none; #67 (t=135, R_eq 13.89, ring): ['A0', 'A1']; #94 (t=250, R_eq 13.15, ring): ['A0', 'A1']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 21 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
