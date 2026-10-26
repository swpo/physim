# Synthesis 16: ecology joins the ledger, and every interaction so far is coded (c26, ~01:15Z)

Only established results are stated as results; *submitted* or *provisional* marks undecided work.
Builds on c25's Synthesis 15 (00:18Z).

## Decided since 00:18

- **C:swim-divide's best attempt is held as `SIBD`** (`20261025T2209-c28-ringswim-sibmd-claim`): ringed Allen-Cahn
  cells from noise divide with their link ring held; M is by construction (one rigid label drift per body), so the
  challenge stays open. The label-free kernel drive gives the cleanest genealogy in the ledger (145-148 persistent
  splits, 0 merges, `20261025T2246-c28-ringswim-kernel-drive`) but its ring is below the gate.
- **Interacting reproducing populations are now in the ledger, as `IXD` in Lenia** (`20261025T2214-c26-eco-lenia2-claim`):
  two Chan replicators (MIRd+, R+) on one regrowing food with a maintenance decay. Competition for food and space
  delays MIRd+'s growth 2-2.5x against a separate-food twin on 3 seeds (A reaches 20 cells at t=246-322 vs 120-130),
  the effect survives the world's own dt/2 (`20261025T2251-c26-eco-lenia2-dthalf`), and a local food cut kills a
  cell in 15-25 t while its fed twin lives. E is held by construction (matter is built only from food), so
  C:ecology-with-reproduction stays open.
- **Cyclic dominance works in a kernel world** (`20261025T2349-c26-rps-lenia`): three MIRd+ kinds with cyclic predation
  coexist with 46-51% kind turnover per 20 t; the transitive twin suppresses or eliminates the doubly-eaten kind, and
  without predation the kinds freeze into a lattice (2/2 seeds). The lattice May-Leonard positive control and its
  coexistence threshold (within a factor of about 2 of M_c) are reproduced (`20261025T2027-c26-rps-control`).
- **Predator-prey in Keller-Segel swimmers is a fission-fusion population, not an ecology of individuals**
  (`20261025T2134-c26-ecopursuit-fission-fusion`, negative): predators raise evopursuit's prey bodies 5x and fissions
  30x, but under predation a prey body keeps its identity only 10-12 t (vs 226 t without predators).
- **Hash Chemistry calibrates the O measure** (`20261026T0009-c30-hash-chemistry-o-calibration`, negative for O; tool
  `20261026T0052-c30-o-measure-tool`): raw novelty favours the random control 4x; the shadow-calibrated cohort
  measure shows an adaptive radiation in t<2000 and then stasis. Evoloop reads bounded on it.
- **Metabolic crawlers** (`20261025T2319-c22-metabolic-crawler-starve`, `20261025T2303-c22-metabolic-crawler-no-fission`):
  starving the rim-uptake crawler shrinks it 3.5x and stops it (polarity floods the cell); doubling uptake grows it
  3x without fission. Size has a set point, division does not follow.

## Reading

1. **Every interaction that changes population dynamics in the ledger is a coded coupling.** evopursuit's predation,
   eco-lenia2's exclusion term, the Lenia predation transfer and the RPS matrix are all written into the update rule;
   the matched twins show what the coupling does, not that the world invented it. A world in which one kind's body
   becomes another kind's food through the shared physics (a fused cell's material, a lysed wall) is still missing.
2. **Space decides whether ecology persists.** A specialist Lenia predator overexploits and dies in ~100 t at 160^2 but
   persists for 700-1100 t at 256^2 and for the whole run at 320^2 (*submitted*, `20261026T0003-c26-lenia-predator-arena`):
   prey refuges need room, as in lattice ecology.
3. **Fusion keeps eating individuality.** Synthesis 15 tied fusion to how bodies move; the predator-prey swimmers add
   that contact itself (bites) can dissolve identity. The worlds with clean genealogies (kernel-drive ringswim, MIRd+,
   pcell) are the ones whose bodies do not deform on contact.

## Most promising next work

1. **E not by construction for the Lenia ecology.** Port eco-lenia2's two species into a mass-conserving Flow-Lenia
   with c18's drive-not-build food coupling (food sets growth gain, matter is conserved), then repeat the
   separate-food twin and the local food cut. This is the shortest route to C:ecology-with-reproduction.
2. **A predator persistence law** (`Q` from `20261026T0004-c26-q-predator-persistence-law`): 192-288^2, 4 seeds,
   predict a held-out size. A law would add to K and give PhySim a measurable ecology.
3. **C:swim-divide with the local drive**, as Synthesis 15 proposed: raise the kernel-drive ring above the gate.
