# Evidence pack: nematic-fuelcell-planted (seed 0)

- world: `../../world_plant.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 674s; status ok
- command: `python -m labkit.run /root/w/world_plant.py --out /root/w/plant/k3_s0 --seeds 0 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.7322, 0.7411], min area 6 px

## Measurements
- components: final 3, mean 3.2, max 5; occupancy final 0.01
- tracks: 20; persistent (alive >= 50% of run): 3; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 5.26 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [1, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00817/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 100, default): splits 7, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio 0.429, nucleations 0
- channel total drift (end/start - 1): [-0.117, -0.947, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 0, rim-vs-core 0.40, rim-vs-outside 0.43, heterogeneity 0.12; core [0.979, 0.963, 0.721, 0.832] rim [0.832, 0.703, 0.941, 0.69]
  - track 13 at frame 111: holes 0, rim-vs-core 0.47, rim-vs-outside 0.39, heterogeneity 0.14; core [0.962, 0.92, 0.764, 0.823] rim [0.779, 0.595, 0.973, 0.617]
  - track 19 at frame 111: holes 0, rim-vs-core 0.47, rim-vs-outside 0.40, heterogeneity 0.14; core [0.96, 0.95, 0.745, 0.801] rim [0.769, 0.638, 0.964, 0.6]
  - track 18 at frame 39: holes 0, rim-vs-core 0.39, rim-vs-outside 0.41, heterogeneity 0.12; core [0.958, 0.883, 0.797, 0.937] rim [0.804, 0.611, 0.968, 0.772]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 19 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.902, rim/outside 4.61 (aggregate of 19 individuals; 0/19 membrane-like individually; rim level 0.899)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 12.1 (aggregate of 19 individuals; 0/19 membrane-like individually; rim level 0.817)
  - radial shell s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 2.05 (aggregate of 19 individuals; 13/19 membrane-like individually; rim level 0.923)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.846, rim/outside 5.26 (aggregate of 19 individuals; 0/19 membrane-like individually; rim level 0.748)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=505, R_eq 3.34): ['shell s']; #13 (t=555, R_eq 3.52): ['shell s']; #19 (t=555, R_eq 3.83): ['shell s']; #18 (t=195, R_eq 2.99): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
