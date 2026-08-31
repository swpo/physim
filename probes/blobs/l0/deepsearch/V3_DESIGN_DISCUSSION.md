
=============================================================================
DISCUSSION DOC: v3 worlds (density + boundaries + radical diversity) & agent env
=============================================================================

PART 1 — THE HOMOGENEITY DIAGNOSIS (why champions look uniform)
Three structural causes in the current search:
 a) UNIFORM COEFFICIENTS: one genome = one chemistry everywhere. Any spatial
    structure must be self-organized against a homogeneous background; the
    PDE dynamics tend toward statistically uniform textures (labyrinths,
    swarms) at the box scale.
 b) SPECIES = FIELDS (cap 4): diversity is architecturally bounded. d7 counts
    field-populations; two blobs of the same field with different sizes/
    behaviors count as one species. No metric REWARDS emergent within-field
    differentiation, so evolution doesn't buy it.
 c) NO PRESSURE FOR EMPTINESS: interest components reward activity density
    (motion, churn, growth). A world that is 80% empty with sparse organisms
    navigating structure scores WORSE on coverage-correlated components than
    a space-filling texture. Emptiness is unpriced.

PART 2 — THE THREE-INGREDIENT RECIPE (user) mapped to certified tech
 R1 DENSITY/DYNAMICS: have it (v2 champions).
 R2 BOUNDING SURFACES: certified pieces exist —
    - membranes/rings (bounded-structures post): closed blob rings, porous
      walls, speed-selective cross-w barriers; topologically protected.
    - b-field landscapes (M6): self-written walls/trails (autophoresis,
      stigmergy) — DYNAMIC boundaries the world draws itself.
    - patch-gluing (PoU, certified): STATIC coefficient regions with seam
      physics (body-force law v ~ -0.4*grad(rho_B)).
    Search-integration options (ranked by leverage/cost):
      B1 add a 4th slow 'wall field' template to the genome grammar (a
         w-like channel with strong self-activation + high threshold =
         bistable curtain material) + operators that mint wall couplings.
         Evolution decides where walls go. [pure grammar extension]
      B2 patch-layout gene: genome carries 2-4 coefficient patches (PoU
         positions/radii evolve; chemistry per patch inherits/mutates).
         [uses certified gluing; makes heterogeneity a first-class gene]
      B3 seed structured ICs (rings/membranes from the atlas as dressing
         options) — cheap, but structure must survive, not just persist.
 R3 RADICAL DIVERSITY (100s of species, EMERGENT not fields):
    - key insight: species should be PHENOTYPE CLUSTERS, not fields. New
      metric d7b: cluster per-blob feature vectors (size, speed, period,
      bond degree, field composition) across the run; n_eff = exp(entropy)
      of cluster occupancy = effective species count. Reward log(n_eff).
    - enablers in the dynamics: (i) wall/patch heterogeneity creates NICHES
      (same chemistry behaves differently in different environments =
      ecological speciation); (ii) size-dependent behavior (already seen:
      area 40 vs 200 blobs move differently); (iii) bilinear predation
      networks (mint_bilin) create trophic differentiation.
    - CAUTION: metrics must resist gaming (noise != diversity): clusters
      must be TEMPORALLY STABLE (a species persists >= K tu) and
      REPRODUCIBLE across seeds.

PART 3 — WHAT RUNS NEXT (proposal)
 Track A (agent env, on current champions — START NOW):
   worldify 3 champions (91.16 rotor, p3g9_022 swarm, p4g2_044 minimal) as
   port-worlds: same anonymous port interface as D/C/B tracks (obs windows,
   probe/poke actions, measurement instruments from the assay's record
   streams). Agents get: local field windows, blob censuses, pokes.
   Test: measurement adequacy + prediction contracts (CRPS on blob-count/
   composition trajectories) — does the god-probe/compact-oracle gap
   reproduce in evolved worlds? (rich-vs-big test on EVOLVED physics).
 Track B (v3 evolution prep — spec + build, spin AFTER agreement):
   B1 wall-field grammar + d7b emergent-species metric + emptiness-aware
   interest reweight (C9 'spatial structure': reward bimodal density
   histograms + boundary length), THEN 12-gen pilot on 2 pods (~$100)
   before any big campaign. Patch-layout gene (B2) held for v4 unless the
   pilot shows walls alone don't produce sparsity.
=============================================================================
