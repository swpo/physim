# Evidence pack: fch-pchemoton (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_noK.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 384s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_noK.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev3/world_noK --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.40 of robust range [-0.0229, 1.5452], min area 6 px

## Measurements
- components: final 5, mean 5.0, max 5; occupancy final 0.01
- tracks: 5; persistent (alive >= 50% of run): 5; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.93 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 5
- channel total drift (end/start - 1): [-0.9975, 1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.25, rim-vs-outside 0.36, heterogeneity 0.06; core [0.925, 1.0, 0.0] rim [0.678, 1.0, 0.0]
  - track 1 at frame 101: holes 0, rim-vs-core 0.33, rim-vs-outside 0.18, heterogeneity 0.06; core [0.902, 1.0, 0.0] rim [0.567, 1.0, 0.0]
  - track 2 at frame 101: holes 0, rim-vs-core 0.34, rim-vs-outside 0.18, heterogeneity 0.06; core [0.891, 1.0, 0.0] rim [0.55, 1.0, 0.0]
  - track 3 at frame 101: holes 0, rim-vs-core 0.33, rim-vs-outside 0.18, heterogeneity 0.06; core [0.902, 1.0, 0.0] rim [0.574, 1.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 12.6 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.728)
  - radial precursor P: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.997)
  - radial catalyst K: flat profile (no radial structure; level 0; aggregate of 30 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 7.55): none; #1 (t=303, R_eq 5.32): none; #2 (t=303, R_eq 5.41): none; #3 (t=303, R_eq 5.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
