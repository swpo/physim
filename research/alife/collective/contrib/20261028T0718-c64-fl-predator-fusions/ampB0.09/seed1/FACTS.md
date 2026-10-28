# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 655s; status ok
- command: `python -m labkit.run /tmp/claude-0/pd/world.py --out /tmp/claude-0/pd/b0.09/seed1 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0017, 1.8825], min area 6 px

## Measurements
- components: final 22, mean 23.0, max 58; occupancy final 0.10
- tracks: 2385; persistent (alive >= 50% of run): 0; longest 102 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.68, final 1; holes at thresholds 0.2/0.35/0.5 final [6, 10, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 24, 18], H1 [14, 7, 0]
- motion: 56 long-lived tracks moved >= 1 body length; max speed 0.855/time; max body lengths 14.2
- replication (lineage window K = 20 frames = time 100, default): splits 758, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 780, merge/split ratio 1.03, nucleations 223
- channel total drift (end/start - 1): [-0.1958, None, -0.0717, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 825 at frame 242: holes 0, rim-vs-core 0.48, rim-vs-outside 0.07, heterogeneity 0.09; core [0.001, 0.553, 0.974, 0.024] rim [0.001, 0.075, 0.97, 0.016]
  - track 1731 at frame 469: holes 0, rim-vs-core 0.56, rim-vs-outside 0.08, heterogeneity 0.10; core [0.002, 0.643, 0.911, 0.044] rim [0.003, 0.084, 0.903, 0.029]
  - track 1648 at frame 444: holes 0, rim-vs-core 0.47, rim-vs-outside 0.10, heterogeneity 0.09; core [0.002, 0.58, 0.966, 0.054] rim [0.003, 0.109, 0.964, 0.037]
  - track 2163 at frame 575: holes 0, rim-vs-core 0.47, rim-vs-outside 0.06, heterogeneity 0.10; core [0.005, 0.534, 0.931, 0.106] rim [0.007, 0.065, 0.928, 0.067]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 127 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 11.8 (aggregate of 127 individuals; 27/127 membrane-like individually; rim level 0.296)
  - radial predator B: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 2.56, rim/outside 10.8 (aggregate of 127 individuals; 48/127 membrane-like individually; rim level 0.271)  MEMBRANE-LIKE
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.64, rim/outside 0.908 (aggregate of 127 individuals; 0/127 membrane-like individually; rim level 0.706)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.712, rim/outside 3.38 (aggregate of 127 individuals; 0/127 membrane-like individually; rim level 0.089)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): predator B
- membrane-like channels per top track at mid-life: #825 (t=1210, R_eq 5.08): ['predator B']; #1731 (t=2345, R_eq 3.99): ['predator B']; #1648 (t=2220, R_eq 5.89, ring): ['predator B']; #2163 (t=2875, R_eq 5.01): ['predator B']
- species `prey` (channels ['prey A'], own threshold): components final 15, mean 16.8, max 52; tracks 1175, persistent 0; splits 396, persistent splits 6 (K=20), max generation 5, merges 363, merge/split 0.917; moving tracks 137
- species `predator` (channels ['predator B'], own threshold): components final 10, mean 9.1, max 12; tracks 70, persistent 7; splits 16, persistent splits 2 (K=20), max generation 1, merges 15, merge/split 0.938; moving tracks 18

## Warnings
- radial: 13 of 127 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
