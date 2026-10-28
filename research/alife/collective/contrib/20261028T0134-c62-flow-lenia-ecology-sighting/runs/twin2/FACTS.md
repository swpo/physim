# Evidence pack: flow-lenia-digestion-ecology (seed 2)

- world: `../../c62work/world_fleco.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 401 frames x 25 steps x dt 0.2 = time 2000; grid [160, 160]; wall 303s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/c62work/world_fleco.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fl2/twin2 --seeds 2 --size 160 160 --frames 400 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0003, 1.8064], min area 6 px

## Measurements
- components: final 17, mean 15.4, max 20; occupancy final 0.08
- tracks: 1057; persistent (alive >= 50% of run): 0; longest 56 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 9, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 20, 17], H1 [12, 1, 0]
- motion: 43 long-lived tracks moved >= 1 body length; max speed 0.966/time; max body lengths 27.5
- replication (lineage window K = 20 frames = time 100, default): splits 366, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 355, merge/split ratio 0.97, nucleations 5
- channel total drift (end/start - 1): [-0.0, None, -0.0812, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 922 at frame 373: holes 0, rim-vs-core 0.58, rim-vs-outside 0.10, heterogeneity 0.13; core [0.599, 0.0, 0.412, 0.0] rim [0.06, 0.0, 0.635, 0.0]
  - track 474 at frame 202: holes 0, rim-vs-core 0.52, rim-vs-outside 0.13, heterogeneity 0.14; core [0.55, 0.0, 0.289, 0.0] rim [0.084, 0.0, 0.511, 0.0]
  - track 754 at frame 296: holes 0, rim-vs-core 0.43, rim-vs-outside 0.34, heterogeneity 0.13; core [0.631, 0.0, 0.198, 0.0] rim [0.259, 0.0, 0.419, 0.0]
  - track 135 at frame 67: holes 0, rim-vs-core 0.54, rim-vs-outside 0.12, heterogeneity 0.13; core [0.611, 0.0, 0.228, 0.0] rim [0.095, 0.0, 0.403, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 99 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 21.6 (aggregate of 99 individuals; 24/99 membrane-like individually; rim level 0.53)
  - radial predator B: flat profile (no radial structure; level 0; aggregate of 99 individuals)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.12, rim/outside 0.841 (aggregate of 99 individuals; 0/99 membrane-like individually; rim level 0.631)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 99 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #922 (t=1865, R_eq 4.51): none; #474 (t=1010, R_eq 5.86): ['prey A']; #754 (t=1480, R_eq 6.18): ['prey A']; #135 (t=335, R_eq 4.69): none
- species `prey` (channels ['prey A'], own threshold): components final 18, mean 16.7, max 22; tracks 933, persistent 0; splits 330, persistent splits 0 (K=20), max generation 0, merges 283, merge/split 0.858; moving tracks 73
- species `predator` (channels ['predator B'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- radial: 1 of 99 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
