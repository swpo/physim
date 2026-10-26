# Evidence pack: phoretic-colloids (seed 5)

- world: `../../world_claim.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 172s; status ok
- command: `python -m labkit.run world_claim.py --out rerun/seed5 --seeds 5 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5081], min area 6 px

## Measurements
- components: final 19, mean 18.6, max 32; occupancy final 0.06
- tracks: 312; persistent (alive >= 50% of run): 5; longest 554 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 18, 10], H1 [0, 0, 0]
- motion: 59 long-lived tracks moved >= 1 body length; max speed 0.478/time; max body lengths 10.0
- replication (lineage window K = 20 frames = time 10, default): splits 31, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 46, merge/split ratio 1.48, nucleations 204
- channel total drift (end/start - 1): [0.4043, 0.43, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 329: holes 0, rim-vs-core 0.30, rim-vs-outside 0.41, heterogeneity 0.12; core [0.926, 0.108, 0.622] rim [0.652, 0.058, 0.508]
  - track 165 at frame 545: holes 0, rim-vs-core 0.42, rim-vs-outside 0.34, heterogeneity 0.20; core [0.926, 0.162, 0.861] rim [0.565, 0.131, 0.648]
  - track 123 at frame 417: holes 0, rim-vs-core 0.44, rim-vs-outside 0.35, heterogeneity 0.22; core [0.878, 0.338, 0.938] rim [0.497, 0.346, 0.722]
  - track 261 at frame 652: holes 0, rim-vs-core 0.30, rim-vs-outside 0.33, heterogeneity 0.21; core [0.811, 0.31, 0.6] rim [0.549, 0.242, 0.482]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 109 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 15.6 (aggregate of 109 individuals; 3/109 membrane-like individually; rim level 0.631)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 13.1 (aggregate of 109 individuals; 40/109 membrane-like individually; rim level 0.36)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 2.54 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.577)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=164.5, R_eq 3.83): ['B density']; #165 (t=272.5, R_eq 4.82): none; #123 (t=208.5, R_eq 5.29): ['B density']; #261 (t=326, R_eq 3.61): ['B density']

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
