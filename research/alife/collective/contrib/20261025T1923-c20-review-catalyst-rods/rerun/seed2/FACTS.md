# Evidence pack: prod-catalyst-rods (seed 2)

- world: `../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 771s; status ok
- command: `python -m labkit.run /tmp/c20cr/world.py --out /tmp/c20cr/pack --seeds 2 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.8956, 0.9098], min area 6 px

## Measurements
- components: final 18, mean 16.5, max 28; occupancy final 0.07
- tracks: 203; persistent (alive >= 50% of run): 2; longest 116 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 17, 14], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.0532/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 100, default): splits 83, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 22, merge/split ratio 0.265, nucleations 15
- channel total drift (end/start - 1): [-0.7161, -0.2247, None, -0.254]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 72 at frame 111: holes 0, rim-vs-core 0.44, rim-vs-outside 0.30, heterogeneity 0.14; core [0.799, 0.532, 0.324, 0.638] rim [0.611, 0.34, 0.628, 0.468]
  - track 58 at frame 99: holes 0, rim-vs-core 0.42, rim-vs-outside 0.37, heterogeneity 0.13; core [0.816, 0.602, 0.296, 0.816] rim [0.654, 0.43, 0.618, 0.673]
  - track 35 at frame 82: holes 0, rim-vs-core 0.75, rim-vs-outside 0.39, heterogeneity 0.22; core [0.909, 0.744, 0.306, 0.904] rim [0.622, 0.427, 0.859, 0.642]
  - track 77 at frame 99: holes 0, rim-vs-core 0.43, rim-vs-outside 0.31, heterogeneity 0.14; core [0.795, 0.509, 0.347, 0.779] rim [0.618, 0.35, 0.647, 0.576]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 103 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 5.17 (aggregate of 103 individuals; 0/103 membrane-like individually; rim level 0.645)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.676, rim/outside 8.63 (aggregate of 103 individuals; 3/103 membrane-like individually; rim level 0.442)
  - radial surfactant s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.52, rim/outside 2.48 (aggregate of 103 individuals; 70/103 membrane-like individually; rim level 0.498)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #72 (t=555, R_eq 2.82): ['surfactant s']; #58 (t=495, R_eq 4.15): none; #35 (t=410, R_eq 5.84): ['surfactant s']; #77 (t=495, R_eq 4.89): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 103 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
