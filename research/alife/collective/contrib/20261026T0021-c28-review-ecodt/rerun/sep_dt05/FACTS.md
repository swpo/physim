# Evidence pack: eco-lenia2-dt (seed 5)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T2251-c26-eco-lenia2-dthalf/world_dt.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 251 frames x 40 steps x dt 0.1 = time 1000; grid [160, 160]; wall 315s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2251-c26-eco-lenia2-dthalf/world_dt.py --out /tmp/claude-0/c28ecodt/sep --seeds 5 --frames 250 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.999], min area 6 px

## Measurements
- components: final 46, mean 43.3, max 60; occupancy final 0.27
- tracks: 918; persistent (alive >= 50% of run): 23; longest 193 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.12 (1 = constant size)
- enclosures: components with a hole mean 1.27, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [67, 46, 32], H1 [2, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.112/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 80, default): splits 209, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 218, merge/split ratio 1.04, nucleations 288
- channel total drift (end/start - 1): [19.7153, 14.121, 9.5907, 6.9947, 6.2187, 7.387, -0.1317]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 497 at frame 155: holes 0, rim-vs-core 0.60, rim-vs-outside 0.72, heterogeneity 0.38; core [0.876, 0.689, 0.443, 0.837, 0.844, 0.831, 0.739] rim [0.547, 0.689, 0.166, 0.554, 0.712, 0.554, 0.765]
  - track 536 at frame 158: holes 0, rim-vs-core 0.54, rim-vs-outside 0.76, heterogeneity 0.38; core [0.912, 0.707, 0.245, 0.846, 0.628, 0.879, 0.646] rim [0.614, 0.764, 0.265, 0.537, 0.665, 0.568, 0.668]
  - track 627 at frame 164: holes 0, rim-vs-core 0.62, rim-vs-outside 0.89, heterogeneity 0.35; core [0.998, 0.668, 0.296, 0.932, 0.873, 0.414, 0.677] rim [0.64, 0.861, 0.158, 0.565, 0.612, 0.434, 0.7]
  - track 811 at frame 189: holes 0, rim-vs-core 0.67, rim-vs-outside 0.71, heterogeneity 0.25; core [1.0, 0.571, 0.57, 0.036, 0.0, 0.026, 0.675] rim [0.899, 1.0, 0.079, 0.123, 0.068, 0.082, 0.697]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 266 components >= 12 px at frames [42, 84, 126, 166, 208, 250]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.669, rim/outside 9.56 (aggregate of 266 individuals; 13/266 membrane-like individually; rim level 0.379)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.898, rim/outside 3.96 (aggregate of 266 individuals; 54/266 membrane-like individually; rim level 0.425)
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.706, rim/outside 2.22 (aggregate of 266 individuals; 90/266 membrane-like individually; rim level 0.201)
  - radial B0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.84, rim/outside 7.05 (aggregate of 266 individuals; 15/266 membrane-like individually; rim level 0.667)
  - radial B1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 3.89 (aggregate of 266 individuals; 87/266 membrane-like individually; rim level 0.622)
  - radial B2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 5.42 (aggregate of 266 individuals; 38/266 membrane-like individually; rim level 0.635)
  - radial F: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 0.964 (aggregate of 266 individuals; 0/266 membrane-like individually; rim level 0.674)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #497 (t=620, R_eq 7.2): none; #536 (t=632, R_eq 7.25): ['A1', 'B1']; #627 (t=656, R_eq 7): ['A1', 'B2']; #811 (t=756, R_eq 6.21): ['A1']
- species `A` (channels ['A0'], own threshold): components final 31, mean 24.0, max 36; tracks 273, persistent 22; splits 90, persistent splits 11 (K=20), max generation 3, merges 49, merge/split 0.544; moving tracks 4
- species `B` (channels ['B0'], own threshold): components final 58, mean 57.4, max 80; tracks 1336, persistent 38; splits 285, persistent splits 1 (K=20), max generation 1, merges 235, merge/split 0.825; moving tracks 3

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 266 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
