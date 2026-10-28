# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 525s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim/world.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim/twin/seed1 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0003, 1.8204], min area 6 px

## Measurements
- components: final 18, mean 15.9, max 21; occupancy final 0.08
- tracks: 1484; persistent (alive >= 50% of run): 0; longest 67 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 7, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 20, 19], H1 [11, 4, 0]
- motion: 92 long-lived tracks moved >= 1 body length; max speed 0.947/time; max body lengths 36.3
- replication (lineage window K = 20 frames = time 100, default): splits 510, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 498, merge/split ratio 0.976, nucleations 4
- channel total drift (end/start - 1): [0.0, None, -0.0788, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 253 at frame 141: holes 0, rim-vs-core 0.55, rim-vs-outside 0.09, heterogeneity 0.12; core [0.569, 0.0, 0.423, 0.0] rim [0.056, 0.0, 0.614, 0.0]
  - track 1248 at frame 529: holes 0, rim-vs-core 0.56, rim-vs-outside 0.12, heterogeneity 0.13; core [0.585, 0.0, 0.353, 0.0] rim [0.071, 0.0, 0.567, 0.0]
  - track 865 at frame 363: holes 0, rim-vs-core 0.59, rim-vs-outside 0.12, heterogeneity 0.13; core [0.602, 0.0, 0.314, 0.0] rim [0.062, 0.0, 0.552, 0.0]
  - track 323 at frame 156: holes 0, rim-vs-core 0.55, rim-vs-outside 0.14, heterogeneity 0.13; core [0.636, 0.0, 0.357, 0.0] rim [0.117, 0.0, 0.552, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 99 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 24.6 (aggregate of 99 individuals; 22/99 membrane-like individually; rim level 0.545)
  - radial predator B: flat profile (no radial structure; level 0; aggregate of 99 individuals)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 3.23, rim/outside 0.828 (aggregate of 99 individuals; 0/99 membrane-like individually; rim level 0.633)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 99 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #253 (t=705, R_eq 4.72): none; #1248 (t=2645, R_eq 5.05): ['prey A']; #865 (t=1815, R_eq 5.05): none; #323 (t=780, R_eq 4.72): ['prey A']
- species `prey` (channels ['prey A'], own threshold): components final 19, mean 16.9, max 21; tracks 1370, persistent 0; splits 475, persistent splits 2 (K=20), max generation 2, merges 428, merge/split 0.901; moving tracks 130
- species `predator` (channels ['predator B'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- radial: 1 of 99 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
