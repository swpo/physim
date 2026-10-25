# Evidence pack: fch-pchemoton (seed 1)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_nogate.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 709s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_nogate.py --out collective/contrib/20261025T0848-c02-fch-chemoton-claim/pack_nogate/seed1 --seeds 1 --frames 200 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.0256, 1.9186], min area 6 px

## Measurements
- components: final 4, mean 4.1, max 6; occupancy final 0.02
- tracks: 18; persistent (alive >= 50% of run): 4; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.55 (1 = constant size)
- enclosures: components with a hole mean 1.45, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 60, default): splits 5, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 0.8, nucleations 4
- channel total drift (end/start - 1): [-0.9904, 1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.34, rim-vs-outside 0.17, heterogeneity 0.06; core [0.886, 1.0, 0.0] rim [0.545, 1.0, 0.0]
  - track 8 at frame 108: holes 1, rim-vs-core 0.19, rim-vs-outside 0.37, heterogeneity 0.04; core [0.833, 1.0, 0.0] rim [0.647, 1.0, 0.0]
  - track 11 at frame 109: holes 1, rim-vs-core 0.19, rim-vs-outside 0.37, heterogeneity 0.04; core [0.833, 1.0, 0.0] rim [0.645, 1.0, 0.0]
  - track 17 at frame 141: holes 0, rim-vs-core 0.29, rim-vs-outside 0.32, heterogeneity 0.06; core [0.908, 1.0, 0.0] rim [0.62, 1.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 25 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 12 (aggregate of 25 individuals; 5/25 membrane-like individually; rim level 0.72)
  - radial precursor P: flat profile (no radial structure; level 0.983; aggregate of 25 individuals)
  - radial catalyst K: flat profile (no radial structure; level 0.0006; aggregate of 25 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=303, R_eq 5.67): none; #8 (t=324, R_eq 10.16, ring): ['amphiphile u+1']; #11 (t=327, R_eq 10.14, ring): ['amphiphile u+1']; #17 (t=423, R_eq 7.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 25 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
