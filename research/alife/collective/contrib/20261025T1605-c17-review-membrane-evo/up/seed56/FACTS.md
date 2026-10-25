# Evidence pack: membrane-evo-up (seed 56)

- world: `../../world_up.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 91s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_up.py --out collective/contrib/c17-mevo-wip/up/seed56 --seeds 56 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7337], min area 6 px

## Measurements
- components: final 15, mean 11.7, max 25; occupancy final 0.30
- tracks: 152; persistent (alive >= 50% of run): 0; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 9.42, final 10; holes at thresholds 0.2/0.35/0.5 final [5, 10, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 15, 14], H1 [17, 15, 9]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00443/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 5000, default): splits 54, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 5, merges 14, merge/split ratio 0.259, nucleations 1
- channel total drift (end/start - 1): [-0.8786, None, 0.4487, 0.0834]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 75: holes 0, rim-vs-core 0.61, rim-vs-outside 0.93, heterogeneity 0.23; core [0.89, 0.0, 0.691, 0.417] rim [0.392, 0.0, 0.627, 0.771]
  - track 50 at frame 85: holes 1, rim-vs-core 0.30, rim-vs-outside 0.78, heterogeneity 0.20; core [0.81, 0.0, 0.6, 0.487] rim [0.542, 0.0, 0.55, 0.615]
  - track 31 at frame 63: holes 1, rim-vs-core 0.45, rim-vs-outside 0.75, heterogeneity 0.21; core [0.86, 0.0, 0.566, 0.294] rim [0.529, 0.0, 0.564, 0.599]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 8.72 (aggregate of 79 individuals; 10/79 membrane-like individually; rim level 0.534)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 1.85 (aggregate of 79 individuals; 2/79 membrane-like individually; rim level 0.118)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.53, rim/outside 3.83 (aggregate of 79 individuals; 58/79 membrane-like individually; rim level 0.518)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 4.21, rim/outside 2.78 (aggregate of 79 individuals; 66/79 membrane-like individually; rim level 0.5)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #33 (t=18750, R_eq 9.85): none; #50 (t=21250, R_eq 10.17, ring): ['L link', 'membrane (wall)']; #31 (t=15750, R_eq 11.47, ring): ['membrane (wall)']; #118 (t=37000, R_eq 11.48, ring): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 63 of 79 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
