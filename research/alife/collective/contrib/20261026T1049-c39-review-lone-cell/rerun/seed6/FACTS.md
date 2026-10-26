# Evidence pack: ringswim-dl2 (seed 6)

- world: `../../../20261026T0227-c29-kernel-ring-screen/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 287s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/c39-rev-lone-wip/rerun/seed6 --seeds 6 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.59], min area 6 px

## Measurements
- components: final 291, mean 183.8, max 291; occupancy final 0.38
- tracks: 1532; persistent (alive >= 50% of run): 86; longest 155 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.19 (1 = constant size)
- enclosures: components with a hole mean 0.27, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [291, 291, 291], H1 [0, 0, 0]
- motion: 114 long-lived tracks moved >= 1 body length; max speed 0.0388/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 1000, default): splits 616, persistent splits 215 (1 more failed only because the siblings re-merged within K), max generation 6, merges 156, merge/split ratio 0.253, nucleations 2
- channel total drift (end/start - 1): [-0.5545, -0.7058, 0.419, 0.3795]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 625 at frame 124: holes 0, rim-vs-core 0.62, rim-vs-outside 0.56, heterogeneity 0.18; core [0.124, 0.765, 0.706, 0.869] rim [0.286, 0.346, 0.414, 0.563]
  - track 665 at frame 124: holes 0, rim-vs-core 0.65, rim-vs-outside 0.56, heterogeneity 0.18; core [0.13, 0.78, 0.72, 0.87] rim [0.293, 0.331, 0.402, 0.568]
  - track 755 at frame 128: holes 0, rim-vs-core 0.78, rim-vs-outside 0.53, heterogeneity 0.21; core [0.186, 0.834, 0.797, 0.87] rim [0.366, 0.29, 0.389, 0.541]
  - track 1395 at frame 163: holes 0, rim-vs-core 0.61, rim-vs-outside 0.59, heterogeneity 0.17; core [0.134, 0.776, 0.747, 0.896] rim [0.273, 0.375, 0.438, 0.587]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1221 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 6.88, rim/outside 0.935 (aggregate of 1221 individuals; 0/1221 membrane-like individually; rim level 0.397)
  - radial K catalyst: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 9.64 (aggregate of 1221 individuals; 3/1221 membrane-like individually; rim level 0.704)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.57, rim/outside 8.76 (aggregate of 1221 individuals; 875/1221 membrane-like individually; rim level 0.792)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 7.69 (aggregate of 1221 individuals; 6/1221 membrane-like individually; rim level 0.917)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link
- membrane-like channels per top track at mid-life: #625 (t=6200, R_eq 5.47): ['L link']; #665 (t=6200, R_eq 5.64): none; #755 (t=6400, R_eq 4.92): ['L link']; #1395 (t=8150, R_eq 5.35): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 1221 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
