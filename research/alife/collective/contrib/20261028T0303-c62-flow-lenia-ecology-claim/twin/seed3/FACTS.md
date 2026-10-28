# Evidence pack: flow-lenia-digestion-ecology (seed 3)

- world: `../../world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 524s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim/world.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/claim/twin/seed3 --seeds 3 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0003, 1.8271], min area 6 px

## Measurements
- components: final 14, mean 15.6, max 21; occupancy final 0.08
- tracks: 1511; persistent (alive >= 50% of run): 0; longest 55 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 7, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 19, 17], H1 [12, 2, 0]
- motion: 81 long-lived tracks moved >= 1 body length; max speed 0.959/time; max body lengths 19.5
- replication (lineage window K = 20 frames = time 100, default): splits 527, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 513, merge/split ratio 0.973, nucleations 3
- channel total drift (end/start - 1): [0.0, None, -0.0803, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 921 at frame 373: holes 0, rim-vs-core 0.49, rim-vs-outside 0.29, heterogeneity 0.15; core [0.648, 0.0, 0.195, 0.0] rim [0.214, 0.0, 0.431, 0.0]
  - track 952 at frame 383: holes 0, rim-vs-core 0.56, rim-vs-outside 0.09, heterogeneity 0.13; core [0.585, 0.0, 0.434, 0.0] rim [0.061, 0.0, 0.616, 0.0]
  - track 1166 at frame 484: holes 0, rim-vs-core 0.45, rim-vs-outside 0.32, heterogeneity 0.14; core [0.639, 0.0, 0.218, 0.0] rim [0.241, 0.0, 0.424, 0.0]
  - track 551 at frame 222: holes 0, rim-vs-core 0.46, rim-vs-outside 0.27, heterogeneity 0.14; core [0.638, 0.0, 0.156, 0.0] rim [0.225, 0.0, 0.359, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 93 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.13, rim/outside 22.5 (aggregate of 93 individuals; 31/93 membrane-like individually; rim level 0.514)
  - radial predator B: flat profile (no radial structure; level 0; aggregate of 93 individuals)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.25, rim/outside 0.836 (aggregate of 93 individuals; 0/93 membrane-like individually; rim level 0.642)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 93 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #921 (t=1865, R_eq 7.36): none; #952 (t=1915, R_eq 4.98): none; #1166 (t=2420, R_eq 6.05): ['prey A']; #551 (t=1110, R_eq 7.96): none
- species `prey` (channels ['prey A'], own threshold): components final 17, mean 16.9, max 21; tracks 1388, persistent 0; splits 483, persistent splits 0 (K=20), max generation 0, merges 414, merge/split 0.857; moving tracks 119
- species `predator` (channels ['predator B'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- radial: 2 of 93 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
