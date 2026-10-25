# Evidence pack: membrane-evo-up (seed 21)

- world: `../../up_nodeath.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 100s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/evo/up_nodeath.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/evo/up_nodeath/seed21 --seeds 21 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6928], min area 6 px

## Measurements
- components: final 8, mean 6.2, max 16; occupancy final 0.28
- tracks: 28; persistent (alive >= 50% of run): 7; longest 135 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.72 (1 = constant size)
- enclosures: components with a hole mean 5.94, final 8; holes at thresholds 0.2/0.35/0.5 final [6, 8, 8]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 8, 8], H1 [9, 8, 7]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0077/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 5000, default): splits 6, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.5805, None, 0.3003, -0.1902]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 93: holes 1, rim-vs-core 0.34, rim-vs-outside 0.75, heterogeneity 0.20; core [0.855, 0.0, 0.689, 0.513] rim [0.546, 0.0, 0.595, 0.62]
  - track 20 at frame 94: holes 1, rim-vs-core 0.29, rim-vs-outside 0.73, heterogeneity 0.20; core [0.775, 0.0, 0.721, 0.676] rim [0.531, 0.0, 0.586, 0.608]
  - track 24 at frame 120: holes 1, rim-vs-core 0.31, rim-vs-outside 0.94, heterogeneity 0.20; core [0.8, 0.0, 0.565, 0.476] rim [0.563, 0.0, 0.621, 0.676]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 39 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 4.09 (aggregate of 39 individuals; 3/39 membrane-like individually; rim level 0.425)
  - radial K2: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 1.53 (aggregate of 39 individuals; 1/39 membrane-like individually; rim level 0.052)
  - radial L link: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 2.48 (aggregate of 39 individuals; 15/39 membrane-like individually; rim level 0.378)
  - radial membrane (wall): peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 3.6, rim/outside 1.62 (aggregate of 39 individuals; 20/39 membrane-like individually; rim level 0.282)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #18 (t=23250, R_eq 13.93, ring): ['L link', 'membrane (wall)']; #19 (t=23250, R_eq 14.21, ring): none; #20 (t=23500, R_eq 13.7, ring): ['membrane (wall)']; #24 (t=30000, R_eq 12.35, ring): ['K1', 'L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 37 of 39 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
