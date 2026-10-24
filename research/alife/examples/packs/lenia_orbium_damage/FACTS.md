# Evidence pack: lenia-orbium-ref (seed 0)

- world: `../../lenia_orbium/world.py`, family `lenia`
- parent: None; mutation: reference
- run: 151 frames x 2 steps x dt 0.1 = time 30; grid [128, 128]; wall 0s; status ok
- command: `python -m labkit.run examples/lenia_orbium/world.py --out examples/packs/lenia_orbium_damage --frames 150 --damage 40:0.4:core`
- segmentation: matter > 0.35 of robust range [0.0, 0.9749], min area 6 px

## Measurements
- components: final 4, mean 2.4, max 5; occupancy final 0.01
- tracks: 28; persistent (alive >= 50% of run): 2; longest 99 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.18 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 4, 2], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 6.06/time; max body lengths 14.6
- replication (lineage window K = 20 frames = time 4, default): splits 8, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio 0.375, nucleations 6
- channel total drift (end/start - 1): [-0.3693]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 95: holes 0, rim-vs-core 0.24, rim-vs-outside 0.44, heterogeneity 0.18; core [0.974] rim [0.73]
  - track 16 at frame 95: holes 0, rim-vs-core 0.24, rim-vs-outside 0.44, heterogeneity 0.18; core [0.974] rim [0.73]
  - track 0 at frame 20: holes 0, rim-vs-core 0.22, rim-vs-outside 0.42, heterogeneity 0.18; core [0.952] rim [0.729]
  - track 1 at frame 11: holes 0, rim-vs-core 0.24, rim-vs-outside 0.47, heterogeneity 0.18; core [0.972] rim [0.729]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 13 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial A: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.938, rim/outside 5.77 (aggregate of 13 individuals; 0/13 membrane-like individually; rim level 0.93)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=19, R_eq 4.44): none; #16 (t=19, R_eq 4.44): none; #0 (t=4, R_eq 4.48): none; #1 (t=2.2, R_eq 4.48): none
- damage `core` (requested 0.40 of the area) at frame 40 (t=8): target = main-run track #0; the individual is one component of 61 px = 1.00x the median individual, aspect 1.58 (rule mature-compact: track age 41 frames vs K=20; 3 individuals from 3 components at that frame; open-ring individuals, not eligible: 0); mask 25 px (25 inside the individual)
- damage MEASURED: the target lost 51.5% of its matter (inside the individual: its components and what they enclose; 25 of 61 px lost > half their matter); net matter lost outside it = 0% of its matter; share of all matter that disappeared that was under labkit's mask 1
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[8.0, 12.4, 16.8, 21.2, 25.6, 30.0]: target [0.262, None, None, None, None, None] (matter [0.422, None, None, None, None, None]; pieces [2, 0, 0, 0, 0, 0]; last seen t=8.2); comparator [1.0, 1.016, 1.049, 1.033, 1.016, 0.918] (matter [1.0, 0.959, 0.969, 0.962, 0.955, 0.836]; pieces [1, 1, 1, 1, 1, 1]). Follow-up: pre-cut field at frame 40, then recorded frames 40..150 segmented with the TARGETING range [0.0, 1.0] (threshold 0.35), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- damage target is elongated (aspect 1.58 > 1.5; rule mature-compact): it may be elongating or pinching (dividing) rather than a compact individual; check damage.png or damage at another frame

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
