# Evidence pack: eco-lenia2-dt (seed 5)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T2251-c26-eco-lenia2-dthalf/world_dt.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 251 frames x 40 steps x dt 0.1 = time 1000; grid [160, 160]; wall 312s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2251-c26-eco-lenia2-dthalf/world_dt.py --out /tmp/claude-0/c28ecodt/shared --seeds 5 --frames 250 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9995], min area 6 px

## Measurements
- components: final 47, mean 50.3, max 87; occupancy final 0.36
- tracks: 2221; persistent (alive >= 50% of run): 6; longest 175 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.36 (1 = constant size)
- enclosures: components with a hole mean 2.24, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 5]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [120, 75, 45], H1 [11, 3, 2]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0348/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 80, default): splits 583, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 565, merge/split ratio 0.969, nucleations 523
- channel total drift (end/start - 1): [17.5025, 12.8017, 9.3972, 5.963, 5.6955, 6.4315, -0.4088]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 117 at frame 101: holes 0, rim-vs-core 0.71, rim-vs-outside 1.26, heterogeneity 0.14; core [0.0, 0.0, 0.0, 1.0, 0.314, 0.922, 0.779] rim [0.0, 0.0, 0.0, 0.809, 0.99, 0.985, 0.797]
  - track 360 at frame 103: holes 0, rim-vs-core 0.58, rim-vs-outside 1.03, heterogeneity 0.12; core [0.0, 0.0, 0.0, 0.999, 0.435, 0.972, 0.614] rim [0.0, 0.0, 0.0, 0.721, 0.942, 0.998, 0.652]
  - track 193 at frame 88: holes 0, rim-vs-core 0.16, rim-vs-outside 1.33, heterogeneity 0.11; core [0.0, 0.0, 0.0, 1.0, 0.989, 0.784, 0.747] rim [0.0, 0.0, 0.0, 0.916, 0.934, 0.909, 0.755]
  - track 1496 at frame 204: holes 0, rim-vs-core 0.20, rim-vs-outside 1.25, heterogeneity 0.10; core [0.0, 0.0, 0.0, 1.0, 0.907, 1.0, 0.502] rim [0.0, 0.0, 0.0, 0.85, 1.0, 0.915, 0.504]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 255 components >= 12 px at frames [42, 84, 126, 166, 208, 250]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.628, rim/outside 3.41 (aggregate of 255 individuals; 23/255 membrane-like individually; rim level 0.146)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.898, rim/outside 1.74 (aggregate of 255 individuals; 38/255 membrane-like individually; rim level 0.171)
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 1.08 (aggregate of 255 individuals; 55/255 membrane-like individually; rim level 0.0936)
  - radial B0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.96, rim/outside 4.97 (aggregate of 255 individuals; 45/255 membrane-like individually; rim level 0.592)
  - radial B1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 2.71 (aggregate of 255 individuals; 92/255 membrane-like individually; rim level 0.56)
  - radial B2: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 3.75 (aggregate of 255 individuals; 81/255 membrane-like individually; rim level 0.525)
  - radial F: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 0.962 (aggregate of 255 individuals; 0/255 membrane-like individually; rim level 0.497)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #117 (t=404, R_eq 6.6): ['B1', 'B2']; #360 (t=412, R_eq 6.6): none; #193 (t=352, R_eq 6.56): none; #1496 (t=816, R_eq 6.63): ['B1']
- species `A` (channels ['A0'], own threshold): components final 27, mean 16.4, max 28; tracks 249, persistent 6; splits 75, persistent splits 8 (K=20), max generation 4, merges 47, merge/split 0.627; moving tracks 7
- species `B` (channels ['B0'], own threshold): components final 58, mean 58.9, max 91; tracks 1690, persistent 25; splits 398, persistent splits 5 (K=20), max generation 2, merges 344, merge/split 0.864; moving tracks 2

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 16 of 255 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
