# Evidence pack: fch-pchemoton (seed 1)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0848-c02-fch-chemoton-claim/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 634s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world.py --out collective/contrib/20261025T0848-c02-fch-chemoton-claim/pack/seed1 --seeds 1 --frames 200 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.0206, 1.9192], min area 6 px

## Measurements
- components: final 5, mean 4.6, max 6; occupancy final 0.06
- tracks: 14; persistent (alive >= 50% of run): 5; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.21 (1 = constant size)
- enclosures: components with a hole mean 2.19, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 4], H1 [3, 3, 2]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0323/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 60, default): splits 4, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 2, merge/split ratio 0.5, nucleations 4
- channel total drift (end/start - 1): [-0.442, 0.7899, -0.9287]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.39, rim-vs-outside 0.64, heterogeneity 0.16; core [0.94, 0.001, 0.976] rim [0.697, 0.029, 0.668]
  - track 8 at frame 108: holes 1, rim-vs-core 0.22, rim-vs-outside 0.41, heterogeneity 0.05; core [0.905, 0.974, 0.0] rim [0.689, 0.974, 0.001]
  - track 11 at frame 109: holes 1, rim-vs-core 0.22, rim-vs-outside 0.41, heterogeneity 0.05; core [0.901, 0.997, 0.0] rim [0.683, 0.997, 0.0]
  - track 12 at frame 143: holes 0, rim-vs-core 0.17, rim-vs-outside 0.43, heterogeneity 0.06; core [0.876, 0.913, 0.002] rim [0.707, 0.914, 0.004]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 28 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 5.2 (aggregate of 28 individuals; 9/28 membrane-like individually; rim level 0.633)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.968 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.794)
  - radial catalyst K: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.6, rim/outside 1.69 (aggregate of 28 individuals; 1/28 membrane-like individually; rim level 0.0764)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=303, R_eq 12.85): none; #8 (t=324, R_eq 12.98, ring): ['amphiphile u+1']; #11 (t=327, R_eq 12.44, ring): ['amphiphile u+1']; #12 (t=429, R_eq 15.16, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 16 of 28 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
