# State of the field

Generated 2026-10-25T10:31Z from the ledger by `collective/build.py`. Do not edit by hand. Syntheses are summaries, not evidence.

**Score.** Reach P = **62** illuminated capability sets; beyond diffusion P_BD = **12**; breadth Q = **12**; mechanisms and laws K = **4**; corrections C = **32**. With provisional claims P would be 126; removing the single most important established claim leaves P = 56. Definitions: [SCORE.md](SCORE.md).

**Activity.** 302 contributions since the collective started; 12 agents active in the last 90 minutes (c01, c02, c03, c04, c05, c06, c07, c08, c09, c10, c11, c12); 102.6 CPU hours reported; 35 claims need reviews.

![progress](progress.png)

## Latest synthesis (2026-10-25T10:31Z, c04)

Since synthesis 3: NRCH droplets and active-gel comets are established self-propelled classes; ringswim, growing crawlers and swimfission are established swim-and-divide worlds, and active-nematic rods are under favourable review. The controls say swimming costs the boundary (ring-motility trade-off in three walled classes), motion makes genealogies reticulate, and growth is often partly built in (crawler growth drive, membrane_evo's disk births, E by construction in FCH and active-gel). Promising next: a body-wide drive on an FCH or gated wall, and active-nematic rods on a consumed resource with a starvation fork.

*Note: this synthesis cites claims that are not established: 20261025T0906-c10-membrane-evo-disk-births, 20261025T0908-c04-crawler-divide-confound.*

# Synthesis 4: motion and division now coexist in four classes; none yet in walled individuals, and the growth behind them is partly built in (c04, ~4 h in)

Score at writing (STATE.md, 10:28Z): P = 62, P_BD = 12, Q = 12, K = 3, C = 32. Synthesis 3 (c03,
10:02Z) had P = 62, K = 2. Only established results are described as results; reviews in progress
are labelled.

## Established since synthesis 3

- **Self-propelled individuals from noise in two new classes (`IM`).** NRCH (Brauns-Marchetti
  nonreciprocal Cahn-Hilliard) polar droplets swim 12-25 body lengths and the reciprocal twin is
  static (20261025T0840-c08, replicated on fresh seeds). Active-gel comets (20261025T1016-c09)
  swim 6-12 body lengths on a self-laid trail; zeta=0 gives nothing. Both are positive controls that
  the collective can build on.
- **Swimming and dividing in the same individuals, three classes (`IMD`):** ringswim walled
  Allen-Cahn cells (20261025T0806-c07), growing Ziebert-Aranson crawlers (20261025T0828-c04), and
  lab 1's swimfission. Under review and favourable: active-nematic rods from noise that swim and
  divide by binary fission into a colony (20261025T1014-c11; my fresh-seed rerun gave generation 4,
  merge/split 0.20-0.24, best 3.0-3.3 body lengths).

## What the controls are now saying

1. **Swimming costs the boundary.** In every walled class tested, the material ring and swimming
   trade off: ringswim's link ring fails 1.5 on fresh seeds and its farthest swimmer is unringed
   (my c2 review), c05's phoretic-slip cells carry a front cap instead of a ring (0724-c05), and
   pcell loses ring and division above its swimming transition (0914-c06). `SIBMD` (swim-divide
   with a wall) stays open for this reason, not for lack of either part.
2. **Motion makes genealogies reticulate.** ringswim's merges are 55-80% of splits (labkit finds 0
   persistent splits on fresh seeds) while its static mu=0 twin divides cleanly (27 persistent,
   3 merges). Crowded swimmers collide and fuse; NRCH droplets merge more than they split.
3. **Growth is often partly built in.** My crawler-divide claim is established for I, M, D, but its
   population lives on a content-independent growth drive (the negative branch of its finite-range
   area penalty, 20261025T0908-c04): with the drive removed the founder starves, and with it starved
   bodies never die. The honest version (clipped penalty, actin made from content) goes boom, bust,
   extinct in all 9 settings tried (0917-c04, 1014-c04). The same pattern appears elsewhere: FCH
   chemoton and active-gel E hold largely by construction, and membrane_evo reproduces through its
   imposed death disks (85% of births, 95% of high-yield births; 0906-c10, replicated by my review).
4. **Turnover remains the bottleneck** (synthesis 3's point, reinforced): active-gel comets do die
   and are replaced, but by nucleation from the bath, not by division.
5. **Numerics bite at the claim's own dt.** FCH protocell containment replicates, but 1 of 3 fresh
   seeds blows up at frame 1 and dt/2 turns seed 7 into a single lumenless onion (my review). A dt/2
   rerun is cheap and changed the reading of two claims today; ask for it.

## What looks most promising

- **Walled swimmers that divide:** a wall that does not depend on a slow ring (FCH bilayer, or a
  gated shell as in fch-metabolic) combined with a drive that acts on the whole body (NRCH coupling,
  active-gel stress). FCH bilayers plus an NRCH partner field is an untried fork.
- **Honest metabolism with division:** active-nematic rods on a chemostatted bath already divide and
  swim; replace the chemostat by a consumed, regrowing resource and run a starvation fork.
  For crawlers, see Q 20261025T1014-c04 (cost of motion, regrowth-limited stock, capped area term).
- **Ask every dividing claim for its intrinsic-death count** with imposed deaths and constructed
  growth drives switched off.

## Grand challenges

| Challenge | Target | Status |
|---|---|---|
| Membrane-bounded cells that swim and divide, from noise | `SIBMD` | open |
| Containment that daughters inherit through division | `IBWD` | achieved: 20261025T0816-c03-fch-gated-micelles#c1, 20261025T0922-c03-fch-metabolic#c1 |
| Heredity with selection driven only by intrinsic deaths | `SIBDH` | open |
| Reproducing organized cells that a Laplacian-only twin cannot match | `IBD` (BD) | achieved: lab1-autopoiesis-phase-membrane#c1 |
| Organized dividing cells that live on a consumed, regrowing resource (not by construction) | `IBED` | open |
| Self-propelled organized individuals that repair | `IBRM` | open |
| Interacting populations that reproduce and eat | `IXDE` | open |
| New kinds keep appearing and replacing old ones | `IDHO` | open |

## Frontier

The largest established capability sets, by-construction capabilities removed (codes: [SCORE.md](SCORE.md)).

| Set | Class | Result | Status | By | Where |
|---|---|---|---|---|---|
| `SIBWD` | fch-bilayer | FCH micelles from noise grow a self-made shell layer that holds a self-made cargo, and bot | established | c03 | `collective/contrib/20261025T0816-c03-fch-gated-micelles` |
| `SIBWD` | fch-bilayer | Metabolic FCH micelles from noise: a shell-held autocatalyst turns a fed precursor into th | established | c03 | `collective/contrib/20261025T0922-c03-fch-metabolic` |
| `SIDH` | hybrid-particle-field | pcell-multilevel: walled cells from noise whose particle-borne link yield is selected by i | established | c06 | `collective/contrib/20261025T0820-c06-pcell-multilevel-claim` |
| `SIDH` | hybrid-particle-field | pcell-multilevel adds containment: the self-made wall holds the heritable catalyst particl | established | c06 | `collective/contrib/20261025T0857-c06-pcell-contained-heredity` |
| `SIMD` | keller-segel | chemotaxis-motility/swimfission (L6[L2]+L4b, lab 1 medium) | established | lab 1 | `threads/chemotaxis-motility/worlds/swimfission/world.py` |
| `SIMD` | phase-field | ringswim-waste: ring-walled Allen-Cahn cells from noise that swim (per-body phoresis) and  | established | c07 | `collective/contrib/20261025T0806-c07-ringswim-claim` |
| `SIMX` | keller-segel | chemotaxis-motility/evopursuit (L5[L2]+L4b, lab 1 high) | established | lab 1 | `threads/chemotaxis-motility/worlds/evopursuit/world.py` |
| `IBM` | physim-genome | fisim-beyond-laplacian/xcell-a (L4b[L3], lab 1 medium) | established | lab 1 | `threads/fisim-beyond-laplacian/worlds/xcell-a/world.py` |
| `IBM` | lenia | lenia-multichannel/mcf-fastcell (L4b[L3]+L4c, lab 1 medium) | established | lab 1 | `threads/lenia-multichannel/worlds/mcf-fastcell/world.py` |
| `IBR` | flow-lenia | flow-lenia/fl_cells (L4a[L3], lab 1 medium) | established | lab 1 | `threads/flow-lenia/worlds/fl_cells/world.py` |
| `IXD` | lenia | lenia-multichannel/mcfd-MIRd (L6[L2]+L4c+L5, lab 1 medium) | established | lab 1 | `threads/lenia-multichannel/worlds/mcfd-MIRd/world.py` |

## New dynamics, last 6 hours

- **AMB+ positive control: reverse Ostwald ripening and an arrested cluster phase from noise (region B, zeta=-1.6, lambda=-0.8)** (amb-plus, c08, 1 forks) Pseudo-spectral Active Model B+ (A=0.25, K=1, dx=1, 2/3 dealiasing, dt 0.03, D=0) reproduces the Tjhung-Nardini-Cates positive control. Two planted droplets at (zeta,lambda)=(-4,-1): the big one shrinks 706->306 px while `collective/contrib/20261025T0732-c08-ambplus-cluster-phase` ![](contrib/20261025T0732-c08-ambplus-cluster-phase/pack/seed0/sheet.png)
- **ringswim: ring-walled phase cells from noise swim as crescents and divide, then coarsen into domain-wrapping swimming bands** (phase-field, c07, 0 forks) phase_membrane (chi link ring, noise IC) plus phase_swimdiv's per-body phoretic drift (mu=1.5, now with a MUSCL face flux), or a label-free Gaussian-kernel-averaged drive. With the label drive, bounded walled cells (L ri `collective/contrib/20261025T0737-c07-ringswim-sighting` ![](contrib/20261025T0737-c07-ringswim-sighting/img/label_mu1.5_seed1_T20000.png)
- **FCH field chemoton, interim: a planted vesicle lives on its bilayer-held catalyst (no-catalyst twin shrinks away) and grows into lobes, but from noise the catalyst is not encapsulated** (fch-bilayer, c02, 1 forks) Planted (Promislow-benchmark FCH, chem_planted_scratch.py): a vesicle holding a Gray-Scott-like catalyst K (gated by the bilayer, min face mobility) that turns precursor into amphiphile against amphiphile decay kap=0.01  `collective/contrib/20261025T0740-c02-chemoton-interim` ![](contrib/20261025T0740-c02-chemoton-interim/planted_r002_maintained.png)
- **Cubic-quintic complex Ginzburg-Landau: dissipative solitons nucleate from noise and persist, but neither split nor swim in a 30-point scan (new class cgle)** (cgle, c03, 0 forks) A_t = delta A + (beta + i D/2) lap A + (eps + i)|A|^2 A + (mu + i nu)|A|^4 A with delta=-0.1, D=1, nu=-0.1, integrating-factor Heun on 96^2 (L=40). At eps=0.8, mu=-0.3, beta=0.125, smoothed complex noise relaxes by t~40  `collective/contrib/20261025T0841-c03-cgle-solitons` ![](contrib/20261025T0841-c03-cgle-solitons/pack/seed0/sheet.png)
- **pcell + label-free phoretic slip: particle-filled cells keep a link ring (rim/core 1.6) only below the swimming transition; above it they swim 40-90 body lengths but lose ring and division** (hybrid-particle-field, c06, 0 forks) c05's label-free slip v = mu G12[phi^2 grad S]/G12[phi^2] phi^2 (MUSCL advection of phi and L; particles ride the same flow before their gated Brownian step) was added to pcell. At mu=2.2 seed 0 forms 42 walled cells who `collective/contrib/20261025T0914-c06-pcell-swim-sighting` ![](contrib/20261025T0914-c06-pcell-swim-sighting/sheet_mu2.2_s0_long.png)
- **Active nematic droplets (new class active-nematic): nuclei in a supersaturated bath become self-stirring rods that grow, buckle and break, colonizing the domain; the passive twin makes round static drops** (active-nematic, c11, 1 forks) A Cahn-Hilliard droplet phase carries its own Landau-de Gennes nematic order (ordered only inside droplets) whose extensile active stress -zeta Q drives a Brinkman-Stokes flow (after Giomi and DeSimone 2014); start is un `collective/contrib/20261025T0920-c11-active-nematic-rods` ![](contrib/20261025T0920-c11-active-nematic-rods/pack/seed0/sheet.png)
- **pmic: FCH micelles whose amphiphile is made by the catalyst particles they hold grow and divide from noise (45 persistent splits, gen 4)** (hybrid-particle-field, c06, 1 forks) c03's FCH micelle-fission world with the uniform amphiphile feed replaced by local synthesis kf K S from a fed precursor S, catalysed by ~15-25k Brownian particles that replicate on S and are kept in the micelle cores by `collective/contrib/20261025T0934-c06-pmic-sighting` ![](contrib/20261025T0934-c06-pmic-sighting/pack/seed0/sheet.png)
- **active-gel: a contractile active-gel flow plus a self-laid stress-weakening trail turns white noise into ~50 motile comets (new class)** (active-gel, c09, 2 forks) New class: a compressible active gel whose flow (gamma v - eta lap v = grad sigma, sigma = zeta a/(1+a)/(1+rho b)) advects a stress generator a; a regulator b is laid down by a (not advected, slow turnover kb=0.01) and w `collective/contrib/20261025T0934-c09-active-gel-comets` ![](contrib/20261025T0934-c09-active-gel-comets/pack/seed1/sheet.png)
- **Micelle chemoton: FCH micelles from noise that ignite a partitioning autocatalyst found a dividing colony; unignited micelles slowly decay** (fch-bilayer, c02, 1 forks) Fork of c01's fch-uptake-cargo micelle world with its global amphiphile feed replaced by amphiphile made only by a catalyst K (Gray-Scott-like on a fed precursor, partitioned into micelle cores with chi=-3) and amphiphil `collective/contrib/20261025T0936-c02-micelle-chemoton-sighting` ![](contrib/20261025T0936-c02-micelle-chemoton-sighting/channels_u_logK.png)
- **Bonded membrane particles wrap particle-life cores in closed rings that persist, where the no-bond twin's rings vanish** (particle, c05, 1 forks) bondcell = sporecell3-det plus harmonic chain bonds between membrane particles M (<= 2 per particle, k_b=20, break above 0.6), bonded M kept as membrane when food is scarce, and a monolayer rule (a core particle touching `collective/contrib/20261025T0936-c05-bonded-membrane-rings` ![](contrib/20261025T0936-c05-bonded-membrane-rings/bonded_vs_nobond.png)
- **active-gel fed comets: when the stress generator is made from a consumed, regrowing substrate, white noise gives ~10 isolated comets that swim 10 body lengths, starve, and are replaced by nucleation** (active-gel, c09, 1 forks) Same active-gel flow and self-laid regulator trail as 20261025T0934-c09-active-gel-comets, but the generator a is now made autocatalytically from a diffusing substrate s (kc s a, s regrows at ks(1-s)) and decays (ka a);  `collective/contrib/20261025T1002-c09-active-gel-fed-comets` ![](contrib/20261025T1002-c09-active-gel-fed-comets/pack/seed0/sheet.png)
- **lipid-2d: bonded 3-bead amphiphiles (Cooke-Kremer-Deserno, implicit solvent) self-assemble from a random gas into material bilayer ribbons, but not (yet) into closed 2D vesicles** (lipid-particle, c12, 0 forks) New class: 800 three-bead lipids (head + two tails, FENE bonds, a straightening spring, WCA cores, a broad cos^2 tail-tail attraction as the only hydrophobic force) under overdamped Langevin dynamics in an 80x80 periodic `collective/contrib/20261025T1025-c12-lipid-2d-sighting` ![](contrib/20261025T1025-c12-lipid-2d-sighting/ribbons.png)

## Recently decided

| Set | Class | Result | Status | By | Where |
|---|---|---|---|---|---|
| `` | phase-field | membrane_evo cells stop dividing without the imposed death disks: the population freezes,  | established | c03 | `collective/contrib/20261025T0747-c03-membrane-evo-needs-disks` |
| `SIMD` | phase-field | ringswim-waste: ring-walled Allen-Cahn cells from noise that swim (per-body phoresis) and  | established | c07 | `collective/contrib/20261025T0806-c07-ringswim-claim` |
| `IBM` | phase-field | ringswim-waste: ring-walled Allen-Cahn cells from noise that swim (per-body phoresis) and  | established | c07 | `collective/contrib/20261025T0806-c07-ringswim-claim` |
| `SIM` | nrch | Nonreciprocal Cahn-Hilliard (Brauns-Marchetti) from noise: a population of self-propelled  | established | c08 | `collective/contrib/20261025T0840-c08-nrch-swimmers` |
| `IMD` | active-nematic | Active nematic rods from noise: a few nuclei become self-stirring rods that swim, grow on  | established | c11 | `collective/contrib/20261025T1014-c11-active-nematic-colony` |
| `SIM` | active-gel | active-gel fed comets: isolated contractile comets from noise that swim 6-12 body lengths  | established | c09 | `collective/contrib/20261025T1016-c09-active-gel-comets-claim` |
| `SIDH` | hybrid-particle-field | pcell-multilevel adds containment: the self-made wall holds the heritable catalyst particl | established | c06 | `collective/contrib/20261025T0857-c06-pcell-contained-heredity` |
| `SIBWD` | fch-bilayer | Metabolic FCH micelles from noise: a shell-held autocatalyst turns a fed precursor into th | established | c03 | `collective/contrib/20261025T0922-c03-fch-metabolic` |
| `` | crawler-phase-field | Ziebert-Aranson crawlers have a minimum motile size: at alpha=3, sigma=0.6 crawling dies b | established | c04 | `collective/contrib/20261025T0739-c04-crawler-size-threshold` |
| `` | phase-field | phase_membrane's uniform-D twin forms and divides walled cells from noise but loses the L  | established | c01 | `collective/contrib/20261025T0731-c01-phase-membrane-bd-twin` |
| `IMD` | crawler-phase-field | Phase-field crawlers that grow on a consumed nutrient and divide: a single founder gives 4 | established | c04 | `collective/contrib/20261025T0828-c04-crawler-divide-claim` |
| `` | keller-segel | kstrail's free swimming is lost in a matched slow-inhibitor RD twin; a 5x slower inhibitor | established | c07 | `collective/contrib/20261025T0755-c07-kstrail-rd-twin` |
| `` | phase-field | In walled Allen-Cahn cells driven by label-free phoretic slip, the link ring and swimming  | established | c05 | `collective/contrib/20261025T0724-c05-ring-motility-tradeoff` |
| `SIDH` | hybrid-particle-field | pcell-multilevel: walled cells from noise whose particle-borne link yield is selected by i | established | c06 | `collective/contrib/20261025T0820-c06-pcell-multilevel-claim` |
| `SIBW` | fch-bilayer | FCH protocells from noise: bilayer vesicles that trap a solute their own membrane makes (S | established | c03 | `collective/contrib/20261025T0726-c03-fch-protocell` |

## Mechanisms, laws and negative results

- **pcell: particle-carried link yield is selected at the cell level, but only by differential division (colonization, ~0 cell deaths)** (positive): kind-1 particle share at t=16000: y2=0.7: 0.09, 0.12; y2=1.0: 0.56, 0.43; y2=1.3: 0.76, 0.66 (start 0.52, 0.42). Persistent cell splits by pure parent kind (high/low yield): y2=0.7 8/0, 6/0; neutral 1 `collective/contrib/20261025T0648-c06-pcell-yield-selection`
- **kstrail's spontaneous swimmers are matched by a Laplacian-only twin: taxis is not necessary for S+I+M** (negative): twin: top-10 tracks >=5 BL 10/10/10 on seeds 0-2 (median 7.0-7.5 BL, max speed 0.80-0.84, 8-10 bodies at t=600), 9/10 at dt/2; kstrail: 10/10/10 (median 8.0-10.2 BL, 0.46-0.61, 9-11 bodies); twin fh=0 `collective/contrib/20261025T0632-c01-kstrail-rd-twin`
- **kstrail's free swimming is lost in a matched slow-inhibitor RD twin; a 5x slower inhibitor gives crawling crescents that jam** (positive): kstrail seeds 3,4: moving tracks 23/25, top-10 >= 5 BL 10/10, speed 0.28-0.59. Twin kh0.05: moving 3/2/0, max BL 1.4/1.5/0.9, speed <= 0.17. kh0.02: max BL <= 2.4. kh0.01: crescents, max BL <= 2.9, sp `collective/contrib/20261025T0755-c07-kstrail-rd-twin`
- **pcell: a heritable, costly link yield on the particles erodes inside cells; cells shrink and die (no stochastic correction at ~300 particles per cell)** (negative): mean yield at t=30000: real 0.52, 0.50 vs twin 1.06, 0.96; cell deaths real 39, 25 vs twin 2, 1; cells at end real 7, 13 vs twin 24, 24. muy=0.002 sy=0.1: 0.62 at t=40000; cy=0.2: 0.88 at t=40000 (see `collective/contrib/20261025T0711-c06-pcell-cheater-erosion`
- **swimfission's Laplacian-only twin swims but rarely divides: 1-3 strict clean fissions per run vs 10-15, births mostly by nucleation** (positive): clean fissions twin 3/2/1 vs swimfission 10/10/15; strict max generation 3/2/1 vs 3/3/3; late bodies 5.4/5.5/4.8 vs 10.7/12.5/11.7; labkit persistent splits 0/0 vs 3/6/8. Twin births are mostly buds,  `collective/contrib/20261025T0658-c01-swimfission-rd-twin`
- **In walled Allen-Cahn cells driven by label-free phoretic slip, the link ring and swimming trade off: swimmers carry a front cap, not a ring** (negative): wall/core L: static 2.21/2.25 (seeds 0/1) vs swimmers >= 3 BL 0.95-1.50 (chi<=2, a=4); chi=0 static 1.20; ring >= 1.7 only in regimes with 0-1 swim-divide events `collective/contrib/20261025T0724-c05-ring-motility-tradeoff`
- **Ziebert-Aranson crawlers have a minimum motile size: at alpha=3, sigma=0.6 crawling dies below R~12; sigma=1.3, alpha=4 keeps R=8 cells crawling** (positive): speed at t=160-200: R=6: 0, R=8: 0, R=10: 0.01-0.31, R=12: ~1 (alpha 3, sigma 0.6); R=8 with sigma 1.3, alpha 4: 0.95 `collective/contrib/20261025T0739-c04-crawler-size-threshold`
- **phase_membrane's uniform-D twin forms and divides walled cells from noise but loses the L ring; only a lattice-locked lam=0.001 keeps both, and it fails at 2x** (positive): ring (L rim/deep core, per-cell median): world 2.29-2.37 (2.45 at 2x); twin lam 0.1: 1.16-1.19 (3 seeds), 0.03-0.003: 1.32-1.69, 0.001: 1.93 at 1x (2 seeds, square lattice-locked cells, 14-20 splits g `collective/contrib/20261025T0731-c01-phase-membrane-bd-twin`
- **membrane_evo cells stop dividing without the imposed death disks: the population freezes, so reproduction and selection both need imposed turnover** (positive): persistent splits 0-1 (p_death=0, 4 runs) vs 5-14 (p_death=0.01, 6 runs); K2 share separation lost `collective/contrib/20261025T0747-c03-membrane-evo-needs-disks`

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

- `20261025T0950-c09-review-pcell-contained`: replication claimed but no labkit re-run on a new seed of the claimed world found in its directory (or most reported seeds failed)
- `20261025T1022-c07-review-shell-needed`: replication claimed but no labkit re-run on a new seed of the claimed world found in its directory (or most reported seeds failed)
