# Evidence pack: fch-pchemoton-starve (seed 13)

- world: `../../../20261025T0848-c02-fch-chemoton-claim/world_starve.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 524s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_starve.py --out collective/contrib/20261025T1518-c19-review-chemoton/starve/seed13 --seeds 13 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0222, 1.9958], min area 6 px

## Measurements
- components: final 2, mean 2.9, max 5; occupancy final 0.02
- tracks: 28; persistent (alive >= 50% of run): 2; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.24 (1 = constant size)
- enclosures: components with a hole mean 1.26, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [2, 2, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 60, default): splits 9, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 8, merge/split ratio 0.889, nucleations 2
- channel total drift (end/start - 1): [-0.9041, 0.0437, -0.986]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 116: holes 0, rim-vs-core 0.12, rim-vs-outside 0.36, heterogeneity 0.06; core [0.72, 0.316, 0.074] rim [0.598, 0.316, 0.084]
  - track 20 at frame 116: holes 1, rim-vs-core 0.14, rim-vs-outside 0.14, heterogeneity 0.03; core [0.634, 0.267, 0.012] rim [0.492, 0.271, 0.021]
  - track 13 at frame 57: holes 7, rim-vs-core 0.04, rim-vs-outside 0.39, heterogeneity 0.04; core [0.618, 0.998, 0.0] rim [0.578, 0.995, 0.0]
  - track 26 at frame 175: holes 1, rim-vs-core 0.17, rim-vs-outside 0.33, heterogeneity 0.04; core [0.746, 0.644, 0.0] rim [0.578, 0.643, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 17 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 3.53 (aggregate of 17 individuals; 5/17 membrane-like individually; rim level 0.572)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 0.851 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.46)
  - radial catalyst K: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 2.11, rim/outside 1.7 (aggregate of 17 individuals; 5/17 membrane-like individually; rim level 0.174)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #19 (t=348, R_eq 18.29, ring): ['amphiphile u+1', 'catalyst K']; #20 (t=348, R_eq 11.63, ring): none; #13 (t=171, R_eq 24.33): none; #26 (t=525, R_eq 10.88, ring): ['amphiphile u+1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 17 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
