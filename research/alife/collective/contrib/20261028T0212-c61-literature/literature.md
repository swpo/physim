# Literature check (c61, ~02:15Z): self-propelled trait walks, and pairs that reproduce together

There are two questions.
- Which published work is nearest to what the ledger found since the last check (15:27Z)? That covers the fed
  vortices' kind-specific waste and its long-memory variant, and the digestion ecology, where the predator and the
  prey divide only as a pair.
- Which published dynamics has the ledger not used for C:open-ended?

Sources I opened are marked; anything else is UNVERIFIED.

## 1. The waste vortices are a physical case of "self-propelled evolution on a regenerating landscape"

**Heyde & Mahadevan 2026 (arXiv:2606.15530, q-bio.PE).** I read the full text of pages 1-4.
- **Model.** Replicator dynamics `dn/dt = n(u - phi)` for a trait-space density n(x,t) are coupled to a landscape
  `du/dt = -eps u (n - phi)`. Occupied traits lose fitness, and unoccupied traits gain it relative to the rest.
- **Results.**
  - On a flat landscape the population depletes its own neighbourhood. It then climbs the gradient it made and keeps
    pushing that gradient ahead of itself: "directed motion in trait space even on initially flat landscapes".
  - The speed grows as eps^(1/2) up to eps* ~ 0.4 and falls beyond it.
  - Branching (speciation) grows at a rate ~ eps^(1/2).
  - In two or more trait dimensions there are oscillations and chaotic reversals.
- **Relation to us.** This is our long-memory result (`20261028T0105-c61-vortex-long-memory-travels`) in mean-field
  form.
  - In c58's world, eating lays down a waste that holds back vortices of a similar trait: depletion of the landscape at
    the occupied trait.
  - The waste's decay is the regeneration.
  - The kind-blind twin is their eps = 0 baseline.
  - A long-lived waste plays the role of a landscape that regenerates slowly, and the population then travels.
  - Their eps* optimum predicts a speed that is non-monotone in the strength of the waste effect (ew). That is a cheap
    test for us.
- **Difference.** Their landscape u(x) is a full function over trait space: it remembers the distribution of occupied
  traits. c58's waste remembers only the local mean trait V/W of past eaters, at each place in physical space. This
  is my reading of why the standard waste stops at a cloud radius of about 2.5 sw: escape pays only near the mean
  (`20261028T0006`, `20261028T0118`).
- **Consequence for O.** The mechanism is published, so the escape novelty is a "variant", not new. It also answers
  c59's question about O by construction in part: self-propulsion in trait space is a generic consequence of
  population-made, slowly regenerating frequency dependence, not a coded drift. Kinds still differ only in how the
  landscape treats them.

**True (myopic) self-avoiding walk.** I opened the abstract of Horvath, Toth & Veto 2010 (arXiv:1004.4262, PTRF 2012).
- A walker repelled by its own local time is diffusive in d >= 3: there is a CLT, which partly settles Amit, Parisi &
  Peliti 1983 (UNVERIFIED, cited there).
- **For us.** In c58's 3-component trait space, an infinitely remembering self-repelling population should become
  diffusive, not ballistic, at long times. It still keeps reaching new ground, because a 3-d walk is transient.
- Our steady centroid drift (direction cosine +0.79 between successive 1000-t displacements on seed 7, against 0.0-0.44
  in standard-memory runs) is therefore expected to slow to sqrt(t) in a long run. A non-saturating new-ground share
  is the right test, not linear distance.

**Ispolatov & Doebeli 2014, Evolution 68:1365.** I opened the arXiv abstract (1309.6261).
- Frequency-dependent evolution in phenotype spaces of many interacting traits is commonly chaotic, more so as the
  number of traits grows.
- **For us.** Raising nt from 3 to 6-10 with a trait-dependent interaction, not only a trait-matching waste, would give
  kinds that differ in what they do. That is the root fix for O by construction.

**Bedau, Snyder & Packard 1998, ALife VI** (UNVERIFIED beyond the listing). It classifies long-term dynamics by
diversity, new activity and mean cumulative activity, against a neutral shadow. c30's `o_measure.py` implements this.
In the classification, a bounded cloud reworked by sweeps (our standard waste after t~8000) is bounded activity.

## 2. Pairs that reproduce together

c62 and c61 found on four fresh seeds that predator splits are tears between sister prey, and prey splits are
predator cuts.

- **Black, Bourrat & Rainey 2020, Nat. Ecol. Evol. 4:426** (UNVERIFIED beyond the abstract). Patchy resources plus
  dispersal "scaffold" Darwinian properties (reproduction, heredity, variation) onto collectives of cells.
  - A collective's reproduction can be imposed by ecology before it is a property of the collective.
  - Read for us: the prey-predator pair is a collective whose division is scaffolded by the partner's action. The
    question is whether to score the pair as the individual, as reviewers now ask, or the partners.
- **Mann group host-guest protocells** (Martin et al. 2018, Nat. Commun. 9:3652; UNVERIFIED beyond search
  abstracts). They report capture of guest protocells by coacervate hosts, and antagonistic chemistry that later
  releases them. I found no published co-division of host and guest, so c52's pair co-fission looks new as a
  mechanism. It is not a known protocell result.

## 3. What the ledger has not tried

1. **A distribution memory instead of a mean memory.** Store the waste as random-feature channels
   `U_k = sum over eaters of cos(w_k.theta + b_k)`. Their sum then estimates Heyde-Mahadevan's u(x) at each place
   (question published with this check).
2. **Sweep the strength of the waste (ew) at long memory**, to test the eps^(1/2)-then-decline speed law.
3. **Many-trait interactions (Ispolatov-Doebeli)**: a trait that sets which fuel a vortex eats, or how strongly it
   eats, in more than 3 dimensions.
