# Evidence pack: lcn (seed 0)

- world: `../../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: closed nutrient ledger (losses return to food, no refill) + shell-gated food diffusion, full-domain noise
- run: 301 frames x 50 steps x dt 0.1 = time 1500; grid [192, 192]; wall 154s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/lcn/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/lcn/pack --seeds 0 1 --frames 300 --spf 50 --no-movie`
- segmentation: matter > 0.30 of robust range [0.0, 0.9998], min area 6 px

## Measurements
- components: final 33, mean 27.9, max 41; occupancy final 0.25
- tracks: 1551; persistent (alive >= 50% of run): 0; longest 58 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 11.09, final 10; holes at thresholds 0.2/0.35/0.5 final [16, 22, 22]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [68, 43, 35], H1 [54, 44, 15]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 100, default): splits 481, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 537, merge/split ratio 1.12, nucleations 17
- channel total drift (end/start - 1): [-0.6071, -0.3903, -0.2059, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 528 at frame 161: holes 0, rim-vs-core 0.14, rim-vs-outside 0.98, heterogeneity 0.22; core [0.882, 0.274, 0.73, 0.11] rim [0.743, 0.266, 0.722, 0.119]
  - track 942 at frame 222: holes 0, rim-vs-core 0.13, rim-vs-outside 0.96, heterogeneity 0.21; core [0.886, 0.293, 0.693, 0.129] rim [0.756, 0.278, 0.695, 0.132]
  - track 850 at frame 207: holes 0, rim-vs-core 0.11, rim-vs-outside 0.96, heterogeneity 0.21; core [0.872, 0.244, 0.823, 0.062] rim [0.783, 0.306, 0.814, 0.069]
  - track 288 at frame 111: holes 0, rim-vs-core 0.37, rim-vs-outside 1.07, heterogeneity 0.19; core [0.951, 0.249, 0.691, 0.151] rim [0.625, 0.074, 0.688, 0.159]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 174 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.48, rim/outside 13.7 (aggregate of 174 individuals; 111/174 membrane-like individually; rim level 0.759)
  - radial A1: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 2.23 (aggregate of 174 individuals; 50/174 membrane-like individually; rim level 0.702)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 0.907 (aggregate of 174 individuals; 0/174 membrane-like individually; rim level 0.451)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.956, rim/outside 1.15 (aggregate of 174 individuals; 0/174 membrane-like individually; rim level 0.455)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #528 (t=805, R_eq 6.18): ['A0']; #942 (t=1110, R_eq 6.18): ['A0']; #850 (t=1035, R_eq 6.21): ['A0']; #288 (t=555, R_eq 5.89): ['A0']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 51 of 174 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
