# Evidence pack: prod-catalyst-rods (seed 5)

- world: `../../../20261025T1655-c14-catalyst-rods-no-selection/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 310s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1655-c14-catalyst-rods-no-selection/world.py --out /home/user/physim/research/alife/collective/contrib/20261025T1845-c19-review-catalyst-rods/rerun/seed5 --seeds 5 --frames 100 --spf 100 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.8904, 0.8867], min area 6 px

## Measurements
- components: final 24, mean 23.7, max 37; occupancy final 0.08
- tracks: 145; persistent (alive >= 50% of run): 5; longest 69 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.44 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 24, 23], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.103/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 100, default): splits 55, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 15, merge/split ratio 0.273, nucleations 21
- channel total drift (end/start - 1): [-0.6695, -0.17, None, -0.138]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 35 at frame 66: holes 0, rim-vs-core 0.41, rim-vs-outside 0.25, heterogeneity 0.13; core [0.821, 0.51, 0.398, 0.689] rim [0.641, 0.322, 0.686, 0.566]
  - track 20 at frame 50: holes 0, rim-vs-core 0.38, rim-vs-outside 0.34, heterogeneity 0.15; core [0.815, 0.539, 0.402, 0.758] rim [0.65, 0.385, 0.688, 0.658]
  - track 62 at frame 70: holes 0, rim-vs-core 0.41, rim-vs-outside 0.34, heterogeneity 0.13; core [0.815, 0.662, 0.394, 0.714] rim [0.637, 0.443, 0.669, 0.601]
  - track 116 at frame 84: holes 0, rim-vs-core 0.49, rim-vs-outside 0.36, heterogeneity 0.16; core [0.851, 0.718, 0.344, 0.743] rim [0.661, 0.466, 0.693, 0.597]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 153 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 4.68 (aggregate of 153 individuals; 1/153 membrane-like individually; rim level 0.674)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.699, rim/outside 7.8 (aggregate of 153 individuals; 2/153 membrane-like individually; rim level 0.431)
  - radial surfactant s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 2.2 (aggregate of 153 individuals; 110/153 membrane-like individually; rim level 0.571)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #35 (t=330, R_eq 2.88): ['surfactant s']; #20 (t=250, R_eq 5.01): none; #62 (t=350, R_eq 3.34): ['surfactant s']; #116 (t=420, R_eq 3.19): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 153 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
