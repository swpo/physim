# Evidence pack: membrane-evo-up (seed 23)

- world: `../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/membrane_evo_up/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 95s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo_up/world.py --out /tmp/claude-0/c11rev5/membrane_evo_up_s23 --seeds 23 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7208], min area 6 px

## Measurements
- components: final 12, mean 11.7, max 29; occupancy final 0.31
- tracks: 166; persistent (alive >= 50% of run): 0; longest 55 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 10.42, final 11; holes at thresholds 0.2/0.35/0.5 final [8, 11, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 12, 12], H1 [12, 12, 10]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00138/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 5000, default): splits 58, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 3, merges 18, merge/split ratio 0.31, nucleations 0
- channel total drift (end/start - 1): [-0.9148, None, 0.6207, 0.1902]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 66: holes 1, rim-vs-core 0.41, rim-vs-outside 0.70, heterogeneity 0.21; core [0.885, 0.0, 0.686, 0.549] rim [0.5, 0.0, 0.558, 0.62]
  - track 63 at frame 101: holes 1, rim-vs-core 0.46, rim-vs-outside 0.75, heterogeneity 0.22; core [0.872, 0.0, 0.681, 0.492] rim [0.451, 0.0, 0.569, 0.634]
  - track 88 at frame 128: holes 1, rim-vs-core 0.34, rim-vs-outside 0.68, heterogeneity 0.21; core [0.732, 0.121, 0.662, 0.573] rim [0.418, 0.069, 0.548, 0.628]
  - track 76 at frame 114: holes 1, rim-vs-core 0.39, rim-vs-outside 0.68, heterogeneity 0.21; core [0.84, 0.004, 0.67, 0.569] rim [0.473, 0.002, 0.547, 0.625]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 74 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 7.57 (aggregate of 74 individuals; 8/74 membrane-like individually; rim level 0.442)
  - radial K2: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 2.4 (aggregate of 74 individuals; 3/74 membrane-like individually; rim level 0.182)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.3, rim/outside 3.6 (aggregate of 74 individuals; 38/74 membrane-like individually; rim level 0.497)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.57, rim/outside 2.54 (aggregate of 74 individuals; 53/74 membrane-like individually; rim level 0.452)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #38 (t=16500, R_eq 8.97, ring): ['K1', 'L link', 'membrane (wall)']; #63 (t=25250, R_eq 7.8, ring): ['L link', 'membrane (wall)']; #88 (t=32000, R_eq 8.54, ring): ['K1', 'L link', 'membrane (wall)']; #76 (t=28500, R_eq 9.04, ring): ['K1', 'L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 57 of 74 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
