# Evidence pack: active-nematic-marangoni-ladder (seed 102)

- world: `../../../20261026T2018-c45-marangoni-ladder/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 947s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2018-c45-marangoni-ladder/world.py --out collective/contrib/c49rev8/runs/twin_s102 --seeds 102 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8299, 0.5744], min area 6 px

## Measurements
- components: final 25, mean 19.4, max 27; occupancy final 0.08
- tracks: 258; persistent (alive >= 50% of run): 0; longest 153 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 25, 23], H1 [0, 0, 0]
- motion: 125 long-lived tracks moved >= 1 body length; max speed 0.411/time; max body lengths 9.1
- replication (lineage window K = 20 frames = time 100, default): splits 118, persistent splits 50 (0 more failed only because the siblings re-merged within K), max generation 10, merges 19, merge/split ratio 0.161, nucleations 5
- channel total drift (end/start - 1): [-0.4886, -0.4775, 9.2702, 5.6344, -0.9929]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 141: holes 0, rim-vs-core 0.65, rim-vs-outside 0.36, heterogeneity 0.13; core [0.96, 0.847, 0.383, 0.005, 0.008] rim [0.763, 0.529, 0.913, 0.014, 0.025]
  - track 77 at frame 205: holes 0, rim-vs-core 0.51, rim-vs-outside 0.32, heterogeneity 0.12; core [0.942, 0.558, 0.415, 0.006, 0.0] rim [0.734, 0.376, 0.838, 0.014, 0.001]
  - track 114 at frame 255: holes 0, rim-vs-core 0.62, rim-vs-outside 0.30, heterogeneity 0.14; core [0.965, 0.57, 0.406, 0.017, 0.012] rim [0.771, 0.325, 0.944, 0.046, 0.031]
  - track 219 at frame 370: holes 0, rim-vs-core 0.53, rim-vs-outside 0.33, heterogeneity 0.11; core [0.944, 0.741, 0.413, 0.013, 0.0] rim [0.743, 0.48, 0.833, 0.029, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 130 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 4.24 (aggregate of 130 individuals; 0/130 membrane-like individually; rim level 0.695)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 8.03 (aggregate of 130 individuals; 14/130 membrane-like individually; rim level 0.525)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 3.05 (aggregate of 130 individuals; 50/130 membrane-like individually; rim level 0.388)
  - radial s1 (mar 40): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 2.96 (aggregate of 130 individuals; 38/130 membrane-like individually; rim level 0.217)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 2.45 (aggregate of 130 individuals; 17/130 membrane-like individually; rim level 0.0749)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #30 (t=705, R_eq 4.72): none; #77 (t=1025, R_eq 4.44): ['order |Q|']; #114 (t=1275, R_eq 4.33): ['s1 (mar 40)']; #219 (t=1850, R_eq 4.03): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 130 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
