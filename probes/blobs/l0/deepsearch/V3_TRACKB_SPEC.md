
=============================================================================
V3 TRACK B SPEC v0.1 — 'spatial economy' (C9) + wall grammar + emergent species
=============================================================================

PRINCIPLE (user, formalized): the search should feel the tension
  density -> organism-level complexity (motion machinery, transport, internal
             dynamics, buildable species)
  sparsity -> interaction economy (no winner-take-all needed; interactions
             relegated to surfaces; organisms compress to their boundary
             behavior — the interaction matrix factorizes)
Design rule: PRICE THE REALIZED CONSEQUENCES, not the appearance. No reward
for 'looking sparse'; reward what sparsity BUYS. Density's payoff is already
priced (C1-C8). C9 prices what emptiness buys. The optimum of the SUM is
dense organisms in sparse space.

C9 SPATIAL ECONOMY = geometric mean of four [0,1] factors (any zero kills it):

 1. TRAVERSAL t9: emptiness that is USED.
    void = complement of blob support (all activator fields, thr_a).
    - void_frac in [0.35, 0.9] (tent; outside -> 0)   [not merely dead: requires
      organisms alive per C1 gate]
    - void percolates (largest void component spans box in either axis)
    - track-through-void: median track displacement of moving organisms
      through void regions >= 3 blob radii per 100tu window
    t9 = tent(void_frac) * 1[percolates] * clip(track_disp / 3r, 0, 1)

 2. SURFACE LOCALITY s9: interaction flux lives at boundaries.
    For every ACTIVE coupling (i,j) in W/K/bilin: flux density f_ij(x) =
    |term_ij(x)| from the record snapshots (computable on CREC snaps).
    shell = pixels within delta=2px of any blob boundary (dilate xor erode).
    s9 = sum_ij int_shell f_ij / sum_ij int_total f_ij
    (bulk-mixed soup -> s9 ~ area ratio ~ small; membrane/contact worlds ->
    s9 -> 1). Report per-pair matrix for analysis (which couplings are
    surface-mediated = the 'simplified interaction matrix' the user wants).

 3. EPISODIC ENCOUNTERS e9: interaction as events, not permanent overlap.
    From the existing bond series (d5): for each bond lifetime L_k (tu),
    episodic if 10tu <= L_k <= 500tu. e9 = fraction of bond-lifetime mass in
    episodic band * (1 - frozen_frac) where frozen_frac = fraction of pairs
    bonded > 80% of window. (Permanent lattice -> e9 ~ 0; gas of never-
    bonding blobs -> no bond mass -> e9 = 0; societies of meetings -> high.)

 4. ROBUST DIVERSITY r9: coexistence without balance-tuning.
    d7b phenotype clusters (per-blob features: area, speed, period, bond
    degree, per-field composition; cluster with HDBSCAN-lite or k-means +
    silhouette over the late window; species = cluster persisting >= 500tu
    and present in >= 2 of 3 seeds).
    n_eff = exp(Shannon entropy of cluster occupancy), r9 = clip(log2(n_eff)
    / log2(24), 0, 1) * (1 - takeover), takeover = max monotone late-window
    share-trend of any cluster (winner-take-all detector).
    NOTE: r9 rewards EMERGENT species: fields stay <= 4; clusters are
    phenotypes. 24 = full credit target (log-scaled: 8 species = 0.65).

INTEREST INTEGRATION: interest_v3 = interest_v2 + W9 * C9, W9 = 0.25 of total
weight (rebalanced so v2 components keep relative proportions). Cell key
gains one axis: spatial class = {mixed | structured | economy} by (s9, t9)
thresholds -> MAP-Elites protects sparse-structured lineages from being
outcompeted in the archive by dense high-C1-C8 worlds (the B3 lesson:
protect the niche, don't fight the gradient).

GRAMMAR EXTENSION (B1) — DEMOTED TO CONTINGENT (2026-08-31 discussion):
The existing grammar already EXPRESSES bounded structure (hand-built membranes
/rings/barriers used the standard 3-component chemistry + existing coupling
types; no special material). The wall template is a search-efficiency bias,
not an expressivity need. v3 CORE = C9 + d7b + spatial-class niche ONLY
(one change at a time — metrics/search co-evolution lesson). Trigger for
adding the wall template in a v3.1 iteration: pilot shows economy-class
cells stay empty (pressure exists, parts unfound) — i.e., archives show
attempts (rising s9/t9 sub-scores) but no C9 >= 0.4 cells by gen 12.
Original template spec kept below for that contingency:
 - new channel template 'wall': non-diffusing-ish (D in [0.05, 0.5]) bistable
   channel (strong self-activation, high threshold, slow tau in [50, 400]);
   couplings to activators via minted W entries only (evolution wires it).
 - operators: mint_wall (add wall channel + 1 coupling), wall_couple (add/
   retune a wall<->activator coupling), keep delete_chan working on walls.
 - IC dressing: walls seeded with 1-3 random smooth curves (arcs/lines with
   random endpoints, drawn at IC; NOT evolved shapes — evolution shapes the
   DYNAMICS that maintain/move/dissolve them). Rationale: bistable curtains
   need supra-threshold seeds (blob-from-noise lesson); curves are the
   minimal structured seed.
 - patch-layout gene (B2) DEFERRED to v4 unless pilot shows walls
   insufficient for sparsity.

METRICS VALIDATION GATE (before ANY evolution): d7b + C9 computed on:
 (a) 7 GT worlds + 3 v2 champions: expect C9 LOW for labyrinths/storms
     (fails traversal or surface-locality), MID for p4g2_044 (sparse rotor).
 (b) hand-built positives: cargo-in-cell membrane world (bounded-structures),
     M5 channel+trains world, M2 dimer gas -> expect HIGH t9/s9/e9.
 (c) anti-gaming probes: dead world (C9=0 via C1 gate), frozen lattice
     (e9=0), noise soup (r9 clusters unstable -> 0).
 All three banks must land in the expected order BEFORE locking metrics_v3.

PILOT (after metrics gate): 2 pods x 12 gens x 96, seeded from union_final v2
top-100 + 20 wall-dressed variants of champions; SUCCESS = >=5 archive cells
in 'economy' spatial class with C9 >= 0.4 AND interest >= 60 by gen 12.
Cost ~$100. Full campaign only after pilot review.

SPATIAL MERGE (2026-08-31 discussion):
 - TRUE patch-gluing merge (per-region COEFFICIENTS, PoU seams) = v4. Hard gate:
   blobkit steppers (CPU+GPU) assume uniform coefficients; the conservative
   div(D grad u) PoU stepper is certified only in probes/blobs/patchworlds.
   Port + parity-regate before any such operator exists. The seam body-force
   law would feed s9 directly — this IS the long-term diversity scaler.
 - v3 bridge (FREE, no numerics change): merge_spatial_ic — offspring inherits
   ONE parent's chemistry; IC composed from BOTH parents' developed snapshots
   stamped into disjoint soft-masked regions (existing dressing machinery).
   Populations meet in space; chemistry stays uniform. Added to the v3
   operator mix at ~8 slots (from mutate's 20 -> 16, merge 24 -> 20).
 - Decision data: spatial-IC offspring dominating economy cells in the pilot
   = the evidence case for funding the v4 PoU-stepper port.

BUILD PLAN (children):
 K1 'v3-metrics': d7b + C9 in metrics_v3.py + merge_spatial_ic in ops (extends locked v2 per relock
    protocol) + validation gate (a/b/c banks) + report. [THE build]
 K2 pilot deploy (controller, after K1 gate + user look at validation
    numbers): UNCHANGED grammar, C9-augmented interest + spatial-class
    archive axis, seeded from v2 union top-100 + hand-built positives
    (membrane/channel worlds as immigrants — the atlas as seed stock).
 K3 (contingent v3.1) wall grammar per above, only on pilot trigger.
=============================================================================
