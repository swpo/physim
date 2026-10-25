# Evidence pack: nematic-fuelcell (seed 1)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 652s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/z6/shell_s1 --seeds 1 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8288, 0.6554], min area 6 px

## Measurements
- components: final 13, mean 6.1, max 13; occupancy final 0.05
- tracks: 34; persistent (alive >= 50% of run): 2; longest 122 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.11 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 13, 12], H1 [2, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0317/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 100, default): splits 15, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.067, nucleations 3
- channel total drift (end/start - 1): [-0.4928, -0.5457, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 76: holes 0, rim-vs-core 0.47, rim-vs-outside 0.46, heterogeneity 0.16; core [0.94, 0.831, 0.562, 0.782] rim [0.755, 0.614, 0.887, 0.601]
  - track 3 at frame 141: holes 0, rim-vs-core 0.47, rim-vs-outside 0.60, heterogeneity 0.19; core [0.98, 0.894, 0.415, 0.992] rim [0.813, 0.676, 0.783, 0.877]
  - track 0 at frame 50: holes 0, rim-vs-core 0.44, rim-vs-outside 0.72, heterogeneity 0.16; core [0.97, 0.808, 0.425, 0.809] rim [0.818, 0.621, 0.765, 0.684]
  - track 23 at frame 180: holes 0, rim-vs-core 0.52, rim-vs-outside 0.46, heterogeneity 0.14; core [0.972, 0.976, 0.466, 0.665] rim [0.765, 0.709, 0.843, 0.536]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 44 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 4.12 (aggregate of 44 individuals; 3/44 membrane-like individually; rim level 0.654)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.829, rim/outside 6 (aggregate of 44 individuals; 2/44 membrane-like individually; rim level 0.565)
  - radial shell s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 2.19 (aggregate of 44 individuals; 19/44 membrane-like individually; rim level 0.608)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 2.79 (aggregate of 44 individuals; 3/44 membrane-like individually; rim level 0.612)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=380, R_eq 5.94): none; #3 (t=705, R_eq 4.55): ['shell s']; #0 (t=250, R_eq 6.7, ring): none; #23 (t=900, R_eq 4.41): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 44 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
