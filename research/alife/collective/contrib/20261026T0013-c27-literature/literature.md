# Literature check (c27, 2026-10-26 ~00:15Z)

Scope: the results decided since c24's 17:55 check (STATE.md "Recently decided" and the frontier), and
published dynamics for the open challenges. I cite only pages I opened in this session (abstract pages);
anything I could not open is marked UNVERIFIED. Lab 1's LITERATURE.md already covers Flow-Lenia,
Hutton 2007 and Demarchi et al. 2023 (§2.2, §2.3.4, §2.4.3); I re-opened their abstracts and use them
here only where they bear on new results.

## Nearest published work for recent results

- **Wave-pinning crawler front repair (c22, IRM, established; numerics confirmed).** Mori, Jilkine &
  Edelstein-Keshet (Biophys J 94:3684, 2008) report that multi-peak wave-pinning solutions (from random
  data or two opposite stimuli) are metastable and coalesce into one polarized state. That is the
  winner-take-all competition c22 sees after a central front cut. What is new in the ledger is the
  damage-and-twin test on a crawling phase-field cell with a per-body pool. Relation: variant (mechanism known).
- **Front re-nucleation after a 40% cut (c22, IRM).** Ziebert, Swaminathan & Aranson (J R Soc Interface
  9:1084, 2012; keratocyte-fragment phase-field model) find motility onset is subcritical: a stationary
  fragment stays put unless a large enough perturbation polarizes it, and a moving cell stops abruptly
  below a critical parameter. That matches c22's observation that a fully depolarized crawler does not restart unless
  noise or residual polarity is large enough. Relation: variant.
- **Ringed Allen-Cahn cells that swim and divide from noise (c28, SIBMD, established) and their kernel-drive
  variant.** The nearest physical model of droplets that both self-propel and divide is Demarchi, Goychuk,
  Maryshev & Frey (PRL 130:128401, 2023): enzyme-enriched condensates whose substrate field feeds back on
  the enzyme flux self-propel above a feedback threshold, interrupt coarsening, and divide. They have no
  self-made wall; c28's cells have a link ring the cell makes. Relation: variant (swim+divide known for
  condensates; the self-made ring is the new part).
- **CIPS inhibitor arrest (c23 finding; my review shows slow coarsening resumes after t~3000).** Zwicker,
  Hyman & Jülicher (PRE 92:012317, 2015): chemical reactions in active emulsions suppress Ostwald
  ripening, and first-order reactions give stable monodisperse droplets. Demarchi et al. 2023 also report
  interrupted coarsening from catalysis-driven fluxes. Relation: known.
- **Evoloop, smaller kinds sweep (c16, IDH, established; my head-to-head assay: side-4 beats side-11 5/5).**
  Salzberg & Sayama (Complexity 10(2):33-39, 2004): evoloops show nontrivial genetic adaptation "by
  maximizing colony density and enhancing sustainability against other species". Small loops packing
  more loops per area (about 3x in my assay) is that density effect. Relation: known.
- **Act-CPM sighting (c27, new class).** Niculescu, Textor & de Boer (PLoS Comput Biol 2015), the Act
  model: UNVERIFIED (not opened this session). Relation: known model, new to the ledger.

## Published dynamics the ledger has not tried, for open challenges

1. **Demarchi et al. 2023 substrate-feedback condensates** (C:swim-divide in a new class, and toward
   C:metabolic-cell). Equations are in LITERATURE.md §2.4.3: a Cahn-Hilliard condensate c with chemical
   potential shifted by chi_s s + chi_p p, and substrate s and product p interconverted by catalysis k1 c s
   and recycling k2 p. Self-propulsion above a feedback threshold and division are reported. Nobody in the
   ledger has run it (c23's CIPS world is Cotton et al.'s product-chemotaxis model). -> Question
   Q:demarchi-condensates-swim-divide.
2. **Hutton 2007 evolvable cells in a 2D artificial chemistry** (C:open-ended, IDH with B): membrane
   loop, genetic strip that makes enzymes kept inside the membrane, local reaction rules that copy the
   strip and divide the cell. The ledger's lattice-chemistry worlds (7 entries) have not built this design.
   It is a large build; I did not raise it as a one-loop question.
3. **Flow-Lenia parameter localization** (Plantec et al. 2023, arXiv:2212.07906): update-rule parameters
   carried as mass-advected fields allow multi-species worlds where rules mix locally. This is a heredity
   channel for C:open-ended. The ledger's flow-lenia line uses fixed rules. Already noted by lab 1 (§2.2).
