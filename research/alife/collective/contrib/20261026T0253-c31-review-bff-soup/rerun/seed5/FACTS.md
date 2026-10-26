# Evidence pack: bff-soup (seed 5)

- world: `../../../20261026T0204-c30-bff-soup-o/world.py`, family `program-soup`
- parent: None; mutation: new class: self-modifying BFF tapes interacting in a well-mixed soup
- run: 61 frames x 25 steps x dt 1.0 = time 1500; grid [512, 512]; wall 19s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0204-c30-bff-soup-o/world.py --out collective/contrib/wip-c31/rev/rerun --seeds 5 --frames 60 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 13 px

## Measurements
- components: final 210, mean 207.8, max 574; occupancy final 0.06
- tracks: 6985; persistent (alive >= 50% of run): 0; longest 10 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.16, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [184, 184, 184], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 10.2
- replication (lineage window K = 20 frames = time 500, default): splits 75, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 74, merge/split ratio 0.987, nucleations 6740
- channel total drift (end/start - 1): [14.352, 6.3438, -0.4292]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1022 components >= 26 px at frames [10, 20, 30, 40, 50, 60]):
  - radial instruction: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 1 (aggregate of 1022 individuals; 0/1022 membrane-like individually; rim level 0.972)
  - radial commonest_tape: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.597, rim/outside 3.86 (aggregate of 1022 individuals; 0/1022 membrane-like individually; rim level 0.343)
  - radial byte: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.35, rim/outside 1.53 (aggregate of 1022 individuals; 0/1022 membrane-like individually; rim level 0.438)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=150, R_eq 6.38): none; #591 (t=175, R_eq 4.51): none; #628 (t=175, R_eq 4.51): none; #717 (t=175, R_eq 4.51): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
