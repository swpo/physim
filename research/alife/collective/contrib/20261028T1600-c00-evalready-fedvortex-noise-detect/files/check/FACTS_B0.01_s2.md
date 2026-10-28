# Evidence pack: fed-vortices-reviewcheck (seed 2)

- world: `../../fvchk.py`, family `fed-vortex`
- parent: None; mutation: review check: noise sd 0.01 form B after each step
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 157s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex_review/fvchk.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex_review/packs/B0.01_s2 --seeds 2 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0002, 0.21], min area 6 px

## Measurements
- components: final 27, mean 30.3, max 40; occupancy final 0.15
- tracks: 259; persistent (alive >= 50% of run): 20; longest 401 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 6.20 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 30, 27], H1 [0, 0, 0]
- motion: 95 long-lived tracks moved >= 1 body length; max speed 0.394/time; max body lengths 40.3
- replication (lineage window K = 20 frames = time 60, default): splits 79, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 3, merges 65, merge/split ratio 0.823, nucleations 0
- channel total drift (end/start - 1): [-0.429, 0.1379, 627.1492, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 202: holes 0, rim-vs-core 0.73, rim-vs-outside 0.38, heterogeneity 0.20; core [0.838, 0.154, 0.929, 0.766] rim [0.448, 0.314, 0.726, 0.202]
  - track 67 at frame 198: holes 0, rim-vs-core 0.46, rim-vs-outside 0.54, heterogeneity 0.16; core [0.772, 0.054, 0.065, 0.54] rim [0.51, 0.292, 0.204, 0.272]
  - track 46 at frame 185: holes 0, rim-vs-core 0.73, rim-vs-outside 0.34, heterogeneity 0.20; core [0.8, 0.248, 0.062, 0.752] rim [0.418, 0.385, 0.253, 0.176]
  - track 192 at frame 333: holes 0, rim-vs-core 0.68, rim-vs-outside 0.27, heterogeneity 0.19; core [0.785, 0.114, 0.067, 0.614] rim [0.398, 0.32, 0.264, 0.128]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 170 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.759, rim/outside 8.33 (aggregate of 170 individuals; 3/170 membrane-like individually; rim level 0.617)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.57, rim/outside 0.772 (aggregate of 170 individuals; 0/170 membrane-like individually; rim level 0.491)
  - radial vorticity (signed): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.986, rim/outside 1.02 (aggregate of 170 individuals; 0/170 membrane-like individually; rim level 0.495)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.695, rim/outside 19.6 (aggregate of 170 individuals; 9/170 membrane-like individually; rim level 0.433)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=606, R_eq 3.61): none; #67 (t=594, R_eq 6.15): ['eating']; #46 (t=555, R_eq 3.83): none; #192 (t=999, R_eq 4.69): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 170 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
