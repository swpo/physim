# Evidence pack: mca-MIRd-branch (seed 0)

- world: `../../../worlds/mca-MIRd-branch/world.py`, family `lenia`
- parent: mca-MIRd (committee r2 branch-point design); mutation: start from a saved neutral-arm state (mutation off) and flip one whole mature cell territory to allele 1; S arm EFF=0.15
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 122s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mca-MIRd-branch/world.py --out threads/lenia-multichannel/packs/mca-MIRd-branch --seeds 0 1 2 --frames 100`
- segmentation: matter > 0.35 of robust range [0.0, 0.997], min area 6 px

## Measurements
- components: final 40, mean 29.7, max 49; occupancy final 0.15
- tracks: 776; persistent (alive >= 50% of run): 3; longest 63 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.32 (1 = constant size)
- enclosures: components with a hole mean 1.02, final 2; holes at thresholds 0.2/0.35/0.5 final [1, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [117, 55, 38], H1 [6, 3, 1]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.174/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 100, META lineage_k): splits 208, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 135, merge/split ratio 0.649, nucleations 241
- channel total drift (end/start - 1): [3.3537, 2.1507, 2.2279, -0.2053, 44.837]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 184 at frame 69: holes 0, rim-vs-core 0.26, rim-vs-outside 0.97, heterogeneity 0.21; core [1.0, 0.784, 0.381, 0.177, 0.0] rim [0.823, 0.927, 0.268, 0.239, 0.0]
  - track 203 at frame 70: holes 0, rim-vs-core 0.48, rim-vs-outside 1.00, heterogeneity 0.22; core [1.0, 0.715, 0.487, 0.252, 1.0] rim [0.796, 0.968, 0.136, 0.298, 1.0]
  - track 271 at frame 73: holes 0, rim-vs-core 0.26, rim-vs-outside 0.98, heterogeneity 0.18; core [1.0, 0.858, 0.344, 0.176, 0.0] rim [0.893, 0.84, 0.122, 0.247, 0.0]
  - track 257 at frame 65: holes 0, rim-vs-core 0.46, rim-vs-outside 0.92, heterogeneity 0.21; core [1.0, 0.741, 0.481, 0.179, 1.0] rim [0.798, 0.95, 0.133, 0.231, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 182 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.975, rim/outside 21.3 (aggregate of 182 individuals; 8/182 membrane-like individually; rim level 0.851)
  - radial A1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.03, rim/outside 4.48 (aggregate of 182 individuals; 105/182 membrane-like individually; rim level 0.721)  MEMBRANE-LIKE
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.618, rim/outside 2.4 (aggregate of 182 individuals; 68/182 membrane-like individually; rim level 0.235)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #184 (t=345, R_eq 7.02): ['A1']; #203 (t=350, R_eq 6.98): ['A1']; #271 (t=365, R_eq 6.91): ['A1']; #257 (t=325, R_eq 6.91): ['A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 182 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
