# Evidence pack: membrane-evo-up-chi0 (seed 21)

- world: `../../world_up_chi0.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 96s; status ok
- command: `python -m labkit.run collective/contrib/wip-c22/rev_me/world_up_chi0.py --out collective/contrib/wip-c22/rev_me/up_chi0/seed21 --seeds 21 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5596], min area 6 px

## Measurements
- components: final 0, mean 1.3, max 14; occupancy final 0.00
- tracks: 14; persistent (alive >= 50% of run): 1; longest 85 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 36.74 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00222/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 5000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-1.0, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 42: holes 0, rim-vs-core 0.92, rim-vs-outside 0.99, heterogeneity 0.27; core [0.983, 0.0, 1.0, 0.443] rim [0.284, 0.0, 0.653, 0.935]
  - track 0 at frame 40: holes 0, rim-vs-core 0.98, rim-vs-outside 0.94, heterogeneity 0.27; core [0.955, 0.0, 0.993, 0.397] rim [0.222, 0.0, 0.624, 0.933]
  - track 8 at frame 16: holes 0, rim-vs-core 0.56, rim-vs-outside 0.73, heterogeneity 0.18; core [0.333, 0.0, 1.0, 1.0] rim [0.0, 0.0, 0.593, 0.805]
  - track 2 at frame 0: holes 0, rim-vs-core 0.28, rim-vs-outside 0.32, heterogeneity 0.13; core [0.633, 0.0, 0.215, 0.548] rim [0.831, 0.0, 0.277, 0.36]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [27, 54, 81]):
  - radial K1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.946, rim/outside 82.7 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.817)
  - radial K2: flat profile (no radial structure; level 0; aggregate of 6 individuals)
  - radial L link: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 100 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.994)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 9.18, rim/outside 64.1 (aggregate of 6 individuals; 5/6 membrane-like individually; rim level 0.97)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #1 (t=10500, R_eq 6.26): ['membrane (wall)']; #0 (t=10000, R_eq 7): ['membrane (wall)']; #8 (t=4000, R_eq 2.26): none; #2 (t=0, R_eq 2.33): ['K1']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
