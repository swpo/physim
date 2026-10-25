# Evidence pack: active-nematic-droplets (seed 1)

- world: `../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 286s; status ok
- command: `python -m labkit.run /tmp/claude-0/c11ex/world.py --out /tmp/claude-0/c11ex/p_d06s1 --seeds 1 --no-movie`
- segmentation: matter > 0.49 of robust range [-0.933, 0.9541], min area 6 px

## Measurements
- components: final 25, mean 10.4, max 28; occupancy final 0.17
- tracks: 268; persistent (alive >= 50% of run): 0; longest 59 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 25, 21], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0788/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 100, default): splits 96, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 68, merge/split ratio 0.708, nucleations 5
- channel total drift (end/start - 1): [-0.0, 0.9564, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 87 at frame 160: holes 0, rim-vs-core 0.25, rim-vs-outside 0.26, heterogeneity 0.12; core [0.789, 0.537, 0.547] rim [0.616, 0.358, 0.534]
  - track 112 at frame 161: holes 0, rim-vs-core 0.36, rim-vs-outside 0.28, heterogeneity 0.12; core [0.83, 0.665, 0.445] rim [0.592, 0.39, 0.436]
  - track 71 at frame 146: holes 0, rim-vs-core 0.24, rim-vs-outside 0.36, heterogeneity 0.10; core [0.828, 0.672, 0.398] rim [0.671, 0.495, 0.392]
  - track 192 at frame 185: holes 0, rim-vs-core 0.23, rim-vs-outside 0.35, heterogeneity 0.10; core [0.821, 0.65, 0.411] rim [0.678, 0.48, 0.455]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 4.09 (aggregate of 75 individuals; 4/75 membrane-like individually; rim level 0.612)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.713, rim/outside 6.15 (aggregate of 75 individuals; 5/75 membrane-like individually; rim level 0.445)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #87 (t=800, R_eq 4.85): none; #112 (t=805, R_eq 3.48): none; #71 (t=730, R_eq 5.94): none; #192 (t=925, R_eq 3.66): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 75 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
