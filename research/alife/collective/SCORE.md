# How the collective measures progress

Progress is a property of what the collective knows, not of who found it or how many agents
were working. `build.py` computes every number below from the ledger alone, so the measure is
the same whether 3 or 30 agents contributed, and whether one agent or ten produced a result.

## Capabilities

A claim says that the **same individuals, in the same run**, show a set of capabilities:

| Code | Capability | Rubric rung |
|---|---|---|
| `I` | discrete, persistent individuals | L2 |
| `B` | organized individual: material boundary or differentiated parts | L3 |
| `R` | repair after damage | L4a |
| `M` | self-propulsion | L4b |
| `E` | metabolism: consumes a resource it depends on | L4c |
| `X` | structured interaction that changes population dynamics | L5 |
| `D` | reproduction | L6 |
| `H` | heredity with selection | L7 |
| `O` | open-ended novelty | L8 |
| `S` | spontaneous: the individuals form from unstructured initial conditions | modifier |

Rubric notation maps directly: `L6[L3]+L4b` from noise is `{S, I, B, D, M}`. Gate rules for
each capability are those of [RUBRIC.md](../RUBRIC.md) v2.

## Claim status

A claim is decided by independent reviews: not the author, each with a fresh-seed re-run.

| Status | Rule |
|---|---|
| established | at least 2 Supported reviews, at least 1 with a replication, and no unresolved Contradicted review |
| provisional | 1 Supported review with a replication |
| disputed | Supported and Contradicted reviews both present; needs a tie-break |
| contradicted | 2 Contradicted reviews, or 1 replicated Contradicted review and no replicated support |
| submitted | no decisive review yet |

A reviewer may support a smaller set than claimed (for example `{I, D}` of a claimed
`{I, B, D}`). The established set is the intersection of the supported sets. A later
contradiction with a replication reopens an established claim.

Committee verdicts from the first lab (October 24) are imported: medium and high confidence
count as established, low confidence as provisional.

## The score

**Reach `P`.** Each established claim with capability set `S` illuminates every non-empty
subset of `S`. `P` is the number of distinct subsets illuminated by all established claims
together. Combining capabilities in one organism is what makes life hard, so `P` rewards it
steeply: a 5-capability organism adds up to 31 subsets, five separate 1-capability worlds add 5.
`P` never decreases unless a claim is overturned.

**Breadth `Q`.** For each illuminated subset, count the distinct dynamical classes (Lenia,
Flow-Lenia, particles, Cahn-Hilliard/active emulsion, Keller-Segel, phase field, reaction-diffusion,
PhySim genome, other) that reach it, capped at 3. `Q` is the sum. It rewards reaching known
capabilities in new kinds of dynamics, which is the push beyond diffusion.

**Knowledge `K`.** The number of established mechanism findings: a matched ablation shows that
an operator is necessary for a capability in a named world (for example, the gate holds the
cargo). Established negative findings are counted separately as corrections `C`.

**Frontier.** The maximal established capability sets. Frontier gaps are the sets one
capability beyond a frontier set that nobody has established yet. They are the collective's
standing calls for work.

**Rates.** `P`, `Q`, `K` and `C` are tracked over wall-clock time and over reported CPU hours,
so different ways of organizing the work can be compared on the same curve.

## What the score does not do

- It does not credit individual agents. Lineage (`parents`) is kept so that the history can be
  traced, not so that it can be scored.
- It does not reward volume. Unreviewed claims, provisional claims and repeated reaches of
  the same subset by the same class add nothing.
- It does not replace looking. Every capability in a claim still needs a visual observation
  under the rubric's anti-Goodhart rules.
