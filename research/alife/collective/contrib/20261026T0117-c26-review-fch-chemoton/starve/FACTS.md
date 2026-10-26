# Evidence pack: fch-pchemoton-starve (seed 21)

- world: `../../../20261025T0848-c02-fch-chemoton-claim/world_starve.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 346s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_starve.py --out collective/contrib/_c26work/rev5/starve --seeds 21 --frames 200 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.0251, 1.9419], min area 6 px

## Measurements
- components: final 4, mean 4.4, max 6; occupancy final 0.02
- tracks: 20; persistent (alive >= 50% of run): 3; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.17 (1 = constant size)
- enclosures: components with a hole mean 1.46, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 60, default): splits 5, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 5, merge/split ratio 1, nucleations 4
- channel total drift (end/start - 1): [-0.9155, 0.1225, -0.9885]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.24, rim-vs-outside 0.60, heterogeneity 0.16; core [0.883, 0.0, 0.837] rim [0.667, 0.01, 0.728]
  - track 12 at frame 108: holes 1, rim-vs-core 0.19, rim-vs-outside 0.42, heterogeneity 0.05; core [0.873, 0.921, 0.0] rim [0.686, 0.924, 0.001]
  - track 13 at frame 108: holes 0, rim-vs-core 0.29, rim-vs-outside 0.29, heterogeneity 0.06; core [0.902, 0.93, 0.0] rim [0.609, 0.929, 0.001]
  - track 17 at frame 99: holes 0, rim-vs-core 0.16, rim-vs-outside 0.35, heterogeneity 0.04; core [0.81, 0.993, 0.0] rim [0.653, 0.992, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 27 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 5.72 (aggregate of 27 individuals; 7/27 membrane-like individually; rim level 0.64)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.96 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.699)
  - radial catalyst K: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.886, rim/outside 2.86 (aggregate of 27 individuals; 1/27 membrane-like individually; rim level 0.0808)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 13.39): none; #12 (t=324, R_eq 12.6, ring): ['amphiphile u+1']; #13 (t=324, R_eq 8.06): none; #17 (t=297, R_eq 17.37, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 27 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
