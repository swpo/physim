# Evidence pack: active-nematic-marangoni-turnover (seed 80)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) plus a trait-blind random dilution of whole bodies every 10 frames (serial-transfer turnover)
- run: 151 frames x 100 steps x dt 0.05 = time 750; grid [128, 128]; wall 271s; status ok
- command: `python -m labkit.run /tmp/claude-0/mt/world.py --out /tmp/claude-0/mt/runs/tune_p0.10/seed80 --seeds 80 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8327, 0.5681], min area 6 px

## Measurements
- components: final 14, mean 17.5, max 26; occupancy final 0.05
- tracks: 90; persistent (alive >= 50% of run): 3; longest 97 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.21 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 14, 14], H1 [0, 0, 0]
- motion: 44 long-lived tracks moved >= 1 body length; max speed 0.39/time; max body lengths 6.2
- replication (lineage window K = 20 frames = time 100, default): splits 36, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 3, merges 4, merge/split ratio 0.111, nucleations 14
- channel total drift (end/start - 1): [-0.566, -0.6441, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 44 at frame 102: holes 0, rim-vs-core 0.40, rim-vs-outside 0.50, heterogeneity 0.15; core [0.967, 0.679, 0.441, 0.0] rim [0.82, 0.612, 0.803, 0.0]
  - track 48 at frame 106: holes 0, rim-vs-core 0.55, rim-vs-outside 0.32, heterogeneity 0.14; core [0.935, 0.702, 0.478, 0.0] rim [0.73, 0.465, 0.924, 0.0]
  - track 16 at frame 64: holes 0, rim-vs-core 0.56, rim-vs-outside 0.33, heterogeneity 0.14; core [0.96, 0.663, 0.412, 0.0] rim [0.754, 0.432, 0.875, 0.0]
  - track 73 at frame 130: holes 0, rim-vs-core 0.62, rim-vs-outside 0.37, heterogeneity 0.16; core [0.963, 0.802, 0.421, 0.0] rim [0.764, 0.511, 0.925, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 112 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.782, rim/outside 4.27 (aggregate of 112 individuals; 0/112 membrane-like individually; rim level 0.697)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.741, rim/outside 8.03 (aggregate of 112 individuals; 5/112 membrane-like individually; rim level 0.545)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 3.3 (aggregate of 112 individuals; 52/112 membrane-like individually; rim level 0.602)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 112 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #44 (t=510, R_eq 4.26): none; #48 (t=530, R_eq 4.37): none; #16 (t=320, R_eq 4.37): none; #73 (t=650, R_eq 4.07): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 112 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
