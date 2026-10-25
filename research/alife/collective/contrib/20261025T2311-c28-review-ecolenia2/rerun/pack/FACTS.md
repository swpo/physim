# Evidence pack: eco-lenia2 (seed 5)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T2214-c26-eco-lenia2-claim/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 346s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2214-c26-eco-lenia2-claim/world.py --out /tmp/claude-0/c28eco/pack --seeds 5 --frames 500 --spf 20 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9991], min area 6 px

## Measurements
- components: final 34, mean 44.4, max 83; occupancy final 0.40
- tracks: 3234; persistent (alive >= 50% of run): 0; longest 245 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.80, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [102, 72, 38], H1 [11, 2, 1]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.112/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 40, default): splits 829, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 801, merge/split ratio 0.966, nucleations 809
- channel total drift (end/start - 1): [18.7092, 13.0591, 9.7789, 6.8404, 6.1211, 7.566, -0.3143]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2224 at frame 345: holes 0, rim-vs-core 0.24, rim-vs-outside 1.29, heterogeneity 0.09; core [0.0, 0.0, 0.0, 1.0, 0.834, 1.0, 0.68] rim [0.0, 0.0, 0.0, 0.824, 1.0, 0.982, 0.699]
  - track 2669 at frame 412: holes 0, rim-vs-core 0.48, rim-vs-outside 0.99, heterogeneity 0.39; core [0.385, 0.243, 0.253, 0.608, 0.276, 0.608, 0.61] rim [0.27, 0.311, 0.058, 0.574, 0.686, 0.658, 0.62]
  - track 677 at frame 130: holes 0, rim-vs-core 0.29, rim-vs-outside 1.28, heterogeneity 0.09; core [0.0, 0.0, 0.0, 1.0, 0.727, 1.0, 0.705] rim [0.0, 0.0, 0.0, 0.917, 1.0, 0.957, 0.724]
  - track 3143 at frame 487: holes 0, rim-vs-core 0.39, rim-vs-outside 0.76, heterogeneity 0.41; core [0.449, 0.281, 0.269, 0.531, 0.478, 0.551, 0.636] rim [0.487, 0.551, 0.099, 0.361, 0.432, 0.426, 0.63]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 214 components >= 12 px at frames [84, 168, 252, 332, 416, 500]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.635, rim/outside 2.87 (aggregate of 214 individuals; 26/214 membrane-like individually; rim level 0.207)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.942, rim/outside 1.55 (aggregate of 214 individuals; 42/214 membrane-like individually; rim level 0.246)
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.847, rim/outside 1.16 (aggregate of 214 individuals; 56/214 membrane-like individually; rim level 0.129)
  - radial B0: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.958, rim/outside 3.96 (aggregate of 214 individuals; 53/214 membrane-like individually; rim level 0.506)
  - radial B1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.4, rim/outside 2.48 (aggregate of 214 individuals; 84/214 membrane-like individually; rim level 0.504)
  - radial B2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 2.77 (aggregate of 214 individuals; 72/214 membrane-like individually; rim level 0.439)
  - radial F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 0.969 (aggregate of 214 individuals; 0/214 membrane-like individually; rim level 0.542)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2224 (t=690, R_eq 6.7): ['B1']; #2669 (t=824, R_eq 11.71): ['B0', 'B1', 'B2']; #677 (t=260, R_eq 6.43): ['B1']; #3143 (t=974, R_eq 9.54): ['A2']
- species `A` (channels ['A0'], own threshold): components final 29, mean 21.8, max 34; tracks 483, persistent 12; splits 132, persistent splits 10 (K=20), max generation 3, merges 94, merge/split 0.712; moving tracks 9
- species `B` (channels ['B0'], own threshold): components final 50, mean 55.6, max 82; tracks 2260, persistent 30; splits 502, persistent splits 4 (K=20), max generation 1, merges 420, merge/split 0.837; moving tracks 4

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 214 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
