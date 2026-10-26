# Evidence pack: cips-layered-lownoise (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 251 frames x 1000 steps x dt 0.1 = time 25000; grid [192, 192]; wall 1910s; status ok
- command: `python -m labkit.run world.py --out pack/seed0 --seeds 0 --frames 250 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0208, 0.9745], min area 6 px

## Measurements
- components: final 17, mean 8.8, max 17; occupancy final 0.09
- tracks: 32; persistent (alive >= 50% of run): 5; longest 163 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.00398/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 15, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 2
- channel total drift (end/start - 1): [0.0, -0.5894, 0.6352, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 170: holes 0, rim-vs-core 0.54, rim-vs-outside 0.63, heterogeneity 0.16; core [0.989, 0.957, 0.046, 0.08] rim [0.786, 0.716, 0.226, 0.486]
  - track 8 at frame 170: holes 0, rim-vs-core 0.57, rim-vs-outside 0.61, heterogeneity 0.17; core [0.985, 0.951, 0.045, 0.082] rim [0.772, 0.706, 0.227, 0.516]
  - track 11 at frame 174: holes 0, rim-vs-core 0.56, rim-vs-outside 0.64, heterogeneity 0.16; core [0.989, 0.96, 0.05, 0.079] rim [0.783, 0.714, 0.233, 0.501]
  - track 22 at frame 212: holes 0, rim-vs-core 0.55, rim-vs-outside 0.63, heterogeneity 0.16; core [0.988, 0.956, 0.039, 0.085] rim [0.784, 0.712, 0.222, 0.491]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 60 components >= 12 px at frames [42, 84, 126, 166, 208, 250]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 28.3 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.834)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.856, rim/outside 11.3 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.814)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 24.1, rim/outside 0.645 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.48)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 3.88, rim/outside 14.6 (aggregate of 60 individuals; 55/60 membrane-like individually; rim level 0.454)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #7 (t=17000, R_eq 7.67): ['s']; #8 (t=17000, R_eq 7.96): ['s']; #11 (t=17400, R_eq 7.55): ['s']; #22 (t=21200, R_eq 7.98): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
