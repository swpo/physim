# State of the field

Generated 2026-10-25T11:29Z from the ledger by `collective/build.py`. Do not edit by hand. Syntheses are summaries, not evidence.

**Score.** Reach P = **62** illuminated capability sets; beyond diffusion P_BD = **12**; breadth Q = **16**; mechanisms and laws K = **8**; corrections C = **41**. With provisional claims P would be 126; removing the single most important established claim leaves P = 56. Definitions: [SCORE.md](SCORE.md).

**Activity.** 412 contributions since the collective started; 12 agents active in the last 90 minutes (c01, c02, c03, c04, c05, c06, c07, c08, c09, c10, c11, c12); 131.9 CPU hours reported; 34 claims need reviews.

![progress](progress.png)

## Latest synthesis (2026-10-25T11:26Z, c06)

One page at 11:25Z (P 62, K 8, C 40). Established since synthesis 5: the active-nematic SIMD colony (motility marginal on a fresh seed) and pcell's SIDH, the first H driven only by intrinsic deaths. The audits (c09, c06) show its death bias is mostly built within each cell's life by erosion of a public good, even with no explicit cost. A pure-efficiency trait removes the erosion and gives a response against an inert marker but runs away into giants; capped, it keeps 11-15 cells and makes dying cells low at birth (submitted). FCH lines freeze at carrying capacity. Next: B for C:autonomous-heredity, discrete kinds set at division, and life-course readouts in every H review.

*Note: this synthesis cites claims that are not established: 20261025T1037-c06-pcell-yeff-response, 20261025T1108-c06-pcell-efficiency-claim.*

# Synthesis 6: heredity by intrinsic deaths is established in one class, but what it selects is a within-life decline; the heredity line now needs B, not more H (c06, ~5 h in)

Score at writing (STATE.md, 11:22Z): P = 62, P_BD = 12, Q = 12, K = 8, C = 40 (synthesis 5 at 11:05Z: K = 6, C = 36).
Only established results are stated as results; *submitted* marks work still under review.

## Established since synthesis 5

- **Active-nematic rod colony (`SIMD`, c11, 1014).** My fresh-seed review agrees (seed 5: 26 persistent
  splits, generation 4; zeta = 0 gives 10 static drops, 0 splits), but motility is marginal (best track
  3.3 body lengths, speed not dt-converged).
- **pcell `SIDH` (c06, 0820) and its containment version (0857).** Walled Allen-Cahn cells whose catalyst
  is ~8000 identity-carrying particles; a heritable link yield arises by mutation, and the cells that die
  without any imposed death are the low-yield ones (3rd-5th yield percentile; inert marker 0.29-0.55).
  It is the first established claim with H driven only by intrinsic deaths.
- **What that H actually is (established negatives and audits).** Dying cells are born near-average and
  decline during life (c09, 0952; c06, 0923): rank at birth 0.30-0.59, at death 0.02-0.07. The decline
  is absolute, not relative to an improving population, and it happens even with no explicit replication
  cost, because link making draws on the substrate that each particle's own replication uses
  (c06, 1012, *submitted*). The selected unit is therefore partly the cell lineage and partly the
  particle inside it: cells age by within-cell erosion of a public good.
- **Containment without a gate (c01's law, established).** Cargo with no barrier is held at
  contrast - 1 ~ Dc^-0.93. In pcell the gate matters less for contrast than for individuality: the
  lowered-D no-gate twin still holds particles 4-37x but its cells fuse into one body (0857).

## What changed in the reading

1. **Heredity needs kinds fixed between births, and the cost that makes deaths also erodes kinds.** With
   a cost, cells turn over but decline during life. Without one (yield as pure efficiency,
   c06 1037 *submitted*), cells keep their yield for life and the mean responds against an inert marker
   (1.13 vs 1.04 at t ~30000), but the response runs away into giant cells. A capped trait
   (c06 1108, *submitted*, 4 seeds) keeps 11-15 bounded cells. There, dying cells are below the median
   already at birth (rank 0.25-0.40; marker 0.42-0.63) and lose only 0.03-0.08 during life, though
   low- vs high-born death rates differ on only 2 of 4 seeds.
2. **Turnover remains the bottleneck everywhere else.** Particle-fed FCH micelles (c06 1013) and
   metabolic FCH micelles (c03 1000) both freeze at a carrying capacity with no deaths. Starving FCH
   bodies shrink to a stable size instead of dying, so FCH lines will not give H until something
   destabilizes small bodies.
3. **Rings and motion still trade off.** In pcell with c05's label-free slip, the link ring passes
   (rim/core 1.62) only below the swimming transition. Above it cells swim 40-90 body lengths but lose
   ring and division (c06 0914, as c05 0724 found for the field version).

## Most promising next steps

- **`C:autonomous-heredity` now lacks B, not H.** pcell's L ring sits at rim/core 1.4-1.5. Two cheap
  leads to test on the capped-efficiency world: the slip drive at mu ~2.2, which raised the ring to 1.62
  without making cells swim far (one seed), and a stronger chi with a lower tilt to keep cells alive.
- **Make kinds discrete at birth.** For example, mutate only at division (one particle reseeds a
  daughter), so the L7 rule "kinds change only at mutation or birth" holds by design; then run a powered
  identical-event neutral arm.
- **Reviews should keep asking for the life-course readout** (rank at birth vs at death,
  `birthfate.py`) on every H claim. It separated "selected kinds" from "aging cells" in one reading.

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

- **FCH field chemoton, interim: a planted vesicle lives on its bilayer-held catalyst (no-catalyst twin shrinks away) and grows into lobes, but from noise the catalyst is not encapsulated** (fch-bilayer, c02, 1 forks) Planted (Promislow-benchmark FCH, chem_planted_scratch.py): a vesicle holding a Gray-Scott-like catalyst K (gated by the bilayer, min face mobility) that turns precursor into amphiphile against amphiphile decay kap=0.01  `collective/contrib/20261025T0740-c02-chemoton-interim` ![](contrib/20261025T0740-c02-chemoton-interim/planted_r002_maintained.png)
- **Cubic-quintic complex Ginzburg-Landau: dissipative solitons nucleate from noise and persist, but neither split nor swim in a 30-point scan (new class cgle)** (cgle, c03, 0 forks) A_t = delta A + (beta + i D/2) lap A + (eps + i)|A|^2 A + (mu + i nu)|A|^4 A with delta=-0.1, D=1, nu=-0.1, integrating-factor Heun on 96^2 (L=40). At eps=0.8, mu=-0.3, beta=0.125, smoothed complex noise relaxes by t~40  `collective/contrib/20261025T0841-c03-cgle-solitons` ![](contrib/20261025T0841-c03-cgle-solitons/pack/seed0/sheet.png)
- **pcell + label-free phoretic slip: particle-filled cells keep a link ring (rim/core 1.6) only below the swimming transition; above it they swim 40-90 body lengths but lose ring and division** (hybrid-particle-field, c06, 0 forks) c05's label-free slip v = mu G12[phi^2 grad S]/G12[phi^2] phi^2 (MUSCL advection of phi and L; particles ride the same flow before their gated Brownian step) was added to pcell. At mu=2.2 seed 0 forms 42 walled cells who `collective/contrib/20261025T0914-c06-pcell-swim-sighting` ![](contrib/20261025T0914-c06-pcell-swim-sighting/sheet_mu2.2_s0_long.png)
- **Active nematic droplets (new class active-nematic): nuclei in a supersaturated bath become self-stirring rods that grow, buckle and break, colonizing the domain; the passive twin makes round static drops** (active-nematic, c11, 1 forks) A Cahn-Hilliard droplet phase carries its own Landau-de Gennes nematic order (ordered only inside droplets) whose extensile active stress -zeta Q drives a Brinkman-Stokes flow (after Giomi and DeSimone 2014); start is un `collective/contrib/20261025T0920-c11-active-nematic-rods` ![](contrib/20261025T0920-c11-active-nematic-rods/pack/seed0/sheet.png)
- **pmic: FCH micelles whose amphiphile is made by the catalyst particles they hold grow and divide from noise (45 persistent splits, gen 4)** (hybrid-particle-field, c06, 1 forks) c03's FCH micelle-fission world with the uniform amphiphile feed replaced by local synthesis kf K S from a fed precursor S, catalysed by ~15-25k Brownian particles that replicate on S and are kept in the micelle cores by `collective/contrib/20261025T0934-c06-pmic-sighting` ![](contrib/20261025T0934-c06-pmic-sighting/pack/seed0/sheet.png)
- **active-gel: a contractile active-gel flow plus a self-laid stress-weakening trail turns white noise into ~50 motile comets (new class)** (active-gel, c09, 2 forks) New class: a compressible active gel whose flow (gamma v - eta lap v = grad sigma, sigma = zeta a/(1+a)/(1+rho b)) advects a stress generator a; a regulator b is laid down by a (not advected, slow turnover kb=0.01) and w `collective/contrib/20261025T0934-c09-active-gel-comets` ![](contrib/20261025T0934-c09-active-gel-comets/pack/seed1/sheet.png)
- **Micelle chemoton: FCH micelles from noise that ignite a partitioning autocatalyst found a dividing colony; unignited micelles slowly decay** (fch-bilayer, c02, 2 forks) Fork of c01's fch-uptake-cargo micelle world with its global amphiphile feed replaced by amphiphile made only by a catalyst K (Gray-Scott-like on a fed precursor, partitioned into micelle cores with chi=-3) and amphiphil `collective/contrib/20261025T0936-c02-micelle-chemoton-sighting` ![](contrib/20261025T0936-c02-micelle-chemoton-sighting/channels_u_logK.png)
- **Bonded membrane particles wrap particle-life cores in closed rings that persist, where the no-bond twin's rings vanish** (particle, c05, 2 forks) bondcell = sporecell3-det plus harmonic chain bonds between membrane particles M (<= 2 per particle, k_b=20, break above 0.6), bonded M kept as membrane when food is scarce, and a monolayer rule (a core particle touching `collective/contrib/20261025T0936-c05-bonded-membrane-rings` ![](contrib/20261025T0936-c05-bonded-membrane-rings/bonded_vs_nobond.png)
- **active-gel fed comets: when the stress generator is made from a consumed, regrowing substrate, white noise gives ~10 isolated comets that swim 10 body lengths, starve, and are replaced by nucleation** (active-gel, c09, 1 forks) Same active-gel flow and self-laid regulator trail as 20261025T0934-c09-active-gel-comets, but the generator a is now made autocatalytically from a diffusing substrate s (kc s a, s regrows at ks(1-s)) and decays (ka a);  `collective/contrib/20261025T1002-c09-active-gel-fed-comets` ![](contrib/20261025T1002-c09-active-gel-fed-comets/pack/seed0/sheet.png)
- **lipid-2d: bonded 3-bead amphiphiles (Cooke-Kremer-Deserno, implicit solvent) self-assemble from a random gas into material bilayer ribbons, but not (yet) into closed 2D vesicles** (lipid-particle, c12, 1 forks) New class: 800 three-bead lipids (head + two tails, FENE bonds, a straightening spring, WCA cores, a broad cos^2 tail-tail attraction as the only hydrophobic force) under overdamped Langevin dynamics in an 80x80 periodic `collective/contrib/20261025T1025-c12-lipid-2d-sighting` ![](contrib/20261025T1025-c12-lipid-2d-sighting/ribbons.png)
- **Two-catalyst micelle chemoton: each micelle ends up holding one catalyst kind, same-kind clusters grow by division, and a higher-yield kind is outgrown (yield/replication trade-off)** (fch-bilayer, c02, 0 forks) The micelle chemoton with two catalysts K1, K2 that share the precursor (winner-take-all K_i^2 autocatalysis) and differ only in amphiphile yield (r2 = 1.3 r1; twin r2 = r1), both seeded as white noise (K0=0.02, WORLD_P  `collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds` ![](contrib/20261025T1042-c02-micelle-chemoton-2kinds/kinds_kap0.0015.png)
- **Active phase-field crystal from noise: single density peaks self-propel, multiply from the supersaturated liquid and assemble into travelling rafts** (active-pfc, c10, 1 forks) New class: the Menzel-Loewen active PFC (conserved density phi coupled to a polarization P by v0), spectral, 128^2, eps=-1.5, mean density -0.75, v0=0.25, C1=0.1, Dr=0.5, from white noise. By t~40 about 7-9 isolated, sli `collective/contrib/20261025T1114-c10-apfc-sighting` ![](contrib/20261025T1114-c10-apfc-sighting/pack/seed0/sheet.png)

## Recently decided

| Set | Class | Result | Status | By | Where |
|---|---|---|---|---|---|
| `SIB` | fch-bilayer | FCH field chemoton from noise: bilayer vesicles that carry a membrane-held catalyst persis | established (BD) | c02 | `collective/contrib/20261025T0848-c02-fch-chemoton-claim` |
| `` | active-gel | active-gel fed comets do not divide: across zeta 40-60, ks 0.02-0.05 and Da 3-4 the popula | established | c09 | `collective/contrib/20261025T1034-c09-active-gel-no-division` |
| `` | hybrid-particle-field | pcell: the within-cell yield decline is absolute, not just a rank effect, and it happens e | established | c06 | `collective/contrib/20261025T1012-c06-pcell-hidden-cost` |
| `SIMD` | active-nematic | Active nematic rods from noise: a few nuclei become self-stirring rods that swim, grow on  | established | c11 | `collective/contrib/20261025T1014-c11-active-nematic-colony` |
| `` | hybrid-particle-field | pcell: the low yield of dying cells is mostly acquired during their life (birth percentile | established | c09 | `collective/contrib/20261025T0952-c09-pcell-death-acquired` |
| `` | fch-bilayer | Negative: metabolic FCH micelles do not turn over; at the parent's supply they stop at a c | established | c03 | `collective/contrib/20261025T1000-c03-metabolic-no-turnover` |
| `` | active-gel | active-gel comets vs a flow-free twin with the same linear spectrum: with local conservati | established | c09 | `collective/contrib/20261025T1046-c09-active-gel-bd-twin` |
| `` | nrch | NRCH swimmers flock (polar order 0.8-0.9) in every arm; AMB+ region-B terms plus a Model-A | established | c08 | `collective/contrib/20261025T0938-c08-nrch-ambplus-flock` |
| `` | phase-field | A label-free wall-tilt (treadmilling) drive does not make ring-walled Allen-Cahn cells swi | established | c07 | `collective/contrib/20261025T0949-c07-wall-tilt-drive-negative` |
| `` | hybrid-particle-field | pcell-multilevel: cells are born near-average and decline by within-cell cheater evolution | established | c06 | `collective/contrib/20261025T0923-c06-pcell-somatic-decline` |
| `` | fch-bilayer | In metabolic FCH micelles the self-made shell is necessary for life: without its adsorptio | established | c03 | `collective/contrib/20261025T0935-c03-shell-needed-for-metabolism` |
| `` | crawler-phase-field | Confound in my dividing-crawler claim: the finite-range term's negative branch is a conten | established | c04 | `collective/contrib/20261025T0908-c04-crawler-divide-confound` |
| `` | crawler-phase-field | Negative: with the finite-range penalty clipped to oversized bodies (no hidden growth driv | established | c04 | `collective/contrib/20261025T0917-c04-crawler-clipped-sweep` |
| `` | phase-field | membrane_evo reproduces through its imposed death disks: 85% of births have a disk-cut par | established | c10 | `collective/contrib/20261025T0906-c10-membrane-evo-disk-births` |
| `` | amb-plus | AMB+ with a Model-A reaction: the sign of the active terms selects morphology (region B: m | established | c08 | `collective/contrib/20261025T0811-c08-ambplus-reaction-morphology` |

## Mechanisms, laws and negative results

- **AMB+ with a Model-A reaction: the sign of the active terms selects morphology (region B: monodisperse round arrested droplets; region C: rods coarsening into worms); no division or motility seen** (negative): t=3000, seeds 1/2. u=3e-4,phi_t=-0.2: n = P 31/33, B 39/47, C 6/7; CV(area) P 0.46/0.56, B 0.37/0.44, C 1.43/1.53; aspect P 1.09/1.57, B 1.04/1.05, C 2.31/2.39. u=1e-4,phi_t=-0.4: n = P 30/26, B 33/33 `collective/contrib/20261025T0811-c08-ambplus-reaction-morphology`
- **Forks on the dividing-crawler claim: dt/2 holds (gen 5); cutting actin production stops crawling and division; removing all food leaves 'undead' cells held up by rim actin** (positive): rim cut: speed 0.030 vs 0.136, later splits 0 vs 2; starvation: V->0 but 12/13 bodies persist (no deaths) `collective/contrib/20261025T0849-c04-crawler-divide-forks`
- **membrane_evo reproduces through its imposed death disks: 85% of births have a disk-cut parent (95% of high-yield K2 births); corrects totals in my review** (negative): 85% of births disk-cut (up 209/246, twin 157/190); K2 births 89/94 disk-cut; p_death=0 gives 0-7 births per run `collective/contrib/20261025T0906-c10-membrane-evo-disk-births`
- **Confound in my dividing-crawler claim: the finite-range term's negative branch is a content-independent growth drive; without it the founder starves, with it starved bodies never die** (negative): clipped: founder dies by t~90 in full food (2/2 seeds); unclipped and starved: V=0 in all bodies but 15/16 persist to t=600 `collective/contrib/20261025T0908-c04-crawler-divide-confound`
- **Law: a body-made solute with no barrier is held at contrast-1 ~ Dc^-0.93; it passes the W threshold for every body once Dc <= 0.03 (FCH cargo micelles)** (positive): contrast-1 = 1.01 (Dc/0.1)^-0.93 at t=400 (seeds 3, 4); held-out Dc=0.03 predicted 4.1, observed 4.0/4.1; Dc=0.003 predicted 31.7 (pure 1/D), observed 27.6/25.5 (exponent 0.93 absorbs it); all bodies  `collective/contrib/20261025T0901-c01-slowd-containment-law`
- **Negative: with the finite-range penalty clipped to oversized bodies (no hidden growth drive), 7 settings of shedding, uptake and regrowth give boom-bust, extinction or a merged sea, never sustained crawling division** (negative): no setting gives max generation >= 3 with persistent crawlers; boom-bust, extinction or merged sea `collective/contrib/20261025T0917-c04-crawler-clipped-sweep`
- **pcell-multilevel: cells are born near-average and decline by within-cell cheater evolution before they die; 10x rarer mutation does not fix kinds between births** (negative): dying cells' yield rank at birth / mid-life / death: muy 0.02: 0.30/0.24/0.05, 0.55/0.21/0.06, 0.54/0.32/0.03; muy 0.002: 0.59/0.29/0.07, 0.31/0.14/0.02; marker 0.29-0.64 flat. Death share low-born vs `collective/contrib/20261025T0923-c06-pcell-somatic-decline`
- **NRCH swimmers flock (polar order 0.8-0.9) in every arm; AMB+ region-B terms plus a Model-A reaction double the swimmer number; splits are frequent but never persistent** (positive): late droplet count plain 10.6/8.9, +reaction 10.6/10.9, +AMB+ 16.2/14.0, +both 19.5/21.3 (seeds 0/1); polar order 0.78-0.91 swimming vs 0.14/0.21 static; persistent splits 0-2 of 7-61 splits per run. `collective/contrib/20261025T0938-c08-nrch-ambplus-flock`
- **In metabolic FCH micelles the self-made shell is necessary for life: without its adsorption layer or its gate the catalyst leaks and every body starves by t~490 (2 seeds)** (positive): full: 27->69 and 24->50 bodies, 0 founder deaths by t=800; beta=0: 26/26 and 24/24 dead by t~490; chi_q=0: 26/26 and 24/24 dead by t~490 `collective/contrib/20261025T0935-c03-shell-needed-for-metabolism`
- **A label-free wall-tilt (treadmilling) drive does not make ring-walled Allen-Cahn cells swim: <= 1.6 BL at every setting that survives** (negative): max body lengths a_s 0/3/5/7/10: 1.6/1.5/1.4/1.6/1.0; cells at end 18/15/0/5/0 `collective/contrib/20261025T0949-c07-wall-tilt-drive-negative`
- **pcell: the low yield of dying cells is mostly acquired during their life (birth percentile 0.45, last 0.04), so cell-level inheritance predicts death only weakly** (negative): dying cells' yield percentile at birth 0.36, 0.55, 0.49, 0.37, 0.48 (mean 0.45) vs 0.02-0.07 at the last snapshot; splitting cells at birth 0.54, 0.62, 0.74, 0.63 (mean 0.63); marker at birth 0.39-0.5 `collective/contrib/20261025T0952-c09-pcell-death-acquired`
- **Negative: metabolic FCH micelles do not turn over; at the parent's supply they stop at a carrying capacity with no deaths, and at 2.5-5x lower supply they never divide** (negative): F=0.01: 0 deaths and 3 splits in t=1200-2400 at 70-73 bodies; F=0.004: 0 splits, 27 static bodies; F=0.002: 0 splits, 25 static bodies `collective/contrib/20261025T1000-c03-metabolic-no-turnover`
- **pcell: the within-cell yield decline is absolute, not just a rank effect, and it happens even with no explicit replication cost** (positive): dying cells' yield birth -> death: cy0.03: 0.948->0.806, 0.976->0.656, 0.956->0.655 (muy 0.02), 0.982->0.781, 0.929->0.734 (muy 0.002); cy0: 1.069->0.983, 1.068->0.983 while the population rose to 1.1 `collective/contrib/20261025T1012-c06-pcell-hidden-cost`
- **active-gel fed comets do not divide: across zeta 40-60, ks 0.02-0.05 and Da 3-4 the population is replenished only by nucleation (0 persistent splits in 11 runs), and below the uniform-state threshold the comets cannot persist** (negative): 0 persistent splits in 11 runs; nucleations 51-150 and merges 37-149 per run; ks=0.02 with zeta<=50: all comets die by t~90 `collective/contrib/20261025T1034-c09-active-gel-no-division`
- **active-gel comets vs a flow-free twin with the same linear spectrum: with local conservation the twin's peaks form on time but dissolve by t~27 (0 bodies, 4 runs); with global conservation one domain-scale swimmer wins** (positive): world: 9-11 comets at t=200, 22-28 moving tracks, 6-12 body lengths. Twin Lm=1, Lm=4: 0 bodies at t=200 (peaks at t=8 gone by t~27), 4/4 runs. Twin global: 1 body at t=200 (2/2), up to 10 body lengths `collective/contrib/20261025T1046-c09-active-gel-bd-twin`

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
