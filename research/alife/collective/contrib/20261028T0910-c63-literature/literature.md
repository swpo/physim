# Literature check (c63, ~09:10Z): why the vortices' trait cloud stays bounded, and heredity for Flow-Lenia predators

Scope: the results the ledger produced since c61's check (02:12Z), and published operators the ledger has not tried for
C:open-ended and C:ecology-with-reproduction. I opened every source cited below unless it is marked UNVERIFIED.

## 1. Heyde and Mahadevan 2026: what their landscape remembers

Heyde and Mahadevan 2026 (arXiv:2606.15530) define the model in its HTML version:
- n is the population density over traits, u the landscape.
- Population: dn/dt = n (u - phi).
- Landscape: du/dt = -eps u (n - phi).
- phi = <n, u> is the mean fitness.

Each trait point is depleted by its own density, with zero kernel width, and is restored relative to the mean fitness
phi. There is no independent decay back to a fixed baseline: a trait point regrows only while the population at it
is below average. They report the following regimes:
- self-propelled travel at speed ~eps^1/2 up to eps* ~ 0.4;
- repeated branching;
- oscillations back and forth in a finite 1D domain;
- slow-fast loops and chaotic reversals in 2D.

**Relation to the ledger.**
- c58's waste memory differs from theirs in two ways:
  - It has a fixed lifetime (dw: 500 t standard, 2000 t long): it forgets on a clock, not relative to phi.
  - It acts through a Gaussian of width sw.
- c63's distribution-memory waste (`20261028T0700`, replicated in `20261028T0833`) stores the full distribution, but
  with the same fixed lifetime. It gives a stable polymorphism of 3-4 clusters in a bounded region (R ~0.55, new
  ground <= 0.02 after t~5000).
- Our trait space is unbounded (R^3), so the bound is not their finite-domain oscillation. The likely cause is the
  clock-driven forgetting: ground left 500-2000 t earlier is fresh again, so the population can cycle among old
  regions instead of leaving them.
- The prediction to test is a waste whose memory is depleted and restored relative to the mean (no fixed decay).
  That is H&M's rule, and the ledger has not tried it.
- Relation: variant (the ledger's vortices are a spatial, individual-based version of a regenerating landscape, with
  a forgetting clock the published model lacks).

## 2. Bounded trait space and Red Queen cycling

Kisdi, Jacobs and Geritz 2001 (Selection 2:161-176, "Red Queen evolution by cycles of evolutionary branching and
extinction"; UNVERIFIED: the PDF at mv.helsinki.fi did not extract, and I have only a search summary). They argue
that because most continuous traits are bounded, Red Queen dynamics usually take the form of evolutionary cycles.
This is the published reading of what c61 found at T=30000: first-time dominant classes keep appearing inside a
bounded region. RUBRIC L8 counts that as a false positive.

## 3. Flow-Lenia with embedded parameters: heredity without averaging

Plantec et al. 2025 (Artificial Life 31(2), arXiv:2506.08569, HTML opened):
- **How parameters travel.** Rule parameters ride on matter by reintegration tracking. When matter from different
  parameter sets lands in one cell, one set is sampled with a softmax over the incoming matter. Averaging was
  rejected because every collision would make a new parameter set.
- **Mutation.** "Beams" perturb a 10x10 patch of the parameter map.
- **What it gives.** Evolutionary activity grows roughly linearly over 500k steps, with slopes that fall as the
  mutation rate rises. The number of distinct parameter sets stabilizes after a fast rise (saturation).
- **Relation to the ledger.** No ledger world uses embedded parameters with sampling at merges. c62's Flow-Lenia
  predators fuse often (merge/split ~0.8, `20261028T0429`). Under averaging, fusion would mix their traits. Under
  sampling, a trait would pass through fusions intact, so a reticulate genealogy would not destroy heredity. This is
  the cheapest route to H in a Flow-Lenia ecology. The caveat: a stochastic rule chosen per cell is a written
  inheritance rule. Reviewers would need to judge whether it is "a label a division rule hands to daughters" (it is
  not keyed to division, but it is imposed).

Michel et al. (arXiv:2505.15998, ALIFE 2025; abstract only) explore Flow-Lenia universes with a curiosity-driven
search on evolutionary activity, compression and multi-scale entropy. The abstract names no predation.

## Prior art for recent ledger results

- `20261028T0700-c63-vortex-distribution-memory`: nearest is Heyde and Mahadevan 2026. Variant: a fixed-lifetime
  memory gives a bounded polymorphism where their phi-relative regeneration gives travel or branching.
- `20261028T0624-c63-vortex-trait-scale-symmetry`: the dm/sw invariance is the standard nondimensionalisation of a
  Gaussian competition kernel in adaptive dynamics. Known (no specific citation opened).
- `20261028T0344-c62-flow-lenia-ecology-s-claim`: no published Flow-Lenia predator-prey ecology found. Its predators
  graze recycled prey matter (`20261028T0536`), which resembles a detritivore loop more than predation.
