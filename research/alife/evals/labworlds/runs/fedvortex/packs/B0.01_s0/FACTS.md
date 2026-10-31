# Evidence pack: fed-vortices-noise (seed 0)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.01 per sqrt(t): additive on ['om'], proportional on ['Y']
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 158s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/B0.01_s0 --seeds 0 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.28 of robust range [0.0002, 0.2147], min area 6 px

## Measurements
- components: final 34, mean 38.5, max 50; occupancy final 0.15
- tracks: 225; persistent (alive >= 50% of run): 28; longest 401 frames; alive start-to-end: 6
- size of persistent tracks: max/min area ratio 6.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 35, 34], H1 [0, 0, 0]
- motion: 91 long-lived tracks moved >= 1 body length; max speed 0.297/time; max body lengths 26.7
- replication (lineage window K = 20 frames = time 60, default): splits 60, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 55, merge/split ratio 0.917, nucleations 0
- channel total drift (end/start - 1): [-0.424, 0.126, -806.4559, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 202: holes 0, rim-vs-core 0.67, rim-vs-outside 0.26, heterogeneity 0.18; core [0.761, 0.121, 0.076, 0.574] rim [0.369, 0.326, 0.282, 0.109]
  - track 16 at frame 202: holes 0, rim-vs-core 0.77, rim-vs-outside 0.29, heterogeneity 0.20; core [0.81, 0.152, 0.064, 0.713] rim [0.394, 0.342, 0.268, 0.127]
  - track 17 at frame 202: holes 0, rim-vs-core 0.71, rim-vs-outside 0.30, heterogeneity 0.20; core [0.798, 0.103, 0.063, 0.639] rim [0.393, 0.304, 0.269, 0.136]
  - track 154 at frame 326: holes 0, rim-vs-core 0.47, rim-vs-outside 0.52, heterogeneity 0.20; core [0.781, 0.184, 0.903, 0.687] rim [0.531, 0.261, 0.769, 0.319]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 226 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.73, rim/outside 9.26 (aggregate of 226 individuals; 1/226 membrane-like individually; rim level 0.644)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.91, rim/outside 0.789 (aggregate of 226 individuals; 0/226 membrane-like individually; rim level 0.481)
  - radial vorticity (signed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 1.02 (aggregate of 226 individuals; 0/226 membrane-like individually; rim level 0.493)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.628, rim/outside 25.4 (aggregate of 226 individuals; 3/226 membrane-like individually; rim level 0.459)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=606, R_eq 4.75): none; #16 (t=606, R_eq 3.78): none; #17 (t=606, R_eq 4.26): none; #154 (t=978, R_eq 3.48): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 226 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
