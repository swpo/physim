# Evidence pack: crawler-divide (seed 1)

- world: `../../cdiv.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 235s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/bV_starve --seeds 1 2 --frames 240 --no-movie`
- segmentation: matter > 0.29 of robust range [-0.0, 0.8729], min area 6 px

## Measurements
- components: final 15, mean 11.8, max 15; occupancy final 0.10
- tracks: 28; persistent (alive >= 50% of run): 15; longest 204 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 1.3/time; max body lengths 5.5
- replication (lineage window K = 20 frames = time 50, default): splits 13, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 6, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [1.4729, -1.0, None, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 139: holes 0, rim-vs-core 0.32, rim-vs-outside 0.30, heterogeneity 0.06; core [0.828, 0.022, 0.031, 0.0] rim [0.506, 0.021, 0.019, 0.0]
  - track 12 at frame 147: holes 0, rim-vs-core 0.37, rim-vs-outside 0.23, heterogeneity 0.05; core [0.81, 0.0, 0.0, 0.0] rim [0.436, 0.0, 0.0, 0.0]
  - track 14 at frame 155: holes 0, rim-vs-core 0.38, rim-vs-outside 0.23, heterogeneity 0.05; core [0.807, 0.0, 0.0, 0.0] rim [0.431, 0.0, 0.0, 0.0]
  - track 26 at frame 171: holes 0, rim-vs-core 0.18, rim-vs-outside 0.39, heterogeneity 0.05; core [0.769, 0.0, 0.0, 0.0] rim [0.592, 0.0, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.75, rim/outside 25.8 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.697)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.83, rim/outside 9.23 (aggregate of 77 individuals; 31/77 membrane-like individually; rim level 0.162)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.82, rim/outside 15.8 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.252)
  - radial n (nutrient): peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 0.98 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.165)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #9 (t=347.5, R_eq 12.7): ['|P| (actin polarization)']; #12 (t=367.5, R_eq 11.93): none; #14 (t=387.5, R_eq 11.95): none; #26 (t=427.5, R_eq 11.98): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
