# Evidence pack: fed-vortices-reviewcheck (seed 2)

- world: `../../fvchk.py`, family `fed-vortex`
- parent: None; mutation: review check: noise sd 0.0 form B after each step
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 120s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex_review/fvchk.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex_review/packs/base_s2 --seeds 2 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2071], min area 6 px

## Measurements
- components: final 27, mean 31.7, max 38; occupancy final 0.13
- tracks: 175; persistent (alive >= 50% of run): 22; longest 401 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 4.62 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 27], H1 [0, 0, 0]
- motion: 91 long-lived tracks moved >= 1 body length; max speed 0.364/time; max body lengths 26.1
- replication (lineage window K = 20 frames = time 60, default): splits 50, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 4, merges 40, merge/split ratio 0.8, nucleations 0
- channel total drift (end/start - 1): [-0.5771, 0.1792, -98.9341, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 202: holes 0, rim-vs-core 0.84, rim-vs-outside 0.33, heterogeneity 0.21; core [0.856, 0.122, 0.94, 0.782] rim [0.412, 0.342, 0.713, 0.147]
  - track 49 at frame 202: holes 0, rim-vs-core 0.78, rim-vs-outside 0.31, heterogeneity 0.21; core [0.834, 0.11, 0.057, 0.714] rim [0.404, 0.324, 0.274, 0.143]
  - track 69 at frame 212: holes 0, rim-vs-core 0.62, rim-vs-outside 0.31, heterogeneity 0.16; core [0.772, 0.096, 0.904, 0.564] rim [0.421, 0.336, 0.717, 0.154]
  - track 125 at frame 333: holes 0, rim-vs-core 0.75, rim-vs-outside 0.30, heterogeneity 0.19; core [0.812, 0.108, 0.925, 0.649] rim [0.389, 0.345, 0.701, 0.127]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 188 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.751, rim/outside 15.2 (aggregate of 188 individuals; 2/188 membrane-like individually; rim level 0.662)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.33, rim/outside 0.777 (aggregate of 188 individuals; 0/188 membrane-like individually; rim level 0.471)
  - radial vorticity (signed): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 0.993 (aggregate of 188 individuals; 0/188 membrane-like individually; rim level 0.487)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.676, rim/outside 26.3 (aggregate of 188 individuals; 6/188 membrane-like individually; rim level 0.496)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #28 (t=606, R_eq 4.51): none; #49 (t=606, R_eq 4.48): none; #69 (t=636, R_eq 5.78): none; #125 (t=999, R_eq 5.05): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 188 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
