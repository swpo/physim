# Evidence pack: bff-soup (seed 0)

- world: `../../world.py`, family `program-soup`
- parent: None; mutation: new class: self-modifying BFF tapes interacting in a well-mixed soup
- run: 61 frames x 25 steps x dt 1.0 = time 1500; grid [512, 512]; wall 18s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261026T0204-c30-bff-soup-o/world.py --out /home/user/physim/research/alife/collective/contrib/20261026T0204-c30-bff-soup-o/pack --seeds 0 1 --frames 60 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 13 px

## Measurements
- components: final 306, mean 237.1, max 607; occupancy final 0.09
- tracks: 7645; persistent (alive >= 50% of run): 0; longest 14 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.41, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [260, 260, 260], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 14.9
- replication (lineage window K = 20 frames = time 500, default): splits 152, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 140, merge/split ratio 0.921, nucleations 7180
- channel total drift (end/start - 1): [14.5909, 10.3438, -0.4284]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1273 components >= 26 px at frames [10, 20, 30, 40, 50, 60]):
  - radial instruction: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 1 (aggregate of 1273 individuals; 0/1273 membrane-like individually; rim level 0.973)
  - radial commonest_tape: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.615, rim/outside 3.6 (aggregate of 1273 individuals; 14/1273 membrane-like individually; rim level 0.353)
  - radial byte: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 1.52 (aggregate of 1273 individuals; 0/1273 membrane-like individually; rim level 0.427)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4201 (t=950, R_eq 4.51): none; #4978 (t=1125, R_eq 4.51): none; #5386 (t=1225, R_eq 4.51): none; #6006 (t=1375, R_eq 4.51): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
