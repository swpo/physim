# Evidence pack: crawler-divide (seed 1)

- world: `../../cdiv.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 229s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/starve --seeds 1 2 --frames 240 --no-movie`
- segmentation: matter > 0.30 of robust range [-0.0, 0.8232], min area 6 px

## Measurements
- components: final 12, mean 9.4, max 13; occupancy final 0.10
- tracks: 33; persistent (alive >= 50% of run): 12; longest 164 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 144.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 2.84/time; max body lengths 7.2
- replication (lineage window K = 20 frames = time 50, default): splits 13, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 4, merges 3, merge/split ratio 0.231, nucleations 3
- channel total drift (end/start - 1): [1.3294, -0.5697, None, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 159: holes 0, rim-vs-core 0.38, rim-vs-outside 0.22, heterogeneity 0.06; core [0.819, 0.132, 0.0, 0.0] rim [0.438, 0.141, 0.0, 0.0]
  - track 19 at frame 163: holes 0, rim-vs-core 0.38, rim-vs-outside 0.22, heterogeneity 0.06; core [0.823, 0.132, 0.0, 0.0] rim [0.442, 0.142, 0.0, 0.0]
  - track 22 at frame 165: holes 0, rim-vs-core 0.38, rim-vs-outside 0.22, heterogeneity 0.06; core [0.82, 0.132, 0.0, 0.0] rim [0.44, 0.141, 0.0, 0.0]
  - track 28 at frame 171: holes 0, rim-vs-core 0.38, rim-vs-outside 0.22, heterogeneity 0.06; core [0.821, 0.132, 0.0, 0.0] rim [0.441, 0.141, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.775, rim/outside 19.8 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.643)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.38, rim/outside 5.49 (aggregate of 62 individuals; 61/62 membrane-like individually; rim level 0.23)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.848, rim/outside 11.7 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.171)
  - radial n (nutrient): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.99 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.189)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #18 (t=397.5, R_eq 13.16): ['|P| (actin polarization)']; #19 (t=407.5, R_eq 13.03): ['|P| (actin polarization)']; #22 (t=412.5, R_eq 13.04): ['|P| (actin polarization)']; #28 (t=427.5, R_eq 13.11): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
