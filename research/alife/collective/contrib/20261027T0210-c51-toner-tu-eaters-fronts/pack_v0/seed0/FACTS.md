# Evidence pack: eating-flocks (seed 0)

- world: `../../world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 151 frames x 80 steps x dt 0.25 = time 3000; grid [128, 128]; wall 19s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/world.py --out collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/pack_v0 --seeds 0 1 --frames 150 --spf 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 0.6471], min area 6 px

## Measurements
- components: final 166, mean 147.3, max 166; occupancy final 0.37
- tracks: 342; persistent (alive >= 50% of run): 154; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.17 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [166, 166, 166], H1 [70, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 400, default): splits 120, persistent splits 58 (0 more failed only because the siblings re-merged within K), max generation 3, merges 15, merge/split ratio 0.125, nucleations 4
- channel total drift (end/start - 1): [0.9614, -0.5913, -0.1791, 1.1391]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 49 at frame 77: holes 0, rim-vs-core 0.37, rim-vs-outside 0.38, heterogeneity 0.17; core [0.837, 0.067, 0.72, 0.486] rim [0.496, 0.206, 0.714, 0.481]
  - track 51 at frame 77: holes 0, rim-vs-core 0.44, rim-vs-outside 0.37, heterogeneity 0.17; core [0.802, 0.075, 0.863, 0.29] rim [0.475, 0.217, 0.63, 0.39]
  - track 54 at frame 77: holes 0, rim-vs-core 0.39, rim-vs-outside 0.42, heterogeneity 0.16; core [0.837, 0.062, 0.715, 0.626] rim [0.534, 0.19, 0.722, 0.419]
  - track 267 at frame 88: holes 0, rim-vs-core 0.47, rim-vs-outside 0.35, heterogeneity 0.16; core [0.827, 0.077, 0.835, 0.128] rim [0.46, 0.211, 0.615, 0.274]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 939 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial density rho: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.746, rim/outside 4.68 (aggregate of 939 individuals; 3/939 membrane-like individually; rim level 0.686)
  - radial food c: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 10.2, rim/outside 0.937 (aggregate of 939 individuals; 0/939 membrane-like individually; rim level 0.334)
  - radial |p|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 3.67 (aggregate of 939 individuals; 17/939 membrane-like individually; rim level 0.776)
  - radial p_x: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.01 (aggregate of 939 individuals; 7/939 membrane-like individually; rim level 0.499)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #49 (t=1540, R_eq 3.48): ['|p|']; #51 (t=1540, R_eq 3.7): none; #54 (t=1540, R_eq 3.57): ['|p|', 'p_x']; #267 (t=1760, R_eq 3.34): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
