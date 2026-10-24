# REPORT r3: chemotaxis-motility (final sprint)

## Headline
**The evasion allele in evopursuit does not win by escaping predators. It wins by exploiting the chase.** In 18 fixed-allele runs
(no mutation), prey chased by *non-consuming, immortal escorts* grow most of all: B 2.4-2.5x, A 1.2-1.6x. Prey with no partner
decline (A 0.41-0.76x, B 0.36-0.54x). Consuming predators subtract from the chase benefit: A collapses (0.11-0.15x), and B still grows (1.3x).
The ordering B+escort > B+predator > B alone is the committee's "exploitation" case. Being chased raises prey speed (B +50% with
escorts), and the B allele, which flees harder, extracts more of that benefit. The ledger shows that, in the evolving runs, B bodies born by clean fission (46 over 3 seeds) outnumber mutation conversions A→B (28) by only 1.6x.
So the committee's pass criterion (births *far* exceed conversions) is **not met**, although strict-rule generation depth reaches 2-4.

## Claims
| world | rung (proposed) | strongest evidence | known weaknesses |
|---|---|---|---|
| `evopursuit` | **L5[L2]** (chase benefit and consumption, decomposed), L4b; L6 Weak; **L7 Weak** | `packs/arms_summary.md` + `packs/arms_*_s{0,1,2}` (18 packs, m = 0). Prey mass t=1500/t=150: A+pred 0.15/0.12/0.11; B+pred 1.28/1.32/1.28; A+escort 1.62/1.41/1.22; B+escort 2.43/2.54/2.43; A alone 0.41/0.56/0.76; B alone 0.36/0.46/0.54. Prey speed (`preyspeed.py`): alone 0.27, A+escort 0.32, B+escort 0.41, with predators 0.53-0.57 px/t. | The mechanism "chase-driven propulsion feeds growth" is correlational: speed and benefit co-vary, but the causal step (less self-toxin, more fresh food) was not isolated. Turning prey toxicity off gives a domain-filling sea (`arms_tox0_*`), not a test. |
| `evopursuit` ledger | — | `preytrack.py` (prey-only, every 2 t, largest-parent rule), `packs/preytrack_evopursuit_s{0,1,2}.json`: clean fissions 6 / 7 / 12; B births by clean fission 10 / 14 / 22 vs A→B conversions 10 / 8 / 10 (B→A 7 / 7 / 9); off-kind daughters 1 / 0 / 0; strict max generation 3 / 2 / 4. Random deepest-generation B-birth strips (`*_Bbirths.png`) show orange crescents pinching into two. | Births exceed conversions only 1.6x (46 vs 28), so heredity through fission is real but is not the dominant source of the B sweep. Many bodies are born by unclean splits (collision debris) and die (B deaths 46-55 per run). The radius-4 patch swap converts whole small bodies, as the committee noted. |

## What changed in my understanding (mechanisms, with the controlling arm)
1. **Chase benefit** (escort arms vs alone): ×2.6 for A, ×5.4 for B. Non-consuming pursuers are mutualists. B's harder flight
   (chi_x × 2) is worth more with a pursuer, and costs ~10-20% without one (B alone < A alone in 3/3 seeds).
2. **Consumption** (predator vs escort): ×0.09 for A (fatal) and ×0.53 for B. The B allele lowers per-body exposure (B/A 0.64-0.72 in
   the evolving runs) and keeps the population above the collapse threshold.
3. The sprint-2 "rescue" stands as a description (A + predators collapses; B + predators persists, and the mutant arises and spreads). Its
   cause is better stated as **B turns the chase into a net benefit**, since B + predators ends with 3x more prey than B alone.
4. Prediction this makes (not run): lowering the consumption rate k toward 0 should raise prey mass continuously up to the escort level,
   and an allele that *weakens* flight should be selected only where predators are absent.

## Negative results
- Prey-toxicity-off probe (pdeath 0): prey fill the box (prey mass 20x, one body), so it cannot separate the toxin route from the food route.
- Births vs conversions: the committee's pass criterion fails (see the ledger).
- Not done this sprint: identical-event neutral twins (the mutation sites depend on the state, so I could not share a schedule in time), evopursuit
  at 1.5-2x resolution and ±10% k/cost, swimfission dt/2 and a resolution change, the clipping-loss log, the n=0 fork packs, and the Laplacian-only
  slow-inhibitor control. Literature entries for §2.6 are in `LITERATURE_2.6_additions.md` (thread directory; not merged into LITERATURE.md).

## Deliverables
`FINAL.md` (2-page summary for the lab), `movies/showcase.mp4` (evopursuit seed 0, 192², from noise to the B sweep).
