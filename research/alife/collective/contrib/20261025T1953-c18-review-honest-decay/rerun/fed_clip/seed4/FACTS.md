# Evidence pack: fch-pchemoton-clip (seed 4)

- world: `../../world_clip.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 354s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev17/world_clip.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev17/fed_clip/seed4 --seeds 4 --no-movie`
- segmentation: matter > 0.33 of robust range [-0.022, 1.8384], min area 6 px

## Measurements
- components: final 4, mean 4.3, max 9; occupancy final 0.04
- tracks: 17; persistent (alive >= 50% of run): 3; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.10 (1 = constant size)
- enclosures: components with a hole mean 1.68, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 3, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 6], H1 [2, 2, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 60, default): splits 3, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 4, merge/split ratio 1.33, nucleations 5
- channel total drift (end/start - 1): [-0.7296, 0.8183, -0.9363]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.25, rim-vs-outside 0.57, heterogeneity 0.18; core [0.916, 0.026, 0.77] rim [0.696, 0.052, 0.659]
  - track 1 at frame 101: holes 0, rim-vs-core 0.30, rim-vs-outside 0.31, heterogeneity 0.06; core [0.91, 0.975, 0.0] rim [0.614, 0.974, 0.001]
  - track 13 at frame 106: holes 1, rim-vs-core 0.21, rim-vs-outside 0.39, heterogeneity 0.05; core [0.869, 0.987, 0.0] rim [0.664, 0.987, 0.0]
  - track 16 at frame 171: holes 1, rim-vs-core 0.20, rim-vs-outside 0.39, heterogeneity 0.05; core [0.865, 0.997, 0.0] rim [0.662, 0.997, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 26 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 6.89 (aggregate of 26 individuals; 7/26 membrane-like individually; rim level 0.62)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.937 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.8)
  - radial catalyst K: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 2.99 (aggregate of 26 individuals; 4/26 membrane-like individually; rim level 0.126)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 11.33): ['catalyst K']; #1 (t=303, R_eq 7.96): none; #13 (t=318, R_eq 11.75, ring): ['amphiphile u+1']; #16 (t=513, R_eq 11.37, ring): ['amphiphile u+1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 26 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
