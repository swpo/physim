# Evidence pack: active-nematic-droplets (seed 4)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 742s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1533-c13-review-rods-res15/world.py --out collective/contrib/20261025T1533-c13-review-rods-res15/rerun_res15/seed4 --seeds 4 --size 192 192 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8024, 0.5358], min area 6 px

## Measurements
- components: final 14, mean 5.3, max 14; occupancy final 0.03
- tracks: 27; persistent (alive >= 50% of run): 0; longest 97 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 14, 13], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.0842/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 100, default): splits 12, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.5014, -0.7255, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 153: holes 0, rim-vs-core 0.45, rim-vs-outside 0.27, heterogeneity 0.15; core [0.964, 0.955, 0.585] rim [0.772, 0.699, 0.903]
  - track 10 at frame 153: holes 0, rim-vs-core 0.43, rim-vs-outside 0.29, heterogeneity 0.15; core [0.969, 0.946, 0.587] rim [0.781, 0.705, 0.893]
  - track 11 at frame 153: holes 0, rim-vs-core 0.49, rim-vs-outside 0.30, heterogeneity 0.16; core [0.969, 0.967, 0.602] rim [0.764, 0.702, 0.957]
  - track 19 at frame 190: holes 0, rim-vs-core 0.47, rim-vs-outside 0.32, heterogeneity 0.16; core [0.973, 0.983, 0.585] rim [0.774, 0.767, 0.951]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 37 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.813, rim/outside 4.73 (aggregate of 37 individuals; 0/37 membrane-like individually; rim level 0.778)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 7.4 (aggregate of 37 individuals; 0/37 membrane-like individually; rim level 0.749)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 2.09 (aggregate of 37 individuals; 24/37 membrane-like individually; rim level 0.697)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=765, R_eq 4.51): ['surfactant s']; #10 (t=765, R_eq 5.5): ['surfactant s']; #11 (t=765, R_eq 4.44): ['surfactant s']; #19 (t=950, R_eq 4.55): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
