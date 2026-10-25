# Evidence pack: membrane-evo-up (seed 57)

- world: `../../world_up.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 91s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_up.py --out collective/contrib/c17-mevo-wip/up/seed57 --seeds 57 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7229], min area 6 px

## Measurements
- components: final 14, mean 9.6, max 17; occupancy final 0.32
- tracks: 145; persistent (alive >= 50% of run): 0; longest 53 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 7.74, final 12; holes at thresholds 0.2/0.35/0.5 final [10, 12, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 14, 14], H1 [18, 14, 11]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00269/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 5000, default): splits 55, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 18, merge/split ratio 0.327, nucleations 2
- channel total drift (end/start - 1): [-0.9606, None, 0.5305, -0.0211]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 66: holes 1, rim-vs-core 0.33, rim-vs-outside 0.70, heterogeneity 0.20; core [0.813, 0.0, 0.657, 0.583] rim [0.507, 0.0, 0.557, 0.633]
  - track 23 at frame 66: holes 1, rim-vs-core 0.42, rim-vs-outside 0.65, heterogeneity 0.22; core [0.839, 0.0, 0.733, 0.592] rim [0.459, 0.0, 0.548, 0.592]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 9.1 (aggregate of 64 individuals; 4/64 membrane-like individually; rim level 0.428)
  - radial K2: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 1.82 (aggregate of 64 individuals; 2/64 membrane-like individually; rim level 0.191)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 3.12 (aggregate of 64 individuals; 35/64 membrane-like individually; rim level 0.499)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.23, rim/outside 2.13 (aggregate of 64 individuals; 42/64 membrane-like individually; rim level 0.43)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #21 (t=16500, R_eq 9.42, ring): ['K1', 'L link', 'membrane (wall)']; #23 (t=16500, R_eq 9.93, ring): ['K1', 'L link', 'membrane (wall)']; #1 (t=5500, R_eq 19.5, ring): none; #97 (t=36000, R_eq 11.83, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 49 of 64 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
