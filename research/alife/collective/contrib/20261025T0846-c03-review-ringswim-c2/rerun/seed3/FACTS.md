# Evidence pack: ringswim-waste (seed 3)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 114s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/rsw/claim/seed3 --seeds 3 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5611], min area 6 px

## Measurements
- components: final 9, mean 11.2, max 17; occupancy final 0.25
- tracks: 581; persistent (alive >= 50% of run): 0; longest 33 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 7.53, final 7; holes at thresholds 0.2/0.35/0.5 final [2, 11, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 11, 9], H1 [14, 13, 7]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.0277/time; max body lengths 3.8
- replication (lineage window K = 20 frames = time 2000, default): splits 204, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 168, merge/split ratio 0.824, nucleations 1
- channel total drift (end/start - 1): [-0.3984, -0.7692, -0.13, -0.3325]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 413 at frame 151: holes 0, rim-vs-core 0.35, rim-vs-outside 0.72, heterogeneity 0.16; core [0.111, 0.697, 0.553, 0.821] rim [0.256, 0.429, 0.54, 0.646]
  - track 7 at frame 15: holes 1, rim-vs-core 0.27, rim-vs-outside 0.67, heterogeneity 0.19; core [0.112, 0.667, 0.572, 0.707] rim [0.209, 0.475, 0.477, 0.578]
  - track 464 at frame 170: holes 1, rim-vs-core 0.28, rim-vs-outside 0.71, heterogeneity 0.21; core [0.107, 0.715, 0.585, 0.641] rim [0.224, 0.486, 0.498, 0.584]
  - track 429 at frame 151: holes 1, rim-vs-core 0.30, rim-vs-outside 0.71, heterogeneity 0.21; core [0.132, 0.737, 0.652, 0.654] rim [0.227, 0.506, 0.5, 0.576]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.23, rim/outside 0.798 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.502)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 6.44 (aggregate of 62 individuals; 4/62 membrane-like individually; rim level 0.63)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.52, rim/outside 5.24 (aggregate of 62 individuals; 43/62 membrane-like individually; rim level 0.558)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.24, rim/outside 5.79 (aggregate of 62 individuals; 45/62 membrane-like individually; rim level 0.6)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #413 (t=15100, R_eq 6.93): none; #7 (t=1500, R_eq 9.98, ring): ['L link', 'membrane (wall)']; #464 (t=17000, R_eq 9.47, ring): ['L link', 'membrane (wall)']; #429 (t=15100, R_eq 9.27, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 37 of 62 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
