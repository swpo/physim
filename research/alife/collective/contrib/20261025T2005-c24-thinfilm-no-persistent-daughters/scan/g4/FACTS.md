# Evidence pack: thinfilm-active (seed 0)

- world: `../world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 200 steps x dt 0.25 = time 4000; grid [128, 128]; wall 185s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/tfscan/world.py --out /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/tfscan/g4 --seeds 0 --frames 80 --no-movie`
- segmentation: matter > 0.10 of robust range [0.0222, 4.784], min area 6 px

## Measurements
- components: final 1, mean 4.4, max 13; occupancy final 0.26
- tracks: 67; persistent (alive >= 50% of run): 0; longest 20 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 1, 1], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.077/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 1000, default): splits 20, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 21, merge/split ratio 1.05, nucleations 0
- channel total drift (end/start - 1): [-0.0, 3.4428, 1902.386, 517.7205]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 22: holes 0, rim-vs-core 0.29, rim-vs-outside 0.22, heterogeneity 0.07; core [0.455, 0.943, 0.63, 0.031] rim [0.191, 0.827, 0.608, 0.088]
  - track 46 at frame 35: holes 0, rim-vs-core 0.42, rim-vs-outside 0.56, heterogeneity 0.11; core [0.754, 0.98, 0.314, 0.007] rim [0.346, 0.896, 0.321, 0.052]
  - track 5 at frame 14: holes 0, rim-vs-core 0.26, rim-vs-outside 0.20, heterogeneity 0.07; core [0.416, 0.941, 0.463, 0.011] rim [0.186, 0.834, 0.469, 0.065]
  - track 9 at frame 14: holes 0, rim-vs-core 0.23, rim-vs-outside 0.19, heterogeneity 0.06; core [0.383, 0.933, 0.041, 0.187] rim [0.182, 0.832, 0.093, 0.218]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 27 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.595, rim/outside 4.8 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.326)
  - radial |p| polar order: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.873, rim/outside 2.12 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.822)
  - radial p_x: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 1.08 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.521)
  - radial p_y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 0.955 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.425)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #33 (t=1100, R_eq 9.42): none; #46 (t=1750, R_eq 18.12): none; #5 (t=700, R_eq 9.06): none; #9 (t=700, R_eq 8.1): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 27 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
