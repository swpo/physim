# Evidence pack: nematic-fuelcell (seed 24)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 664s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1834-c24-review-fuelring/slowD03/seed24 --seeds 24 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8605, 0.6011], min area 6 px

## Measurements
- components: final 18, mean 7.9, max 19; occupancy final 0.08
- tracks: 34; persistent (alive >= 50% of run): 5; longest 184 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 32.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 18, 18], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0594/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 100, default): splits 14, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [-0.5028, -0.3415, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 109: holes 0, rim-vs-core 0.25, rim-vs-outside 0.64, heterogeneity 0.10; core [0.958, 0.795, 0.951, 0.914] rim [0.833, 0.605, 0.917, 0.806]
  - track 0 at frame 99: holes 0, rim-vs-core 0.38, rim-vs-outside 0.68, heterogeneity 0.10; core [0.987, 0.963, 0.932, 0.944] rim [0.826, 0.644, 0.917, 0.8]
  - track 5 at frame 114: holes 0, rim-vs-core 0.29, rim-vs-outside 0.69, heterogeneity 0.10; core [0.978, 0.865, 0.966, 0.966] rim [0.837, 0.648, 0.938, 0.835]
  - track 16 at frame 185: holes 0, rim-vs-core 0.38, rim-vs-outside 0.42, heterogeneity 0.12; core [0.963, 0.885, 0.963, 0.952] rim [0.763, 0.615, 0.894, 0.777]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 55 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 3.1 (aggregate of 55 individuals; 13/55 membrane-like individually; rim level 0.561)
  - radial order |Q|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 4.34 (aggregate of 55 individuals; 13/55 membrane-like individually; rim level 0.467)
  - radial shell s: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.95, rim/outside 1.43 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.817)
  - radial fuel f: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 2.4 (aggregate of 55 individuals; 3/55 membrane-like individually; rim level 0.655)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=545, R_eq 6.15, ring): none; #0 (t=495, R_eq 6.79, ring): none; #5 (t=570, R_eq 7.14, ring): ['phi (droplet)', 'order |Q|']; #16 (t=925, R_eq 4.75): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 19 of 55 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
