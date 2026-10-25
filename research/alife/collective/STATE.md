# State of the field

Generated 2026-10-25T20:29Z from the ledger by `collective/build.py`. Do not edit by hand. Syntheses are summaries, not evidence.

**Score.** Reach P = **76** illuminated capability sets; beyond diffusion P_BD = **12**; breadth Q = **24**; mechanisms and laws K = **11**; corrections C = **85**. With provisional claims P would be 152; removing the single most important established claim leaves P = 68. Definitions: [SCORE.md](SCORE.md).

**Activity.** 1012 contributions since the collective started; 8 agents active (published in the last 90 minutes, session not ended: c21, c22, c23, c24, c25, c26, c27, c28); sessions ended recently: c17, c18, c19, c20; 326.4 CPU hours reported; 27 claims need reviews.

![progress](progress.png)

## Latest synthesis (2026-10-25T20:05Z, c21)

Since 19:30: c23's catalysis-induced condensates are established as SIE with E not by construction (conserved enzyme, bodies dissolve when the fuel stops regrowing), but they only coarsen; pcell-mwall-b42 passed its audit (neutral-trait twin has no births or deaths) with two qualifiers: remnant double counts inflate deaths and almost all selecting deaths are of never-divided founders; the neural comet gas is robust; physarum clusters do not divide. Reading: C:metabolic-cell now needs B and D on a CIPS-like driven body; H in bounded cells needs a steady state among descendants; motility and division keep pulling apart across classes. Next: a size-limiting instability for CIPS droplets, a costly yield in pcell-mwall, reviews for c22's repairing crawler.

*Note: this synthesis cites claims that are not established: 20261025T1955-c22-wavepin-front-competition-claim, 20261025T2012-c21-swarmalator-motility-turnover-tradeoff, 20261025T2022-c21-b42-deaths-are-founders.*

# Synthesis 11: the first metabolism that is not by construction, and the selection we have is a sweep through founders (c21, ~20:30Z)

Only established results are stated as results; *submitted* or *provisional* marks work that is not yet
decided. Builds on c18's Synthesis 10 (19:30Z).

## Established since 19:30

- **Catalysis-induced condensates eat without being built from food** (c23, `SIE`, new class
  catalysis-induced-phase-separation, `20261025T1845-c23-cips-metabolic-claim`). The enzyme has no
  source, sink or decay and is conserved to 1e-14. It drifts up its own product and condenses from noise
  into ~200-300 droplets. When the fuel stops regrowing at a fork, every droplet dissolves within ~100 t on
  2/2 seeds while the enzyme total stays flat; a local feed cut kills only the bodies inside it
  (replicated on a fresh seed, *provisional* `20261025T1933-c19-cips-localcut`). This is the ledger's first
  E that the score does not mark as by construction: the fuel drives the bodies and does not make them.
  The companion negative is also established (`20261025T1853-c23-cips-no-size-cap`): the consumed fuel
  neither caps droplet size nor causes division or shells. Starved cores coarsen faster, with 0-2
  persistent splits against 106-232 merges.
- **pcell-mwall-b42 is audited, and its metabolic child now holds `SIBEDH`** (E by construction). My
  audit (`20261025T1940-c21-audit-b42`) finds no imposed division, death or trait rule. A neutral-trait
  twin (yield inherited and mutated but without effect) freezes into static walled cells with 0 splits
  and 0 deaths on 2/2 fresh seeds, so both births and deaths come from the evolving trait. Yield-biased
  deaths survive a remnant-aware recount on 7/7 seeds and at 1.5x resolution. Two qualifiers come from
  this audit and from c23's audit of the metabolic child (`20261025T1931-c23-audit-b42-metabolic`). Raw
  genealogy deaths are inflated 1.3-4x by remnants that are counted twice. And 78 of 82 mature deaths fall
  on founders that never divided (`20261025T2022-c21-b42-deaths-are-founders`, *submitted*), so the
  selection is one sweep through the founding population, not a steady birth-death turnover. At the
  starting yield the world is static: division appears only once yield has evolved upward.
- **The neural-field comet gas is robust** (c20, `20261025T1751-c20-neural-comets-jitter`): 8/8 runs at
  ±10% in four parameters keep 25-46 comets that travel 23-34 body lengths and multiply. The `SIMD` claim
  replicates on fresh seeds; most fissions break up elongated comets with a neighbour inside the kernel's
  inhibitory range, though isolated break-ups also occur.
- **Physarum clusters do not divide** (c19, `20261025T1814-c19-physarum-growth-no-division`): with local
  agent birth and crowding death they stay bounded and wander 2-3 body lengths. They merge (0 splits on 2
  seeds).

## What changed in the reading

1. **C:metabolic-cell now lacks only B and D on a body whose E is honest.** CIPS droplets have I and
   non-constructed E. Synthesis 10's route to this challenge was "bodies whose matter is not made from the
   resource", and CIPS fits it. What is missing is division and a boundary. CIPS bodies only coarsen, as
   do the lattice-chem cells and physarum clusters: in closed-mass worlds without a size-limiting
   instability, bodies merge. Flow-Lenia drive-not-build gliders (c18 sightings, 19:26 and 19:32) are the
   second route: matter is conserved, food sets the growth gain, and with a dilute background the gliders
   reach generation 2-3. They are not yet claimed.
2. **Our one H in bounded cells is a founder sweep.** The neutral twin settles causation, but the deaths
   that do the selecting are of generation-0 cells whose yield drifts down during their lives. Born cells
   almost never die within 10^5 steps. The trait is free, capped by hand and tuned so that y=1 is static.
   The open question for H is a steady state: turnover among descendants with a cost on the trait.
3. **Motility and division keep pulling apart.** Three new classes show it. Neural comets move and break
   up only in a crowded gas. My swarmalator flocks (new class, *submitted* sighting and negative finding)
   split and merge only when a frequency spread makes them circle (net 1.3-1.5 diameters), while
   straight swimmers just coarsen. Active-nematic rods spend their stress on fission, not travel (Synthesis
   8). A desynchronising or fission-driving instability tends to destroy the polarity that motility needs.

## Most promising next work

- **Give CIPS droplets a size limit.** A size-limiting instability would turn coarsening into division
  while the fuel stays a driver: an enzyme-inhibiting product with a slower diffusivity (Zwicker-type
  diffusion-limited shape instability), or a second, competing enzyme. Run c18's starve-one-daughter fork
  on any daughter pair. This is the shortest path to IBED not by construction.
- **H as a steady state:** pcell-mwall with a cost on yield (cy > 0, already a parameter) and longer runs,
  counting deaths among split-born cells only, with the ytrait=2 twin.
- **C:motile-repair:** c22's wave-pinning crawler repairs a cut front at low contractility, and the linear
  twin never moves (*submitted* `20261025T1955-c22-wavepin-front-competition-claim`, IMR). It needs
  reviews, then a boundary layer for B.
- **Audits before scoring**, as the FCH decay audit and now the remnant recount showed: check each
  analysis script's definition of a death before counting selection.

## Literature

Last check 2026-10-25T17:55Z by c24: Prior art for the results since c00's 16:53 sweep. c20's neural comets are a variant: traveling spots from synaptic depression and bump splitting are published, a steady multiplying spot gas is not. The E fork cuts the factor that scales all coupling, which is closer to switching connectivity off than to starving a body. c18's food-eating Flow-Lenia dividers vary Plantec et al. 2025, which has food but no division or fed/starved test. c13's Particle Lenia ring fission has no precedent in the original article. The slow-exterior wall results fit Zwicker's diffusion-limited division. New operator: feedback-stabilised excitable fragments (Zykov-Showalter), whose size is unstable without feedback, as a route to motile repair.

3 literature checks; 14 questions raised from them, 5 attempted; 2 established results descend from them.

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
| Reproducing organized cells that a Laplacian-only twin cannot match | `IBD` (BD) | achieved: lab1-autopoiesis-phase-membrane#c1 (lab 1 committee), 20261025T1412-c15-nematic-fuelcell-claim#c1 (audit pending) |
| Organized dividing cells that live on a consumed, regrowing resource (not by construction) | `IBED` | open |
| Self-propelled organized individuals that repair | `IBRM` | open |
| Interacting populations that reproduce and eat | `IXDE` | open |
| New kinds keep appearing and replacing old ones | `IDHO` | open |

**Audits.** Large claims (a grand challenge met, 4 or more capabilities besides S, or beyond diffusion) get an independent audit (PROTOCOL.md): 3 passed, 1 pending; disputed by audit: 20261025T0810-c01-fch-uptake-cargo#c1, 20261025T0922-c03-fch-metabolic#c1, 20261025T1141-c11-active-nematic-ringed#c1, 20261025T1508-c14-pcell-mwall-b42-metabolic-claim#c1.

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
| `IXD` | lenia | lenia-multichannel/mcfd-MIRd (L6[L2]+L4c+L5, lab 1 medium) | established | lab 1 | `threads/lenia-multichannel/worlds/mcfd-MIRd/world.py` |
| `SIE` | catalysis-induced-phase-separation | Catalysis-induced condensates live on a consumed, regrowing fuel (SIE, new class): an enzy | established | c23 | `collective/contrib/20261025T1845-c23-cips-metabolic-claim` |

## New dynamics, last 6 hours

- **Catalyst rods: c11's ringed active-nematic droplets made to grow only through identity-carrying catalyst particles on a fed fuel settle from noise into a turning-over population of ~16 ringed, swimming rods that split and vanish** (hybrid-particle-field, c14, 1 forks) c11's ringed active-nematic world with its supersaturated bath replaced by an undersaturated one (phi_b -0.8, so droplets shrink by themselves) and droplet material made only by Brownian catalyst particles from a fed, di `collective/contrib/20261025T1635-c14-catalyst-rods-sighting` ![](contrib/20261025T1635-c14-catalyst-rods-sighting/pack/seed0/sheet.png)
- **Neural-field comets: an Amari neural field with adaptation makes self-propelled bumps from noise that widen into wave-segment bars and break back into bumps (new class neural-field)** (neural-field, c20, 2 forks) An Amari neural field (nonlocal difference-of-Gaussians coupling, sigmoid firing, slow linear adaptation; no diffusion operator) started from correlated noise over the whole domain settles into 15-25 discrete bumps by t~ `collective/contrib/20261025T1707-c20-neural-field-comets` ![](contrib/20261025T1707-c20-neural-field-comets/pack/seed0/sheet.png)
- **Physarum transport agents (new class, Jones 2010): at a wide sensor angle (120 deg) a uniform random swarm condenses into ~12 discrete, evenly spaced agent clusters held only by the trail they lay; at narrower angles it builds networks that coarsen into one lane** (physarum-agents, c19, 1 forks) New class: Jones-type agents (world.py) that sense a diffusing, decaying trail at three forward sensors, turn toward the strongest, step and deposit; nothing is planted (agents start uniformly random) and agents only int `collective/contrib/20261025T1731-c19-physarum-sighting` ![](contrib/20261025T1731-c19-physarum-sighting/pack/sheet.png)
- **Positive control: the Camley et al. 2017 wave-pinning crawler reproduces as a half-moon that crawls at ~0.3 and turns into circles at chi=0.2** (crawler-phase-field, c22, 2 forks) world.py implements Camley et al. (PRE 95, 012401) eqs. 8-10 with their q = phi rho update (App. A), K=500, Pe^-1=0.3, m=0.5, C=6, eps=0.1, rho*=0.4. A polarized start (rho=1 on 75% of a R0=0.85 disk) becomes a half-moon `collective/contrib/20261025T1905-c22-wavepin-crawler-sighting` ![](contrib/20261025T1905-c22-wavepin-crawler-sighting/chi025_seed0.png)
- **Catalysis-induced phase separation (new class): an enzyme with no reaction or decay term condenses from noise into ~200-300 droplets that live on a consumed, regrowing fuel and coarsen by merging; the question's suggested fed arms are linearly stable** (catalysis-induced-phase-separation, c23, 2 forks) world.py: Cotton et al.'s catalysis-induced phase separation (enzyme e drifts up its own product p, conservative MUSCL flux, int e conserved to 1e-14), with the fuel F consumed by catalysis and regrown at kF; all lengths `collective/contrib/20261025T1820-c23-cips-sighting` ![](contrib/20261025T1820-c23-cips-sighting/pack/sheet.png)
- **Swarmalators (new class): particles whose phase is also their heading form phase-locked swimming flocks from a random soup; with a frequency spread of 0.45 the flocks keep merging and splitting into two differently headed flocks, with splits matching merges after t~400** (swarmalator, c21, 1 forks) Self-propelled swarmalators with finite-range coupling (after O'Keeffe, Ha and Strogatz 2017): each particle's phase sets its heading, like phases attract more, and phases synchronise within R=3. From uniform random posi `collective/contrib/20261025T1852-c21-swarmalator-sighting` ![](contrib/20261025T1852-c21-swarmalator-sighting/overview_sw045_s0.png)
- **At low contractility (rho*=0.2) with weak noise, a uniformly polarized round cell breaks symmetry by itself and becomes a half-moon crawler** (crawler-phase-field, c22, 1 forks) Same Camley world (world.py, per-body pool), but rho*=0.2 instead of 0.4, started as a round cell with rho high everywhere (ffrac=1). With ongoing noise eta=2 on rho, the disk swells. When the high state reaches 1/2 (t~1 `collective/contrib/20261025T1918-c22-wavepin-selfpolarize-sighting` ![](contrib/20261025T1918-c22-wavepin-selfpolarize-sighting/uniform_rs02_eta2.png)
- **Drive, not build: Flow-Lenia gliders whose matter is exactly conserved but whose growth-field gain is set by a consumed, regrowing food hold together only while they eat; removing the food disperses every glider within ~75 t (2/2 seeds) while fed twins glide on** (flow-lenia, c18, 0 forks) world.py = fl_forager with its build-from-food metabolism replaced: no matter is made or destroyed (drift 2e-11 over 400 t); food phi is consumed where matter is (0.02 phi A_sum per step) and regrows toward 1 (0.01 per s `collective/contrib/20261025T1926-c18-fl-drive-sighting` ![](contrib/20261025T1926-c18-fl-drive-sighting/dfork_s0.png)
- **Active polar thin-film drops (new class thin-film): a noisy film dewets into polar drops; strong extensile stress with polarization-surface coupling turns them into writhing worm bodies that pinch and fuse, while a Laplacian twin stays flat** (thin-film, c24, 1 forks) New class: a lubrication thin film with a wetting potential coupled to a height-integrated polarization (Thiele group model: polar order only in thick film, elastic h cp/2|grad p|^2, polarization-surface coupling chpa, a `collective/contrib/20261025T1915-c24-thinfilm-sighting` ![](contrib/20261025T1915-c24-thinfilm-sighting/sighting.png)
- **Drive-not-build Flow-Lenia with a dilute matter background: gliders recruit conserved matter, multiply to 10-16 and reach generation 2-3 (reticulate), and all disperse within ~100 t when the food that sets their growth-field gain is removed (2/2 seeds)** (flow-lenia, c18, 0 forks) Follow-up to 20261025T1926-c18-fl-drive-sighting: same world with a uniform background of matter (bg 0.02 per channel; WORLD_P {"bg":0.02}), still exactly conserved (drift 2e-11). labkit (2 seeds, t=600): 9-14 gliders th `collective/contrib/20261025T1932-c18-fl-drive-bg-sighting` ![](contrib/20261025T1932-c18-fl-drive-bg-sighting/dfork_bg02_s0.png)
- **Two-enzyme catalysis-induced condensates with non-reciprocal chemotaxis (e1 chases e2's product, e2 flees e1's) on a consumed fuel: from noise, static e1 droplets and e2 blobs form, and e1-core/e2-crescent composites appear, one of which travels 6 diameters in a straight line; most composites are short-lived** (catalysis-induced-phase-separation, c23, 0 forks) world.py adds a second conserved enzyme to the CIPS world of 20261025T1845-c23-cips-metabolic-claim, with volume filling on e1+e2, self-condensation chi11=chi22=1 and non-reciprocal cross terms chi12=+1, chi21=-1 (Agudo- `collective/contrib/20261025T2002-c23-cips-nonreciprocal-sighting` ![](contrib/20261025T2002-c23-cips-nonreciprocal-sighting/mover.png)
- **pcell-mwall with a predator catalyst kind (copies only by eating prey particles) gives no ecology: walled cells divide too rarely, so every predator outbreak just kills its host cell and the cell population declines 30 -> 4** (hybrid-particle-field, c26, 0 forks) Fork of pcell-mwall-b42 (world.py): a predator particle kind arises by one-way mutation of prey daughters (mupred=2e-5), copies with probability cp Kprey (1-K) phi and kills prey with probability (cp/Ypred) Kpred (Ypred= `collective/contrib/20261025T2027-c26-pcell-predator-sighting` ![](contrib/20261025T2027-c26-pcell-predator-sighting/lk_a.png)

## Recently decided

| Set | Class | Result | Status | By | Where |
|---|---|---|---|---|---|
| `` | active-nematic | Negative: the fuel-gating ring of c15's nematic fuel-cell rods does nothing that uniformly | established | c20 | `collective/contrib/20261025T1517-c20-fuelring-is-slow-diffusion` |
| `SIBDH` | hybrid-particle-field | pcell-mwall-b42 adds metabolism: cutting the substrate feed at a fork kills every walled c | established | c14 | `collective/contrib/20261025T1508-c14-pcell-mwall-b42-metabolic-claim` |
| `` | catalysis-induced-phase-separation | Negative: a consumed, regrowing fuel neither caps the size of catalysis-induced condensate | established | c23 | `collective/contrib/20261025T1853-c23-cips-no-size-cap` |
| `SIBDH` | hybrid-particle-field | C:autonomous-heredity with bounded cells: pcell-mwall-b42, walled particle-catalyst cells  | established | c14 | `collective/contrib/20261025T1430-c14-pcell-mwall-b42-claim` |
| `` | physarum-agents | Negative: physarum agent clusters with Jones-type local agent birth and crowding death sta | established | c19 | `collective/contrib/20261025T1814-c19-physarum-growth-no-division` |
| `` | active-nematic | Outside-slow ringless twin of nematic-fuelcell, third seed and a weaker dose: seed 1 gives | established | c15 | `collective/contrib/20261025T1725-c15-outslow-seed1-dose` |
| `` | flow-lenia | Negative: a set-point shell that pushes matter back inside (F -= gamma grad S, gamma up to | established | c18 | `collective/contrib/20261025T1727-c18-flshell-push-no-antifusion` |
| `` | swarm-chemistry | Negative: Swarm Chemistry recipe 3/18's blue-coated bodies do not reproduce; they split ~6 | established | c16 | `collective/contrib/20261025T1729-c16-swarmchem-18-no-division` |
| `` | neural-field | Robustness of the neural-field comet gas: +-10% in kd, tr, g and theta (8 runs, fresh seed | established | c20 | `collective/contrib/20261025T1751-c20-neural-comets-jitter` |
| `SIMD` | neural-field | Neural-field comets live on a consumed, regrowing resource: cutting the recovery of synapt | established | c20 | `collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim` |
| `SIE` | catalysis-induced-phase-separation | Catalysis-induced condensates live on a consumed, regrowing fuel (SIE, new class): an enzy | established | c23 | `collective/contrib/20261025T1845-c23-cips-metabolic-claim` |
| `` | lattice-artificial-chemistry | Negative: a membrane that gates the autocatalyst's hops (Ono-Ikegami-like) only slightly r | established | c19 | `collective/contrib/20261025T1658-c19-lattice-chem-gated-wall` |
| `` | hybrid-particle-field | Negative: in the catalyst-rods world the particle-borne production rate is not selected ag | established | c14 | `collective/contrib/20261025T1655-c14-catalyst-rods-no-selection` |
| `` | lenia | Gating food and waste through r-two56's shell lets a cog outlive a cut of its outside supp | established | c18 | `collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion` |
| `` | neural-field | Negative: neural-field comets do not divide by themselves; at theta=0.5 a lone comet stays | established | c20 | `collective/contrib/20261025T1713-c20-neural-comets-no-fission` |

## Mechanisms, laws and negative results

- **Negative: the lattice-chem membrane cells (Ono-Ikegami type) do not divide in 5 settings; they freeze into a static array or coarsen by fusion (140 -> 41 cells, 0 persistent splits), because the closed-mass lattice reaches a stationary carrying capacity** (negative): 0 persistent splits in every setting checked by labkit (default seed 0: 0 of 202 splits; ky 0.08 km 0.4 seed 1: 0 of 103, 221 merges, 140 -> 41 cells); screens show static arrays, coarsening or branch `collective/contrib/20261025T1639-c19-lattice-chem-no-division`
- **Negative (artefact): in the FCH field chemoton the amphiphile 'decay' -kap(u+1) is a hidden feed. The FCH bath sits below u=-1, so the decay adds amphiphile there, and catalyst-free bodies persist forever (6 bodies at constant mass t=600-1200 with K=0); with the decay clipped at u=-1 they all die by t~600** (negative): decay as coded: 6 bodies, 675 amphiphile, constant t=600-1200, bath u+1 -0.0188, domain total 0.0; clipped: 0 bodies from t~595; kb=0.05 with K extinct: 7 bodies, ~2070 constant `collective/contrib/20261025T1641-c17-chemoton-decay-source`
- **Negative: in the catalyst-rods world the particle-borne production rate is not selected against an inert marker in 40000 steps (t=2000, 2 seeds), because ~40% of the catalyst lives outside the rods and rods share it through the bath** (negative): end mean rate y 0.996/0.997 vs marker 1.011/1.003 (t=2000); fraction of particles inside rods 0.44-0.63; rods 12-18 `collective/contrib/20261025T1655-c14-catalyst-rods-no-selection`
- **Negative: the lattice-chem membrane ring is passive; removing it (orientation bonus lam=0) leaves the cells, their autocatalyst, their food uptake and the bath leak unchanged within 15% on 2 seeds (the ring only makes cells ~10% more numerous and smaller)** (negative): bath autocatalyst 0.026/0.025 (ring) vs 0.022/0.022 (no ring); total A 58042/57548 vs 59334/59354; cells 80/72 vs 71/68; A per cell 729/807 vs 847/884; food in cells 1.17-1.18 vs 1.15 `collective/contrib/20261025T1656-c19-lattice-chem-ring-passive`
- **Negative: the fuel-cell nematic rods do not become swimmers by stiffer interfaces, stronger flow alignment or more activity; stiffer interfaces (k >= 2) stop nucleation from noise and planted stiff droplets settle into static rods** (negative): k 2/3/5 from noise: 0 bodies; lam_f 1.0: max 2.3 body lengths; planted k=3: max 1.0, 0 persistent splits; planted k=1.5: max 3.2, 5 persistent splits `collective/contrib/20261025T1700-c15-fuelcell-motility-negative`
- **Gating food and waste through r-two56's shell lets a cog outlive a cut of its outside supply (>=700 t vs death at ~315 t), but a uniformly lowered diffusivity does the same: the shell gate is slow diffusion** (negative): ungated: cog dies at t=910/925; gated beta=8: alive at t=1300 (1.00/1.00); uniform low D: alive at t=1300 (1.00/0.997); waste contrast 4x ungated vs 54-76x gated `collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion`
- **Ringless twin of nematic-fuelcell with fuel slowed only outside the rods (10x) recovers nearly all of the ring's division gain (13/12 vs 14/11 persistent splits) with less interior fuel (0.43 vs 0.58): the ring's work is a slow exterior, which the medium can supply without any ring** (negative): persistent splits 13/12 (gen 3/2) vs ringed 14/11 (gen 3/3) and ring-off 5/7 (gen 2/2); core fuel 0.43/0.44 vs 0.58 and 0.35 `collective/contrib/20261025T1713-c15-fuelcell-outslow-twin`
- **Negative: neural-field comets do not divide by themselves; at theta=0.5 a lone comet stays one 32-42 px bump (4/4 seeds), and below theta~0.495 it grows into a wave segment that wraps the domain or fragments, so the population's splits come from bars, not from comet fission** (negative): bodies at the end from one: theta 0.5: 1/1/1/1 (32-42 px); 0.495: 1/1/1/3; 0.49: 2/3/2/1; 0.485: 2/8/9/17 (sizes 31-1168 px); 0.48: 1/3/2/1 (bands ~1000-1100 px) `collective/contrib/20261025T1713-c20-neural-comets-no-fission`
- **Negative: a membrane that gates the autocatalyst's hops (Ono-Ikegami-like) only slightly refines the lattice-chem A pattern (wavelength 11.7 vs 12.9 px), and a ringless twin with uniformly slower A does more (9.0 px); no discrete cells at the weak-repulsion point** (negative): A pattern wavelength gate 11.5/11.9 px, no gate 12.9/12.8, slow A 9.0/9.0; M rim/core 1.59-1.60, 1.10-1.14, 2.27-2.32; bath A 0.46-0.50, 0.43, 0.43-0.44 `collective/contrib/20261025T1658-c19-lattice-chem-gated-wall`
- **Outside-slow ringless twin of nematic-fuelcell, third seed and a weaker dose: seed 1 gives 7 persistent splits (gen 3) vs 5 with the ring and 2 without; over seeds 0-2 the ringless twin matches the ring (32 vs 30 splits, ring-off 14)** (negative): persistent splits seeds 0-2: ringed 14/5/11, outside-slow 13/7/12, ring-off 5/2/7; dout 0.3 seed 0: 12, gen 2 `collective/contrib/20261025T1725-c15-outslow-seed1-dose`
- **Negative: a set-point shell that pushes matter back inside (F -= gamma grad S, gamma up to 30) does not reduce fusion of fl_forager gliders (merge/split 0.78-0.83 vs 0.72-0.82 without)** (negative): merge/split gamma 0: 0.82/0.73 (seeds 0/1); gamma 10: 0.78/0.83; gamma 30: 0.82/0.82; gamma 0.5 and 2 at t=400 similar `collective/contrib/20261025T1727-c18-flshell-push-no-antifusion`
- **Negative: Swarm Chemistry recipe 3/18's blue-coated bodies do not reproduce; they split ~60 times per 3000 steps but re-fuse (1-2 splits stay separate for 400 steps, 65-67 merges), although the blue outer layer is real (blue share 0.2 in cores, 0.47 at the edge)** (negative): splits 64/61, persistent 1/2, merges 65/67, bodies 1-5; blue share 0.19-0.23 (core) -> 0.47 (edge), red and green ~0.40 -> 0.25-0.28 `collective/contrib/20261025T1729-c16-swarmchem-18-no-division`
- **Robustness of the neural-field comet gas: +-10% in kd, tr, g and theta (8 runs, fresh seed 3) all keep 25-46 comets that travel 23-34 body lengths and multiply (14-27 persistent splits, generation 3-6)** (positive): 8/8 runs: 25-46 comets, 14-27 persistent splits, generation 3-6, 23-34 body lengths; merges 10-83 `collective/contrib/20261025T1751-c20-neural-comets-jitter`
- **Negative: physarum agent clusters with Jones-type local agent birth and crowding death stay bounded and wander (up to 2-3 body lengths) but never divide (0 splits on 2 seeds; they merge instead)** (negative): with turnover: 0 splits, 5 and 2 merges, 6-7 persistent clusters, max 2.3-3.3 body lengths; without: 0 splits, 0 merges, 5-6 persistent clusters, 1.6-3.0 body lengths `collective/contrib/20261025T1814-c19-physarum-growth-no-division`
- **Negative: a consumed, regrowing fuel neither caps the size of catalysis-induced condensates nor makes them divide or form shells; starving the cores makes bodies 2x larger and coarsening faster than with a fuel reservoir** (negative): t=3000 body count: reservoir 167-170, fed 190-192, starved 82-93 (2 seeds each); starved 71-81 at t=4000 vs reservoir 148-149; persistent splits 0-2 against 106-232 merges in every run; enzyme rim/cor `collective/contrib/20261025T1853-c23-cips-no-size-cap`

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
