# Evidence pack: crawler-divide (seed 1)

- world: `../cdiv2.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 222s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv2.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/v2a --seeds 1 --frames 240 --no-movie`
- segmentation: matter > 0.26 of robust range [-0.0, 0.9699], min area 6 px

## Measurements
- components: final 1, mean 5.5, max 12; occupancy final 0.03
- tracks: 99; persistent (alive >= 50% of run): 2; longest 131 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 32.45 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.823/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 50, default): splits 40, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 20, merge/split ratio 0.5, nucleations 0
- channel total drift (end/start - 1): [-0.0933, -0.8297, None, -0.2348]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 93 at frame 175: holes 0, rim-vs-core 0.48, rim-vs-outside 0.56, heterogeneity 0.12; core [0.934, 0.224, 0.145, 0.039] rim [0.519, 0.443, 0.08, 0.104]
  - track 69 at frame 161: holes 0, rim-vs-core 0.45, rim-vs-outside 0.46, heterogeneity 0.10; core [0.864, 0.307, 0.092, 0.043] rim [0.446, 0.446, 0.047, 0.086]
  - track 92 at frame 163: holes 0, rim-vs-core 0.43, rim-vs-outside 0.46, heterogeneity 0.10; core [0.848, 0.315, 0.076, 0.062] rim [0.441, 0.442, 0.04, 0.102]
  - track 97 at frame 173: holes 0, rim-vs-core 0.22, rim-vs-outside 0.54, heterogeneity 0.10; core [0.818, 0.352, 0.071, 0.081] rim [0.599, 0.382, 0.052, 0.098]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 34 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 8.62 (aggregate of 34 individuals; 1/34 membrane-like individually; rim level 0.689)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.95, rim/outside 8.41 (aggregate of 34 individuals; 30/34 membrane-like individually; rim level 0.422)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.855, rim/outside 4.44 (aggregate of 34 individuals; 1/34 membrane-like individually; rim level 0.13)
  - radial n (nutrient): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.75, rim/outside 0.868 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.249)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #93 (t=437.5, R_eq 26.04): ['|P| (actin polarization)']; #69 (t=402.5, R_eq 21.39): ['|P| (actin polarization)']; #92 (t=407.5, R_eq 20.15): ['|P| (actin polarization)']; #97 (t=432.5, R_eq 19.87): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 34 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
