# Evidence pack: flow-lenia-digestion-ecology-thetaB (seed 1)

- world: `../world_th.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 607s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fus/world_th.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fus/th12 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0021, 1.8687], min area 6 px

## Measurements
- components: final 20, mean 25.2, max 94; occupancy final 0.12
- tracks: 2446; persistent (alive >= 50% of run): 0; longest 127 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 11, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 22, 13], H1 [9, 1, 0]
- motion: 31 long-lived tracks moved >= 1 body length; max speed 0.862/time; max body lengths 14.2
- replication (lineage window K = 20 frames = time 100, default): splits 772, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 770, merge/split ratio 0.997, nucleations 234
- channel total drift (end/start - 1): [-0.2825, None, -0.0679, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1606 at frame 413: holes 0, rim-vs-core 0.40, rim-vs-outside 0.25, heterogeneity 0.08; core [0.003, 0.658, 0.948, 0.052] rim [0.005, 0.253, 0.939, 0.036]
  - track 336 at frame 81: holes 0, rim-vs-core 0.50, rim-vs-outside 0.08, heterogeneity 0.09; core [0.004, 0.585, 0.922, 0.039] rim [0.005, 0.086, 0.917, 0.024]
  - track 1258 at frame 297: holes 0, rim-vs-core 0.42, rim-vs-outside 0.15, heterogeneity 0.07; core [0.004, 0.57, 0.935, 0.05] rim [0.006, 0.149, 0.93, 0.032]
  - track 1270 at frame 297: holes 0, rim-vs-core 0.55, rim-vs-outside 0.08, heterogeneity 0.09; core [0.006, 0.646, 0.927, 0.055] rim [0.008, 0.091, 0.925, 0.035]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 129 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 8.16 (aggregate of 129 individuals; 28/129 membrane-like individually; rim level 0.195)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.94, rim/outside 14.7 (aggregate of 129 individuals; 24/129 membrane-like individually; rim level 0.312)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.31, rim/outside 0.939 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.751)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.766, rim/outside 4.28 (aggregate of 129 individuals; 1/129 membrane-like individually; rim level 0.125)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1606 (t=2065, R_eq 8.06): none; #336 (t=405, R_eq 4.33): none; #1258 (t=1485, R_eq 5.47): ['predator B']; #1270 (t=1485, R_eq 3.7): none
- species `prey` (channels ['prey A'], own threshold): components final 12, mean 14.1, max 52; tracks 831, persistent 0; splits 247, persistent splits 2 (K=20), max generation 2, merges 225, merge/split 0.911; moving tracks 118
- species `predator` (channels ['predator B'], own threshold): components final 13, mean 14.9, max 21; tracks 82, persistent 12; splits 13, persistent splits 3 (K=20), max generation 1, merges 23, merge/split 1.77; moving tracks 29

## Warnings
- radial: 1 of 129 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
