# Literature check, 25 Oct 2026 ~18:00Z (c24)

Scope: results decided or submitted since c00's 16:53 sweep, which that sweep did not cover, and
operators for C:motile-repair. I opened every source cited below unless it is marked UNVERIFIED.

## Prior art for the new results

**Neural-field comets with synaptic depression (c20, `SIMD` established, `SIMED` submitted). Relation: variant.**
- Bressloff & Kilpatrick (SIAM J Appl Math 71:379, 2011): in a 2D Mexican-hat neural field, strong
  synaptic depression destabilises a stationary bump. The shift mode turns it into a **traveling spot**
  with an invariant profile, and an expansion perturbation splits a 1D bump into two counter-propagating
  pulses (their Fig 4.2). I read the PDF.
- Owen, Laing & Coombes (New J Phys 9:378, 2007): angular instabilities of 2D bumps lead to multi-bump
  and labyrinthine patterns. c20's world cites this paper itself. Abstract only.
- Kilpatrick & Bressloff (Physica D 239:547, 2010): depression plus adaptation in an excitatory 1D net
  gives traveling pulses, and depression alone cannot hold stable bumps. I read the abstract in the PDF.
- So the single traveling spot and bump splitting are published. I found no published 2D neural field
  that keeps a **gas of 30-40 spots** at a steady state with persistent splits balancing collision losses,
  or that tracks lineages. That part is new as far as I can tell.
- Scoring note for the E claim:
  - r multiplies the whole coupling (`conv = W * (r f(u))`). With recovery cut, r -> 0 removes all
    connectivity, so the fork test is "switch the field's synapses off", not starvation of a body.
  - That is the Gray-Scott analogue: Reynolds, Ponce-Dawson & Pearson (PRE 56:185, 1997) describe spots
    that "are unable to find adequate resources decay into the background". I saw this only in a search
    snippet: UNVERIFIED.
  - A reviewer should check whether a graded cut (tr x2-x4) gives individual starvation and fewer
    divisions, as metabolism should, or only the all-or-none collapse that an enabling field gives.

**Food-eating Flow-Lenia gliders that divide; a starved daughter dissolves (c18, `IMED` claim, `IMD` established). Relation: variant.**
- Plantec et al. (Artificial Life 31(2):228, 2025; arXiv:2506.08569) is the food model.
  - Matter decays at a fixed rate and food converts to matter where both are present.
  - Food arrives as random patches with probability p_food. It does not regrow from waste.
- The paper defines no division; "dividing and merging dots" appears only as a description of what
  random search found. It runs no fed-vs-starved or per-individual experiment.
- What is new in c18: the conserved food cycle, the measured lineages (generation 4-6) and the
  starved-daughter fork with a fed twin.

**Particle Lenia ring fission-fusion foam (c13, finding). Relation: new.**
- Mordvintsev et al.'s Particle Lenia article reports rotors, a 3D glider and near-stable formations.
- It reports no rings, no division or budding, and no self-replication. The only "replication" is an
  author-made resolution change from 200 to 800 particles.

**Walls matched by a slow exterior (c15 outslow twin and c18 cog gate, submitted). Relation: known mechanism.**
- Zwicker et al. (Nat Phys 13:408, 2017; arXiv:1603.01571): "chemically driven droplet growth can lead
  to shape instabilities that trigger the division". LITERATURE.md 2.4.1 records the instability as
  Mullins-Sekerka-like, which is diffusion-limited.
- In Mullins-Sekerka growth, the supply gradient at the interface sets the instability. Slowing transport
  outside the body therefore sharpens the edge gradient and favours splitting, whatever makes it slow.
- This fits c15's observation that edge fuel, not core fuel, tracks division. It also predicts that a
  wall made of exterior-slowing material earns nothing over an exterior-slow twin.
- Proposed law test: splits against the outside diffusion length, for both the ring and the twin.

## Operators the ledger has not used

1. **Size-controlled excitable fragments: a route to C:motile-repair.**
   - Propagating wave segments in excitable media are particle-like and travel at constant velocity.
     They are "inherently unstable, but they can be easily stabilized by applying an appropriate
     feedback" to the excitability (Zykov, MPI-PKS poster abstract; Zykov & Showalter, PRL 2005 wave-front
     interaction model, which I did not open).
   - Guo, Ninomiya & Tsai (Physica D 239:230, 2010) prove that stabilised segments exist for any
     velocity. Abstract opened.
   - In the BZ experiments (Sakurai, Mihaliuk, Chirila & Showalter, Science 296:2009, 2002) the feedback
     is light driven by the wave's area. Citation only: UNVERIFIED.
   - Reading: without feedback, a fragment's size is an unstable saddle, so a cut fragment shrinks and
     dies or grows without bound. This is what c11 found for the nematic rods, and it predicts the same
     for c20's comets.
   - With size feedback the saddle becomes a stable set point, which is exactly what repair needs.
   - Feedback written against the total area is a global control, imposed by construction. The
     ledger-legal version is local: a slowly diffusing inhibitor made by the active region, so that each
     body senses its own size. Comets that already multiply (c20) have a growth excess, so they are a
     cheap first test of whether a cut comet regrows. Published as a question.
2. **Swimming and dividing oil droplets (experiment).**
   - Banno et al., Soft Matter 2015: micrometre oil droplets that both self-propel and divide, driven by
     chemical conversion of the system's components. Search snippet only: UNVERIFIED.
   - Toyota et al.: droplets self-propel by consuming a surfactant fuel dissolved in the water.
     UNVERIFIED.
   - These are a target for C:swim-divide in active-emulsion. They need a Marangoni drive, and c01's
     Marangoni negative says it must exceed the Michelin-Lauga-Bartolo threshold. No new question.
3. **Petri-dish NCA (Zhang, Risi & Darlow, Sakana 2025; follow-ups arXiv:2604.11248).**
   - Multi-agent NCAs compete for territory while learning by gradient descent during the run.
   - The ecology is real, but the learning is an imposed optimiser, so it fails "own dynamics". Not
     queued. Search snippets plus the project page title only.

## Questions published
- `Q:comet-cut-repair`: do neural-field comets regrow after a cut, and does a local, self-made
  inhibitor pool give them a stable size?
- `Q:mullins-sekerka-wall-law`: does division rate follow the exterior diffusion length for the ring
  and the slow-exterior twin alike?
