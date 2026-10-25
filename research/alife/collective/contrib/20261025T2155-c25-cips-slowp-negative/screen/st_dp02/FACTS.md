# Evidence pack: cips-fuel (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 81s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/../world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/st_dp02 --seeds 0 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.52 of robust range [0.0006, 0.9558], min area 6 px

## Measurements
- components: final 55, mean 69.4, max 107; occupancy final 0.13
- tracks: 207; persistent (alive >= 50% of run): 63; longest 284 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [58, 56, 56], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.0118/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 53, merge/split ratio n/a, nucleations 154
- channel total drift (end/start - 1): [0.0, -0.5305, 0.4413]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 159: holes 0, rim-vs-core 0.12, rim-vs-outside 0.38, heterogeneity 0.05; core [0.937, 0.901, 0.019] rim [0.84, 0.848, 0.064]
  - track 24 at frame 159: holes 0, rim-vs-core 0.14, rim-vs-outside 0.54, heterogeneity 0.06; core [0.978, 0.962, 0.005] rim [0.865, 0.89, 0.053]
  - track 26 at frame 159: holes 0, rim-vs-core 0.19, rim-vs-outside 0.49, heterogeneity 0.06; core [0.949, 0.936, 0.014] rim [0.794, 0.849, 0.082]
  - track 28 at frame 159: holes 0, rim-vs-core 0.16, rim-vs-outside 0.45, heterogeneity 0.05; core [0.969, 0.947, 0.008] rim [0.839, 0.867, 0.064]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 359 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.9, rim/outside 23.1 (aggregate of 359 individuals; 0/359 membrane-like individually; rim level 0.868)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.933, rim/outside 4.27 (aggregate of 359 individuals; 0/359 membrane-like individually; rim level 0.901)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 22.9, rim/outside 0.493 (aggregate of 359 individuals; 0/359 membrane-like individually; rim level 0.404)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=1590, R_eq 1.87): none; #24 (t=1590, R_eq 3.04): none; #26 (t=1590, R_eq 2.76): none; #28 (t=1590, R_eq 2.71): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
