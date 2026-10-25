# Evidence pack: lcn (seed 5)

- world: `../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: closed nutrient ledger (losses return to food, no refill) + shell-gated food diffusion, full-domain noise
- run: 301 frames x 50 steps x dt 0.1 = time 1500; grid [192, 192]; wall 175s; status ok
- command: `python -m labkit.run world.py --out fromnoise --seeds 5 --frames 300 --spf 50 --no-movie`
- segmentation: matter > 0.30 of robust range [0.0, 0.9998], min area 6 px

## Measurements
- components: final 28, mean 22.3, max 39; occupancy final 0.22
- tracks: 1357; persistent (alive >= 50% of run): 0; longest 65 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 8.65, final 10; holes at thresholds 0.2/0.35/0.5 final [21, 17, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [54, 36, 29], H1 [40, 31, 12]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 100, default): splits 420, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 457, merge/split ratio 1.09, nucleations 14
- channel total drift (end/start - 1): [-0.6459, -0.4454, -0.196, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 43: holes 0, rim-vs-core 0.17, rim-vs-outside 1.02, heterogeneity 0.20; core [0.888, 0.295, 0.923, 0.04] rim [0.738, 0.213, 0.927, 0.038]
  - track 814 at frame 237: holes 0, rim-vs-core 0.12, rim-vs-outside 0.97, heterogeneity 0.21; core [0.892, 0.259, 0.7, 0.121] rim [0.777, 0.288, 0.694, 0.129]
  - track 1038 at frame 275: holes 0, rim-vs-core 0.12, rim-vs-outside 1.10, heterogeneity 0.20; core [0.867, 0.318, 0.79, 0.072] rim [0.819, 0.213, 0.776, 0.077]
  - track 188 at frame 131: holes 0, rim-vs-core 0.31, rim-vs-outside 0.89, heterogeneity 0.20; core [0.949, 0.247, 0.712, 0.11] rim [0.641, 0.234, 0.695, 0.123]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 146 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.44, rim/outside 12.9 (aggregate of 146 individuals; 81/146 membrane-like individually; rim level 0.739)
  - radial A1: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.46, rim/outside 2.35 (aggregate of 146 individuals; 44/146 membrane-like individually; rim level 0.685)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.16, rim/outside 0.905 (aggregate of 146 individuals; 0/146 membrane-like individually; rim level 0.443)
  - radial W: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.952, rim/outside 1.16 (aggregate of 146 individuals; 0/146 membrane-like individually; rim level 0.461)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=215, R_eq 6.18): ['A0']; #814 (t=1185, R_eq 6.15): none; #1038 (t=1375, R_eq 6.13): ['A0']; #188 (t=655, R_eq 5.89): ['A0']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 40 of 146 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
