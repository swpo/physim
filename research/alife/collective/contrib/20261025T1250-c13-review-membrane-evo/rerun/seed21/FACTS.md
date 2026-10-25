# Evidence pack: membrane-evo-up (seed 21)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 201 frames x 200 steps x dt 1.0 = time 40000; grid [128, 128]; wall 96s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1250-c13-review-membrane-evo/world.py --out collective/contrib/20261025T1250-c13-review-membrane-evo/rerun/seed21 --seeds 21 --spf 200 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7221], min area 6 px

## Measurements
- components: final 12, mean 10.8, max 17; occupancy final 0.31
- tracks: 122; persistent (alive >= 50% of run): 0; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 9.27, final 8; holes at thresholds 0.2/0.35/0.5 final [9, 8, 9]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 12, 9], H1 [15, 10, 4]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.00775/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 4000, default): splits 45, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 11, merge/split ratio 0.244, nucleations 0
- channel total drift (end/start - 1): [-0.969, None, 0.5682, -0.042]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 118: holes 0, rim-vs-core 0.76, rim-vs-outside 0.97, heterogeneity 0.25; core [0.942, 0.0, 0.85, 0.35] rim [0.355, 0.0, 0.673, 0.807]
  - track 58 at frame 148: holes 0, rim-vs-core 0.62, rim-vs-outside 0.97, heterogeneity 0.22; core [0.848, 0.0, 0.592, 0.445] rim [0.372, 0.0, 0.64, 0.839]
  - track 50 at frame 136: holes 1, rim-vs-core 0.36, rim-vs-outside 0.78, heterogeneity 0.21; core [0.806, 0.0, 0.602, 0.521] rim [0.475, 0.0, 0.563, 0.662]
  - track 72 at frame 155: holes 1, rim-vs-core 0.34, rim-vs-outside 0.68, heterogeneity 0.20; core [0.794, 0.0, 0.628, 0.568] rim [0.47, 0.0, 0.528, 0.632]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 9.61 (aggregate of 71 individuals; 6/71 membrane-like individually; rim level 0.542)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 1.92 (aggregate of 71 individuals; 3/71 membrane-like individually; rim level 0.096)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.46, rim/outside 4.57 (aggregate of 71 individuals; 48/71 membrane-like individually; rim level 0.515)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.87, rim/outside 3.44 (aggregate of 71 individuals; 57/71 membrane-like individually; rim level 0.499)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #38 (t=23600, R_eq 6.93): ['membrane (wall)']; #58 (t=29600, R_eq 6.48): ['L link', 'membrane (wall)']; #50 (t=27200, R_eq 7.69, ring): ['L link', 'membrane (wall)']; #72 (t=31000, R_eq 9.56, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 59 of 71 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
