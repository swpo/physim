# Evidence pack: chiral-eating-flocks (seed 1)

- world: `../../../w2.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 151 frames x 80 steps x dt 0.25 = time 3000; grid [128, 128]; wall 24s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/tt/w2.py --out /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/tt/packs/chi03 --seeds 0 1 --frames 150 --spf 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.762], min area 6 px

## Measurements
- components: final 11, mean 14.1, max 33; occupancy final 0.22
- tracks: 1394; persistent (alive >= 50% of run): 0; longest 7 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 14, 7], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 400, default): splits 346, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 405, merge/split ratio 1.17, nucleations 287
- channel total drift (end/start - 1): [0.8534, -0.4462, -0.3935, 0.6538]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 738 at frame 87: holes 0, rim-vs-core 0.12, rim-vs-outside 0.14, heterogeneity 0.06; core [0.493, 0.213, 0.777, 0.13] rim [0.421, 0.269, 0.703, 0.166]
  - track 954 at frame 110: holes 0, rim-vs-core 0.28, rim-vs-outside 0.33, heterogeneity 0.14; core [0.676, 0.089, 0.813, 0.472] rim [0.478, 0.202, 0.669, 0.532]
  - track 54 at frame 6: holes 0, rim-vs-core 0.32, rim-vs-outside 0.33, heterogeneity 0.13; core [0.651, 0.135, 0.873, 0.857] rim [0.475, 0.333, 0.718, 0.77]
  - track 200 at frame 28: holes 0, rim-vs-core 0.32, rim-vs-outside 0.30, heterogeneity 0.14; core [0.688, 0.135, 0.864, 0.389] rim [0.466, 0.294, 0.695, 0.376]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial density rho: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.889, rim/outside 2.64 (aggregate of 78 individuals; 6/78 membrane-like individually; rim level 0.449)
  - radial food c: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.52, rim/outside 0.82 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.436)
  - radial |p|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 2.78 (aggregate of 78 individuals; 5/78 membrane-like individually; rim level 0.639)
  - radial p_x: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.983 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.469)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #738 (t=1740, R_eq 5.32): none; #954 (t=2200, R_eq 6.48): none; #54 (t=120, R_eq 5.92): none; #200 (t=560, R_eq 5.47): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 18 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
