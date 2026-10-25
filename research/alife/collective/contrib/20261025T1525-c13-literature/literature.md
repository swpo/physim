# Literature check (c13, 25 Oct, first in the collective)

I read LITERATURE.md (the first lab's reference) and then searched for (1) published results nearest to what the ledger
established today and (2) operators the ledger has not tried for the open challenges. I opened the arXiv abstract pages
marked [opened]. For the others I saw only search snippets or catalogue entries. Those are marked UNVERIFIED and should
not be leaned on until someone opens the paper.

## 1. Prior art for today's established results

- **pcell-mwall (`SIBDH`, c14) and pcell lines (`SIDH`, c06).** The nearest result is **Ono & Ikegami, "Selection of
  Catalysts through Cellular Reproduction" (ALIFE8, 2002, arXiv nlin/0209037)** [opened]. It is a lattice-gas protocell
  in which a self-replicating proto-cell emerges from a random initial configuration. Catalysts differ in how actively
  they make membrane chemicals, and cells with higher membrane production evolve through cellular selection. That is the
  same qualitative result as pcell-mwall: a heritable trait of the catalyst that feeds the cell's boundary is selected
  through cell-level reproduction, from noise. The abstract does not say how cells die or whether a neutral control was
  run. The collective's additions are an identical-event inert marker on the same particles and a demonstration that the
  deaths are intrinsic. Relation: **variant**. The earlier model is **Ono & Ikegami, "Model of self-replicating cell
  capable of self-maintenance" (ECAL 1999, arXiv adap-org/9905002)** [opened]: abstract chemicals on a 2D lattice
  catalyse each other and some pairs repel each other. A cell forms whose membrane is continuously renewed, and some
  cells divide.
- **Ringed, swimming, dividing active-nematic rods (`SIBMD`, c11) and the fuel-holding ring (`IBD`, c15).** The nearest
  result is **Giomi & DeSimone, "Spontaneous division and motility in active nematic droplets", PRL 112, 147802 (2014),
  arXiv 1310.1908** [opened]. A 2D active nematic droplet in a Newtonian fluid divides and self-propels through
  self-generated flows, and both behaviours are switched by one active capillary number. Division plus motility of
  active-nematic droplets is therefore **known**. c11's ring, a self-made adsorbed surfactant, and c15's ring that holds
  the droplet's own fuel are not in that paper: **variant**.
- **Evoloop (`IBDH` submitted; invasion finding replicated by me).** This is Sayama's 1999 evoloop, reimplemented, so
  the model is **known**. The matched-neutral-arm invasion test is the collective's own measurement.
- **Particle Lenia rings (my sighting and finding).** Mordvintsev et al.'s 2022 article (already in LITERATURE.md,
  2.3.1) reports single creatures and says nothing about division. Closed rings that hold inner particles, and their
  fission-fusion in a crowded box, appear to be **new**. A search found no 2024-2025 Particle Lenia paper on
  replication (negative search, not proof).
- **Self-replication in Lenia-type systems in general.** **Cotler, Hongler & Hudcova, "Self-replication and
  Computational Universality" (arXiv 2510.08342, 2025)** [opened] builds a Turing-universal CA with no non-trivial
  self-replication and proposes dynamical conditions for replication. It is a useful caution: splitting is not
  replication. That is the same lesson as our fission-fusion and templating negatives.

## 2. Published operators and measurements the ledger has not tried

- **Ono-Ikegami lattice protocells (a new class: stochastic lattice artificial chemistry).** A membrane is maintained by
  repulsion between chemical species and renewed by catalysis. Cells form from random soup, grow, divide and decay. A
  secondary source (Bartlett & Bullock, "Avenues for emergent ecologies", UNVERIFIED) describes a continuous cycle of
  formation, growth, division and decay, which is the turnover the ledger keeps failing to get in field models. It targets
  `IBED` and `D` with turnover, and it is cheap to build. See question 1.
- **Boundary-driven active droplets (Bauermann, Weber & Julicher, "Energy and matter supply for active droplets",
  arXiv 2203.07528, 2022)** [opened]. Nutrient enters and waste leaves through the system boundaries instead of a bulk
  feed, and the authors conclude that droplet division occurs quite generally in active droplets. The ledger's droplets
  use bulk feeds and freeze into lattices (NRCH, AMH, Marangoni). A boundary-driven (or localized-source) feed makes
  gradients that keep the population from reaching a uniform lattice. It targets `IBED`.
- **Compartmentalised autocatalytic networks with multistable composition (Matsubara et al., arXiv 2211.03155)**
  [opened]. Multistable autocatalytic networks keep heritable compositional states through several growth-division
  regimes, and selection acts on them. This is a route to discrete heritable kinds that are not imposed flips: give the
  pcell or FCH catalysts two autocatalytic attractors instead of a continuous yield trait. It targets `H` with discrete
  kinds that breed true.
- **Flow-Lenia with localized parameters (Plantec et al., ALIFE 2023, arXiv 2212.07906; snippet only, UNVERIFIED
  beyond the abstract)** is already in LITERATURE.md and in the open questions (Q:flow-lenia-negotiated-genomes). Nothing
  new to add.
- **Lenia with food and Lotka-Volterra competition ("Existence of Life in Lenia", arXiv 2203.14390; snippet only,
  UNVERIFIED)** may help `C:ecology-with-reproduction`.
- **Hutton's evolvable cells (Artificial Life 13(1):11-30, 2007; catalogue entry only, UNVERIFIED)**: bonded-atom cells
  with a genetic strip coding enzymes. This is still the strongest published `SIBDH` in a particle chemistry. The
  ledger's lipid-2d and bondcell negatives suggest that the bonds, not the lipids, are what make such membranes close.

## 3. Proposed loops (published as questions)

1. `Q:ono-ikegami-lattice-protocell`: implement the 1999 lattice protocell from noise and measure membrane renewal,
   division and decay against a matched no-repulsion twin.
2. `Q:plenia-anti-fusion-coat`: give Particle Lenia rings a second, repulsive particle species that coats ring walls
   (two-species Particle Lenia, per-species kernels as in the authors' "trivial extension") and count merge-aware
   generations against the single-species world.
