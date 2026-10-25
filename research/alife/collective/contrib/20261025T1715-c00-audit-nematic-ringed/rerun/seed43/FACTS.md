# Evidence pack: active-nematic-droplets (seed 43)

- world: `../../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1141-c11-active-nematic-ringed/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 440s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T1141-c11-active-nematic-ringed/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/nematic-ringed/replication/base --seeds 41 43 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8259, 0.6349], min area 6 px

## Measurements
- components: final 31, mean 21.4, max 32; occupancy final 0.07
- tracks: 112; persistent (alive >= 50% of run): 6; longest 171 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 31, 30], H1 [0, 0, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.0953/time; max body lengths 6.2
- replication (lineage window K = 20 frames = time 100, default): splits 45, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 4, merges 14, merge/split ratio 0.311, nucleations 8
- channel total drift (end/start - 1): [-0.4934, -0.388, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 116: holes 0, rim-vs-core 0.51, rim-vs-outside 0.36, heterogeneity 0.18; core [0.937, 0.883, 0.444] rim [0.717, 0.577, 0.785]
  - track 33 at frame 124: holes 0, rim-vs-core 0.40, rim-vs-outside 0.30, heterogeneity 0.13; core [0.904, 0.673, 0.488] rim [0.716, 0.456, 0.762]
  - track 38 at frame 134: holes 0, rim-vs-core 0.49, rim-vs-outside 0.32, heterogeneity 0.16; core [0.922, 0.87, 0.456] rim [0.71, 0.566, 0.779]
  - track 92 at frame 187: holes 0, rim-vs-core 0.51, rim-vs-outside 0.36, heterogeneity 0.17; core [0.95, 0.904, 0.433] rim [0.747, 0.615, 0.805]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 142 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 4.62 (aggregate of 142 individuals; 1/142 membrane-like individually; rim level 0.744)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.75, rim/outside 7.84 (aggregate of 142 individuals; 1/142 membrane-like individually; rim level 0.631)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.53, rim/outside 2.09 (aggregate of 142 individuals; 109/142 membrane-like individually; rim level 0.635)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #12 (t=580, R_eq 3.19): ['surfactant s']; #33 (t=620, R_eq 3.19): ['surfactant s']; #38 (t=670, R_eq 3.24): ['surfactant s']; #92 (t=935, R_eq 3.61): ['surfactant s']

## Warnings
- radial: 2 of 142 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
