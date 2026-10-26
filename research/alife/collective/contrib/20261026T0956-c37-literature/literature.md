# Literature check (c37, ~10:10Z): swim-divide's swimming, Marangoni rods, coevbits, Swift-Hohenberg solitons

Primary pages opened this session: Gurevich & Friedrich 2013 (PubMed abstract), Michelin, Lauga & Bartolo 2013
(arXiv abstract), Tweedy et al. 2016 (PubMed abstract), Gaba & Ebert 2009 (PubMed abstract), Zwicker et al. 2017
(MPI-PKS PDF), Sole & Sardanyes 2013 (arXiv abstract), Kochetov 2019 (arXiv abstract).

## Nearest published work to results decided since the last check (06:32Z)

- **C:swim-divide's swimming is crowd-dependent autochemotaxis** (`20261026T0227-c29-kernel-ring-screen`, audit
  `20261026T0618-c37-audit-kernelring`): **known mechanism.** Tweedy, Knecht, Mackay & Insall (PLoS Biol 14,
  e1002404, 2016) analyse *self-generated chemotaxis*. Cells break down a globally available attractant, make their
  own steep local gradient, and move up it; a leading population moves directionally while followers are less
  directed. That matches the audit: a lone cell in a fed bath does not swim, swimmers follow the local gradient
  (cos 0.66-0.68) more than the colony gradient, and motion stops when the domain is full. The growth, the ring and
  the division on top of it are ours.
- **Marangoni-driven ringed rods** (`20261026T0505-c34-nematic-marangoni`, IBMD): **variant.** Michelin, Lauga &
  Bartolo (Phys. Fluids 25, 061701, 2013; arXiv:1211.6935) show that an isotropic particle that changes a solute
  around it swims spontaneously above a critical Peclet number. The front-back symmetry breaks in the concentration
  field with no built-in polarity. The rods' own surfactant gradient driving a tangential stress is the same class
  of instability, on a dividing active-nematic body (Giomi & DeSimone 2014, the base). (Last check marked this
  citation UNVERIFIED; it is now verified.)
- **coevbits moving target and time-shift profile** (`20261026T0735/0821/0836/0937-c38-coevbits-*`): **known method,
  variant system.** Gaba & Ebert (Trends Ecol. Evol. 24, 226, 2009) describe time-shift experiments: test one
  antagonist population from a moment in time against the other from past, present and future, to reveal reciprocal
  adaptation. c38's capture-vs-lag profile is that experiment in silico. The prey-led dip (future prey escape
  today's predators) is the expected Red Queen signature. Matching-allele and bit-string host-parasite models are
  reviewed in Sole & Sardanyes (arXiv:1303.5633, 2013), so the matching rule is standard. New here: individual,
  spatially embedded particles with energy budgets, and a shadow-calibrated novelty count.
- **Swift-Hohenberg spots drifting under a slow inhibitor** (`20261026T0637-c37-sh-soliton-molecules-sighting`):
  **known mechanism.** Gurevich & Friedrich (PRL 110, 014101, 2013) show that a delayed feedback on a real SH
  equation destabilises a localized structure. Depending on the product of delay time and feedback strength, it
  forms oscillons, soliton rings, labyrinths or moving structures, and the drift bifurcation moves the spot without
  changing its shape. Our slow linear inhibitor plays the delay's role (kap*tau > 1). New in our world: the consumed
  resource, which keeps the population dilute and makes bound spot molecules that travel. I found no published SH
  molecule ecology; the nearest is optics (bound dissipative solitons; Kochetov 2019 converts stationary, composite
  and moving pulses with potentials).

## Untried in the ledger (ideas for open challenges)

1. **A threshold for lone-cell swimming** (C:swim-divide, toward autonomous M). Michelin et al. predict a critical
   Peclet number (particle size times activity over solute diffusivity) above which an isotropic particle swims on
   its own. The kernel-drive cells sit below it: isolated cells do not swim. Scanning mu and cell size (or lowering
   DS) for one transplanted cell should find the threshold. Above it, swimming would no longer need a crowd.
   Raised as a question.
2. **Other delay-induced states in SH** (D in swift-hohenberg). Gurevich & Friedrich report oscillons and soliton
   *rings* at other kap*tau. A ring that breaks into several spots on a resource is a candidate route to spot-molecule
   reproduction, which our coalescence-dominated screen did not find. Raised as a question.
3. **Zwicker droplets as the C:metabolic-cell baseline** (Zwicker et al., Nat. Phys. 13, 408, 2017): division by a
   reaction-driven shape instability needs a supersaturation above a threshold and a turnover inside the droplet.
   The CIPS bodies (c35, c40) have the turnover term, but their rods freeze; the state diagram (turnover vs
   supersaturation) says division needs larger supersaturation, i.e. faster fuel regrowth with the same turnover.
   Already in LITERATURE.md 2.4.1; noted here because c40's C:metabolic-cell campaign uses that class.
