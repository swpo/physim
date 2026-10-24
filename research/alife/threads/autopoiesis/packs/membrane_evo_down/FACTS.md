# Evidence pack: membrane-evo-down (seed 1)

- world: `../../worlds/membrane_evo_down/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 0.7 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 93s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo_down/world.py --out threads/autopoiesis/packs/membrane_evo_down --seeds 1 --frames 160 --spf 250`
- segmentation: matter > 0.35 of robust range [0.0, 1.7263], min area 6 px

## Measurements
- components: final 14, mean 10.0, max 28; occupancy final 0.27
- tracks: 109; persistent (alive >= 50% of run): 2; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.17 (1 = constant size)
- enclosures: components with a hole mean 9.07, final 14; holes at thresholds 0.2/0.35/0.5 final [9, 15, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 14, 14], H1 [15, 14, 13]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00309/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 5000, default): splits 39, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.6621, None, 0.0449, -0.0557]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 46 at frame 102: holes 1, rim-vs-core 0.41, rim-vs-outside 0.68, heterogeneity 0.22; core [0.839, 0.0, 0.726, 0.54] rim [0.471, 0.0, 0.565, 0.605]
  - track 45 at frame 93: holes 0, rim-vs-core 0.78, rim-vs-outside 1.00, heterogeneity 0.25; core [0.928, 0.0, 0.75, 0.281] rim [0.366, 0.0, 0.711, 0.817]
  - track 69 at frame 125: holes 1, rim-vs-core 0.32, rim-vs-outside 0.75, heterogeneity 0.20; core [0.822, 0.0, 0.632, 0.509] rim [0.533, 0.0, 0.562, 0.623]
  - track 101 at frame 151: holes 1, rim-vs-core 0.30, rim-vs-outside 0.72, heterogeneity 0.20; core [0.801, 0.0, 0.634, 0.566] rim [0.519, 0.0, 0.537, 0.612]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 69 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 8.73 (aggregate of 69 individuals; 17/69 membrane-like individually; rim level 0.541)
  - radial K2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 4.3 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.0333)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 6.07 (aggregate of 69 individuals; 48/69 membrane-like individually; rim level 0.469)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.33, rim/outside 4.26 (aggregate of 69 individuals; 63/69 membrane-like individually; rim level 0.448)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #46 (t=25500, R_eq 9.69, ring): ['L link', 'membrane (wall)']; #45 (t=23250, R_eq 6.72): ['L link', 'membrane (wall)']; #69 (t=31250, R_eq 10.73, ring): ['K1', 'L link', 'membrane (wall)']; #101 (t=37750, R_eq 12.02, ring): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 60 of 69 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
