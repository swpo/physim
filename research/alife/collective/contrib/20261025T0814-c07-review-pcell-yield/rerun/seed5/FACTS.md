# Evidence pack: pcell-y07 (seed 5)

- world: `../../world_y07.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 80 steps x dt 1.0 = time 16000; grid [128, 128]; wall 70s; status ok
- command: `python -m labkit.run collective/contrib/_c07rev4/world_y07.py --out collective/contrib/_c07rev4/rerun/seed5 --seeds 5 --spf 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.618], min area 6 px

## Measurements
- components: final 24, mean 20.9, max 28; occupancy final 0.32
- tracks: 88; persistent (alive >= 50% of run): 17; longest 198 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.52 (1 = constant size)
- enclosures: components with a hole mean 6.95, final 11; holes at thresholds 0.2/0.35/0.5 final [0, 12, 18]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 24, 24], H1 [18, 18, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.00134/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 1600, default): splits 23, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.13, nucleations 1
- channel total drift (end/start - 1): [-0.4594, -0.6905, 0.0515, -0.2427]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 103: holes 0, rim-vs-core 0.68, rim-vs-outside 0.55, heterogeneity 0.23; core [0.21, 0.665, 0.816, 0.711] rim [0.445, 0.146, 0.469, 0.606]
  - track 44 at frame 103: holes 0, rim-vs-core 0.31, rim-vs-outside 0.88, heterogeneity 0.23; core [0.137, 0.643, 0.709, 0.496] rim [0.264, 0.403, 0.661, 0.639]
  - track 46 at frame 103: holes 0, rim-vs-core 0.72, rim-vs-outside 0.52, heterogeneity 0.22; core [0.252, 0.692, 0.877, 0.787] rim [0.448, 0.161, 0.486, 0.567]
  - track 80 at frame 151: holes 0, rim-vs-core 0.31, rim-vs-outside 0.83, heterogeneity 0.21; core [0.125, 0.587, 0.656, 0.498] rim [0.25, 0.337, 0.618, 0.628]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 129 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.27, rim/outside 0.851 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.586)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.734, rim/outside 26 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.539)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.55, rim/outside 21.7 (aggregate of 129 individuals; 100/129 membrane-like individually; rim level 0.79)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.85, rim/outside 18.1 (aggregate of 129 individuals; 124/129 membrane-like individually; rim level 0.805)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #38 (t=8240, R_eq 5.89): ['L link', 'membrane (wall)']; #44 (t=8240, R_eq 7.53): ['L link', 'membrane (wall)']; #46 (t=8240, R_eq 5.2): ['membrane (wall)']; #80 (t=12080, R_eq 8.1): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 41 of 129 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
