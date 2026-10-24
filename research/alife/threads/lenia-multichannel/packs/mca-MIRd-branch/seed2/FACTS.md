# Evidence pack: mca-MIRd-branch (seed 2)

- world: `../../../worlds/mca-MIRd-branch/world.py`, family `lenia`
- parent: mca-MIRd (committee r2 branch-point design); mutation: start from a saved neutral-arm state (mutation off) and flip one whole mature cell territory to allele 1; S arm EFF=0.15
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 96s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mca-MIRd-branch/world.py --out threads/lenia-multichannel/packs/mca-MIRd-branch --seeds 0 1 2 --frames 100`
- segmentation: matter > 0.35 of robust range [0.0, 0.997], min area 6 px

## Measurements
- components: final 34, mean 23.6, max 36; occupancy final 0.10
- tracks: 932; persistent (alive >= 50% of run): 0; longest 42 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.11, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [92, 45, 25], H1 [8, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.475/time; max body lengths 5.5
- replication (lineage window K = 20 frames = time 100, META lineage_k): splits 247, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 138, merge/split ratio 0.559, nucleations 281
- channel total drift (end/start - 1): [0.3155, 0.3615, 0.35, -0.1437, 6.178]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 432 at frame 65: holes 0, rim-vs-core 0.37, rim-vs-outside 0.58, heterogeneity 0.14; core [0.853, 0.129, 0.025, 0.005, 0.0] rim [0.666, 0.431, 0.118, 0.033, 0.0]
  - track 71 at frame 23: holes 0, rim-vs-core 0.31, rim-vs-outside 0.97, heterogeneity 0.19; core [1.0, 0.987, 0.403, 0.118, 0.0] rim [0.796, 0.833, 0.245, 0.19, 0.0]
  - track 285 at frame 47: holes 0, rim-vs-core 0.36, rim-vs-outside 0.68, heterogeneity 0.18; core [0.84, 0.356, 0.043, 0.004, 0.0] rim [0.691, 0.581, 0.274, 0.044, 0.0]
  - track 16 at frame 14: holes 0, rim-vs-core 0.30, rim-vs-outside 0.92, heterogeneity 0.19; core [0.985, 0.93, 0.098, 0.153, 0.0] rim [0.804, 0.709, 0.148, 0.237, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 116 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.913, rim/outside 14.7 (aggregate of 116 individuals; 6/116 membrane-like individually; rim level 0.735)
  - radial A1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.81, rim/outside 1.72 (aggregate of 116 individuals; 44/116 membrane-like individually; rim level 0.46)  MEMBRANE-LIKE
  - radial A2: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 1.66, rim/outside 1.75 (aggregate of 116 individuals; 74/116 membrane-like individually; rim level 0.214)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1, A2
- membrane-like channels per top track at mid-life: #432 (t=325, R_eq 7.42): ['A1', 'A2']; #71 (t=115, R_eq 7.07): none; #285 (t=235, R_eq 7.59): ['A1', 'A2']; #16 (t=70, R_eq 7.2): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 116 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
