> Historical method, completed 11 October 2026. This unchanged excerpt documents a morphology detector, not the organism rubric. Its frame score is not evidence of same-individual survival, physical confinement or organism status. The evaluator uses its separate diagnostics provisionally.

# Offline enclosure scoring: first research loop

This probe detects visible, localized enclosures in stored activator fields and
scores their quality together with the sparsity of the surrounding field. It
returns interior masks, including contained objects, so the proposed inside and
outside can be inspected directly. It does not run simulations or change the
evolutionary objective.

The first loop was completed on 2026-10-11: one baseline, two revisions after
visual inspection, and a final sensitivity check. This is a morphology score,
not evidence that a boundary physically confines material or behaves as a cell.

## Data and results

The input is the existing Sebastian-worlds collection under
`outputs/sebastian-worlds-20261011`:

- 50 supplied archive states at t=250, from `supplied/final_updated/worlds`.
- 154 frames from four previously recorded CPU movies, sampled every 25 time
  units: p2g4_068, p11g4_043, and p14g5_029 through t=1000; p7g2_009 through t=750.
- 204 frames in total, covering 51 distinct candidate names. Movie frames are
  correlated samples. These are not 204 independent worlds or replicate seeds.
- The compact comparison set contains 54 frames: all 50 archive states plus
  the last frame of each movie. Original GPU archive states and fresh CPU movie
  states are different realizations; they are identified separately.

The supplied archive fields at t=250 are not the original runs' late-time full
fields. Positions from later tracking records are not used to reconstruct fields.
Only activators enter this first detector; inhibitor and memory channels do not.

| Example | Source / time | Enclosures | Score / 100 | Exterior occupied |
| --- | --- | ---: | ---: | ---: |
| p2g4_068 | CPU movie / 1000 | 1 | 50.0 | 28.3% |
| p2g4_068 | Supplied archive / 250 | 2 | 48.6 | 27.3% |
| p2g5_024 | Supplied archive / 250 | 1 | 46.6 | 28.5% |
| p8g11_012 | Supplied archive / 250 | 4 | 14.9 | 48.8% |
| p7g2_009 | CPU movie / 750 | 8 | 7.6 | 62.3% |

These are the five positive frames in the compact comparison set; the other 49
score zero. Three of the 50 archive states qualify. Across all movie samples,
p2g4_068 has enclosures in 39/41 frames, p7g2_009 in 30/31, and the other two in
0/41 each. Presence across frames does not establish individual object survival.

## What changed after looking at the results

**v0:** threshold the union of activators at 0.45, find enclosed empty regions,
and multiply their count by the globally unoccupied fraction. This over-rewarded
crowded fields: p7g2_009 at t=750 had 22 pockets, and a synthetic grid had 64.
It also cut internal objects out of the proposed interior and split nested
structures into multiple pockets.

**v1:** inspect each activator and their union across five thresholds; restore
contained objects to the interior; merge nested detections; reward the best
enclosure instead of multiplying by count; measure wall locality and exterior
sparsity. This reduced p7g2_009 to 15 detections, but seven were still incidental
spaces between neighboring structures, connected to a much larger wall network.

**v2:** require at least half the enclosing wall component to be near its own
interior. This removed those incidental spaces, leaving eight plausible local
enclosures in p7g2_009. p8g11_012 fell from seven detections to four. The synthetic
grid now has zero qualifying enclosures. The p2 ring examples were retained.

The reviewed p7 enclosures have orange boundaries with blue/orange contents and
are visibly distinguishable from adjacent open spirals. The p8 shapes are more
irregular and attached to other wall material; treat them as weaker examples.
The p2g5 ring correctly includes its central blue spot. This is a development
audit by the same assistant that built the score, not independent ground truth
or a held-out accuracy measurement.

## Definition of the current score

Normalize each activator using fixed genome parameters, not image contrast:

```text
A_i = (u_i - u0_i) / (sqrt(lam_i) - u0_i)
```

For each A_i and their pixelwise maximum, threshold at
`[0.25, 0.35, 0.45, 0.55, 0.65]`. A candidate is a bounded region of the
4-connected complement of an 8-connected wall. Detection uses a 3×3 periodic
cover, rejects regions that reach its outer edge, and retains one central copy.
This handles local enclosures crossing the periodic seam and rejects bands
that wind around the torus.

Candidate interiors must have area ≥25 and inscribed radius ≥2 in simulation
units, and span at most 60% of the domain in either axis. Occupied islands
inside a closed region are included in the interior. No closing, convex hull,
or dilation is used to create an enclosure from an open arc.

Match interiors across thresholds using intersection-over-union >0.5, and
require support at three of the five levels. This is a discrete robustness
check, not a full persistent-homology calculation and not temporal persistence.
Use the observation nearest 0.45 as the representative geometry. For enclosure j:

```text
R_j = number of supporting thresholds / 5
W_j = fraction of its actual enclosing wall component within 5 units of its interior
C_j = unoccupied fraction in the exterior annulus 5–12 units from its interior
q_j = R_j × min(inscribed_radius_j / 4, 1) × sqrt(W_j × C_j)
```

Require `W_j ≥ 0.5`. Keep the outer detection when it contains at least 85% of
a smaller candidate. This merges nested pockets and duplicate channel
detections. The best-supported channel is used for exactly identical masks.
No circularity preference is imposed.

The exterior excludes the union of all accepted interiors and their 5-unit
rims. Let E be the occupied fraction of that exterior and F its fraction of
the entire domain. Occupied means `max_i A_i ≥ 0.45` throughout these measures.

```text
score = 100 × max_j(q_j) × (1 - E)^2 × sqrt(F)
```

With no enclosures the score is zero; with no exterior it is also zero.
The count is reported separately. Using the maximum quality avoids directly
rewarding a larger number of holes; sqrt(F) discourages claiming the entire
domain as interior. Individual quality, inside occupancy, exterior occupancy,
and exterior area are retained alongside the scalar score. The score is not a
calibrated probability. v0 and v2 use different scales.

## Checks and remaining uncertainty

Nine geometry/invariance tests pass, covering contained objects, mixed-channel
walls, open arcs and narrow gaps, spots/disks/noise/grids/winding bands, periodic
translation, channel permutation, clutter, nested rims, and coarse/noncircular
examples. Closed-ring controls score 94.7; adding exterior clutter lowers this
to 44.1. An empty ring intentionally receives the same score as one with cargo:
this first loop asks for enclosure existence, not internal diversity or autonomy.

Eight selected stored examples were also evaluated with the threshold sweep
shifted ±0.05, the wall-locality cutoff changed to 0.4 or 0.6, and the fields
decimated from spacing 0.5 to 1.0. The ranking and positive/zero decisions were
unchanged. Counts were unchanged except for p8g11_012: cutoff 0.4 admits a fifth,
borderline wall-connected pocket. The largest score change was 1.44 points.
Decimation is an image-resolution check, not a simulation convergence study.
Two stored positive examples preserve their masks and scores exactly under
periodic translation and reversal of channel order. Finite inputs, mask sizes,
physical domain dimensions, and mask areas were checked for all 204 frames.

p7g2_009 scores 78.6 at t=25, when early rings have sparse surroundings, then
settles around 6–8 as the exterior becomes crowded. Its median from t=100
onward is 7.6; p2g4_068's corresponding median is 49.6. Thus a peak-over-time
objective would reward startup appearances. A later search objective should
use a declared evaluation window and require sustained enclosure presence.
No temporal term has been added to this frame score.

Size cutoffs, finite grid connectivity, activator normalization, and the
locality cutoff are modeling choices. Tiny, weak, filled-in same-channel,
very large, or strongly attached compartments can be missed. A connected wall
network can contain meaningful regions that this isolated-object preference
rejects. The current validation set is small and was used to tune the method.
The score has not been tested under optimization pressure. Physical retention,
individual tracking, reproduction, heredity, and species identification remain
outside this loop.


---

This is a verbatim excerpt of the original method through its uncertainty section.
Original document SHA-256: `7a074681203ecd234ef33630e431d0736f958232f7260d21eaaaf2a91318a128`.
