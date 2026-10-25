# Evidence pack: membrane-evo-up (seed 51)

- world: `../../world_up.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 91s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_up.py --out collective/contrib/c17-mevo-wip/up/seed51 --seeds 51 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7131], min area 6 px

## Measurements
- components: final 9, mean 9.9, max 18; occupancy final 0.30
- tracks: 206; persistent (alive >= 50% of run): 0; longest 46 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 8.16, final 9; holes at thresholds 0.2/0.35/0.5 final [7, 10, 10]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 9, 9], H1 [15, 10, 7]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0023/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 5000, default): splits 73, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 40, merge/split ratio 0.548, nucleations 0
- channel total drift (end/start - 1): [-0.985, None, 0.5818, -0.1295]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 43 at frame 77: holes 0, rim-vs-core 0.90, rim-vs-outside 0.55, heterogeneity 0.21; core [0.858, 0.0, 0.686, 0.681] rim [0.0, 0.0, 0.413, 0.713]
  - track 128 at frame 129: holes 1, rim-vs-core 0.35, rim-vs-outside 0.67, heterogeneity 0.20; core [0.0, 0.811, 0.669, 0.659] rim [0.0, 0.497, 0.526, 0.624]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 68 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 7.67 (aggregate of 68 individuals; 2/68 membrane-like individually; rim level 0.359)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 2.07 (aggregate of 68 individuals; 5/68 membrane-like individually; rim level 0.28)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.4, rim/outside 2.72 (aggregate of 68 individuals; 34/68 membrane-like individually; rim level 0.505)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.92, rim/outside 1.94 (aggregate of 68 individuals; 41/68 membrane-like individually; rim level 0.444)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #43 (t=19250, R_eq 5.97): ['L link', 'membrane (wall)']; #18 (t=5750, R_eq 20.81, ring): none; #85 (t=26500, R_eq 13.46, ring): none; #128 (t=32250, R_eq 9.59, ring): ['K2', 'L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 52 of 68 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
