# Evidence pack: active-nematic-droplets (seed 4)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1036-c11-active-nematic-res15/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 679s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1036-c11-active-nematic-res15/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/nemr/res/seed4 --seeds 4 --size 192 192 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8026, 0.5369], min area 6 px

## Measurements
- components: final 14, mean 5.4, max 14; occupancy final 0.03
- tracks: 27; persistent (alive >= 50% of run): 0; longest 97 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 14, 14], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.0904/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 100, default): splits 12, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.5014, -0.711, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 153: holes 0, rim-vs-core 0.33, rim-vs-outside 0.27, heterogeneity 0.16; core [0.963, 0.952, 0.288] rim [0.768, 0.69, 0.321]
  - track 10 at frame 153: holes 0, rim-vs-core 0.30, rim-vs-outside 0.29, heterogeneity 0.16; core [0.969, 0.943, 0.531] rim [0.783, 0.708, 0.537]
  - track 11 at frame 153: holes 0, rim-vs-core 0.34, rim-vs-outside 0.30, heterogeneity 0.18; core [0.971, 0.97, 0.367] rim [0.768, 0.706, 0.419]
  - track 19 at frame 190: holes 0, rim-vs-core 0.31, rim-vs-outside 0.32, heterogeneity 0.16; core [0.978, 0.986, 0.318] rim [0.783, 0.766, 0.424]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 37 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 4.9 (aggregate of 37 individuals; 0/37 membrane-like individually; rim level 0.784)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.838, rim/outside 7.63 (aggregate of 37 individuals; 0/37 membrane-like individually; rim level 0.766)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=765, R_eq 4.55): none; #10 (t=765, R_eq 5.47): none; #11 (t=765, R_eq 4.44): none; #19 (t=950, R_eq 4.44): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
