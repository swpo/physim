# Evidence pack: phoretic-colloids (seed 2)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 1601 frames x 1 steps x dt 0.5 = time 800; grid [128, 128]; wall 241s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33-sdfix/world.py --out collective/contrib/wip-c33-sdfix/pack --seeds 0 2 --frames 1600 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7548], min area 6 px

## Measurements
- components: final 12, mean 14.4, max 25; occupancy final 0.05
- tracks: 542; persistent (alive >= 50% of run): 0; longest 536 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 14, 10], H1 [0, 0, 0]
- motion: 105 long-lived tracks moved >= 1 body length; max speed 0.515/time; max body lengths 9.7
- replication (lineage window K = 20 frames = time 10, default): splits 53, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 9, merges 69, merge/split ratio 1.3, nucleations 368
- channel total drift (end/start - 1): [0.5514, 0.265, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 172 at frame 605: holes 0, rim-vs-core 0.25, rim-vs-outside 0.28, heterogeneity 0.06; core [0.871, 0.0, 0.419] rim [0.633, 0.0, 0.361]
  - track 178 at frame 592: holes 0, rim-vs-core 0.26, rim-vs-outside 0.27, heterogeneity 0.05; core [0.868, 0.0, 0.344] rim [0.616, 0.0, 0.306]
  - track 9 at frame 296: holes 0, rim-vs-core 0.18, rim-vs-outside 0.22, heterogeneity 0.16; core [0.62, 0.442, 0.387] rim [0.487, 0.331, 0.346]
  - track 520 at frame 1573: holes 0, rim-vs-core 0.24, rim-vs-outside 0.23, heterogeneity 0.23; core [0.612, 0.457, 0.635] rim [0.455, 0.321, 0.51]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [269, 538, 807, 1062, 1331, 1600]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 18 (aggregate of 77 individuals; 1/77 membrane-like individually; rim level 0.644)
  - radial B density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 11.8 (aggregate of 77 individuals; 28/77 membrane-like individually; rim level 0.322)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.831, rim/outside 2.94 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.583)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #172 (t=302.5, R_eq 2.71): none; #178 (t=296, R_eq 2.26): none; #9 (t=148, R_eq 2.52): none; #520 (t=786.5, R_eq 4.44): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 77 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
