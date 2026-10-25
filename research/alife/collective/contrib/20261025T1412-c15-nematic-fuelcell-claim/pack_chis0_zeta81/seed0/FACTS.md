# Evidence pack: nematic-fuelcell (seed 0)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 645s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/z45/chis0_z81_s0 --seeds 0 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8458, 0.6571], min area 6 px

## Measurements
- components: final 27, mean 17.6, max 28; occupancy final 0.08
- tracks: 75; persistent (alive >= 50% of run): 5; longest 160 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 28, 27], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.0616/time; max body lengths 3.9
- replication (lineage window K = 20 frames = time 100, default): splits 30, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 3, merges 6, merge/split ratio 0.2, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.2181, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 121: holes 0, rim-vs-core 0.42, rim-vs-outside 0.35, heterogeneity 0.12; core [0.927, 0.882, 0.904, 0.908] rim [0.69, 0.557, 0.826, 0.797]
  - track 16 at frame 123: holes 0, rim-vs-core 0.40, rim-vs-outside 0.37, heterogeneity 0.10; core [0.953, 0.908, 0.878, 0.886] rim [0.735, 0.596, 0.813, 0.793]
  - track 17 at frame 126: holes 0, rim-vs-core 0.37, rim-vs-outside 0.39, heterogeneity 0.11; core [0.938, 0.889, 0.903, 0.893] rim [0.726, 0.606, 0.834, 0.799]
  - track 33 at frame 151: holes 0, rim-vs-core 0.40, rim-vs-outside 0.36, heterogeneity 0.10; core [0.94, 0.894, 0.966, 0.959] rim [0.721, 0.584, 0.899, 0.864]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 119 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 4.91 (aggregate of 119 individuals; 2/119 membrane-like individually; rim level 0.713)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 7.87 (aggregate of 119 individuals; 2/119 membrane-like individually; rim level 0.616)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 1.46 (aggregate of 119 individuals; 0/119 membrane-like individually; rim level 0.867)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 1.49 (aggregate of 119 individuals; 0/119 membrane-like individually; rim level 0.841)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=605, R_eq 3.74): none; #16 (t=615, R_eq 3.04): none; #17 (t=630, R_eq 3.74): none; #33 (t=755, R_eq 3.52): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 119 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
