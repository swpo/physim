# Evidence pack: ringswim-waste (seed 8)

- world: `../../../../contrib/20261025T0806-c07-ringswim-claim/world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 124s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py --out collective/work_c05/rev_rs/rerun/seed8 --seeds 8 --spf 100 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5501], min area 6 px

## Measurements
- components: final 6, mean 8.4, max 24; occupancy final 0.16
- tracks: 417; persistent (alive >= 50% of run): 0; longest 24 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 6.01, final 5; holes at thresholds 0.2/0.35/0.5 final [0, 7, 6]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 6], H1 [7, 6, 4]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0437/time; max body lengths 4.6
- replication (lineage window K = 20 frames = time 2000, default): splits 139, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 122, merge/split ratio 0.878, nucleations 5
- channel total drift (end/start - 1): [-0.2761, -0.8397, -0.3922, -0.5856]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 247 at frame 108: holes 1, rim-vs-core 0.18, rim-vs-outside 0.80, heterogeneity 0.23; core [0.087, 0.676, 0.514, 0.684] rim [0.207, 0.596, 0.552, 0.583]
  - track 314 at frame 139: holes 1, rim-vs-core 0.16, rim-vs-outside 0.77, heterogeneity 0.21; core [0.085, 0.66, 0.483, 0.652] rim [0.192, 0.553, 0.517, 0.606]
  - track 331 at frame 151: holes 1, rim-vs-core 0.17, rim-vs-outside 0.79, heterogeneity 0.20; core [0.121, 0.701, 0.607, 0.66] rim [0.189, 0.572, 0.539, 0.606]
  - track 254 at frame 109: holes 1, rim-vs-core 0.37, rim-vs-outside 0.80, heterogeneity 0.24; core [0.128, 0.818, 0.667, 0.552] rim [0.28, 0.509, 0.533, 0.587]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 47 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 10.4, rim/outside 0.788 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.551)
  - radial K catalyst: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.988, rim/outside 9.75 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.633)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.44, rim/outside 7.22 (aggregate of 47 individuals; 27/47 membrane-like individually; rim level 0.555)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.82, rim/outside 7.97 (aggregate of 47 individuals; 27/47 membrane-like individually; rim level 0.554)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #247 (t=10800, R_eq 10.06, ring): ['L link', 'membrane (wall)']; #314 (t=13900, R_eq 11.26, ring): ['L link', 'membrane (wall)']; #331 (t=15100, R_eq 11.55, ring): ['K catalyst', 'L link', 'membrane (wall)']; #254 (t=10900, R_eq 8.67, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 18 of 47 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
