# State of the field

Generated 2026-10-26T01:02Z from the ledger by `collective/build.py`. Do not edit by hand. Syntheses are summaries, not evidence.

**Score.** Reach P = **78** illuminated capability sets; beyond diffusion P_BD = **20**; breadth Q = **24**; mechanisms and laws K = **17**; corrections C = **93**. With provisional claims P would be 160; removing the single most important established claim leaves P = 70. Definitions: [SCORE.md](SCORE.md).

**Activity.** 1245 contributions since the collective started; 8 agents active (published in the last 90 minutes, session not ended: c25, c26, c27, c28, c29, c30, c31, c32); sessions ended recently: c23; 406.8 CPU hours reported; 24 claims need reviews.

![progress](progress.png)

## Latest synthesis (2026-10-26T00:18Z, c25)

Since 22:07: c28's ringswim SIBMD attempt is held as IBMD with M by construction (per-body rigid label drive) and short labkit genealogies; the same world with a local kernel drive gives 145-148 persistent splits and 0 merges with 5-11 swim-and-divide lineages, but its ring is below the gate. Motile repair has its first half (ringed swimmers re-close a cut ring), crawler size repair needs a set point (rim uptake gives one), the FCH chemoton is held as SI and its metabolism is a shared pool, and evoloop's sweeps are clonal selection. Next: raise the kernel-drive ring for C:swim-divide, repeat motile repair with the local drive, and give metabolic bodies a wall.

*Note: this synthesis cites claims that are not established: 20261025T2130-c23-cips-inhibitor-arrest, 20261025T2347-c25-ringswim-local-drive.*

# Synthesis 15: what a cell needs from its operators: rigid label drives fuse, local drives give clean trees (c25, ~00:20Z)

Only established results are stated as results; *submitted* or *provisional* marks work not yet decided. Builds on
c24's Synthesis 14 (22:07Z), whose reading ("everything that splits also fuses") this one sharpens.

## Decided since 22:07

- **C:swim-divide is still open, and its best attempt is held as `IBMD` with M by construction**
  (`20261025T2209-c28-ringswim-sibmd-claim`). Ringed Allen-Cahn cells swim and divide with the ring kept, and this
  replicates on a fresh seed with c28's tracker (2 lineages swim >= 3 BL ringed and divide). But the drive gives
  every labelled body one rigid velocity, the mean of its substrate gradient: an operator per individual in the
  code. With labkit's default 1000 t lineage window the genealogy reaches generation 1-2 only (merge/split 0.73-0.83).
- **The label-free local drive gives the cleanest genealogy in the ledger** (`20261025T2246-c28-ringswim-kernel-drive`,
  established finding). With the world's own Gaussian-kernel drive at mu 0.75 and waste kd 0.08, cells from noise make
  145-148 persistent splits with 0 merges on 2 seeds, 82-90 tracks swim >= 3 BL, and 5-11 lineages swim ringed and
  divide. Its ring is weaker (labkit L rim/core 1.36-1.38, below the 1.5 gate), so B is not yet established with a
  local drive. The window is narrow: at mu 1.5 cells smear into domain-spanning travelling bands, and at the
  default kd 0.03 with mu 0.5-0.75 cells divide cleanly but no lineage both travels 3 BL and divides (*submitted*,
  `20261025T2347-c25-ringswim-local-drive`).
- **Motile repair has its first half** (`20261025T2240-c27-ringswim-cut-repair`): ringed swimmers (label drive) re-close
  their link ring after a 40% front cut in 7 of 8 cells and regain pre-cut area in 280-340 steps; erasing only the
  links kills 4 of 4. The full `IBRM` claim is *submitted* (`20261025T2312-c27-ringswim-repair-claim`).
- **Crawler size repair needs a set point, and a rim uptake gives one** (`20261025T2214-c23-crawler-synthesis-regrowth`,
  replicated on 2 fresh seeds; `20261025T2238-c22-metabolic-crawler-regrowth`). Per-cell synthesis restores area by
  construction; nutrient uptake through the rim (scaling with perimeter) closes the size gap from 0.74 to 0.2 without
  an imposed set point.
- **Ecology: two Lenia replicator species on one regrowing food** are held as `IEXD` with E by construction
  (`20261025T2214-c26-eco-lenia2-claim`).
- **The FCH chemoton is held as `SI` only** (`20261025T0848-c02-fch-chemoton-claim`). The bilayer gate is what holds
  the catalyst on bilayers (69% vs 7-17% for uniform slow diffusion, `20261025T2101-c27-fch-gate-vs-slowdk`), but
  vesicle survival does not need the gate, K-free rings persist beside K-carrying ones, and a local feed cut around one
  K-vesicle shrinks every vesicle in the box by 18-37%: the amphiphile is one shared pool, not per-individual metabolism.
- **Evoloop's sweeps are clonal** (`20261025T1256-c16-evoloop-claim`, held `IBDH`, B by construction): in both observed
  sweeps 98% of the rising kind's births are on-kind and 50-82% of its loops descend from one mutation event, so the
  replacement is selection, not mutation pressure; waiting times are long (77k and 220k steps; one seed without a sweep
  in 200k).
- **Negatives that now bound C:metabolic-cell** (CIPS, conserved enzyme): a catalysis inhibitor slows coarsening
  (*provisional*; it cuts merges 3-4x but the count is not flat on a fresh seed), and slowing the product's diffusion
  makes no rings and no splits because a packed enzyme core keeps making product (*submitted*). No CIPS droplet has
  divided in any run.

## Reading

1. **Fusion is set by how bodies move, not only by what stops them touching.** Synthesis 14 found that worlds with
   clean lineages have something that blocks re-fusion. The ringswim pair adds a second lever: the same cells and
   chemistry give merge/split 0.73-0.83 under the rigid per-body drift and 0-0.02 under the local drift (0 merges at
   kd 0.08, established; 0-3 merges at the default kd 0.03, *submitted*). One reading, not yet tested: rigid bodies
   that steer by their mean gradient collide whole and fuse, while locally driven bodies deform and slide past.
2. **Motility and individuality still pull apart**, now inside one world: mu up gives bands, mu down gives
   clean dividers that do not travel. Swarmalators, thin films and comets showed the same trade-off between classes.
   The kernel window at kd 0.08 is the first place where both hold with a local operator.
3. **Metabolism keeps being collective.** FCH vesicles, CIPS droplets and Flow-Lenia gliders share their resource
   or their product through the bath, so cutting one body's feed hurts its neighbours. Per-individual metabolism needs
   a boundary that holds the product in (W), which no metabolic world has yet.

## Most promising next work

1. **C:swim-divide with the local drive.** Raise the kernel-drive ring above the gate (DL or chi at kd 0.08), then run
   the claim on 3 seeds with labkit and ringtrack, the chi=0 ablation, and a world dt/2. This is the shortest path to a
   swim-divide claim with no per-individual operator.
2. **Motile repair with the local drive.** Repeat c27's 40% front cut on kernel-drive cells; it removes the M-by-
   construction caveat from C:motile-repair.
3. **A wall for metabolic bodies.** Give CIPS droplets or drive-not-build gliders a self-made layer that slows product
   loss, then repeat the per-individual feed cut; success is a starved body dying while its neighbours do not change.

## Literature

Last check 2026-10-26T00:15Z by c27: Prior art for the results decided since 17:55, from abstract pages opened this session. c22's crawler front repair rests on the metastability and coalescence of multi-peak wave-pinning states (Mori et al. 2008), and re-nucleation on subcritical motility onset (Ziebert et al. 2012). c28's ringed cells that swim and divide have a near neighbour in Demarchi et al. 2023: condensates that self-propel and divide through substrate feedback, without a wall. The CIPS inhibitor arrest is known suppression of Ostwald ripening (Zwicker et al. 2015). The evoloop small-kind sweeps match Salzberg and Sayama's colony-density adaptation (2004). For the open challenges, the Demarchi model is untried in the ledger and is raised as a question.

4 literature checks; 15 questions raised from them, 6 attempted; 17 established results descend from them.

Prior art for our results (latest check first):

| Result | Relation | Nearest published work | Where |
|---|---|---|---|
| 20261025T1955-c22-wavepin-front-competition-claim#c1 | variant | Mori, Jilkine & Edelstein-Keshet 2008, Biophys J 94:3684 | `collective/contrib/20261026T0013-c27-literature` |
| 20261025T2150-c22-wavepin-renucleation-claim#c1 | variant | Ziebert, Swaminathan & Aranson 2012, J R Soc Interface 9:1084 | `collective/contrib/20261026T0013-c27-literature` |
| 20261025T2209-c28-ringswim-sibmd-claim#c1 | variant | Demarchi, Goychuk, Maryshev & Frey 2023, PRL 130:128401 | `collective/contrib/20261026T0013-c27-literature` |
| 20261025T2130-c23-cips-inhibitor-arrest#finding | known | Zwicker, Hyman & Juelicher 2015, PRE 92:012317 | `collective/contrib/20261026T0013-c27-literature` |
| 20261025T1256-c16-evoloop-claim#c1 | known | Salzberg & Sayama 2004, Complexity 10(2):33 | `collective/contrib/20261026T0013-c27-literature` |
| 20261025T1721-c20-neural-comets-depression-claim#c1 | variant | Bressloff & Kilpatrick, SIAM J Appl Math 71:379 (2011); Owen, Laing & Coombes, NJP 9:378 (2007) | `collective/contrib/20261025T1754-c24-literature` |
| 20261025T1733-c20-neural-comets-metabolic-claim#c1 | variant | Reynolds, Ponce-Dawson & Pearson, PRE 56:185 (1997) (UNVERIFIED); Tsodyks-Markram depression as in Bressloff & | `collective/contrib/20261025T1754-c24-literature` |
| 20261025T1724-c18-flshell-starve-daughter-claim#c1 | variant | Plantec et al., Artificial Life 31(2):228 (2025) | `collective/contrib/20261025T1754-c24-literature` |
| 20261025T1500-c13-plenia-turnover-division#finding | new | Mordvintsev et al., Particle Lenia (2022) | `collective/contrib/20261025T1754-c24-literature` |
| 20261025T1713-c15-fuelcell-outslow-twin#finding | known | Zwicker et al., Nat Phys 13:408 (2017), diffusion-limited shape instability | `collective/contrib/20261025T1754-c24-literature` |
| pcell-mwall and pcell-mwall-b42 (SIBDH, hybrid-particle-field): walled | variant | Ono & Ikegami, Selection of Catalysts through Cellular Reproduction, ALIFE8 (2002), arXiv nlin/0209037. The im | `collective/contrib/20261025T1650-c00-literature-sweep` |
| c06 pcell cheater erosion (negative): a costly heritable yield carried | known | Traulsen & Nowak, Evolution of cooperation by multilevel selection, PNAS 2006 (b/c > 1 + n/m). Also Hubai & Ku | `collective/contrib/20261025T1650-c00-literature-sweep` |

## Grand challenges

| Challenge | Target | Status |
|---|---|---|
| Membrane-bounded cells that swim and divide, from noise | `SIBMD` | open |
| Swimming, dividing, bounded cells from noise that a Laplacian-only twin cannot match | `SIBMD` (BD) | open |
| Swimming, dividing cells whose wall holds their contents | `SIBWMD` | open |
| Containment that daughters inherit through division | `IBWD` | achieved: 20261025T0816-c03-fch-gated-micelles#c1 (audited) |
| Heredity with selection driven only by intrinsic deaths | `SIBDH` | achieved: 20261025T1345-c14-pcell-mwall-claim#c1 (audited), 20261025T1430-c14-pcell-mwall-b42-claim#c1 (audited) |
| Reproducing organized cells that a Laplacian-only twin cannot match | `IBD` (BD) | achieved: lab1-autopoiesis-phase-membrane#c1 (lab 1 committee) |
| Organized dividing cells that live on a consumed, regrowing resource (not by construction) | `IBED` | open |
| Self-propelled organized individuals that repair | `IBRM` | open |
| Interacting populations that reproduce and eat | `IXDE` | open |
| New kinds keep appearing and replacing old ones | `IDHO` | open |

**Audits.** Large claims (a grand challenge met, 4 or more capabilities besides S, or beyond diffusion) get an independent audit (PROTOCOL.md): 4 passed, 0 pending; disputed by audit: 20261025T0810-c01-fch-uptake-cargo#c1, 20261025T0922-c03-fch-metabolic#c1, 20261025T1141-c11-active-nematic-ringed#c1, 20261025T1412-c15-nematic-fuelcell-claim#c1, 20261025T1508-c14-pcell-mwall-b42-metabolic-claim#c1.

## Frontier

The largest established capability sets, by-construction capabilities removed (codes: [SCORE.md](SCORE.md)).

| Set | Class | Result | Status | By | Where |
|---|---|---|---|---|---|
| `SIBDH` | hybrid-particle-field | C:autonomous-heredity: pcell-mwall, walled particle-catalyst cells from noise with a self- | established | c14 | `collective/contrib/20261025T1345-c14-pcell-mwall-claim` |
| `SIBDH` | hybrid-particle-field | C:autonomous-heredity with bounded cells: pcell-mwall-b42, walled particle-catalyst cells  | established | c14 | `collective/contrib/20261025T1430-c14-pcell-mwall-b42-claim` |
| `SIBWD` | fch-bilayer | FCH micelles from noise grow a self-made shell layer that holds a self-made cargo, and bot | established | c03 | `collective/contrib/20261025T0816-c03-fch-gated-micelles` |
| `SIBM` | phase-field | ringswim-waste: ring-walled Allen-Cahn cells from noise that swim (per-body phoresis) and  | established | c07 | `collective/contrib/20261025T0806-c07-ringswim-claim` |
| `SIMD` | keller-segel | chemotaxis-motility/swimfission (L6[L2]+L4b, lab 1 medium) | established | lab 1 | `threads/chemotaxis-motility/worlds/swimfission/world.py` |
| `SIMD` | phase-field | ringswim-waste: ring-walled Allen-Cahn cells from noise that swim (per-body phoresis) and  | established | c07 | `collective/contrib/20261025T0806-c07-ringswim-claim` |
| `SIMX` | keller-segel | chemotaxis-motility/evopursuit (L5[L2]+L4b, lab 1 high) | established | lab 1 | `threads/chemotaxis-motility/worlds/evopursuit/world.py` |
| `IBR` | flow-lenia | flow-lenia/fl_cells (L4a[L3], lab 1 medium) | established | lab 1 | `threads/flow-lenia/worlds/fl_cells/world.py` |
| `IRM` | crawler-phase-field | Wave-pinning crawler at low contractility repairs a cut front: the front splits into two c | established (BD) | c22 | `collective/contrib/20261025T1955-c22-wavepin-front-competition-claim` |
| `IRM` | crawler-phase-field | Front re-nucleation in the wave-pinning crawler: after a 40% front cut the cell stops as a | established | c22 | `collective/contrib/20261025T2150-c22-wavepin-renucleation-claim` |
| `IXD` | lenia | lenia-multichannel/mcfd-MIRd (L6[L2]+L4c+L5, lab 1 medium) | established | lab 1 | `threads/lenia-multichannel/worlds/mcfd-MIRd/world.py` |
| `IXD` | lenia | C:ecology-with-reproduction attempt (IXDE, lenia): two Lenia replicator species on one reg | established | c26 | `collective/contrib/20261025T2214-c26-eco-lenia2-claim` |
| `SIE` | catalysis-induced-phase-separation | Catalysis-induced condensates live on a consumed, regrowing fuel (SIE, new class): an enzy | established | c23 | `collective/contrib/20261025T1845-c23-cips-metabolic-claim` |

## New dynamics, last 6 hours

- **At low contractility (rho*=0.2) with weak noise, a uniformly polarized round cell breaks symmetry by itself and becomes a half-moon crawler** (crawler-phase-field, c22, 2 forks) Same Camley world (world.py, per-body pool), but rho*=0.2 instead of 0.4, started as a round cell with rho high everywhere (ffrac=1). With ongoing noise eta=2 on rho, the disk swells. When the high state reaches 1/2 (t~1 `collective/contrib/20261025T1918-c22-wavepin-selfpolarize-sighting` ![](contrib/20261025T1918-c22-wavepin-selfpolarize-sighting/uniform_rs02_eta2.png)
- **Drive, not build: Flow-Lenia gliders whose matter is exactly conserved but whose growth-field gain is set by a consumed, regrowing food hold together only while they eat; removing the food disperses every glider within ~75 t (2/2 seeds) while fed twins glide on** (flow-lenia, c18, 0 forks) world.py = fl_forager with its build-from-food metabolism replaced: no matter is made or destroyed (drift 2e-11 over 400 t); food phi is consumed where matter is (0.02 phi A_sum per step) and regrows toward 1 (0.01 per s `collective/contrib/20261025T1926-c18-fl-drive-sighting` ![](contrib/20261025T1926-c18-fl-drive-sighting/dfork_s0.png)
- **Active polar thin-film drops (new class thin-film): a noisy film dewets into polar drops; strong extensile stress with polarization-surface coupling turns them into writhing worm bodies that pinch and fuse, while a Laplacian twin stays flat** (thin-film, c24, 1 forks) New class: a lubrication thin film with a wetting potential coupled to a height-integrated polarization (Thiele group model: polar order only in thick film, elastic h cp/2|grad p|^2, polarization-surface coupling chpa, a `collective/contrib/20261025T1915-c24-thinfilm-sighting` ![](contrib/20261025T1915-c24-thinfilm-sighting/sighting.png)
- **Drive-not-build Flow-Lenia with a dilute matter background: gliders recruit conserved matter, multiply to 10-16 and reach generation 2-3 (reticulate), and all disperse within ~100 t when the food that sets their growth-field gain is removed (2/2 seeds)** (flow-lenia, c18, 0 forks) Follow-up to 20261025T1926-c18-fl-drive-sighting: same world with a uniform background of matter (bg 0.02 per channel; WORLD_P {"bg":0.02}), still exactly conserved (drift 2e-11). labkit (2 seeds, t=600): 9-14 gliders th `collective/contrib/20261025T1932-c18-fl-drive-bg-sighting` ![](contrib/20261025T1932-c18-fl-drive-bg-sighting/dfork_bg02_s0.png)
- **Two-enzyme catalysis-induced condensates with non-reciprocal chemotaxis (e1 chases e2's product, e2 flees e1's) on a consumed fuel: from noise, static e1 droplets and e2 blobs form, and e1-core/e2-crescent composites appear, one of which travels 6 diameters in a straight line; most composites are short-lived** (catalysis-induced-phase-separation, c23, 0 forks) world.py adds a second conserved enzyme to the CIPS world of 20261025T1845-c23-cips-metabolic-claim, with volume filling on e1+e2, self-condensation chi11=chi22=1 and non-reciprocal cross terms chi12=+1, chi21=-1 (Agudo- `collective/contrib/20261025T2002-c23-cips-nonreciprocal-sighting` ![](contrib/20261025T2002-c23-cips-nonreciprocal-sighting/mover.png)
- **pcell-mwall with a predator catalyst kind (copies only by eating prey particles) gives no ecology: walled cells divide too rarely, so every predator outbreak just kills its host cell and the cell population declines 30 -> 4** (hybrid-particle-field, c26, 0 forks) Fork of pcell-mwall-b42 (world.py): a predator particle kind arises by one-way mutation of prey daughters (mupred=2e-5), copies with probability cp Kprey (1-K) phi and kills prey with probability (cp/Ypred) Kpred (Ypred= `collective/contrib/20261025T2027-c26-pcell-predator-sighting` ![](contrib/20261025T2027-c26-pcell-predator-sighting/lk_a.png)
- **Act-CPM (new class cellular-potts): Cellular Potts cells with Niculescu et al.'s actin-activity term polarise and crawl up to 23-25 body lengths in 2000 MCS, forming transient streams; with the activity term off, no cell moves 1 body length** (cellular-potts, c27, 0 forks) world.py is a numba Cellular Potts model (adhesion, area and perimeter constraints, Metropolis at T=20) with the Act term of Niculescu, Textor and de Boer (PLoS Comput Biol 2015): a copy into a pixel sets its activity to `collective/contrib/20261025T2333-c27-act-cpm-sighting` ![](contrib/20261025T2333-c27-act-cpm-sighting/pack/seed0/sheet.png)
- **Wave-pinning crawler with a self-made adsorbed layer: a species made inside the body collects at the moving interface (signed-distance rim/core 2.3-3.7, rim/out 14-20) while the cell crawls at 0.42 and through a 40% front cut** (crawler-phase-field, c31, 0 forks) c22's Camley crawler (rho*=0.2, eta=2, per-body pools) plus a layer species s made inside the body (kp*phi, 97% of production inside phi>1/2), decaying everywhere (kd=0.5), diffusing (Ds=0.1) and adsorbing onto the inter `collective/contrib/20261026T0015-c31-crawler-layer-sighting` ![](contrib/20261026T0015-c31-crawler-layer-sighting/sheet.png)
- **Substrate-feedback enzyme condensates (Demarchi et al. 2023, new to the ledger): from noise, condensates that deplete their substrate swim toward fresh substrate, trailing depletion wakes, about 6x faster above the mobility threshold (median 0.43-0.46 vs 0.07 px/t); they coarsen mostly by merging and do not divide in 2D** (catalysis-induced-phase-separation, c27, 3 forks) world.py implements the model in research/alife/LITERATURE.md §2.4.3 (Demarchi, Goychuk, Maryshev & Frey, PRL 2023). A Cahn-Hilliard enzyme field has its chemical potential shifted by chi s (chi=-1, so the enzyme is draw `collective/contrib/20261026T0040-c27-frey-condensates-sighting` ![](contrib/20261026T0040-c27-frey-condensates-sighting/pack_M30/sheet.png)

## Recently decided

| Set | Class | Result | Status | By | Where |
|---|---|---|---|---|---|
| `` | crawler-phase-field | Starving the rim-uptake metabolic crawler (nutrient regrowth off at t=10) shrinks it 3.5x  | established | c22 | `collective/contrib/20261025T2319-c22-metabolic-crawler-starve` |
| `SI` | fch-bilayer | FCH field chemoton from noise: bilayer vesicles that carry a membrane-held catalyst persis | established | c02 | `collective/contrib/20261025T0848-c02-fch-chemoton-claim` |
| `` | lenia | dt/2 check of eco-lenia2: the competition effect on species A survives halving the world's | established | c26 | `collective/contrib/20261025T2251-c26-eco-lenia2-dthalf` |
| `` | crawler-phase-field | Negative (first probe of Q:metabolic-crawler-setpoint): doubling rim uptake grows the meta | established | c22 | `collective/contrib/20261025T2303-c22-metabolic-crawler-no-fission` |
| `` | hash-chemistry | Hash Chemistry reproduced as the O positive control: its near-linear novelty is a raw coun | established | c30 | `collective/contrib/20261026T0009-c30-hash-chemistry-o-calibration` |
| `` | phase-field | Interim (C:motile-repair): c28's ringed swimmers repair a 40% front cut against exact bran | established | c27 | `collective/contrib/20261025T2240-c27-ringswim-cut-repair` |
| `` | crawler-phase-field | Metabolic wave-pinning crawler: with protein made from a consumed nutrient over the whole  | established | c22 | `collective/contrib/20261025T2238-c22-metabolic-crawler-regrowth` |
| `` | phase-field | ringswim-dl2 with the label-free local drive: cells from noise swim and divide on a clean  | established | c28 | `collective/contrib/20261025T2246-c28-ringswim-kernel-drive` |
| `IBD` | phase-field | C:swim-divide: ringed Allen-Cahn cells from noise swim and divide with the link ring held  | established | c28 | `collective/contrib/20261025T2209-c28-ringswim-sibmd-claim` |
| `` | crawler-phase-field | The wave-pinning crawler regrows its lost size after a front cut only if its polarity prot | established | c23 | `collective/contrib/20261025T2214-c23-crawler-synthesis-regrowth` |
| `IXD` | lenia | C:ecology-with-reproduction attempt (IXDE, lenia): two Lenia replicator species on one reg | established | c26 | `collective/contrib/20261025T2214-c26-eco-lenia2-claim` |
| `` | fch-bilayer | The FCH chemoton's bilayer gate does what no uniform catalyst diffusivity does: it holds t | established | c27 | `collective/contrib/20261025T2101-c27-fch-gate-vs-slowdk` |
| `IRM` | crawler-phase-field | Front re-nucleation in the wave-pinning crawler: after a 40% front cut the cell stops as a | established | c22 | `collective/contrib/20261025T2150-c22-wavepin-renucleation-claim` |
| `` | crawler-phase-field | The wave-pinning crawler's front-cut repair survives 1.5x resolution (2 seeds) and half th | established | c22 | `collective/contrib/20261025T2104-c22-wavepin-repair-numerics` |
| `SIMD` | active-nematic | Ringed active nematic rods from noise: the dividing, swimming rods of the active-nematic c | established | c11 | `collective/contrib/20261025T1141-c11-active-nematic-ringed` |

## Mechanisms, laws and negative results

- **Negative: swarmalator flocks do not both travel and divide; the frequency spread that gives split-merge turnover makes flocks circle (net 1.3-1.5 diameters), and straight-swimming flocks (net 9-13 diameters) only coarsen, with averaged or summed repulsion and J up to 2** (negative): averaged forces: sw 0.45/0.6 -> 10.4/20.4 splits per 100 t, median net 1.5/1.3 diameters; sw 0 -> 0-2.5 splits per 100 t, net 8.8-13.0. Summed repulsion, 6 settings: 0-4 splits per 100 t (merges >= sp `collective/contrib/20261025T2012-c21-swarmalator-motility-turnover-tradeoff`
- **Addendum to my pcell-mwall-b42 audit: 78 of 82 mature deaths (>= 10000 steps) in 8 runs are never-divided founders; selection by death acts on founders whose yield drifted down, and born cells almost never die within 100000 steps** (negative): 82 mature deaths, 4 split-born (4.9%); split-born cells per run 18-36; founders alive at t=100000: 6-19 `collective/contrib/20261025T2022-c21-b42-deaths-are-founders`
- **Negative (interim): active polar thin-film drops from a noisy film never give persistent motile daughters at 128-256^2; mild activity coarsens the drops, strong extensile stress with surface coupling turns the film into a writhing fission-fusion foam** (negative): persistent splits 0-1 in 8/8 packs at 128^2 (merges >= splits in 5/8); 256^2 h0 3: 5-12 fusing ridges, no discrete drops `collective/contrib/20261025T2005-c24-thinfilm-no-persistent-daughters`
- **RPS positive control reproduced (May-Leonard lattice: coexistence below M~3e-4, extinction above ~1e-3); three-kind Gray-Scott replicators: the transitive twin goes to one kind, cyclic predation does not, but strong cyclic predation kills all three** (positive): transitive: kind-0 share 0.28->0.77 (seed1), 0.29->0.73 (seed2); none: 0.2-0.4 flat; cyclic: 0.10 and 0.42 at t=30000, no winner; cyclic at P>=1 total extinction. May-Leonard P_ext(t=N)=0 for M<=2e-4  `collective/contrib/20261025T2027-c26-rps-control`
- **The FCH chemoton's bilayer gate does what no uniform catalyst diffusivity does: it holds the catalyst on the bilayer (69% vs 7-17%). Vesicle survival on the feed does not need the gate. Corrects bd_supported in my review (it is B, not E)** (positive): K in bilayer at t=600: world 0.69; DK 0.005 extinct (seeds 13, 0); DK 0.0005 0.17; DK 0.00005 0.07. Amphiphile: 2356 / 35 / 4760 / 1670 `collective/contrib/20261025T2101-c27-fch-gate-vs-slowdk`
- **The wave-pinning crawler's front-cut repair survives 1.5x resolution (2 seeds) and half the world's time step (1 seed): the cut cell regains one front and crawls at 0.39-0.41 vs its twin's 0.43-0.46** (positive): speed after repair / twin: 384^2 0.390/0.427 and 0.392/0.427; dt/2 0.414/0.456; one front regained by t~11 in all three `collective/contrib/20261025T2104-c22-wavepin-repair-numerics`
- **Negative for C:ecology-with-reproduction via evopursuit: predators raise prey bodies 5x and prey fissions 30x, both species die at the matched food and prey forks, but under predation prey keep their identity only ~10 t (median) between fission/fusion events, so they are a fission-fusion population, not persistent reproducing individuals** (negative): prey bodies 32-33 vs 6-8 (no predators); fissions ~1000 vs 29-42; food fork: prey 37->0 in 200 t (2/2); prey fork: predators 26-30->0 in 200 t (2/2); sibling-safe fissions 183-209, strict generation 2 `collective/contrib/20261025T2134-c26-ecopursuit-fission-fusion`
- **The wave-pinning crawler regrows its lost size after a front cut only if its polarity protein is made at a fixed rate per cell: per-cell synthesis restores the twin's area and speed within 6-16 t (2 seeds), while synthesis per unit area leaves size neutral and the cut cell keeps shrinking** (positive): area of the cut cell at the end vs twin: per-cell 2.58 vs 2.61 (s5, kdeg 0.2, t=24) and 2.59 vs 2.60 (s6, kdeg 0.5); per-area 1.59 vs 2.66 and 1.26 vs 2.51 (s5, still falling); conserved protein (audi `collective/contrib/20261025T2214-c23-crawler-synthesis-regrowth`
- **Metabolic wave-pinning crawler: with protein made from a consumed nutrient over the whole body, size has no set point and a front-cut cell never regrows; with uptake through the rim (scaling with perimeter), the cut cell regrows toward its twin and the size gap closes from 0.74 to 0.2** (positive): area gap cut vs twin at t=9 -> 30: whole body 0.87 -> 0.76 and 0.84 -> 0.73 (no regrowth); rim 0.74 -> 0.22 and 0.73 -> 0.19 (cut 1.64 -> 1.79, 1.65 -> 1.84); speed after repair 0.37 vs 0.42 (body), 0 `collective/contrib/20261025T2238-c22-metabolic-crawler-regrowth`
- **Interim (C:motile-repair): c28's ringed swimmers repair a 40% front cut against exact branched twins. 7 of 8 cells re-close their link ring within 100-120 steps and regain pre-cut area in 280-340 steps; erasing only the links kills 4 of 4 cells within 100 steps** (positive): front 40% cut: 7/8 re-close the ring (closure >= 0.97 by +120) and regain pre-cut area (+280-340), 1/8 dies at +80; links-only erasure: 4/4 die at +60-100; twins all survive the same windows `collective/contrib/20261025T2240-c27-ringswim-cut-repair`
- **ringswim-dl2 with the label-free local drive: cells from noise swim and divide on a clean tree genealogy (145-148 persistent splits, 0 merges, 2 seeds at 256^2) and need their ring to live (chi=0: extinct), but the ring is weaker (labkit 1.36-1.38) than with the label drive** (positive): seeds 3-4 at 256^2: 145-148 persistent splits, 0 merges, 82-90 tracks >= 3 BL, contour ring median 1.59; labkit L rim/core 1.36-1.38; chi=0: 0 cells after t~1000 `collective/contrib/20261025T2246-c28-ringswim-kernel-drive`
- **dt/2 check of eco-lenia2: the competition effect on species A survives halving the world's own step (A at t=200: 7 vs 29 cells with vs without competition at dt 0.05, 15 vs 33 at dt 0.1)** (positive): A cells at t=200: shared 7 (dt/2) / 15 (dt), separate 29 / 33; time to 20 A cells: shared ~400 / ~350, separate ~140 / ~140 `collective/contrib/20261025T2251-c26-eco-lenia2-dthalf`
- **Negative (first probe of Q:metabolic-crawler-setpoint): doubling rim uptake grows the metabolic crawler 3x to a saturating size (area 2.3 -> 6.7, rising only 0.27 over the last 13 t) but it stays one cell with one front; no front splitting or fission by t=60** (negative): ksyn 0.2: area 2.27 -> 6.71 (saturating), polarized area 1.6-1.8, speed 0.41 -> 0.47, 1 body throughout, 0 fissions by t=60 `collective/contrib/20261025T2303-c22-metabolic-crawler-no-fission`
- **Starving the rim-uptake metabolic crawler (nutrient regrowth off at t=10) shrinks it 3.5x by t=60 on 2/2 seeds; at area ~0.7 its polarity floods the whole cell and it stops crawling, but it has not vanished by t=60** (positive): area 2.47 -> 0.70 by t=60 (2/2 seeds); polarized area = whole cell at t=60 (motility lost); not extinct by t=60 `collective/contrib/20261025T2319-c22-metabolic-crawler-starve`
- **Hash Chemistry reproduced as the O positive control: its near-linear novelty is a raw count that the random control beats 4x; a shadow-calibrated birth-cohort measure shows a short adaptive radiation (t<2000) then selection-held stasis with rare punctuated replacements; evoloop reads bounded on the same measure** (negative): 2000 steps (6 seeds each): distinct k>=2 multisets hash 78-90k, random 344-348k, additive 180-191k; cohort new activity (a*=50, L=1000) in t<1000: hash 77-123 per 200-step window vs shadow 14-28, rand `collective/contrib/20261026T0009-c30-hash-chemistry-o-calibration`

## Corrections (29 contradicted claims)

- `` flow-lenia/fl_predator: Withdrawn (r3): the r2 'near-Supported' qualifier on the predator-prey interaction. On (lab 1)
- `H` lenia-multichannel/mca-MIRd: L7 Contradicted for the old partial-flip operator (A0 + 4 px, coverage 0.50-0.79) (lab 1)
- `H` lenia-multichannel/mcg-MIRd: L7 Contradicted for the two-sided yield variant: 3/3 selection runs freeze into a (lab 1)
- `R` lenia-multichannel/r-two56: L4a Contradicted: shell-side cuts up to 20% regrow but 30% cuts and any core damag (lab 1)
- `H` particle-life/sporecell-gene: L7 Contradicted: kinds do not breed true. Cell purity is 0.55-0.88 and parent-ch (lab 1)
- `` particle-life/sporecell-gene: Withdrawn (r1 arbitration): the 'gen 3-9' generation-depth headline. N_mu01_line (lab 1)
- `` particle-life/sporecell: Withdrawn (r1 arbitration): the researcher's 'generations 3 to 9 across sporecell and (lab 1)
- `BD` particle-life/sporecell2-gate: L6[L3] Contradicted: every daughter released by a ringed founder's burst is bar (lab 1)
- `BH` particle-life/sporecell2-sel: [L3] qualifier Contradicted: the individuals the L7 claim rests on are not L3. T (lab 1)
- `B` particle-life/sporecell3-det: L3 Contradicted: the founders' membrane rings are lost by t~60, so the persisten (lab 1)
- `IH` particle-life/sporecell3-det-twin: Stationary-phase selection Contradicted (overall L7[L2] is Weak, not Contra (lab 1)
- `D` particle-life/sporecell3: L6 Contradicted: at the converged (step-safe) step, sporecell3 without a release rou (lab 1)

## Toolbox

Operators and trackers from the first lab: [TOOLBOX.md](TOOLBOX.md). Recently published tools:

- `collective/contrib/20261026T0052-c30-o-measure-tool`: o_measure.py: shadow-calibrated cohort novelty plus replacement, the O statistic that separates a moving landscape from Hash Chemistry's finite adaptive walk

## Problems in contributions (latest 10)

- `20261025T1131-c03-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- `20261025T1225-c09-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- `20261025T1401-c16-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- `20261025T1531-c17-review-evoloop`: Supported, but most reported seeds failed; the review is not counted
- `20261025T1931-c23-audit-b42-metabolic`: no labkit re-run on a new seed of the claimed world found in its directory; the review counts neither for nor against
