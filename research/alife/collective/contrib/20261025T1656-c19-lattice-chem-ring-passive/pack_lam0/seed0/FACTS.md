# Evidence pack: lattice-chem (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1518-c19-lattice-chem-sighting/world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 287s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1518-c19-lattice-chem-sighting/world.py --out (c19 run of research/alife/collective/contrib/20261025T1518-c19-lattice-chem-sighting/world.py) --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 27.0], min area 6 px

## Measurements
- components: final 56, mean 71.6, max 161; occupancy final 0.17
- tracks: 1558; persistent (alive >= 50% of run): 45; longest 198 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [82, 60, 52], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00356/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 429, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 551, merge/split ratio 1.28, nucleations 189
- channel total drift (end/start - 1): [2.5255, None, -0.6224, 1.2819]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 50 at frame 103: holes 0, rim-vs-core 0.35, rim-vs-outside 0.43, heterogeneity 0.17; core [0.63, 0.143, 0.0, 0.431] rim [0.622, 0.488, 0.05, 0.481]
  - track 77 at frame 103: holes 0, rim-vs-core 0.22, rim-vs-outside 0.40, heterogeneity 0.15; core [0.7, 0.114, 0.06, 0.533] rim [0.62, 0.323, 0.048, 0.527]
  - track 85 at frame 103: holes 0, rim-vs-core 0.06, rim-vs-outside 0.34, heterogeneity 0.17; core [0.651, 0.264, 0.046, 0.444] rim [0.619, 0.286, 0.08, 0.474]
  - track 94 at frame 103: holes 0, rim-vs-core 0.21, rim-vs-outside 0.40, heterogeneity 0.17; core [0.622, 0.232, 0.05, 0.438] rim [0.632, 0.437, 0.047, 0.425]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 395 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.972, rim/outside 9.31 (aggregate of 395 individuals; 26/395 membrane-like individually; rim level 0.522)
  - radial M (membrane): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 3.08 (aggregate of 395 individuals; 178/395 membrane-like individually; rim level 0.344)
  - radial X (food): peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.77, rim/outside 0.704 (aggregate of 395 individuals; 3/395 membrane-like individually; rim level 0.233)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #50 (t=5150, R_eq 2.52): ['M (membrane)']; #77 (t=5150, R_eq 2.99): none; #85 (t=5150, R_eq 2.99): ['M (membrane)']; #94 (t=5150, R_eq 3.24): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 34 of 395 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
