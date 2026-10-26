# Evidence pack: ringswim-dl2 (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 477s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/rev4/lk_s5 --seeds 5 --frames 200 --size 256 256 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5902], min area 6 px

## Measurements
- components: final 285, mean 184.5, max 285; occupancy final 0.38
- tracks: 1555; persistent (alive >= 50% of run): 63; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.44 (1 = constant size)
- enclosures: components with a hole mean 0.40, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [285, 285, 285], H1 [0, 0, 0]
- motion: 143 long-lived tracks moved >= 1 body length; max speed 0.0316/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 1000, default): splits 623, persistent splits 235 (1 more failed only because the siblings re-merged within K), max generation 6, merges 121, merge/split ratio 0.194, nucleations 2
- channel total drift (end/start - 1): [-0.5546, -0.7059, 0.424, 0.3465]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 708 at frame 126: holes 0, rim-vs-core 0.38, rim-vs-outside 0.94, heterogeneity 0.18; core [0.069, 0.808, 0.592, 0.798] rim [0.244, 0.474, 0.565, 0.741]
  - track 759 at frame 128: holes 0, rim-vs-core 0.55, rim-vs-outside 0.54, heterogeneity 0.16; core [0.129, 0.72, 0.708, 0.907] rim [0.267, 0.395, 0.444, 0.571]
  - track 771 at frame 129: holes 0, rim-vs-core 0.57, rim-vs-outside 0.58, heterogeneity 0.16; core [0.117, 0.747, 0.692, 0.885] rim [0.262, 0.374, 0.424, 0.574]
  - track 1472 at frame 168: holes 0, rim-vs-core 0.31, rim-vs-outside 0.96, heterogeneity 0.15; core [0.057, 0.765, 0.571, 0.826] rim [0.211, 0.509, 0.581, 0.763]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1206 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 6.23, rim/outside 0.937 (aggregate of 1206 individuals; 0/1206 membrane-like individually; rim level 0.404)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 8.89 (aggregate of 1206 individuals; 4/1206 membrane-like individually; rim level 0.7)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.56, rim/outside 8.25 (aggregate of 1206 individuals; 856/1206 membrane-like individually; rim level 0.784)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 7.24 (aggregate of 1206 individuals; 4/1206 membrane-like individually; rim level 0.912)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #708 (t=6300, R_eq 6.18): ['L link']; #759 (t=6400, R_eq 5.73): none; #771 (t=6450, R_eq 5.61): ['L link']; #1472 (t=8400, R_eq 6.23): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 1206 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
