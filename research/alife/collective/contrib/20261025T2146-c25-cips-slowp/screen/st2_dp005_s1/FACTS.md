# Evidence pack: cips-fuel (seed 1)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 76s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/../world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/st2_dp005_s1 --seeds 1 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.73 of robust range [0.0022, 0.6837], min area 6 px

## Measurements
- components: final 51, mean 42.2, max 61; occupancy final 0.10
- tracks: 126; persistent (alive >= 50% of run): 36; longest 271 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [61, 53, 50], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.00458/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 22, merge/split ratio n/a, nucleations 104
- channel total drift (end/start - 1): [0.0, -0.4658, 0.6584]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 166: holes 0, rim-vs-core 0.04, rim-vs-outside 0.18, heterogeneity 0.01; core [0.997, 0.998, 0.0] rim [0.963, 0.986, 0.005]
  - track 3 at frame 176: holes 0, rim-vs-core 0.05, rim-vs-outside 0.22, heterogeneity 0.01; core [1.0, 0.999, 0.0] rim [0.957, 0.983, 0.007]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 203 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 4.25 (aggregate of 203 individuals; 7/203 membrane-like individually; rim level 0.841)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.965, rim/outside 2.38 (aggregate of 203 individuals; 1/203 membrane-like individually; rim level 0.939)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.96, rim/outside 0.426 (aggregate of 203 individuals; 0/203 membrane-like individually; rim level 0.255)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1660, R_eq 2.26): none; #2 (t=1760, R_eq 1.78): none; #3 (t=1760, R_eq 1.95): none; #5 (t=1790, R_eq 1.78): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 203 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
