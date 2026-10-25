# Evidence pack: bondcell (seed 3)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1104-c05-bondcell-rings-decay/world_small.py`, family `particle`
- parent: threads/particle-life/worlds/sporecell3-det; mutation: membrane particles form harmonic chain bonds (<=2 per particle); bonded M does not revert to core
- run: 201 frames x 50 steps x dt 0.02 = time 200; grid [128, 128]; wall 1440s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1104-c05-bondcell-rings-decay/world_small.py --out /tmp/claude-0/c11rev21/rerun --seeds 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 11.5676], min area 6 px

## Measurements
- components: final 1, mean 1.1, max 3; occupancy final 0.01
- tracks: 40; persistent (alive >= 50% of run): 1; longest 154 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.60 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.473/time; max body lengths 12.2
- replication (lineage window K = 20 frames = time 20, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 40
- channel total drift (end/start - 1): [-0.7508, 13.6429, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 124: holes 0, rim-vs-core 0.39, rim-vs-outside 0.40, heterogeneity 0.13; core [0.0, 0.613, 0.808, 1.0] rim [0.001, 0.274, 1.0, 0.993]
  - track 1 at frame 39: holes 0, rim-vs-core 0.11, rim-vs-outside 0.17, heterogeneity 0.03; core [0.0, 0.107, 0.178, 1.0] rim [0.0, 0.079, 0.283, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [67, 101, 133, 166, 200]):
  - radial F food: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.534, rim/outside 1.21 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.106)
  - radial C0 core kind 0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 3.06 (aggregate of 6 individuals; 2/6 membrane-like individually; rim level 0.0239)
  - radial M membrane: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.81, rim/outside 8.12 (aggregate of 6 individuals; 5/6 membrane-like individually; rim level 0.93)  MEMBRANE-LIKE
  - radial C1 core kind 1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 20.5 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M membrane
- membrane-like channels per top track at mid-life: #7 (t=124, R_eq 5.59): ['M membrane']; #11 (t=116, R_eq 1.49): none; #13 (t=116, R_eq 1.49): none; #1 (t=39, R_eq 1.95): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
