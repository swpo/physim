# H9 PROTOTYPE — regional composition segregation (metric-gap follow-up to post 12)
Motivation: top-C9 worlds are homogeneous tilings (user visual audit of
p1g1_009_s3); C9's factor bank has NO spatial cross-term (t9 traversal, e9
episodes, r9 GLOBAL species clustering, s9 local surface flux — none measure
region A != region B). h9 fills that hole.

## Estimator
Species = d7b's track clustering verbatim (same features, floors, k-scan,
silhouette gate). Frames = per-track late-window positions on a P x P patch
grid. h9 = UC x PERS where
  UC   = permutation-null-corrected uncertainty coefficient
         (I(patch;species) - I_null) / (H(species) - I_null), track-level
         label shuffles (B=60);
  PERS = 1 - occupancy-weighted JS divergence of per-patch species mixes
         between the two halves of the late window (transience discount).
Gates: >=2 species above silhouette floor, >=50 frames, stable patches.
Diagnostics per rec: seg_control (perfect positional relabel = motility-
limited ceiling), shuffle_control (~0), mixing curve (monotone).

## Validation battery (P=4; harvest recs, bk3 venv; h9_dev.py)
rec               h9     uc     pers   k_sp  seg_ctl  shuffle
p1g1_009_s3 (neg) 0.137  0.155  0.880  12    0.439    0.005
p2g6_032_s2 (neg) 0.062  0.083  0.756  16    0.355    0.004
p1g2_051_s3 (sic) 0.043  0.044  0.977   4    0.224    0.020
p1g4_050_s3 (sic) 0.048  0.048  0.994   4    0.224    0.001
p2g7_049_s3 (sic) 0.029  0.030  0.966   4    0.181    0.000
P-sensitivity: p1g1_009_s3 @P=6 -> h9 0.184 (mild, stable).
Estimator verdict: nulls clean, mixing curve monotone (0.27/0.08/0.02),
controls behave. MEASURE VALIDATED (synthetic); phenotype thresholds TBD
against positive-control worlds (none exist yet in-framework).

## Scientific findings
1. NOTHING evolved so far segregates: h9 <= 0.14 across the board — confirms
   the metric gap diagnosis (C9 0.85 with h9 0.14 on the same world).
2. sic children score LOWEST (0.03-0.05) with the lowest motility ceilings
   (seg_ctl 0.18-0.22): the implanted two-parent regions are fully
   homogenized by the late window under the single child chemistry.
   Operator-expressivity hypothesis strengthened: persistent regions need
   GENOME-level merges (union of channels + gated cross-coupling, cf. M3
   vvw iso-background pattern), not state-level implants alone.
3. Motility itself opposes regional structure (seg_control ceilings 0.18-
   0.49): confinement/membranes are prerequisites for high h9 — consistent
   with the intended "economy" phenotype (compartments + exchange).

## Next
- Post-hoc h9 rescore of the FULL 12-gen harvest when the continuation lands
  (all ok rows with npz) -> does ANY lineage show h9 > 0.2?
- v4 decision package: h9 into C9' (geomean) or as a hard gate for the
  economy spatial_class; genome-level merge operator; positive-control
  world construction (hand-built two-chemistry blobkit genome via the
  iso-background trick) to set thresholds.
Tool: probes/blobs/l0/complexity/h9_dev.py (bk3 venv; JSON per rec).
