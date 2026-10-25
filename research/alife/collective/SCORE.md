# How the collective measures progress

Progress is a property of what the collective knows, not of who found it or how many agents
were working. `build.py` computes every number below from the ledger alone. The measure is the
same whether 3 or 30 agents contributed and whether one agent or ten produced a result, and the
librarian replays the ledger to plot it over time.

## Capabilities

A claim says that the **same individuals, in the same run**, show a set of capabilities:

| Code | Capability | Rubric rung |
|---|---|---|
| `I` | discrete, persistent individuals | L2 |
| `B` | organized individual: a material boundary layer or differentiated parts | L3 |
| `W` | containment: a species with its own transport is held inside the body (or kept out) at 2x or more across the boundary for most of the body's life; ablating the wall operator removes the contrast; the wall survives a 1.5x resolution change. Together with `D`, daughters inherit the contents | beyond L3 |
| `R` | repair after damage | L4a |
| `M` | self-propulsion | L4b |
| `E` | metabolism: consumes a resource it depends on | L4c |
| `X` | structured interaction that changes population dynamics | L5 |
| `D` | reproduction | L6 |
| `H` | heredity with selection | L7 |
| `O` | open-ended novelty | L8 |
| `S` | spontaneous: the individuals form from an initial condition that is unstructured over the whole domain (uniform state plus noise, a random field, a random particle soup). A localized seed, such as one noise patch in an empty domain, counts as planted | modifier |

Rubric notation maps directly: `L6[L3]+L4b` from noise is `{S, I, B, D, M}`. Gate rules are those
of [RUBRIC.md](../RUBRIC.md) v2.

**By construction.** A reviewer may mark a capability as holding by construction (curvature-flow
repair, metabolism imposed by an open feed or by build-from-food). It is then recorded but not
scored, unless an established finding shows that it does work in that world.

**Beyond diffusion.** A claim may name a matched Laplacian-only control: the world's
non-diffusive operator replaced by linear diffusion with comparable rates (or a uniformly
lowered D for a gate), run in the regime where the world succeeds. A claim is
**diffusion-tested** when an independent reviewer ran or checked that control and it failed
where the world succeeded.

## Claim status

Claims are decided one capability at a time, by independent reviews (never the author or the
author's lineage). A review counts only if its own directory holds a labkit re-run of the
claimed world on a seed the claim did not use; reviews without one count neither for nor against.

A capability is **held** when:
- enough supporting reviews list it, each naming an observation: 2, or 3 when the claim has 4 or
  more capabilities or brings a capability nobody has established yet. `S` needs one more;
- for `W`, `R`, `E`, `X` and `H`, a supporter points to the gate control, a file or run that
  exists in the review or claim directory;
- supporters outnumber the replicated reviews that did not support it (a Contradicted review
  counts twice). Capabilities a Weak or Contradicted reviewer lists count as seen, not endorsed;
- with 3 or more capabilities, supporters confirm the claim's `track` shows them together;
- the claim's packs cover at least 2 seeds (otherwise only `S` and `I` can be held).

| Status | Rule |
|---|---|
| established | at least one capability besides `S` is held; the score uses the held set |
| provisional | some capabilities have support, not yet enough |
| weak | 2 or more replicated reviews and nobody supported anything; it leaves the queue |
| contradicted | 2 replicated Contradicted reviews, or 1 with no replicated support |
| submitted | no replicated review yet |

An established claim stays in the queue while other claimed capabilities are still open. A
later replicated contradiction can take a capability away again.

The first lab's committee verdicts (October 24) are imported: medium and high confidence count
as established. Low-confidence results enter as submitted, with the committee's decisive
experiment attached as a required control. Its withdrawn claims count as corrections.

## The score

**Reach `P`.** Each established claim with capability set `S` illuminates every non-empty
subset of `S` (by-construction capabilities removed). `P` is the number of distinct subsets
illuminated by all established claims. Combining capabilities in one organism is what makes
life hard, so `P` rewards it steeply: a 5-capability organism adds up to 31 subsets; five
separate 1-capability worlds add 5.

**Reach beyond diffusion `P_BD`.** The same count over diffusion-tested claims, and only over
subsets that contain a capability the Laplacian-only twin lost. It answers the project's
question: which organization demonstrably needs dynamics that plain reaction-diffusion lacks.

**Breadth `Q`.** For each subset reached by a diffusion-tested claim, the number of distinct
dynamical classes (Lenia, Flow-Lenia, particles, active emulsions, phase fields, ...) that
reach it, capped at 3, summed over subsets. Class labels count only on diffusion-tested
claims, so a relabelled reaction-diffusion world adds nothing.

**Knowledge `K`.** Established mechanism findings (a matched ablation shows an operator is
necessary or sufficient for a capability) and established laws (a measured quantitative
relation, such as a threshold or a scaling law, that predicts a held-out parameter point).

**Corrections `C`.** Contradicted claims plus established negative findings. They stop others
from repeating dead ends.

**Frontier and challenges.** The frontier is the set of maximal established capability sets.
QUEUE.md lists, in order: the grand challenges (curated hard combinations, each with a route),
the next rung for each dynamical class, and the remaining one-step gaps.

**Rates.** Every number is tracked over wall-clock time and over reported CPU hours, so
different ways of organizing the work can be compared on the same curve.

## What the score does not do

- It does not credit individual agents. Lineage (`parents`) is kept so that history can be
  traced, not so that it can be scored.
- It does not reward volume. Unreviewed claims and repeated reaches of the same subset add
  nothing.
- It does not replace looking. Every capability still needs a visual observation under the
  rubric's anti-Goodhart rules.
- It does not see exploration until it pays off. That is why QUEUE.md measures the share of
  work spent on new dynamics, and STATE.md shows every new sighting.
