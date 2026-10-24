# Evidence pack: mca-MIRd-branch (seed 1)

- world: `../../../worlds/mca-MIRd-branch/world.py`, family `lenia`
- parent: mca-MIRd (committee r2 branch-point design); mutation: start from a saved neutral-arm state (mutation off) and flip one whole mature cell territory to allele 1; S arm EFF=0.15
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 94s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mca-MIRd-branch/world.py --out threads/lenia-multichannel/packs/mca-MIRd-branch --seeds 0 1 2 --frames 100`
- segmentation: matter > 0.35 of robust range [0.0, 0.997], min area 6 px

## Measurements
- components: final 35, mean 29.6, max 43; occupancy final 0.11
- tracks: 1091; persistent (alive >= 50% of run): 2; longest 73 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.52 (1 = constant size)
- enclosures: components with a hole mean 1.39, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 2, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [112, 55, 25], H1 [4, 3, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.442/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 100, META lineage_k): splits 277, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 183, merge/split ratio 0.661, nucleations 353
- channel total drift (end/start - 1): [0.5855, 0.446, 0.4611, -0.2243, 15.417]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 256 at frame 62: holes 0, rim-vs-core 0.35, rim-vs-outside 1.00, heterogeneity 0.19; core [0.993, 0.875, 0.344, 0.162, 1.0] rim [0.784, 0.731, 0.121, 0.245, 1.0]
  - track 477 at frame 75: holes 0, rim-vs-core 0.43, rim-vs-outside 1.04, heterogeneity 0.24; core [0.938, 0.903, 0.573, 0.207, 1.0] rim [0.835, 0.736, 0.19, 0.263, 0.985]
  - track 558 at frame 78: holes 0, rim-vs-core 0.29, rim-vs-outside 1.02, heterogeneity 0.20; core [1.0, 0.996, 0.097, 0.3, 1.0] rim [0.922, 0.797, 0.294, 0.324, 1.0]
  - track 696 at frame 84: holes 0, rim-vs-core 0.44, rim-vs-outside 0.93, heterogeneity 0.23; core [1.0, 0.798, 0.514, 0.18, 1.0] rim [0.772, 0.928, 0.173, 0.256, 0.986]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 148 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 15.9 (aggregate of 148 individuals; 8/148 membrane-like individually; rim level 0.766)
  - radial A1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.78, rim/outside 2.25 (aggregate of 148 individuals; 68/148 membrane-like individually; rim level 0.55)  MEMBRANE-LIKE
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 1.85 (aggregate of 148 individuals; 87/148 membrane-like individually; rim level 0.209)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #256 (t=310, R_eq 7.11): ['A1']; #477 (t=375, R_eq 7.57): none; #558 (t=390, R_eq 6.86): ['A1']; #696 (t=420, R_eq 6.96): ['A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 148 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
