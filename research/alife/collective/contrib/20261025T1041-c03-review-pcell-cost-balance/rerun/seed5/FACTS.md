# Evidence pack: pcell (seed 5)

- world: `../../world_cy0.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 44s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/pcb/world_cy0.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/pcb/pack_cy0/seed5 --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5316], min area 6 px

## Measurements
- components: final 22, mean 19.0, max 22; occupancy final 0.36
- tracks: 70; persistent (alive >= 50% of run): 19; longest 191 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.00 (1 = constant size)
- enclosures: components with a hole mean 8.21, final 8; holes at thresholds 0.2/0.35/0.5 final [1, 8, 20]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 22, 22], H1 [22, 21, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 1000, default): splits 20, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 2, merge/split ratio 0.1, nucleations 0
- channel total drift (end/start - 1): [-0.4918, -0.6668, 0.1206, -0.1967]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 106: holes 1, rim-vs-core 0.47, rim-vs-outside 0.79, heterogeneity 0.22; core [0.132, 0.662, 0.665, 0.486] rim [0.302, 0.267, 0.602, 0.664]
  - track 36 at frame 106: holes 1, rim-vs-core 0.36, rim-vs-outside 0.72, heterogeneity 0.21; core [0.133, 0.6, 0.637, 0.524] rim [0.276, 0.294, 0.563, 0.614]
  - track 42 at frame 108: holes 0, rim-vs-core 0.53, rim-vs-outside 0.92, heterogeneity 0.23; core [0.115, 0.75, 0.652, 0.421] rim [0.314, 0.347, 0.661, 0.706]
  - track 51 at frame 111: holes 1, rim-vs-core 0.42, rim-vs-outside 0.77, heterogeneity 0.21; core [0.127, 0.596, 0.622, 0.491] rim [0.294, 0.255, 0.565, 0.66]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 122 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 9.61, rim/outside 0.92 (aggregate of 122 individuals; 0/122 membrane-like individually; rim level 0.565)
  - radial K particles: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 13.6 (aggregate of 122 individuals; 0/122 membrane-like individually; rim level 0.542)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.52, rim/outside 9.07 (aggregate of 122 individuals; 86/122 membrane-like individually; rim level 0.692)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 4.97, rim/outside 7.48 (aggregate of 122 individuals; 113/122 membrane-like individually; rim level 0.695)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #33 (t=5300, R_eq 8.25): ['L link', 'membrane (wall)']; #36 (t=5300, R_eq 9.85, ring): ['membrane (wall)']; #42 (t=5400, R_eq 7.57): ['L link', 'membrane (wall)']; #51 (t=5550, R_eq 9.52): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 43 of 122 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
