# Evidence pack: cips-turnover (seed 3)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS on a consumed fuel plus uniform, fuel-independent enzyme turnover d(e0-e) (Zwicker-type made-outside / lost-inside)
- run: 161 frames x 1000 steps x dt 0.1 = time 16000; grid [192, 192]; wall 946s; status ok
- command: `python -m labkit.run /tmp/claude-0/cipsw/world.py --out /tmp/claude-0/cipsw/runs/switch8000_s3 --seeds 3 --size 192 192 --frames 160 --spf 1000 --no-movie`
- segmentation: matter > 0.51 of robust range [0.0081, 0.9784], min area 6 px

## Measurements
- components: final 1, mean 3.9, max 12; occupancy final 0.00
- tracks: 14; persistent (alive >= 50% of run): 0; longest 76 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.25, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 2000, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio 1, nucleations 9
- channel total drift (end/start - 1): [-0.0005, -0.8617, 0.9272]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 122: holes 0, rim-vs-core 0.21, rim-vs-outside 0.13, heterogeneity 0.06; core [0.769, 0.406, 0.676] rim [0.584, 0.31, 0.72]
  - track 1 at frame 69: holes 0, rim-vs-core 0.22, rim-vs-outside 0.83, heterogeneity 0.11; core [0.986, 0.955, 0.009] rim [0.862, 0.828, 0.137]
  - track 2 at frame 69: holes 0, rim-vs-core 0.23, rim-vs-outside 0.81, heterogeneity 0.11; core [0.992, 0.974, 0.019] rim [0.856, 0.817, 0.125]
  - track 4 at frame 69: holes 0, rim-vs-core 0.28, rim-vs-outside 0.76, heterogeneity 0.11; core [0.989, 0.96, 0.013] rim [0.824, 0.788, 0.167]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 22 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.972, rim/outside 12.1 (aggregate of 22 individuals; 2/22 membrane-like individually; rim level 0.809)
  - radial p: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 12.2 (aggregate of 22 individuals; 2/22 membrane-like individually; rim level 0.626)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.92, rim/outside 0.761 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.647)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=12200, R_eq 5.86): none; #1 (t=6900, R_eq 11.77): none; #2 (t=6900, R_eq 12.5): none; #4 (t=6900, R_eq 12.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 22 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
