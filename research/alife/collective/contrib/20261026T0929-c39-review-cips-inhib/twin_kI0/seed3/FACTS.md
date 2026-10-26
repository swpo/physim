# Evidence pack: cips-turnover (seed 3)

- world: `../../../20261026T0726-c35-cips-coop-inhib-screen/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS on a consumed fuel plus uniform, fuel-independent enzyme turnover d(e0-e) (Zwicker-type made-outside / lost-inside)
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 763s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0726-c35-cips-coop-inhib-screen/world.py --out collective/contrib/c39-rev-cips-wip/twin_kI0/seed3 --seeds 3 --size 192 192 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.51 of robust range [0.0076, 0.9819], min area 6 px

## Measurements
- components: final 9, mean 6.4, max 9; occupancy final 0.11
- tracks: 9; persistent (alive >= 50% of run): 9; longest 97 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.73 (1 = constant size)
- enclosures: components with a hole mean 0.48, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 9
- channel total drift (end/start - 1): [-0.0004, -0.5675, 0.6114]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 73: holes 1, rim-vs-core 0.21, rim-vs-outside 0.80, heterogeneity 0.10; core [0.971, 0.898, 0.059] rim [0.834, 0.758, 0.132]
  - track 1 at frame 77: holes 0, rim-vs-core 0.24, rim-vs-outside 0.81, heterogeneity 0.12; core [0.977, 0.908, 0.027] rim [0.839, 0.781, 0.174]
  - track 2 at frame 78: holes 0, rim-vs-core 0.25, rim-vs-outside 0.78, heterogeneity 0.12; core [0.987, 0.945, 0.044] rim [0.841, 0.771, 0.159]
  - track 3 at frame 79: holes 0, rim-vs-core 0.30, rim-vs-outside 0.75, heterogeneity 0.12; core [0.985, 0.943, 0.045] rim [0.816, 0.758, 0.209]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 45 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.866, rim/outside 25.6 (aggregate of 45 individuals; 5/45 membrane-like individually; rim level 0.759)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.913, rim/outside 12.3 (aggregate of 45 individuals; 4/45 membrane-like individually; rim level 0.764)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.67, rim/outside 0.642 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.505)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=7300, R_eq 15.95, ring): ['e', 'p']; #1 (t=7700, R_eq 11.81): none; #2 (t=7800, R_eq 12.49): none; #3 (t=7900, R_eq 11.3): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 45 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
