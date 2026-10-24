# Evidence pack: membrane-evo-up (seed 4)

- world: `../../worlds/membrane_evo_up/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 94s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo_up/world.py --out threads/autopoiesis/packs/membrane_evo_up --seeds 4 --frames 160 --spf 250`
- segmentation: matter > 0.35 of robust range [0.0, 1.7271], min area 6 px

## Measurements
- components: final 15, mean 9.8, max 20; occupancy final 0.32
- tracks: 180; persistent (alive >= 50% of run): 1; longest 97 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 39.80 (1 = constant size)
- enclosures: components with a hole mean 7.40, final 13; holes at thresholds 0.2/0.35/0.5 final [11, 15, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 17, 13], H1 [22, 16, 13]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.00361/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 5000, default): splits 64, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 25, merge/split ratio 0.391, nucleations 1
- channel total drift (end/start - 1): [-0.9882, None, 0.5761, -0.109]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 89: holes 0, rim-vs-core 0.61, rim-vs-outside 0.94, heterogeneity 0.22; core [0.842, 0.0, 0.582, 0.46] rim [0.355, 0.0, 0.617, 0.827]
  - track 46 at frame 102: holes 1, rim-vs-core 0.40, rim-vs-outside 0.72, heterogeneity 0.22; core [0.832, 0.0, 0.669, 0.551] rim [0.459, 0.0, 0.546, 0.626]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 65 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 11.5 (aggregate of 65 individuals; 4/65 membrane-like individually; rim level 0.427)
  - radial K2: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 2.11 (aggregate of 65 individuals; 1/65 membrane-like individually; rim level 0.224)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 3.47 (aggregate of 65 individuals; 41/65 membrane-like individually; rim level 0.535)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.2, rim/outside 2.37 (aggregate of 65 individuals; 50/65 membrane-like individually; rim level 0.464)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #28 (t=22250, R_eq 6.48): ['L link', 'membrane (wall)']; #69 (t=30000, R_eq 15.65, ring): none; #46 (t=25500, R_eq 8.08, ring): ['L link', 'membrane (wall)']; #23 (t=15250, R_eq 10.22, ring): ['K1', 'L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 48 of 65 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
