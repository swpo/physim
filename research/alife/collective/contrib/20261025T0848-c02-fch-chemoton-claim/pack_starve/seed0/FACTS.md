# Evidence pack: fch-pchemoton-starve (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_starve.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 716s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_starve.py --out collective/contrib/20261025T0848-c02-fch-chemoton-claim/pack_starve/seed0 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.33 of robust range [-0.0239, 1.8952], min area 6 px

## Measurements
- components: final 3, mean 3.1, max 6; occupancy final 0.02
- tracks: 13; persistent (alive >= 50% of run): 3; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.93 (1 = constant size)
- enclosures: components with a hole mean 2.76, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 5], H1 [1, 1, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 60, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 2, nucleations 4
- channel total drift (end/start - 1): [-0.9104, -0.2201, -0.9932]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 1, rim-vs-core 0.21, rim-vs-outside 0.44, heterogeneity 0.06; core [0.926, 0.891, 0.001] rim [0.714, 0.883, 0.003]
  - track 3 at frame 101: holes 1, rim-vs-core 0.16, rim-vs-outside 0.61, heterogeneity 0.17; core [0.888, 0.004, 0.559] rim [0.739, 0.012, 0.504]
  - track 9 at frame 79: holes 5, rim-vs-core 0.21, rim-vs-outside 0.56, heterogeneity 0.21; core [0.641, 0.066, 0.182] rim [0.698, 0.157, 0.359]
  - track 12 at frame 171: holes 1, rim-vs-core 0.21, rim-vs-outside 0.41, heterogeneity 0.05; core [0.903, 0.391, 0.0] rim [0.696, 0.391, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 18 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.97, rim/outside 15.2 (aggregate of 18 individuals; 11/18 membrane-like individually; rim level 0.767)  MEMBRANE-LIKE
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.22, rim/outside 0.868 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.441)
  - radial catalyst K: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 4.59 (aggregate of 18 individuals; 4/18 membrane-like individually; rim level 0.158)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u+1
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 12.93, ring): ['amphiphile u+1']; #3 (t=303, R_eq 15.56, ring): ['amphiphile u+1', 'catalyst K']; #9 (t=237, R_eq 28.5): ['catalyst K']; #12 (t=513, R_eq 11.01, ring): ['amphiphile u+1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 18 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
