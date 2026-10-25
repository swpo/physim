# Evidence pack: nematic-fuelcell (seed 2)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 535s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1619-c19-fuelcell-slowd-twins/chis0_Df0.2/seed2 --seeds 2 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8503, 0.6316], min area 6 px

## Measurements
- components: final 21, mean 12.8, max 21; occupancy final 0.09
- tracks: 43; persistent (alive >= 50% of run): 6; longest 176 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 45.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 23, 21], H1 [1, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.0408/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 100, default): splits 17, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.059, nucleations 8
- channel total drift (end/start - 1): [-0.5106, -0.3099, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 113: holes 0, rim-vs-core 0.45, rim-vs-outside 0.46, heterogeneity 0.12; core [0.965, 0.962, 0.897, 0.932] rim [0.75, 0.679, 0.826, 0.671]
  - track 9 at frame 109: holes 0, rim-vs-core 0.34, rim-vs-outside 0.64, heterogeneity 0.10; core [0.961, 0.851, 0.966, 0.938] rim [0.805, 0.585, 0.941, 0.795]
  - track 10 at frame 124: holes 0, rim-vs-core 0.43, rim-vs-outside 0.39, heterogeneity 0.11; core [0.942, 0.915, 0.883, 0.868] rim [0.738, 0.611, 0.82, 0.655]
  - track 25 at frame 160: holes 0, rim-vs-core 0.35, rim-vs-outside 0.42, heterogeneity 0.11; core [0.929, 0.81, 0.912, 0.867] rim [0.753, 0.576, 0.859, 0.69]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 88 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.825, rim/outside 3.89 (aggregate of 88 individuals; 4/88 membrane-like individually; rim level 0.642)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.855, rim/outside 5.88 (aggregate of 88 individuals; 5/88 membrane-like individually; rim level 0.529)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.925, rim/outside 1.45 (aggregate of 88 individuals; 0/88 membrane-like individually; rim level 0.849)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.824, rim/outside 2.78 (aggregate of 88 individuals; 0/88 membrane-like individually; rim level 0.649)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=565, R_eq 3.43): none; #9 (t=545, R_eq 7.48, ring): none; #10 (t=620, R_eq 3.7): none; #25 (t=800, R_eq 4.62): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 88 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
