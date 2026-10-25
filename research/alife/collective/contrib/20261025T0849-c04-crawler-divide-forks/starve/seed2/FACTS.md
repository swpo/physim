# Evidence pack: crawler-divide (seed 2)

- world: `../../cdiv.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 217s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/starve --seeds 1 2 --frames 240 --no-movie`
- segmentation: matter > 0.30 of robust range [-0.0, 0.8235], min area 6 px

## Measurements
- components: final 13, mean 9.8, max 13; occupancy final 0.11
- tracks: 32; persistent (alive >= 50% of run): 13; longest 205 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 28.06 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 13], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 2.69/time; max body lengths 14.5
- replication (lineage window K = 20 frames = time 50, default): splits 13, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.077, nucleations 4
- channel total drift (end/start - 1): [1.5271, -0.5349, None, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 139: holes 0, rim-vs-core 0.38, rim-vs-outside 0.22, heterogeneity 0.06; core [0.817, 0.136, 0.0, 0.0] rim [0.439, 0.146, 0.0, 0.0]
  - track 9 at frame 139: holes 0, rim-vs-core 0.38, rim-vs-outside 0.22, heterogeneity 0.06; core [0.816, 0.136, 0.0, 0.0] rim [0.44, 0.146, 0.0, 0.0]
  - track 17 at frame 157: holes 0, rim-vs-core 0.38, rim-vs-outside 0.22, heterogeneity 0.06; core [0.816, 0.136, 0.0, 0.0] rim [0.438, 0.146, 0.0, 0.0]
  - track 19 at frame 157: holes 0, rim-vs-core 0.38, rim-vs-outside 0.22, heterogeneity 0.06; core [0.819, 0.136, 0.0, 0.0] rim [0.442, 0.146, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 66 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.767, rim/outside 19.5 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.638)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.33, rim/outside 5.14 (aggregate of 66 individuals; 64/66 membrane-like individually; rim level 0.226)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.823, rim/outside 11.6 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.165)
  - radial n (nutrient): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.99 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.176)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #8 (t=347.5, R_eq 13): ['|P| (actin polarization)']; #9 (t=347.5, R_eq 12.99): ['|P| (actin polarization)']; #17 (t=392.5, R_eq 13.12): ['|P| (actin polarization)']; #19 (t=392.5, R_eq 13.01): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
