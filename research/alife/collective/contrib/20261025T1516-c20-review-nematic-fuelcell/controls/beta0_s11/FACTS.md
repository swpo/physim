# Evidence pack: nematic-fuelcell (seed 11)

- world: `../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 677s; status ok
- command: `python -m labkit.run /tmp/c20rev/world.py --out /tmp/c20rev/beta0_s11 --seeds 11 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8771, 0.7138], min area 6 px

## Measurements
- components: final 20, mean 11.0, max 20; occupancy final 0.11
- tracks: 33; persistent (alive >= 50% of run): 7; longest 186 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 53.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 20, 19], H1 [2, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0449/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 100, default): splits 12, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 9
- channel total drift (end/start - 1): [-0.5045, 0.047, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 108: holes 0, rim-vs-core 0.43, rim-vs-outside 0.60, heterogeneity 0.14; core [0.935, 0.805, 0.34, 0.912] rim [0.793, 0.62, 0.694, 0.857]
  - track 5 at frame 108: holes 0, rim-vs-core 0.60, rim-vs-outside 0.61, heterogeneity 0.15; core [0.972, 0.915, 0.242, 0.931] rim [0.778, 0.611, 0.718, 0.871]
  - track 1 at frame 76: holes 0, rim-vs-core 0.51, rim-vs-outside 0.62, heterogeneity 0.15; core [0.954, 0.849, 0.279, 0.924] rim [0.784, 0.626, 0.703, 0.861]
  - track 25 at frame 187: holes 0, rim-vs-core 0.61, rim-vs-outside 0.39, heterogeneity 0.16; core [0.945, 0.926, 0.345, 0.989] rim [0.729, 0.637, 0.829, 0.947]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 3.49 (aggregate of 75 individuals; 11/75 membrane-like individually; rim level 0.546)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 5.06 (aggregate of 75 individuals; 11/75 membrane-like individually; rim level 0.466)
  - radial shell s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 2.23 (aggregate of 75 individuals; 24/75 membrane-like individually; rim level 0.504)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 1.5 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.823)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=540, R_eq 7.69, ring): ['phi (droplet)', 'order |Q|', 'shell s']; #5 (t=540, R_eq 6.23): none; #1 (t=380, R_eq 7.05, ring): none; #25 (t=935, R_eq 4.72): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 20 of 75 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
