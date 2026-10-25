# Evidence pack: membrane-evo-down (seed 21)

- world: `../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/membrane_evo_down/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 0.7 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 94s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo_down/world.py --out /tmp/claude-0/c11rev5/membrane_evo_down_s21 --seeds 21 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7266], min area 6 px

## Measurements
- components: final 15, mean 11.7, max 17; occupancy final 0.26
- tracks: 99; persistent (alive >= 50% of run): 2; longest 105 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.87 (1 = constant size)
- enclosures: components with a hole mean 10.68, final 13; holes at thresholds 0.2/0.35/0.5 final [7, 13, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 15, 15], H1 [14, 13, 11]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.00764/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 5000, default): splits 40, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.025, nucleations 0
- channel total drift (end/start - 1): [-0.6806, None, 0.0007, -0.2339]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 29 at frame 86: holes 1, rim-vs-core 0.37, rim-vs-outside 0.74, heterogeneity 0.22; core [0.87, 0.0, 0.7, 0.454] rim [0.536, 0.0, 0.583, 0.569]
  - track 54 at frame 121: holes 1, rim-vs-core 0.40, rim-vs-outside 0.69, heterogeneity 0.21; core [0.83, 0.0, 0.697, 0.563] rim [0.459, 0.0, 0.558, 0.616]
  - track 38 at frame 93: holes 1, rim-vs-core 0.38, rim-vs-outside 0.68, heterogeneity 0.22; core [0.838, 0.0, 0.746, 0.536] rim [0.496, 0.0, 0.589, 0.606]
  - track 67 at frame 130: holes 1, rim-vs-core 0.39, rim-vs-outside 0.68, heterogeneity 0.21; core [0.837, 0.0, 0.647, 0.514] rim [0.478, 0.0, 0.56, 0.641]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 8.16 (aggregate of 76 individuals; 11/76 membrane-like individually; rim level 0.569)
  - radial K2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 2.29 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.0132)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.44, rim/outside 5.67 (aggregate of 76 individuals; 53/76 membrane-like individually; rim level 0.486)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.07, rim/outside 4.09 (aggregate of 76 individuals; 68/76 membrane-like individually; rim level 0.476)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #29 (t=21500, R_eq 11.98): none; #54 (t=30250, R_eq 8.81, ring): ['L link', 'membrane (wall)']; #38 (t=23250, R_eq 9.08, ring): ['K1', 'L link', 'membrane (wall)']; #67 (t=32500, R_eq 9.17, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 66 of 76 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
