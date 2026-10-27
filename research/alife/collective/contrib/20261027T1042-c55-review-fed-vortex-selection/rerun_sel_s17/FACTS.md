# Evidence pack: fed-vortices (seed 17)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0845-c53-fed-vortex-selection-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1501 frames x 150 steps x dt 0.02 = time 4500; grid [128, 128]; wall 923s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0845-c53-fed-vortex-selection-claim/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/vsel/pack_sel --seeds 17 --frames 1500 --spf 150 --no-movie`
- segmentation: matter > 0.28 of robust range [0.0, 0.2149], min area 6 px

## Measurements
- components: final 37, mean 35.5, max 46; occupancy final 0.22
- tracks: 1918; persistent (alive >= 50% of run): 0; longest 485 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 46, 38], H1 [0, 0, 0]
- motion: 655 long-lived tracks moved >= 1 body length; max speed 0.958/time; max body lengths 58.2
- replication (lineage window K = 20 frames = time 60, default): splits 649, persistent splits 114 (0 more failed only because the siblings re-merged within K), max generation 17, merges 589, merge/split ratio 0.908, nucleations 0
- channel total drift (end/start - 1): [-0.3132, -0.0458, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 239: holes 0, rim-vs-core 0.49, rim-vs-outside 0.57, heterogeneity 0.16; core [0.815, 0.161, 0.889, 0.013] rim [0.506, 0.301, 0.541, 0.008]
  - track 19 at frame 239: holes 0, rim-vs-core 0.62, rim-vs-outside 0.38, heterogeneity 0.14; core [0.786, 0.154, 0.917, 0.002] rim [0.41, 0.327, 0.459, 0.002]
  - track 129 at frame 517: holes 0, rim-vs-core 0.60, rim-vs-outside 0.39, heterogeneity 0.14; core [0.798, 0.275, 0.867, 0.017] rim [0.416, 0.381, 0.416, 0.01]
  - track 1776 at frame 1450: holes 0, rim-vs-core 0.62, rim-vs-outside 0.32, heterogeneity 0.17; core [0.809, 0.096, 0.403, 0.563] rim [0.388, 0.289, 0.167, 0.233]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 213 components >= 12 px at frames [252, 504, 756, 996, 1248, 1500]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.719, rim/outside 7.62 (aggregate of 213 individuals; 6/213 membrane-like individually; rim level 0.571)
  - radial fuel Y: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 5.16, rim/outside 0.802 (aggregate of 213 individuals; 0/213 membrane-like individually; rim level 0.426)
  - radial label a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.742, rim/outside 7.77 (aggregate of 213 individuals; 10/213 membrane-like individually; rim level 0.246)
  - radial label b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.703, rim/outside 7.51 (aggregate of 213 individuals; 7/213 membrane-like individually; rim level 0.424)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #33 (t=717, R_eq 4.03): none; #19 (t=717, R_eq 4.15): none; #129 (t=1551, R_eq 2.76): none; #1776 (t=4350, R_eq 4.75): none

## Warnings
- radial: 9 of 213 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
