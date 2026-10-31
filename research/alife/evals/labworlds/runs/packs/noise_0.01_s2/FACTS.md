# Evidence pack: phase-membrane-noise (seed 2)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: additive dynamics noise sd 0.01 per sqrt(t) on ['S', 'K', 'L', 'phi']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 24s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/noise_0.01_s2 --seeds 2 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0129, 1.4672], min area 6 px

## Measurements
- components: final 0, mean 1.1, max 39; occupancy final 0.00
- tracks: 73; persistent (alive >= 50% of run): 0; longest 62 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.40, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [260, 84, 5], H1 [223, 36, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 1000, default): splits 14, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 0.429, nucleations 22
- channel total drift (end/start - 1): [-0.237, -0.8781, 0.5709, -0.928]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 35 at frame 32: holes 1, rim-vs-core 0.22, rim-vs-outside 0.72, heterogeneity 0.20; core [0.094, 0.871, 0.535, 0.643] rim [0.168, 0.676, 0.481, 0.608]
  - track 55 at frame 11: holes 0, rim-vs-core 0.31, rim-vs-outside 0.77, heterogeneity 0.18; core [0.118, 0.784, 0.546, 0.875] rim [0.192, 0.593, 0.495, 0.653]
  - track 56 at frame 11: holes 0, rim-vs-core 0.38, rim-vs-outside 0.66, heterogeneity 0.17; core [0.091, 0.778, 0.493, 0.785] rim [0.26, 0.465, 0.517, 0.648]
  - track 62 at frame 9: holes 1, rim-vs-core 0.21, rim-vs-outside 0.72, heterogeneity 0.16; core [0.054, 0.673, 0.322, 0.848] rim [0.111, 0.578, 0.374, 0.672]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 2 components >= 12 px at frames [27, 54]):
  - radial S: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 43.8, rim/outside 0.695 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.469)
  - radial K catalyst: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 7.15 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.834)
  - radial L link: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.37, rim/outside 2.15 (aggregate of 2 individuals; 2/2 membrane-like individually; rim level 0.595)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 9.56, rim/outside 28 (aggregate of 2 individuals; 2/2 membrane-like individually; rim level 0.85)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #35 (t=1600, R_eq 11.06, ring): ['L link', 'membrane (wall)']; #55 (t=550, R_eq 8.18): ['L link', 'membrane (wall)']; #56 (t=550, R_eq 8.25): ['L link', 'membrane (wall)']; #62 (t=450, R_eq 14.64): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 2 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
