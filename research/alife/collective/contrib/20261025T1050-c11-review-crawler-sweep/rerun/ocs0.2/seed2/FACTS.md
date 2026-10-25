# Evidence pack: crawler-divide (seed 2)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0908-c04-crawler-divide-confound/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 269s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0908-c04-crawler-divide-confound/world.py --out /tmp/claude-0/c11rev13/ocs0.2 --seeds 2 --frames 240 --no-movie`
- segmentation: matter > 0.26 of robust range [-0.0, 0.9513], min area 6 px

## Measurements
- components: final 2, mean 2.0, max 3; occupancy final 0.04
- tracks: 11; persistent (alive >= 50% of run): 0; longest 95 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 2.79/time; max body lengths 8.6
- replication (lineage window K = 20 frames = time 50, default): splits 4, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.5, nucleations 0
- channel total drift (end/start - 1): [0.0722, -0.5476, None, -0.4166]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 194: holes 0, rim-vs-core 0.20, rim-vs-outside 0.59, heterogeneity 0.13; core [0.773, 0.285, 0.276, 0.056] rim [0.601, 0.372, 0.214, 0.078]
  - track 1 at frame 95: holes 0, rim-vs-core 0.36, rim-vs-outside 0.79, heterogeneity 0.20; core [0.804, 0.306, 0.65, 0.258] rim [0.589, 0.526, 0.477, 0.322]
  - track 9 at frame 212: holes 0, rim-vs-core 0.36, rim-vs-outside 0.65, heterogeneity 0.16; core [0.829, 0.294, 0.475, 0.048] rim [0.56, 0.462, 0.321, 0.103]
  - track 2 at frame 87: holes 0, rim-vs-core 0.28, rim-vs-outside 0.90, heterogeneity 0.21; core [0.822, 0.345, 0.797, 0.367] rim [0.647, 0.471, 0.628, 0.417]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 13 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.716, rim/outside 27.7 (aggregate of 13 individuals; 0/13 membrane-like individually; rim level 0.612)
  - radial |P| (actin polarization): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.42, rim/outside 20.1 (aggregate of 13 individuals; 7/13 membrane-like individually; rim level 0.35)
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.66, rim/outside 21.7 (aggregate of 13 individuals; 0/13 membrane-like individually; rim level 0.332)
  - radial n (nutrient): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.52, rim/outside 0.87 (aggregate of 13 individuals; 0/13 membrane-like individually; rim level 0.281)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=485, R_eq 22.08): ['|P| (actin polarization)']; #1 (t=237.5, R_eq 31.28): none; #9 (t=530, R_eq 26.57): ['|P| (actin polarization)']; #2 (t=217.5, R_eq 34.13): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
