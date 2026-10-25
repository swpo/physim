# Evidence pack: crawler-divide (seed 3)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0908-c04-crawler-divide-confound/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 263s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0908-c04-crawler-divide-confound/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/ccs/ocs0.2/seed3 --seeds 3 --frames 240 --no-movie`
- segmentation: matter > 0.26 of robust range [-0.0, 0.9521], min area 6 px

## Measurements
- components: final 2, mean 1.9, max 4; occupancy final 0.04
- tracks: 9; persistent (alive >= 50% of run): 1; longest 183 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 2.79/time; max body lengths 18.8
- replication (lineage window K = 20 frames = time 50, default): splits 4, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.0337, -0.5185, None, -0.4118]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 149: holes 0, rim-vs-core 0.23, rim-vs-outside 0.75, heterogeneity 0.18; core [0.832, 0.319, 0.557, 0.07] rim [0.659, 0.409, 0.441, 0.097]
  - track 7 at frame 190: holes 0, rim-vs-core 0.34, rim-vs-outside 0.65, heterogeneity 0.16; core [0.818, 0.293, 0.44, 0.067] rim [0.562, 0.468, 0.302, 0.116]
  - track 0 at frame 28: holes 0, rim-vs-core 0.33, rim-vs-outside 0.95, heterogeneity 0.22; core [0.786, 0.379, 0.849, 0.695] rim [0.622, 0.592, 0.66, 0.755]
  - track 1 at frame 81: holes 0, rim-vs-core 0.35, rim-vs-outside 0.92, heterogeneity 0.22; core [0.792, 0.333, 0.799, 0.411] rim [0.621, 0.572, 0.625, 0.465]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 12 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.722, rim/outside 17.6 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.597)
  - radial |P| (actin polarization): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 14.1 (aggregate of 12 individuals; 6/12 membrane-like individually; rim level 0.349)
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.682, rim/outside 17.5 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.392)
  - radial n (nutrient): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.54, rim/outside 0.887 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.286)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=372.5, R_eq 28.45): none; #7 (t=475, R_eq 26.02): none; #0 (t=70, R_eq 36.13): none; #1 (t=202.5, R_eq 34.6): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
