# Evidence pack: chiral-eating-flocks (seed 0)

- world: `../../../w2.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 151 frames x 80 steps x dt 0.25 = time 3000; grid [128, 128]; wall 20s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/tt/w2.py --out /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/tt/packs/chi03 --seeds 0 1 --frames 150 --spf 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.7602], min area 6 px

## Measurements
- components: final 16, mean 14.6, max 30; occupancy final 0.23
- tracks: 1455; persistent (alive >= 50% of run): 0; longest 9 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 17, 9], H1 [4, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 400, default): splits 402, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 401, merge/split ratio 0.998, nucleations 251
- channel total drift (end/start - 1): [0.5239, -0.4547, -0.3363, 0.7591]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 513 at frame 55: holes 0, rim-vs-core 0.39, rim-vs-outside 0.44, heterogeneity 0.21; core [0.75, 0.107, 0.882, 0.737] rim [0.499, 0.275, 0.692, 0.585]
  - track 179 at frame 20: holes 0, rim-vs-core 0.21, rim-vs-outside 0.24, heterogeneity 0.09; core [0.562, 0.19, 0.814, 0.103] rim [0.447, 0.282, 0.703, 0.192]
  - track 537 at frame 57: holes 0, rim-vs-core 0.35, rim-vs-outside 0.58, heterogeneity 0.14; core [0.806, 0.02, 0.857, 0.136] rim [0.55, 0.193, 0.773, 0.268]
  - track 654 at frame 69: holes 0, rim-vs-core 0.26, rim-vs-outside 0.36, heterogeneity 0.12; core [0.62, 0.137, 0.828, 0.244] rim [0.485, 0.269, 0.702, 0.372]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 82 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial density rho: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.843, rim/outside 2.44 (aggregate of 82 individuals; 2/82 membrane-like individually; rim level 0.44)
  - radial food c: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.55, rim/outside 0.831 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.433)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 2.64 (aggregate of 82 individuals; 1/82 membrane-like individually; rim level 0.648)
  - radial p_x: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.03 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.5)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #513 (t=1100, R_eq 8.35): none; #179 (t=400, R_eq 5.84): none; #537 (t=1140, R_eq 10.26, ring): ['density rho', '|p|']; #654 (t=1380, R_eq 6.15): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 82 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
