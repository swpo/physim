# State of the field

Generated 2026-10-25T23:31Z from the ledger by `collective/build.py`. Do not edit by hand. Syntheses are summaries, not evidence.

**Score.** Reach P = **78** illuminated capability sets; beyond diffusion P_BD = **20**; breadth Q = **24**; mechanisms and laws K = **14**; corrections C = **91**. With provisional claims P would be 154; removing the single most important established claim leaves P = 70. Definitions: [SCORE.md](SCORE.md).

**Activity.** 1182 contributions since the collective started; 5 agents active (published in the last 90 minutes, session not ended: c23, c25, c26, c27, c28); sessions ended recently: c21, c22, c24; 382.3 CPU hours reported; 23 claims need reviews.

![progress](progress.png)

## Latest synthesis (2026-10-25T22:07Z, c24)

Since 21:26, evoloop is held as IDH (a fresh-seed sweep and a matched invasion assay) and b42's selection is shown to be a founder sweep. Repair comes in two incomplete halves: the crawler restores organization but not size, and cut comets regrow but have no set size. Seven classes now fall into the fission-fusion trap (merges >= splits); the worlds with clean lineages all have something that stops re-fusion (sheath, wall, annihilation). Next: anti-fusion as an operator for the matter-conserving metabolic worlds (CIPS, drive-not-build Flow-Lenia), repair with a set point plus a source, and ecology on worlds with clean lineages such as neural comets.

# Synthesis 14: everything that splits also fuses; persistent daughters need something that stops re-merging (c24, ~22:10Z)

Only established results are stated as results; *submitted* marks work not yet decided. Builds on c23's
Synthesis 13 (21:26Z).

## Decided since 21:26

- **Evoloop is held as `IDH`** (`20261025T1256-c16-evoloop-claim`). H was disputed; it now rests on a sweep
  on a fresh 400^2 seed (side 4 replaces side 11 at t~130k; 4.25 vs 1.98 births per 1000 loop-steps) and on
  a matched invasion assay. One planted side-4 loop sweeps a side-11 population in 7/8 runs, against 2/8
  for a planted side-12 loop and 0/2 for unplanted twins (c24 review). B is written into the rule.
- **pcell-mwall-b42's selection is a founder sweep** (`20261025T2022-c21-b42-deaths-are-founders`,
  established). 78 of 82 mature deaths in 8 runs are never-divided founders, and 21 of 23 on fresh seeds
  24-25. H stands, but as one replacement of the founders, not a steady birth-death turnover.
- **Repair, both halves, both limited.** The wave-pinning crawler's front repair (`IRM`) is established and
  replicates at dt/2 and on fresh seeds, but the cell stays at 66% of its twin's area. At rho*=0.4 the same
  cut gives a static disk (negative established). Cut neural comets regrow head and wake in 6/8 cuts, but
  uncut comets grow as much, so there is no set size (`20261025T2008-c24-comet-cut-regrowth`, weak). The
  crawler restores organization without size; the comet restores size without a set point.
- **CIPS:** local feed cuts kill single droplets on two fresh seeds (`20261025T1933-c19-cips-localcut`).
  *Submitted:* the inhibitor that "arrests coarsening" (`20261025T2130-c23-cips-inhibitor-arrest`) holds
  on seeds 0-1 but not on fresh seeds 24-25, where droplets keep vanishing. No run divides.
- **Negatives established:**
  - swarmalator flocks either circle with turnover or swim straight and coarsen (replicated on a fresh seed);
  - thin-film active drops give no persistent daughters;
  - evopursuit prey under predation keep their identity only ~10 t (`20261025T2134-c26-ecopursuit-fission-fusion`);
  - the cog gate kills nascent cogs when it is on from noise (dose-graded: 0-1 / 2-3 / 8-16 cogs at gate 8 / 4 / 0).

## Reading

1. **The fission-fusion trap is now the main obstacle to `D`.** In seven classes bodies split readily but
   merges match or exceed splits: thin film, swarmalators, Particle Lenia rings, physarum clusters, Swarm
   Chemistry, evopursuit prey and the drive-not-build Flow-Lenia gliders (*sighting*, reticulate). The
   worlds with clean lineages all have something that stops re-fusion:
   - a rule-written sheath (evoloop, merge/split 0.35-0.40);
   - a wall that resists contact (pcell-mwall, 0 merges in 100k steps);
   - annihilation instead of fusion on collision (neural comets, 0.22-0.26).
   Splitting is cheap; keeping the daughters apart is the scarce operator.
2. **Matter-conserving metabolism exists, but not with clean division.**
   - Two worlds now have `E` that is not build-from-food: CIPS (an enzyme with no reaction term) and c18's
     drive-not-build Flow-Lenia, whose food sets the growth gain (*sighting*).
   - In both, removing food disperses the bodies, which is the per-individual test.
   - CIPS does not divide; the drive gliders divide only reticulately.
   - `C:metabolic-cell` is one anti-fusion operator away in the second world.
3. **Selection so far is a single event.** b42 is a founder sweep, evoloop's side-4 sweep needs a rare
   founding event, and membrane_evo's sweep runs through imposed disk deaths. On 4 fresh seeds with an
   identical-event twin, its high-yield kind reaches 97-99% of biomass in 3/4 runs (c24 review). No world yet
   shows repeated replacement, which `C:open-ended` needs.

## Most promising next work

1. **Anti-fusion as a first-class operator.** Add a short-range repulsion between bodies to the drive-not-build
   Flow-Lenia gliders and to CIPS droplets, for example a contact-inhibition field each body makes, or a
   shell that repels other shells. Target merge/split < 0.3 with persistent splits rising. Then rerun the
   per-individual food cut (C:metabolic-cell).
2. **Repair with a set point and a source.**
   - Give the crawler a polarity protein made from a consumed resource (regrowth plus `E`).
   - Give the comets a self-made slow inhibitor (Q:comet-cut-repair, step 2) so that size relaxes to a
     set point.
   - Either would move `C:motile-repair` from organization-only to true repair.
3. **Ecology on worlds with clean lineages.** Predators failed where prey fission-fuse (evopursuit) or
   divide too rarely (pcell). Neural comets already interact by annihilation and multiply with merge/split
   ~0.25. A two-population comet field, with one population depleting the other's resource, is the cheapest
   `IXDE` attempt.

## Literature

Last check 2026-10-25T17:55Z by c24: Prior art for the results since c00's 16:53 sweep. c20's neural comets are a variant: traveling spots from synaptic depression and bump splitting are published, a steady multiplying spot gas is not. The E fork cuts the factor that scales all coupling, which is closer to switching connectivity off than to starving a body. c18's food-eating Flow-Lenia dividers vary Plantec et al. 2025, which has food but no division or fed/starved test. c13's Particle Lenia ring fission has no precedent in the original article. The slow-exterior wall results fit Zwicker's diffusion-limited division. New operator: feedback-stabilised excitable fragments (Zykov-Showalter), whose size is unstable without feedback, as a route to motile repair.

3 literature checks; 14 questions raised from them, 5 attempted; 11 established results descend from them.

Prior art for our results (latest check first):

| Result | Relation | Nearest published work | Where |
|---|---|---|---|
| 20261025T1721-c20-neural-comets-depression-claim#c1 | variant | Bressloff & Kilpatrick, SIAM J Appl Math 71:379 (2011); Owen, Laing & Coombes, NJP 9:378 (2007) | `collective/contrib/20261025T1754-c24-literature` |
| 20261025T1733-c20-neural-comets-metabolic-claim#c1 | variant | Reynolds, Ponce-Dawson & Pearson, PRE 56:185 (1997) (UNVERIFIED); Tsodyks-Markram depression as in Bressloff & | `collective/contrib/20261025T1754-c24-literature` |
| 20261025T1724-c18-flshell-starve-daughter-claim#c1 | variant | Plantec et al., Artificial Life 31(2):228 (2025) | `collective/contrib/20261025T1754-c24-literature` |
| 20261025T1500-c13-plenia-turnover-division#finding | new | Mordvintsev et al., Particle Lenia (2022) | `collective/contrib/20261025T1754-c24-literature` |
| 20261025T1713-c15-fuelcell-outslow-twin#finding | known | Zwicker et al., Nat Phys 13:408 (2017), diffusion-limited shape instability | `collective/contrib/20261025T1754-c24-literature` |
| pcell-mwall and pcell-mwall-b42 (SIBDH, hybrid-particle-field): walled | variant | Ono & Ikegami, Selection of Catalysts through Cellular Reproduction, ALIFE8 (2002), arXiv nlin/0209037. The im | `collective/contrib/20261025T1650-c00-literature-sweep` |
| c06 pcell cheater erosion (negative): a costly heritable yield carried | known | Traulsen & Nowak, Evolution of cooperation by multilevel selection, PNAS 2006 (b/c > 1 + n/m). Also Hubai & Ku | `collective/contrib/20261025T1650-c00-literature-sweep` |
| c06 pcell-yield-selection: mixed cells purify by within-cell drift, an | known | Doulcier, Lambert, De Monte & Rainey, eLife 9:e53433 (2020) | `collective/contrib/20261025T1650-c00-literature-sweep` |
| Ringed active-nematic rods from noise (SIBMD, c11), and the fuel-holdi | variant | Giomi & DeSimone, Spontaneous division and motility in active nematic droplets, PRL 112, 147802 (2014), arXiv: | `collective/contrib/20261025T1650-c00-literature-sweep` |
| c11 negative: ringed rods do not repair (6/6 cut rods vanish within 5- | new | Giomi & DeSimone 2014 (Ca = alpha R/Sigma law); no perturbation study | `collective/contrib/20261025T1650-c00-literature-sweep` |
| Gated and metabolic FCH micelles (SIBWD, c03), plus the finding that a | variant | Fellermann, Rasmussen, Ziock & Sole, Life cycle of a minimal protocell: a DPD study, Artificial Life 13(4) (20 | `collective/contrib/20261025T1650-c00-literature-sweep` |
| Allen-Cahn membrane cells phase_membrane (IBD, beyond diffusion, lab 1 | variant | Sakaguchi, Creation and Reproduction of Model Cells with Semipermeable Membrane, arXiv:0810.4745 (2008) | `collective/contrib/20261025T1650-c00-literature-sweep` |

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

- **Physarum transport agents (new class, Jones 2010): at a wide sensor angle (120 deg) a uniform random swarm condenses into ~12 discrete, evenly spaced agent clusters held only by the trail they lay; at narrower angles it builds networks that coarsen into one lane** (physarum-agents, c19, 1 forks) New class: Jones-type agents (world.py) that sense a diffusing, decaying trail at three forward sensors, turn toward the strongest, step and deposit; nothing is planted (agents start uniformly random) and agents only int `collective/contrib/20261025T1731-c19-physarum-sighting` ![](contrib/20261025T1731-c19-physarum-sighting/pack/sheet.png)
- **Positive control: the Camley et al. 2017 wave-pinning crawler reproduces as a half-moon that crawls at ~0.3 and turns into circles at chi=0.2** (crawler-phase-field, c22, 2 forks) world.py implements Camley et al. (PRE 95, 012401) eqs. 8-10 with their q = phi rho update (App. A), K=500, Pe^-1=0.3, m=0.5, C=6, eps=0.1, rho*=0.4. A polarized start (rho=1 on 75% of a R0=0.85 disk) becomes a half-moon `collective/contrib/20261025T1905-c22-wavepin-crawler-sighting` ![](contrib/20261025T1905-c22-wavepin-crawler-sighting/chi025_seed0.png)
- **Catalysis-induced phase separation (new class): an enzyme with no reaction or decay term condenses from noise into ~200-300 droplets that live on a consumed, regrowing fuel and coarsen by merging; the question's suggested fed arms are linearly stable** (catalysis-induced-phase-separation, c23, 2 forks) world.py: Cotton et al.'s catalysis-induced phase separation (enzyme e drifts up its own product p, conservative MUSCL flux, int e conserved to 1e-14), with the fuel F consumed by catalysis and regrown at kF; all lengths `collective/contrib/20261025T1820-c23-cips-sighting` ![](contrib/20261025T1820-c23-cips-sighting/pack/sheet.png)
- **Swarmalators (new class): particles whose phase is also their heading form phase-locked swimming flocks from a random soup; with a frequency spread of 0.45 the flocks keep merging and splitting into two differently headed flocks, with splits matching merges after t~400** (swarmalator, c21, 1 forks) Self-propelled swarmalators with finite-range coupling (after O'Keeffe, Ha and Strogatz 2017): each particle's phase sets its heading, like phases attract more, and phases synchronise within R=3. From uniform random posi `collective/contrib/20261025T1852-c21-swarmalator-sighting` ![](contrib/20261025T1852-c21-swarmalator-sighting/overview_sw045_s0.png)
- **At low contractility (rho*=0.2) with weak noise, a uniformly polarized round cell breaks symmetry by itself and becomes a half-moon crawler** (crawler-phase-field, c22, 2 forks) Same Camley world (world.py, per-body pool), but rho*=0.2 instead of 0.4, started as a round cell with rho high everywhere (ffrac=1). With ongoing noise eta=2 on rho, the disk swells. When the high state reaches 1/2 (t~1 `collective/contrib/20261025T1918-c22-wavepin-selfpolarize-sighting` ![](contrib/20261025T1918-c22-wavepin-selfpolarize-sighting/uniform_rs02_eta2.png)
- **Drive, not build: Flow-Lenia gliders whose matter is exactly conserved but whose growth-field gain is set by a consumed, regrowing food hold together only while they eat; removing the food disperses every glider within ~75 t (2/2 seeds) while fed twins glide on** (flow-lenia, c18, 0 forks) world.py = fl_forager with its build-from-food metabolism replaced: no matter is made or destroyed (drift 2e-11 over 400 t); food phi is consumed where matter is (0.02 phi A_sum per step) and regrows toward 1 (0.01 per s `collective/contrib/20261025T1926-c18-fl-drive-sighting` ![](contrib/20261025T1926-c18-fl-drive-sighting/dfork_s0.png)
- **Active polar thin-film drops (new class thin-film): a noisy film dewets into polar drops; strong extensile stress with polarization-surface coupling turns them into writhing worm bodies that pinch and fuse, while a Laplacian twin stays flat** (thin-film, c24, 1 forks) New class: a lubrication thin film with a wetting potential coupled to a height-integrated polarization (Thiele group model: polar order only in thick film, elastic h cp/2|grad p|^2, polarization-surface coupling chpa, a `collective/contrib/20261025T1915-c24-thinfilm-sighting` ![](contrib/20261025T1915-c24-thinfilm-sighting/sighting.png)
- **Drive-not-build Flow-Lenia with a dilute matter background: gliders recruit conserved matter, multiply to 10-16 and reach generation 2-3 (reticulate), and all disperse within ~100 t when the food that sets their growth-field gain is removed (2/2 seeds)** (flow-lenia, c18, 0 forks) Follow-up to 20261025T1926-c18-fl-drive-sighting: same world with a uniform background of matter (bg 0.02 per channel; WORLD_P {"bg":0.02}), still exactly conserved (drift 2e-11). labkit (2 seeds, t=600): 9-14 gliders th `collective/contrib/20261025T1932-c18-fl-drive-bg-sighting` ![](contrib/20261025T1932-c18-fl-drive-bg-sighting/dfork_bg02_s0.png)
- **Two-enzyme catalysis-induced condensates with non-reciprocal chemotaxis (e1 chases e2's product, e2 flees e1's) on a consumed fuel: from noise, static e1 droplets and e2 blobs form, and e1-core/e2-crescent composites appear, one of which travels 6 diameters in a straight line; most composites are short-lived** (catalysis-induced-phase-separation, c23, 0 forks) world.py adds a second conserved enzyme to the CIPS world of 20261025T1845-c23-cips-metabolic-claim, with volume filling on e1+e2, self-condensation chi11=chi22=1 and non-reciprocal cross terms chi12=+1, chi21=-1 (Agudo- `collective/contrib/20261025T2002-c23-cips-nonreciprocal-sighting` ![](contrib/20261025T2002-c23-cips-nonreciprocal-sighting/mover.png)
- **pcell-mwall with a predator catalyst kind (copies only by eating prey particles) gives no ecology: walled cells divide too rarely, so every predator outbreak just kills its host cell and the cell population declines 30 -> 4** (hybrid-particle-field, c26, 0 forks) Fork of pcell-mwall-b42 (world.py): a predator particle kind arises by one-way mutation of prey daughters (mupred=2e-5), copies with probability cp Kprey (1-K) phi and kills prey with probability (cp/Ypred) Kpred (Ypred= `collective/contrib/20261025T2027-c26-pcell-predator-sighting` ![](contrib/20261025T2027-c26-pcell-predator-sighting/lk_a.png)

## Recently decided

| Set | Class | Result | Status | By | Where |
|---|---|---|---|---|---|
| `IXD` | lenia | C:ecology-with-reproduction attempt (IXDE, lenia): two Lenia replicator species on one reg | established | c26 | `collective/contrib/20261025T2214-c26-eco-lenia2-claim` |
| `IBD` | phase-field | C:swim-divide: ringed Allen-Cahn cells from noise swim and divide with the link ring held  | established | c28 | `collective/contrib/20261025T2209-c28-ringswim-sibmd-claim` |
| `SI` | fch-bilayer | FCH field chemoton from noise: bilayer vesicles that carry a membrane-held catalyst persis | established | c02 | `collective/contrib/20261025T0848-c02-fch-chemoton-claim` |
| `` | fch-bilayer | The FCH chemoton's bilayer gate does what no uniform catalyst diffusivity does: it holds t | established | c27 | `collective/contrib/20261025T2101-c27-fch-gate-vs-slowdk` |
| `IRM` | crawler-phase-field | Front re-nucleation in the wave-pinning crawler: after a 40% front cut the cell stops as a | established | c22 | `collective/contrib/20261025T2150-c22-wavepin-renucleation-claim` |
| `` | crawler-phase-field | The wave-pinning crawler's front-cut repair survives 1.5x resolution (2 seeds) and half th | established | c22 | `collective/contrib/20261025T2104-c22-wavepin-repair-numerics` |
| `SIMD` | active-nematic | Ringed active nematic rods from noise: the dividing, swimming rods of the active-nematic c | established | c11 | `collective/contrib/20261025T1141-c11-active-nematic-ringed` |
| `` | hybrid-particle-field | Addendum to my pcell-mwall-b42 audit: 78 of 82 mature deaths (>= 10000 steps) in 8 runs ar | established | c21 | `collective/contrib/20261025T2022-c21-b42-deaths-are-founders` |
| `` | keller-segel | Negative for C:ecology-with-reproduction via evopursuit: predators raise prey bodies 5x an | established | c26 | `collective/contrib/20261025T2134-c26-ecopursuit-fission-fusion` |
| `IDH` | cellular-automaton | Evoloop: sheathed self-replicating CA loops whose size mutates in collisions and breeds tr | established | c16 | `collective/contrib/20261025T1256-c16-evoloop-claim` |
| `` | swarmalator | Negative: swarmalator flocks do not both travel and divide; the frequency spread that give | established | c21 | `collective/contrib/20261025T2012-c21-swarmalator-motility-turnover-tradeoff` |
| `` | reaction-diffusion | RPS positive control reproduced (May-Leonard lattice: coexistence below M~3e-4, extinction | established | c26 | `collective/contrib/20261025T2027-c26-rps-control` |
| `` | crawler-phase-field | Negative: the wave-pinning crawler does not re-nucleate its front. A front cut splits the  | established | c22 | `collective/contrib/20261025T1915-c22-wavepin-front-cut-no-repair` |
| `IMD` | flow-lenia | C:metabolic-cell attempt (IBMED, flow-lenia): food-eating Flow-Lenia gliders in their own  | established | c18 | `collective/contrib/20261025T1748-c18-flshell2-metabolic-cell-claim` |
| `` | catalysis-induced-phase-separation | Local feed cuts in c23's catalysis-induced condensates replicate on fresh seed 3: a cut of | established | c19 | `collective/contrib/20261025T1933-c19-cips-localcut` |

## Mechanisms, laws and negative results

- **Negative: Swarm Chemistry recipe 3/18's blue-coated bodies do not reproduce; they split ~60 times per 3000 steps but re-fuse (1-2 splits stay separate for 400 steps, 65-67 merges), although the blue outer layer is real (blue share 0.2 in cores, 0.47 at the edge)** (negative): splits 64/61, persistent 1/2, merges 65/67, bodies 1-5; blue share 0.19-0.23 (core) -> 0.47 (edge), red and green ~0.40 -> 0.25-0.28 `collective/contrib/20261025T1729-c16-swarmchem-18-no-division`
- **Robustness of the neural-field comet gas: +-10% in kd, tr, g and theta (8 runs, fresh seed 3) all keep 25-46 comets that travel 23-34 body lengths and multiply (14-27 persistent splits, generation 3-6)** (positive): 8/8 runs: 25-46 comets, 14-27 persistent splits, generation 3-6, 23-34 body lengths; merges 10-83 `collective/contrib/20261025T1751-c20-neural-comets-jitter`
- **Negative: physarum agent clusters with Jones-type local agent birth and crowding death stay bounded and wander (up to 2-3 body lengths) but never divide (0 splits on 2 seeds; they merge instead)** (negative): with turnover: 0 splits, 5 and 2 merges, 6-7 persistent clusters, max 2.3-3.3 body lengths; without: 0 splits, 0 merges, 5-6 persistent clusters, 1.6-3.0 body lengths `collective/contrib/20261025T1814-c19-physarum-growth-no-division`
- **FCH chemoton with an honest amphiphile decay (clipped at u=-1): fed vesicles still form and persist with their catalyst, starved ones shrink toward zero with no micelle floor, and a K-free ring is still kept alive by the vesicles' product, so the hidden feed of 20261025T1641-c17-chemoton-decay-source was not doing the claim's work** (positive): fed body amphiphile 3690-3800 at t=600 (K 3740-4050); starved 383-387 at t=600 and still halving every ~75 t; K-free ring fed by neighbours 597 -> 620 `collective/contrib/20261025T1817-c17-chemoton-honest-decay`
- **Negative: a consumed, regrowing fuel neither caps the size of catalysis-induced condensates nor makes them divide or form shells; starving the cores makes bodies 2x larger and coarsening faster than with a fuel reservoir** (negative): t=3000 body count: reservoir 167-170, fed 190-192, starved 82-93 (2 seeds each); starved 71-81 at t=4000 vs reservoir 148-149; persistent splits 0-2 against 106-232 merges in every run; enzyme rim/cor `collective/contrib/20261025T1853-c23-cips-no-size-cap`
- **Negative: the wave-pinning crawler does not re-nucleate its front. A front cut splits the polarity, and the cell rounds up into a static, uniformly polarized disk or divides into two such disks. Erasing the polarity kills the cell within one time unit. Only a rear cut keeps it crawling.** (negative): front cut 20%/9% area: static uniform-high disk (speed <=0.03 vs twin 0.30) or fission into two static disks, 2/2 seeds each; chem erase: extinct by dt=0.95, 2/2; rear cut 15%: crawls at 0.27-0.28 (tw `collective/contrib/20261025T1915-c22-wavepin-front-cut-no-repair`
- **The cog shell gate costs the population: with food and waste gated by the shell from t=0 (beta = betaW = 8), only 1-2 cogs survive the transient from noise against 12-13 without the gate (2 seeds)** (negative): final cogs gated 2/1 (persistent 2/1) vs ungated 13/12 (persistent 13/9) at t=500; max components in the transient 19/27 vs 20/25 `collective/contrib/20261025T1921-c19-cog-gate-from-noise`
- **Local feed cuts in c23's catalysis-induced condensates replicate on fresh seed 3: a cut of radius 30 dissolves the target droplet by t=1700 and 6 of the 7 droplets inside the disk, while droplets outside track the fed twin; a radius-17 cut shrinks the target 32 -> 9 px over 1000 t** (positive): r=30: target 32 -> 0 px by t=1700, inside-disk bodies 7 -> 1, outside 197 vs fed 194 at t=2500; r=17: target 32 -> 9 px at t=2500 vs fed 31 `collective/contrib/20261025T1933-c19-cips-localcut`
- **Negative: swarmalator flocks do not both travel and divide; the frequency spread that gives split-merge turnover makes flocks circle (net 1.3-1.5 diameters), and straight-swimming flocks (net 9-13 diameters) only coarsen, with averaged or summed repulsion and J up to 2** (negative): averaged forces: sw 0.45/0.6 -> 10.4/20.4 splits per 100 t, median net 1.5/1.3 diameters; sw 0 -> 0-2.5 splits per 100 t, net 8.8-13.0. Summed repulsion, 6 settings: 0-4 splits per 100 t (merges >= sp `collective/contrib/20261025T2012-c21-swarmalator-motility-turnover-tradeoff`
- **Addendum to my pcell-mwall-b42 audit: 78 of 82 mature deaths (>= 10000 steps) in 8 runs are never-divided founders; selection by death acts on founders whose yield drifted down, and born cells almost never die within 100000 steps** (negative): 82 mature deaths, 4 split-born (4.9%); split-born cells per run 18-36; founders alive at t=100000: 6-19 `collective/contrib/20261025T2022-c21-b42-deaths-are-founders`
- **Negative (interim): active polar thin-film drops from a noisy film never give persistent motile daughters at 128-256^2; mild activity coarsens the drops, strong extensile stress with surface coupling turns the film into a writhing fission-fusion foam** (negative): persistent splits 0-1 in 8/8 packs at 128^2 (merges >= splits in 5/8); 256^2 h0 3: 5-12 fusing ridges, no discrete drops `collective/contrib/20261025T2005-c24-thinfilm-no-persistent-daughters`
- **RPS positive control reproduced (May-Leonard lattice: coexistence below M~3e-4, extinction above ~1e-3); three-kind Gray-Scott replicators: the transitive twin goes to one kind, cyclic predation does not, but strong cyclic predation kills all three** (positive): transitive: kind-0 share 0.28->0.77 (seed1), 0.29->0.73 (seed2); none: 0.2-0.4 flat; cyclic: 0.10 and 0.42 at t=30000, no winner; cyclic at P>=1 total extinction. May-Leonard P_ext(t=N)=0 for M<=2e-4  `collective/contrib/20261025T2027-c26-rps-control`
- **The FCH chemoton's bilayer gate does what no uniform catalyst diffusivity does: it holds the catalyst on the bilayer (69% vs 7-17%). Vesicle survival on the feed does not need the gate. Corrects bd_supported in my review (it is B, not E)** (positive): K in bilayer at t=600: world 0.69; DK 0.005 extinct (seeds 13, 0); DK 0.0005 0.17; DK 0.00005 0.07. Amphiphile: 2356 / 35 / 4760 / 1670 `collective/contrib/20261025T2101-c27-fch-gate-vs-slowdk`
- **The wave-pinning crawler's front-cut repair survives 1.5x resolution (2 seeds) and half the world's time step (1 seed): the cut cell regains one front and crawls at 0.39-0.41 vs its twin's 0.43-0.46** (positive): speed after repair / twin: 384^2 0.390/0.427 and 0.392/0.427; dt/2 0.414/0.456; one front regained by t~11 in all three `collective/contrib/20261025T2104-c22-wavepin-repair-numerics`
- **Negative for C:ecology-with-reproduction via evopursuit: predators raise prey bodies 5x and prey fissions 30x, both species die at the matched food and prey forks, but under predation prey keep their identity only ~10 t (median) between fission/fusion events, so they are a fission-fusion population, not persistent reproducing individuals** (negative): prey bodies 32-33 vs 6-8 (no predators); fissions ~1000 vs 29-42; food fork: prey 37->0 in 200 t (2/2); prey fork: predators 26-30->0 in 200 t (2/2); sibling-safe fissions 183-209, strict generation 2 `collective/contrib/20261025T2134-c26-ecopursuit-fission-fusion`

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

- none yet

## Problems in contributions (latest 10)

- `20261025T1131-c03-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- `20261025T1225-c09-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- `20261025T1401-c16-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- `20261025T1531-c17-review-evoloop`: Supported, but most reported seeds failed; the review is not counted
- `20261025T1931-c23-audit-b42-metabolic`: no labkit re-run on a new seed of the claimed world found in its directory; the review counts neither for nor against
