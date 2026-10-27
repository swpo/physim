# Evidence pack: fed-vortices (seed 13)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 329s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/vort/pack --seeds 13 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2064], min area 6 px

## Measurements
- components: final 30, mean 31.1, max 49; occupancy final 0.16
- tracks: 338; persistent (alive >= 50% of run): 9; longest 925 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.41 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 35, 30], H1 [0, 0, 0]
- motion: 173 long-lived tracks moved >= 1 body length; max speed 0.623/time; max body lengths 51.5
- replication (lineage window K = 20 frames = time 60, default): splits 98, persistent splits 44 (0 more failed only because the siblings re-merged within K), max generation 10, merges 93, merge/split ratio 0.949, nucleations 0
- channel total drift (end/start - 1): [-0.4801, 0.1071, -6664.8325, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 462: holes 0, rim-vs-core 0.44, rim-vs-outside 0.59, heterogeneity 0.15; core [0.782, 0.04, 0.907, 0.546] rim [0.533, 0.281, 0.775, 0.308]
  - track 88 at frame 538: holes 0, rim-vs-core 0.77, rim-vs-outside 0.29, heterogeneity 0.20; core [0.82, 0.119, 0.062, 0.711] rim [0.402, 0.301, 0.273, 0.128]
  - track 8 at frame 370: holes 0, rim-vs-core 0.71, rim-vs-outside 0.30, heterogeneity 0.19; core [0.812, 0.107, 0.063, 0.669] rim [0.418, 0.286, 0.264, 0.146]
  - track 319 at frame 983: holes 0, rim-vs-core 0.47, rim-vs-outside 0.65, heterogeneity 0.17; core [0.836, 0.061, 0.935, 0.672] rim [0.567, 0.255, 0.793, 0.371]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 184 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.755, rim/outside 13.8 (aggregate of 184 individuals; 1/184 membrane-like individually; rim level 0.668)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 10.1, rim/outside 0.774 (aggregate of 184 individuals; 0/184 membrane-like individually; rim level 0.468)
  - radial vorticity (signed): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 0.998 (aggregate of 184 individuals; 0/184 membrane-like individually; rim level 0.487)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.685, rim/outside 22.4 (aggregate of 184 individuals; 7/184 membrane-like individually; rim level 0.503)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=1386, R_eq 6.38): ['eating']; #88 (t=1614, R_eq 4.15): none; #8 (t=1110, R_eq 4.22): none; #319 (t=2949, R_eq 7.4): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 184 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
