# Evidence pack: membrane-evo-down (seed 23)

- world: `../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/membrane_evo_down/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 0.7 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 94s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo_down/world.py --out /tmp/claude-0/c11rev5/membrane_evo_down_s23 --seeds 23 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7284], min area 6 px

## Measurements
- components: final 16, mean 10.5, max 29; occupancy final 0.29
- tracks: 103; persistent (alive >= 50% of run): 0; longest 61 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 9.47, final 15; holes at thresholds 0.2/0.35/0.5 final [8, 15, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 16, 16], H1 [15, 15, 10]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00595/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 5000, default): splits 35, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.6319, None, 0.139, 0.0693]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 54 at frame 101: holes 1, rim-vs-core 0.40, rim-vs-outside 0.73, heterogeneity 0.20; core [0.863, 0.0, 0.608, 0.393] rim [0.526, 0.0, 0.568, 0.613]
  - track 71 at frame 132: holes 1, rim-vs-core 0.36, rim-vs-outside 0.70, heterogeneity 0.20; core [0.81, 0.0, 0.666, 0.561] rim [0.476, 0.0, 0.554, 0.633]
  - track 38 at frame 66: holes 1, rim-vs-core 0.39, rim-vs-outside 0.71, heterogeneity 0.21; core [0.864, 0.0, 0.672, 0.516] rim [0.508, 0.0, 0.571, 0.631]
  - track 73 at frame 136: holes 1, rim-vs-core 0.35, rim-vs-outside 0.76, heterogeneity 0.20; core [0.839, 0.0, 0.633, 0.428] rim [0.551, 0.0, 0.586, 0.618]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 66 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 8.67 (aggregate of 66 individuals; 18/66 membrane-like individually; rim level 0.552)
  - radial K2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 2.39 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.0152)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 5.76 (aggregate of 66 individuals; 41/66 membrane-like individually; rim level 0.468)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.61, rim/outside 4.04 (aggregate of 66 individuals; 57/66 membrane-like individually; rim level 0.452)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #54 (t=25250, R_eq 11.64, ring): ['L link', 'membrane (wall)']; #71 (t=33000, R_eq 8.94, ring): ['L link', 'membrane (wall)']; #38 (t=16500, R_eq 8.85, ring): ['K1', 'L link', 'membrane (wall)']; #73 (t=34000, R_eq 10.46, ring): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 58 of 66 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
