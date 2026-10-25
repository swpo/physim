# Evidence pack: membrane-evo-up (seed 32)

- world: `../../membrane_evo_up_nodisk.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 136s; status ok
- command: `python -m labkit.run collective/work_c05/rev_md/membrane_evo_up_nodisk.py --out collective/work_c05/rev_md/rerun/seed32 --seeds 32 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7048], min area 6 px

## Measurements
- components: final 11, mean 7.3, max 15; occupancy final 0.27
- tracks: 31; persistent (alive >= 50% of run): 8; longest 124 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.84 (1 = constant size)
- enclosures: components with a hole mean 4.30, final 10; holes at thresholds 0.2/0.35/0.5 final [4, 10, 11]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 11, 11], H1 [11, 11, 5]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00165/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 5000, default): splits 8, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.5519, None, 0.292, -0.2282]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 102: holes 0, rim-vs-core 0.74, rim-vs-outside 0.95, heterogeneity 0.23; core [0.905, 0.0, 0.655, 0.406] rim [0.298, 0.0, 0.672, 0.834]
  - track 19 at frame 105: holes 1, rim-vs-core 0.53, rim-vs-outside 0.73, heterogeneity 0.23; core [0.903, 0.0, 0.726, 0.526] rim [0.406, 0.0, 0.574, 0.617]
  - track 20 at frame 105: holes 1, rim-vs-core 0.50, rim-vs-outside 0.83, heterogeneity 0.23; core [0.886, 0.0, 0.673, 0.449] rim [0.443, 0.0, 0.629, 0.683]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 11.3 (aggregate of 48 individuals; 1/48 membrane-like individually; rim level 0.679)
  - radial K2: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.66, rim/outside 0.745 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.0437)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.65, rim/outside 4.81 (aggregate of 48 individuals; 29/48 membrane-like individually; rim level 0.648)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 4.36, rim/outside 3.62 (aggregate of 48 individuals; 33/48 membrane-like individually; rim level 0.58)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #0 (t=15500, R_eq 21.2, ring): none; #18 (t=25500, R_eq 6.51): ['L link', 'membrane (wall)']; #19 (t=26250, R_eq 7.78, ring): ['L link', 'membrane (wall)']; #20 (t=26250, R_eq 7.2, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 33 of 48 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
