# Evidence pack: chiral-eating-flocks (seed 0)

- world: `../../w2.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 40 steps x dt 0.25 = time 3000; grid [128, 128]; wall 20s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/tt/w2.py --out /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/tt/packs/chi08 --seeds 0 --frames 300 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.6125], min area 6 px

## Measurements
- components: final 22, mean 19.8, max 31; occupancy final 0.33
- tracks: 1813; persistent (alive >= 50% of run): 0; longest 133 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.12, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 26, 23], H1 [1, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0273/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 200, default): splits 620, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 599, merge/split ratio 0.966, nucleations 4
- channel total drift (end/start - 1): [0.4873, -0.4488, -0.3112, 0.7252]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 886 at frame 234: holes 0, rim-vs-core 0.17, rim-vs-outside 0.59, heterogeneity 0.12; core [0.616, 0.114, 0.824, 0.712] rim [0.56, 0.198, 0.74, 0.824]
  - track 950 at frame 212: holes 0, rim-vs-core 0.31, rim-vs-outside 0.51, heterogeneity 0.15; core [0.629, 0.095, 0.832, 0.784] rim [0.549, 0.278, 0.7, 0.584]
  - track 385 at frame 108: holes 0, rim-vs-core 0.27, rim-vs-outside 0.45, heterogeneity 0.13; core [0.645, 0.101, 0.83, 0.865] rim [0.512, 0.271, 0.68, 0.814]
  - track 474 at frame 124: holes 0, rim-vs-core 0.18, rim-vs-outside 0.54, heterogeneity 0.15; core [0.625, 0.12, 0.826, 0.738] rim [0.585, 0.242, 0.745, 0.65]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 128 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 3.12 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.599)
  - radial food c: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 5.31, rim/outside 0.926 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.498)
  - radial |p|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 3.58 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.752)
  - radial p_x: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 0.998 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.485)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #886 (t=2340, R_eq 8.88): none; #950 (t=2120, R_eq 8.37): none; #385 (t=1080, R_eq 7.57): none; #474 (t=1240, R_eq 9.79): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 128 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
