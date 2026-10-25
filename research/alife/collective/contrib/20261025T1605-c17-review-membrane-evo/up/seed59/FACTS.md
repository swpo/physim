# Evidence pack: membrane-evo-up (seed 59)

- world: `../../world_up.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 94s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_up.py --out collective/contrib/c17-mevo-wip/up/seed59 --seeds 59 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7295], min area 6 px

## Measurements
- components: final 16, mean 11.7, max 20; occupancy final 0.30
- tracks: 129; persistent (alive >= 50% of run): 1; longest 85 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.28 (1 = constant size)
- enclosures: components with a hole mean 10.16, final 11; holes at thresholds 0.2/0.35/0.5 final [6, 11, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 16, 15], H1 [19, 15, 8]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.00221/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 5000, default): splits 48, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 9, merge/split ratio 0.188, nucleations 0
- channel total drift (end/start - 1): [-0.8615, None, 0.392, -0.0273]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 46 at frame 89: holes 1, rim-vs-core 0.34, rim-vs-outside 0.69, heterogeneity 0.21; core [0.817, 0.0, 0.746, 0.584] rim [0.516, 0.0, 0.584, 0.587]
  - track 36 at frame 79: holes 1, rim-vs-core 0.37, rim-vs-outside 0.76, heterogeneity 0.21; core [0.8, 0.0, 0.616, 0.553] rim [0.452, 0.0, 0.547, 0.661]
  - track 76 at frame 126: holes 1, rim-vs-core 0.39, rim-vs-outside 0.70, heterogeneity 0.21; core [0.833, 0.0, 0.673, 0.561] rim [0.468, 0.0, 0.549, 0.631]
  - track 98 at frame 144: holes 1, rim-vs-core 0.32, rim-vs-outside 0.74, heterogeneity 0.21; core [0.814, 0.0, 0.663, 0.553] rim [0.517, 0.0, 0.578, 0.614]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 10.4 (aggregate of 83 individuals; 14/83 membrane-like individually; rim level 0.56)
  - radial K2: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.13, rim/outside 1.48 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.064)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 4.76 (aggregate of 83 individuals; 54/83 membrane-like individually; rim level 0.512)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.66, rim/outside 3.59 (aggregate of 83 individuals; 71/83 membrane-like individually; rim level 0.499)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #46 (t=22250, R_eq 9.87, ring): ['K1', 'L link', 'membrane (wall)']; #36 (t=19750, R_eq 7.67, ring): ['L link', 'membrane (wall)']; #76 (t=31500, R_eq 9.3, ring): ['L link', 'membrane (wall)']; #98 (t=36000, R_eq 8.33, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 61 of 83 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
