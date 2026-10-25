# Evidence pack: membrane-evo-up (seed 58)

- world: `../../world_up.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 92s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_up.py --out collective/contrib/c17-mevo-wip/up/seed58 --seeds 58 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7259], min area 6 px

## Measurements
- components: final 14, mean 10.1, max 16; occupancy final 0.28
- tracks: 127; persistent (alive >= 50% of run): 0; longest 73 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 8.24, final 8; holes at thresholds 0.2/0.35/0.5 final [6, 8, 11]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 14, 14], H1 [15, 12, 5]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00212/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 5000, default): splits 48, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 13, merge/split ratio 0.271, nucleations 1
- channel total drift (end/start - 1): [-0.9249, None, 0.4655, -0.1974]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 82: holes 0, rim-vs-core 0.53, rim-vs-outside 0.93, heterogeneity 0.21; core [0.784, 0.0, 0.525, 0.389] rim [0.437, 0.0, 0.618, 0.776]
  - track 71 at frame 136: holes 1, rim-vs-core 0.33, rim-vs-outside 0.68, heterogeneity 0.22; core [0.117, 0.758, 0.749, 0.631] rim [0.075, 0.486, 0.575, 0.61]
  - track 39 at frame 81: holes 0, rim-vs-core 0.64, rim-vs-outside 0.95, heterogeneity 0.22; core [0.87, 0.0, 0.604, 0.457] rim [0.357, 0.0, 0.634, 0.831]
  - track 68 at frame 129: holes 0, rim-vs-core 0.51, rim-vs-outside 0.87, heterogeneity 0.23; core [0.87, 0.0, 0.653, 0.429] rim [0.437, 0.0, 0.612, 0.695]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 11.4 (aggregate of 67 individuals; 4/67 membrane-like individually; rim level 0.502)
  - radial K2: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 1.61 (aggregate of 67 individuals; 3/67 membrane-like individually; rim level 0.157)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.41, rim/outside 3.68 (aggregate of 67 individuals; 41/67 membrane-like individually; rim level 0.531)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.46, rim/outside 2.74 (aggregate of 67 individuals; 51/67 membrane-like individually; rim level 0.491)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #30 (t=20500, R_eq 8.44): ['membrane (wall)']; #71 (t=34000, R_eq 9.62, ring): ['K1', 'K2', 'L link', 'membrane (wall)']; #39 (t=20250, R_eq 6.26): ['L link', 'membrane (wall)']; #68 (t=32250, R_eq 6.98, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 47 of 67 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
