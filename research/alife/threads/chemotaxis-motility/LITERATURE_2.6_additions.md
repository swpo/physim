# Proposed additions to LITERATURE.md §2.6 (chemotaxis / active matter)

Written in the thread directory because researchers only edit their own thread. The committee may merge it into §2.6.
Citations are from memory: venues and years are believed correct, but nothing below was re-verified online this sprint.

- **Krischer & Mikhailov (1994)**, "Bifurcation to traveling spots in reaction-diffusion systems", *Phys. Rev. Lett.* 73, 3165.
  A stationary spot in a two-component RD system with a slow, long-range inhibitor undergoes a drift (pitchfork) bifurcation to a travelling
  spot when the inhibitor relaxes slowly enough. *Relevance:* this is the Laplacian-only analogue of our kstrail swimmer: a slow
  self-made inhibitor h that the body leaves behind. Our version replaces the activator's local kinetics by conservative chemotactic
  advection with volume filling. The committee's requested "Laplacian-only slow-inhibitor control" tests whether RD alone gives the
  same swimmers from noise. Not run (see REPORT_r3).
- **Kranz, Sokolov & Golestanian (2016)**, "Effective dynamics of microorganisms that interact with their own trail", *Phys. Rev. Lett.* 116, 038101.
  Single autochemotactic particles that deposit a slowly decaying chemical: a self-repelling trail gives persistent (ballistic) motion, and
  self-attraction gives localisation. *Relevance:* the particle version of our self-propulsion operator.
- **Soto & Golestanian (2014)**, "Self-assembly of catalytically active colloidal molecules: tailoring activity through surface chemistry",
  *Phys. Rev. Lett.* 112, 068301. Non-reciprocal chemical interactions between two species (one chases, the other flees) make bound
  pairs and clusters that self-propel. *Relevance:* our pursuit pairs (predator lodged behind a fleeing prey) are a continuum,
  many-body version of these non-reciprocal "chaser-fleer" molecules.
- **Agudo-Canalejo & Golestanian (2019)**, "Active phase separation in mixtures of chemically interacting particles",
  *Phys. Rev. Lett.* 123, 018101. Mixtures of species with non-reciprocal chemotactic couplings phase-separate even when no single species
  does, and form self-propelled clusters (non-reciprocal active matter). *Relevance:* the theory frame for the pursuit/evopursuit worlds.
  Non-reciprocity (chi_x ≠ chi_y in sign) is what makes our composites move.
- **Tsyganov, Brindley, Holden & Biktashev (2003)**, "Quasisoliton interaction of pursuit-evasion waves in a predator-prey system",
  *Phys. Rev. Lett.* 91, 218102. Taxis-coupled predator-prey PDEs (predators climb prey gradients, prey flee predators) support travelling
  pursuit-evasion waves that can pass through or reflect off each other. *Relevance:* closest PDE precedent for our pursuit/ecology
  worlds. Ours adds self-propulsion, bounded bodies and division, so the waves become discrete individuals.
