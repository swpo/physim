# Evidence pack: cips-turnover (seed 3)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS on a consumed fuel plus uniform, fuel-independent enzyme turnover d(e0-e) (Zwicker-type made-outside / lost-inside)
- run: 141 frames x 1000 steps x dt 0.1 = time 14000; grid [192, 192]; wall 847s; status ok
- command: `python -m labkit.run /tmp/claude-0/cipsw/world.py --out /tmp/claude-0/cipsw/runs/switch8000_weak_s3 --seeds 3 --size 192 192 --frames 140 --spf 1000 --no-movie`
- segmentation: matter > 0.51 of robust range [0.0081, 0.9789], min area 6 px

## Measurements
- components: final 9, mean 6.7, max 9; occupancy final 0.06
- tracks: 9; persistent (alive >= 50% of run): 9; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.73 (1 = constant size)
- enclosures: components with a hole mean 0.31, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 9
- channel total drift (end/start - 1): [-0.0004, -0.8086, 0.8701]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 82: holes 1, rim-vs-core 0.15, rim-vs-outside 0.40, heterogeneity 0.06; core [0.805, 0.48, 0.485] rim [0.678, 0.41, 0.523]
  - track 1 at frame 87: holes 0, rim-vs-core 0.27, rim-vs-outside 0.32, heterogeneity 0.08; core [0.888, 0.54, 0.508] rim [0.676, 0.405, 0.6]
  - track 2 at frame 87: holes 0, rim-vs-core 0.15, rim-vs-outside 0.42, heterogeneity 0.09; core [0.869, 0.523, 0.506] rim [0.743, 0.451, 0.553]
  - track 3 at frame 88: holes 0, rim-vs-core 0.29, rim-vs-outside 0.31, heterogeneity 0.09; core [0.881, 0.536, 0.525] rim [0.65, 0.393, 0.616]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 46 components >= 12 px at frames [24, 47, 71, 93, 116, 140]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 14.9 (aggregate of 46 individuals; 2/46 membrane-like individually; rim level 0.865)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 11.9 (aggregate of 46 individuals; 2/46 membrane-like individually; rim level 0.663)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.11, rim/outside 0.76 (aggregate of 46 individuals; 0/46 membrane-like individually; rim level 0.636)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=8200, R_eq 14.19, ring): ['e', 'p']; #1 (t=8700, R_eq 8.74): none; #2 (t=8700, R_eq 9.39): none; #3 (t=8800, R_eq 8.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 46 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
