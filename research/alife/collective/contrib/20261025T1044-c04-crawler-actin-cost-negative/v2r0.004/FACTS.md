# Evidence pack: crawler-divide (seed 1)

- world: `../../cdiv2.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 228s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv2.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/v2r0.004 --seeds 1 2 --frames 240 --no-movie`
- segmentation: matter > 0.26 of robust range [-0.0, 0.9738], min area 6 px

## Measurements
- components: final 12, mean 6.2, max 15; occupancy final 0.38
- tracks: 303; persistent (alive >= 50% of run): 0; longest 59 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 13], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 50, default): splits 120, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 74, merge/split ratio 0.617, nucleations 0
- channel total drift (end/start - 1): [8.4988, 1.3944, None, -0.3461]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 219 at frame 212: holes 0, rim-vs-core 0.41, rim-vs-outside 0.49, heterogeneity 0.10; core [0.857, 0.222, 0.097, 0.033] rim [0.5, 0.404, 0.056, 0.075]
  - track 225 at frame 214: holes 0, rim-vs-core 0.42, rim-vs-outside 0.50, heterogeneity 0.10; core [0.835, 0.2, 0.069, 0.079] rim [0.486, 0.425, 0.04, 0.135]
  - track 254 at frame 222: holes 0, rim-vs-core 0.44, rim-vs-outside 0.45, heterogeneity 0.10; core [0.879, 0.231, 0.055, 0.027] rim [0.472, 0.383, 0.029, 0.075]
  - track 161 at frame 163: holes 0, rim-vs-core 0.42, rim-vs-outside 0.52, heterogeneity 0.10; core [0.891, 0.195, 0.069, 0.012] rim [0.527, 0.391, 0.041, 0.054]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 44 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 2.92 (aggregate of 44 individuals; 3/44 membrane-like individually; rim level 0.64)
  - radial |P| (actin polarization): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.21, rim/outside 2.75 (aggregate of 44 individuals; 34/44 membrane-like individually; rim level 0.334)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 1.68 (aggregate of 44 individuals; 3/44 membrane-like individually; rim level 0.103)
  - radial n (nutrient): peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.72, rim/outside 0.962 (aggregate of 44 individuals; 1/44 membrane-like individually; rim level 0.217)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #219 (t=530, R_eq 25.11): ['|P| (actin polarization)']; #225 (t=535, R_eq 26.89): ['|P| (actin polarization)']; #254 (t=555, R_eq 24.41): ['|P| (actin polarization)']; #161 (t=407.5, R_eq 26.34): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 44 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 1 of 44 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
