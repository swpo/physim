# Evidence pack: phase-membrane (seed 1)

- world: `../../../worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 12s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out threads/autopoiesis/packs/phase_membrane_damage_mature/seed1 --seeds 1 --frames 160 --damage 120:0.5:rim --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5366], min area 6 px

## Measurements
- components: final 15, mean 16.2, max 27; occupancy final 0.28
- tracks: 161; persistent (alive >= 50% of run): 2; longest 90 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.61 (1 = constant size)
- enclosures: components with a hole mean 10.84, final 5; holes at thresholds 0.2/0.35/0.5 final [3, 5, 9]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [15, 11, 4]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0248/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 61, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 12, merge/split ratio 0.197, nucleations 0
- channel total drift (end/start - 1): [-0.4565, -0.7319, -0.0403, -0.0471]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 53 at frame 47: holes 1, rim-vs-core 0.18, rim-vs-outside 0.75, heterogeneity 0.18; core [0.097, 0.746, 0.553, 0.684] rim [0.147, 0.601, 0.494, 0.612]
  - track 88 at frame 94: holes 0, rim-vs-core 0.54, rim-vs-outside 0.99, heterogeneity 0.22; core [0.095, 0.868, 0.58, 0.474] rim [0.319, 0.466, 0.593, 0.755]
  - track 77 at frame 62: holes 1, rim-vs-core 0.18, rim-vs-outside 0.82, heterogeneity 0.19; core [0.098, 0.777, 0.558, 0.632] rim [0.164, 0.618, 0.519, 0.609]
  - track 81 at frame 56: holes 1, rim-vs-core 0.19, rim-vs-outside 0.81, heterogeneity 0.19; core [0.095, 0.769, 0.541, 0.628] rim [0.168, 0.602, 0.512, 0.61]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 98 components >= 12 px at frames [27, 54, 81, 106, 133, 160]; 2 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 11.3, rim/outside 0.877 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.458)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 4.95 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.709)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.66, rim/outside 3.88 (aggregate of 98 individuals; 79/98 membrane-like individually; rim level 0.559)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.49, rim/outside 3.95 (aggregate of 98 individuals; 79/98 membrane-like individually; rim level 0.638)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #53 (t=2350, R_eq 13.91, ring): ['L link', 'membrane (wall)']; #88 (t=4700, R_eq 8.12): ['L link', 'membrane (wall)']; #77 (t=3100, R_eq 10.97, ring): ['L link', 'membrane (wall)']; #81 (t=2800, R_eq 11.23, ring): ['L link', 'membrane (wall)']
- damage `rim` (requested 0.50 of the area) at frame 120 (t=6000): target track #129 (rule mature-compact: track age 25 frames vs K=20, area 191 px = 0.64x median, aspect 1.04); mask 97 px (46 inside the component)
- damage MEASURED: the target lost 24.9% of its matter (46 of 191 px lost > half their matter); matter lost outside it = 1.25% of its matter; share of all lost matter that was under labkit's mask 1
- (rim mode: the disk has the requested area but is centred on the boundary, so about half of it lies outside the matter component and cuts the layer at the edge)
- after damage, area of the individual's largest piece / area before the cut at t=[6000.0, 6400.0, 6800.0, 7200.0, 7600.0, 8000.0]: target #129 [0.822, None, None, None, None, None]; comparator #130 [1.064, 1.355, 1.32, 1.744, 1.951, None] (followed through its own splits and re-merges; None = died or merged with another individual); target lineage tracks []; baseline recorded frame 119 (damage.png)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 62 of 98 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, damage.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
