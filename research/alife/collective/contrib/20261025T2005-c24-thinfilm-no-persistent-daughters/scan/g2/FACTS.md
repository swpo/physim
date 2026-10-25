# Evidence pack: thinfilm-active (seed 0)

- world: `../world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 200 steps x dt 0.25 = time 4000; grid [128, 128]; wall 218s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/tfscan/world.py --out /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/tfscan/g2 --seeds 0 --frames 80 --no-movie`
- segmentation: matter > 0.08 of robust range [0.032, 5.9924], min area 6 px

## Measurements
- components: final 1, mean 3.4, max 17; occupancy final 0.31
- tracks: 76; persistent (alive >= 50% of run): 0; longest 26 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.15, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 2, 1], H1 [1, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0666/time; max body lengths 4.6
- replication (lineage window K = 20 frames = time 1000, default): splits 21, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 25, merge/split ratio 1.19, nucleations 0
- channel total drift (end/start - 1): [-0.0, 5.2215, -366.3908, -172.2472]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 54 at frame 28: holes 0, rim-vs-core 0.18, rim-vs-outside 0.30, heterogeneity 0.11; core [0.322, 0.922, 0.684, 0.969] rim [0.24, 0.857, 0.537, 0.94]
  - track 75 at frame 70: holes 0, rim-vs-core 0.41, rim-vs-outside 0.60, heterogeneity 0.22; core [0.623, 0.922, 0.756, 0.354] rim [0.352, 0.915, 0.452, 0.421]
  - track 26 at frame 17: holes 0, rim-vs-core 0.13, rim-vs-outside 0.19, heterogeneity 0.10; core [0.308, 0.886, 0.89, 0.764] rim [0.179, 0.881, 0.881, 0.747]
  - track 53 at frame 21: holes 0, rim-vs-core 0.16, rim-vs-outside 0.20, heterogeneity 0.11; core [0.276, 0.91, 0.05, 0.439] rim [0.149, 0.861, 0.099, 0.516]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 17 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.551, rim/outside 2.73 (aggregate of 17 individuals; 2/17 membrane-like individually; rim level 0.198)
  - radial |p| polar order: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 1.51 (aggregate of 17 individuals; 1/17 membrane-like individually; rim level 0.737)
  - radial p_x: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 0.99 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.481)
  - radial p_y: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.956, rim/outside 1.13 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.533)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #54 (t=1400, R_eq 10.16): none; #75 (t=3500, R_eq 38.92, ring): ['height above precursor h - ha', '|p| polar order']; #26 (t=850, R_eq 9.34): none; #53 (t=1050, R_eq 13.11): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 17 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 2 of 17 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
