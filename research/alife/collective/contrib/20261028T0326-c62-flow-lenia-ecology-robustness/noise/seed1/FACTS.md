# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 610s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261028T0303-c62-flow-lenia-ecology-claim/world.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim2/noise/seed1 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.06 of robust range [0.0023, 2.3704], min area 6 px

## Measurements
- components: final 28, mean 34.0, max 83; occupancy final 0.21
- tracks: 7453; persistent (alive >= 50% of run): 0; longest 34 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.30, final 1; holes at thresholds 0.2/0.35/0.5 final [11, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [62, 38, 28], H1 [18, 6, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.611/time; max body lengths 11.5
- replication (lineage window K = 20 frames = time 100, default): splits 2675, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2698, merge/split ratio 1.01, nucleations 189
- channel total drift (end/start - 1): [-0.4297, None, -0.0879, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3607 at frame 303: holes 0, rim-vs-core 0.52, rim-vs-outside 0.05, heterogeneity 0.09; core [0.009, 0.561, 0.833, 0.056] rim [0.011, 0.047, 0.833, 0.035]
  - track 1136 at frame 86: holes 0, rim-vs-core 0.42, rim-vs-outside 0.15, heterogeneity 0.09; core [0.008, 0.572, 0.878, 0.066] rim [0.011, 0.152, 0.873, 0.042]
  - track 2422 at frame 197: holes 0, rim-vs-core 0.33, rim-vs-outside 0.20, heterogeneity 0.09; core [0.011, 0.53, 0.862, 0.079] rim [0.012, 0.204, 0.86, 0.05]
  - track 3125 at frame 257: holes 0, rim-vs-core 0.53, rim-vs-outside 0.03, heterogeneity 0.09; core [0.009, 0.556, 0.876, 0.054] rim [0.013, 0.03, 0.872, 0.032]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 203 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 5.3 (aggregate of 203 individuals; 49/203 membrane-like individually; rim level 0.161)
  - radial predator B: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.952, rim/outside 9.5 (aggregate of 203 individuals; 42/203 membrane-like individually; rim level 0.276)
  - radial food: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.21, rim/outside 0.956 (aggregate of 203 individuals; 0/203 membrane-like individually; rim level 0.737)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.713, rim/outside 2.66 (aggregate of 203 individuals; 5/203 membrane-like individually; rim level 0.09)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3607 (t=1515, R_eq 4.26): none; #1136 (t=430, R_eq 6.79): ['predator B']; #2422 (t=985, R_eq 7.16): ['predator B']; #3125 (t=1285, R_eq 4.55): none
- species `prey` (channels ['prey A'], own threshold): components final 16, mean 19.3, max 69; tracks 1550, persistent 0; splits 478, persistent splits 0 (K=20), max generation 0, merges 421, merge/split 0.881; moving tracks 128
- species `predator` (channels ['predator B'], own threshold): components final 36, mean 36.2, max 56; tracks 5975, persistent 0; splits 1650, persistent splits 1 (K=20), max generation 1, merges 1757, merge/split 1.06; moving tracks 123

## Warnings
- radial: 4 of 203 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
