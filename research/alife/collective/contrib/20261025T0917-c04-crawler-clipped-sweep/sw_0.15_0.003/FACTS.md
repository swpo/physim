# Evidence pack: crawler-divide (seed 1)

- world: `../cdiv.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 224s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/sw_0.15_0.003 --seeds 1 --frames 240 --no-movie`
- segmentation: matter > 0.25 of robust range [-0.0, 0.9917], min area 6 px

## Measurements
- components: final 0, mean 9.1, max 26; occupancy final 0.00
- tracks: 65; persistent (alive >= 50% of run): 0; longest 104 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.22, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 3.64/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 50, default): splits 27, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 7, merge/split ratio 0.259, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, None, -0.6298]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 157: holes 0, rim-vs-core 0.25, rim-vs-outside 0.46, heterogeneity 0.07; core [0.837, 0.138, 0.019, 0.025] rim [0.588, 0.164, 0.013, 0.031]
  - track 24 at frame 153: holes 0, rim-vs-core 0.42, rim-vs-outside 0.33, heterogeneity 0.07; core [0.848, 0.131, 0.019, 0.019] rim [0.436, 0.18, 0.01, 0.029]
  - track 19 at frame 151: holes 0, rim-vs-core 0.42, rim-vs-outside 0.32, heterogeneity 0.07; core [0.849, 0.131, 0.019, 0.016] rim [0.432, 0.177, 0.01, 0.026]
  - track 52 at frame 157: holes 0, rim-vs-core 0.41, rim-vs-outside 0.32, heterogeneity 0.07; core [0.839, 0.133, 0.017, 0.023] rim [0.434, 0.18, 0.009, 0.033]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 53 components >= 12 px at frames [40, 81, 121, 159, 200]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.802, rim/outside 2.27 (aggregate of 53 individuals; 1/53 membrane-like individually; rim level 0.71)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.25, rim/outside 2.6 (aggregate of 53 individuals; 46/53 membrane-like individually; rim level 0.185)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.827, rim/outside 1.36 (aggregate of 53 individuals; 1/53 membrane-like individually; rim level 0.145)
  - radial n (nutrient): peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 1.05 (aggregate of 53 individuals; 3/53 membrane-like individually; rim level 0.0573)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #21 (t=392.5, R_eq 20.31): ['|P| (actin polarization)']; #24 (t=382.5, R_eq 20.17): ['|P| (actin polarization)']; #19 (t=377.5, R_eq 20.27): ['|P| (actin polarization)']; #52 (t=392.5, R_eq 19.45): ['|P| (actin polarization)']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 53 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 2 of 53 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
