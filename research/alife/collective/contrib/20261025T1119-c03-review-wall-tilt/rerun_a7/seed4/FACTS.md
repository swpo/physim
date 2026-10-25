# Evidence pack: ringswim-waste (seed 4)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 42s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/wtilt/a7/seed4 --seeds 4 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.607], min area 6 px

## Measurements
- components: final 0, mean 5.4, max 36; occupancy final 0.00
- tracks: 153; persistent (alive >= 50% of run): 0; longest 29 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.21, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0136/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 1000, default): splits 52, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 3, merges 7, merge/split ratio 0.135, nucleations 0
- channel total drift (end/start - 1): [0.0, -1.0, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 13: holes 0, rim-vs-core 0.65, rim-vs-outside 0.56, heterogeneity 0.18; core [0.096, 0.744, 0.836, 0.917] rim [0.289, 0.35, 0.562, 0.519]
  - track 33 at frame 17: holes 0, rim-vs-core 0.36, rim-vs-outside 0.40, heterogeneity 0.11; core [0.267, 0.614, 0.963, 0.657] rim [0.311, 0.445, 0.838, 0.372]
  - track 145 at frame 134: holes 0, rim-vs-core 0.85, rim-vs-outside 0.58, heterogeneity 0.24; core [0.144, 0.885, 0.874, 0.794] rim [0.358, 0.255, 0.38, 0.617]
  - track 43 at frame 15: holes 0, rim-vs-core 0.67, rim-vs-outside 0.49, heterogeneity 0.19; core [0.083, 0.778, 0.799, 0.889] rim [0.261, 0.349, 0.526, 0.487]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 21 components >= 12 px at frames [34, 67, 101, 133]):
  - radial S: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.38, rim/outside 0.796 (aggregate of 21 individuals; 0/21 membrane-like individually; rim level 0.544)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 19.6 (aggregate of 21 individuals; 1/21 membrane-like individually; rim level 0.757)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.3, rim/outside 11.4 (aggregate of 21 individuals; 8/21 membrane-like individually; rim level 0.862)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.56, rim/outside 20.3 (aggregate of 21 individuals; 12/21 membrane-like individually; rim level 0.796)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #9 (t=650, R_eq 6): none; #33 (t=850, R_eq 4.51, ring): ['K catalyst', 'membrane (wall)']; #145 (t=6700, R_eq 4.82): ['membrane (wall)']; #43 (t=750, R_eq 5.56): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
