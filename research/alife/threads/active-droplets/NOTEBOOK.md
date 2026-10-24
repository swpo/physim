# active-droplets notebook

Sprint 1 started 2026-10-24 14:29 UTC. Tools: `screen.py` (quick strip of all channels),
`kinds.py` (per-kind droplet counts for catalyst worlds), `montage.py`. Screens in `screens/`.

## ad0-zwicker: Cahn-Hilliard + linear production/decay (Zwicker-style active emulsion)
- `d phi = M lap mu + kp(1-phi)/2 - kd(1+phi)/2`. Spectral semi-implicit, stabilized (A=2), dt 0.2-0.5.
- From noise with kp=kd: arrested coarsening into a dense droplet/stripe emulsion (`screens/ad0_base.png`). Validates
  the known result (reactions arrest Ostwald ripening, Ohta-Kawasaki-like size selection). L1/L2.
- From 3 seeds in a dilute background (kp=0.001, kd=0.005): droplets grow, elongate into dumbbells and **never pinch**
  (`screens/ad0_long_a.png`, 16k steps). NEGATIVE: in 2D there is no Rayleigh-Plateau instability, so Zwicker
  shape instability gives stable elongated droplets, not division. Higher kp (0.002) nucleates the background
  instead (`screens/ad0_s_kp0.002_kd0.005.png`).

## ad1-fuel: production needs a diffusing, consumed fuel u
- `prod = k u c^n`, `c=(1+phi)/2`, decay `kd c`; `u` fed from a bath `F(1-u)`, diffusion Du.
- n=1 (linear in c): dilute phase is autocatalytically unstable -> background nucleation, plus a striking
  expanding-ring pattern around the seed droplet (`screens/ad1_early.png`). Not individuals.
- n=2 (cooperative): background stable, single droplets grow to a fixed, fuel-limited size
  (`screens/ad1o2_k-0.05_kd-0.01_F-0.002.png`). No division for M=1 at any Du tried (0.5-4).
- Diagnosis: interior CH transport (D_eff ~ 2M) heals the fuel-starved core faster than decay acts.
  **Lowering M to 0.03** (CH slow vs chemistry): core starves -> droplet hollows into a ring -> ring breaks into
  3-4 daughters -> each regrows -> later elongated droplets pinch into two (binary fission) until the domain is
  filled with a fuel-limited droplet lattice (`packs/ad1-fuel-try/sheet.png`, 12 persistent splits, gen 2).
  Mechanism: fuel penetration length sqrt(Du/k) ~ 4.5 < droplet radius, with slow internal redistribution.
- LITERATURE.md (pulled 15:00) agrees: Zwicker 2017 division was 3D/axisymmetric; "no heredity: all droplets
  converge to one attractor". Our 2D route to division is different: core starvation + slow interior transport.

## ad2-catalysts: heritable catalysts (fork of ad1-fuel)
- Production needs one of two catalysts a, b: `prod = u c^2 (ka a + kb b)`. Catalysts replicate only inside droplets
  (`r c a (1 - a - beta b)`), decay outside (`g (1-c) a`), cross-inhibit (beta=1.5, bistable -> pure droplets).
- Seeds alternate kinds. Neutral (ka=kb=0.15): both kinds multiply, every droplet stays pure (`screens/ad2_neutral.png`).
  Biased (ka=0.15, kb=0.10): A droplets multiply ~3 -> ~10 by t=15000, B stay ~2-3 and barely divide
  (`screens/ad2_sel.png`). Division splits the catalyst with the material: kinds breed true in every division seen.
- Weakness: after colonization the population freezes into a static, fuel-limited lattice, so "selection" is
  only differential colonization speed. No turnover yet. Counts in the .txt files over-count droplets cut by the
  periodic edge (fixed in kinds.py later: periodic labels).

## ad2n-noisy: demographic noise on catalyst replication
- sigma 0.05 and 0.15 (pixel-white noise): no kind flips, no catalyst loss (`screens/ad2n_s*.png`). NEGATIVE: pixel
  noise averages out over a ~100 px droplet and bistability absorbs it. Mutation/turnover need droplet-scale noise
  or a mechanism, not pixel noise.

## ad3-membrane: droplets synthesize an amphiphile that binds their own interface
- `psi` made by the fuel reaction (`kp prod`), drift up `|grad phi|^2` (chi=8), slow decay. s=0 (no back-reaction).
- Result (`screens/ad3_base.png`): psi forms thin bright shells exactly on every interface: around the hollow-ring
  stage it lines both inner and outer edges; after ring break-up each daughter is wrapped in its own shell.
  Division unchanged vs ad1. Boundary channel differs from interior (low) and exterior (zero).
- Back-reaction s (kappa_eff = kappa - 2 s psi): s=0.1 no visible change; s=0.3 blows up at once (psi peaks 1.6 ->
  kappa_eff < 0). Needs a saturating coupling if revisited.

## ad1 regime sweep (40k steps, `screens/ad1sw_*.png`)
- F=0.002 kd=0.02 (low fuel): sparse population, divisions still happen late (t~35000) and some droplets dissolve
  (10 -> 7 -> 8): the only regime so far with turnover. F=0.004-0.008 / lower kd / lower M / lower Du: faster
  colonization, then a static lattice of 20-24 droplets.
- phi overshoots the binodal inside growing droplets (max 1.2-1.4): production outruns CH relaxation. To be checked
  with dt halving.

## Spontaneity
- Uniform starts (phi0 = -0.7, -0.5, -0.2, 0.0 with noise; seeds=0): everything goes EXTINCT in all four
  (`screens/ad1_spont*.png`). NEGATIVE, with a mechanism: the uniform soup consumes fuel everywhere at once, fuel
  crashes globally, and decay wins before the slow (M=0.03) phase separation can concentrate material into droplets.
  Individuals need a pre-concentrated nucleus. Same trade-off that makes division possible (slow M) kills nucleation.
- "Soup" start (40 random blobs of random radius 1.5-6 and random amplitude; `soup=40`): about 25 droplets survive
  and immediately fill the box as a static lattice (`screens/ad1_soup.png`); ad4 soup also keeps both kinds, pure
  (`screens/ad4_soup.txt`). A sparse soup (fewer blobs) is the right spontaneity test; not done yet.

## ad4-protocell (ad2 catalysts + ad3 membrane)
- ka=0.15, kb=0.12, 40k steps: A 3 -> 6, B 3 -> 5 (`screens/ad4_F4.png`); low fuel F=0.002: A 2 -> 3, B 2 -> 2.
  Kinds breed true, but the selection signal is weak because populations are tiny at 128^2 and freeze into a
  static lattice. Motivates ad5 (dilution for turnover + mutation for variation).

## Packs (15:00-15:40)
- `packs/ad1-fuel` (3 seeds, t=20000): 12-16 persistent splits, max generation 2-4, 18 droplets final in every seed,
  occupancy 0.13. Sheet: ring break-up of the seeds, then binary dumbbell fission, then a static lattice.
- `packs/ad1-fuel-damage` (seed 0, 50% of the largest component erased at frame 60): the cut happened to hit a
  droplet in mid-division (cut through the neck); both halves regrew to the control size within ~4-8 frames
  (droplet area 1487 -> 1608 px vs control 1599; `screens/ad1_damage_vs_ctrl.png`, top control, bottom damaged).
- `packs/ad3-membrane` (3 seeds): same division sequence; every droplet carries an amphiphile rim at all times
  (FACTS: psi rim 0.50-0.69 vs core 0.17-0.20, outside ~0; tracks.png shows a magenta shell on every tracked droplet
  through t=20000). 10-14 persistent splits, generation 2-4.
- `packs/ad4-protocell` (3 seeds): 11 droplets final, 5-6 persistent splits, gen 2. Kinds visible as colour in the
  sheet (A whitish, B cyan); B droplets mostly do not divide. Sheet colouring with 5 channels is hard to read.

## ad5-evolve: alleles + mutation patches + dilution
- 4 alleles k = 0.10/0.12/0.14/0.16, all droplets start as allele 0; mutation patch (disk -> another allele) at
  rate 0.002/time; dilution disk (r=10) at 0.0005/time.
- beta=1.5, rm=3: 31 mutation patches, NONE fixed (`screens/ad5_base.txt`): a small minority patch always loses the
  intra-droplet competition (bistability). NEGATIVE but informative: strong winner-take-all blocks innovation.
- beta=1.1, rm=5: mutants fix. Allele 3 (fastest) rises 0 -> 9 of 12 droplets, ancestor 4 -> 0 by t=20000
  (`screens/ad5_rm5_b1.1.png`, `.txt`). Mutant droplets visibly larger (size set by k). With beta=1.3, dil=0.001,
  F=0.003 the population stays mixed (8 droplets, [2,1,2,3]): more dilution + lower fuel = more drift.

## ad5 packs and controls (15:40-16:05)
- `packs/ad5-evolve` vs `packs/ad5n-neutral` (all alleles k=0.13), 3 seeds each, t=20000; `packs/ad5-evolve/alleles.png`.
  End counts [a0,a1,a2,a3]: selection s0 [0,2,1,9], s1 [4,1,2,4], s2 [1,1,3,6]; neutral s0 [7,0,0,2], s1 [8,1,1,0],
  s2 [4,4,2,1]. Fastest allele share 19/34 (selection) vs 3/30 (neutral); ancestor share 5/34 vs 19/30.
  Sheet (seed 0): a blue a3 mutant arises inside an ancestral droplet at t~3000, takes it over, and its descendants
  divide repeatedly (blue -> blue + blue); ancestral droplets stay small and mostly stop dividing.
- Ablation dil=0 (no dilution): seed 0 [1,0,0,12], seed 1 [3,1,4,3] (`screens/abl_ad5_nodil*.txt`). Dilution is
  not what drives the shift; selection acts through faster growth/division during colonization.

## Ablations and checks
- ad1 F=0 (no fuel feed): all droplets dissolve by t~6000 (`screens/abl_ad1_nofuelfeed.png`). Metabolic dependence.
- ad1 M=1 (fast interior transport): no division at any Du in 0.5-4 (earlier screens). Slow M is necessary.
- ad1 order n=1 (linear production): dilute phase unstable, background nucleates (`screens/ad1_early.png`).
- ad3 chi=0: amphiphile fills the droplet body instead of forming thin shells (`screens/abl_ad3_chi0.png`).
  The interfacial coupling makes the membrane.
- ad3 damage (`packs/ad3-membrane-damage`, seed 1, frame 120, 95 of 191 px erased): the elongated droplet is cut
  into two; each fragment closes a full amphiphile shell over its cut face within ~2 frames and regrows; droplet
  area back to control in 5 frames (1916 vs 1902 px). Control divides on its own at frame ~160.
  `screens/ad3_damage_vs_ctrl.png` (top control, bottom damaged).
- Numerics: ad1 with dt 0.25 vs 0.5, same simulated time: identical droplet counts at every frame and identical field
  ranges (`screens/num_ad1_dt*.png`). Resolution change not tested.

## ad3s-soup: membrane droplets from an unstructured start
- 8 random blobs (random radius 1.5-6, random amplitude), no planted disks. `packs/ad3s-soup`, 3 seeds: blobs grow,
  hollow, break up and pinch into 15-18 membrane-wrapped droplets; 8-12 persistent splits, gen 2-3; psi rim
  0.69-0.73 vs core 0.18. All division before t~5000, then a static lattice (same limitation as ad1).

Sprint 1 ended 16:15 UTC. Report: `REPORT_r1.md`.

# Sprint 2 (started 16:36 UTC)
Committee digest: convergence on gated mobility at boundaries; L7 bar = in-run variation + neutral control + 3 seeds;
challenge = fork a mechanism from another thread; go for motile or interacting heritable individuals.

## ad6-motile / ad6b-repellent: attempts at self-propulsion (NEGATIVE)
- ad6: Frey-type affinity of droplet material to fuel, mu += chi_u u (chi_u = -1, -3). Division as before, no
  motion (labkit: max 0.7 body lengths). My quick path metric in screen.py said 20 body diameters: an artifact of
  non-periodic labels at the box edge; use labkit tracking for motion.
- ad6b (fork of the chemotaxis-motility thread's slow self-secreted repellent): waste w made by the fuel reaction,
  mu += chi_w w. chi_w=10: droplets balloon and dissolve within t=700 (waste is made INSIDE the droplet, so it
  raises mu of the whole droplet). chi_w=1, 3 with faster waste decay: divide normally, <= 0.8 body lengths.
- Pure treadmilling (low Du 0.5-1, low F): no motion; Du=0.5 F=0.002 goes extinct.
- Interpretation: the regime that divides (slow condensate mobility M=0.03, so the core starves) is the opposite of
  the regime where Frey condensates swim (M >> D). Division and motility pull M in opposite directions here.
  Next idea if revisited: let an allele or a second component control local mobility.

## ad7-gated: membrane gates diffusion (fork of fisim's div(D e^{-beta m} grad c))
- ad3's self-made amphiphile shell now gates diffusion: fuel D_u e^{-0.5 psi} (weak gate), catalyst
  D_c e^{-3 psi} (strong gate); catalyst now diffuses (Dc=0.3) and dies outside droplets, so leakage is lethal.
  Alleles differ only in amphiphile output kp_i (all catalyse equally).
- Single-allele screens (no mutation, t=8000, `screens/ad7_kp*.png/.txt`): kp=0 -> 4 droplets (leaky: blurred
  catalyst halo, no growth); kp=0.5 -> 12; kp=1.5 -> 10; kp=4 -> 6 small starved droplets. An INTERIOR optimum:
  permeability (fuel in) vs retention (catalyst kept). Classic protocell trade-off, from one operator.
- Evolution test: all droplets start as allele 0 (no membrane), alleles kp = 0/0.5/1.5/4, mutation + dilution as
  ad5. Prediction: allele 1 (kp=0.5) wins, not the thickest. Neutral control ad7n: all alleles kp=0.
- Result `packs/ad7-gated` vs `packs/ad7n-neutral` (dil 0.0005, 3 seeds each, t=20000; `packs/ad7-gated/alleles.png`):
  end counts [kp0, kp0.5, kp1.5, kp4]: selection [5,1,1,0], [4,2,1,1], [2,4,1,3]; neutral [5,0,0,0], [3,1,0,1],
  [1,2,0,1]. WEAK: ancestor share 11/25 vs 9/14. The leaky ancestor barely divides AND never dies, so it simply
  persists; most allele counts are mutation events, not divisions.
- But the phenotypes are striking and distinct (`packs/ad7-gated/seed2/protocells.png`, new renderer):
  kp=0.5 (green) = thin white membrane, divides by dumbbell fission (t~5400, 16300); kp=4 (red) = thick bright
  membrane, small, never divides (starved: fuel gate); kp=0 (blue) = large diffuse leaky blob with a catalyst halo,
  does not divide. Genotype -> membrane -> metabolism -> fitness is visible in single frames.
- Rerun with 4x dilution (ad7-gated-d4 / ad7n-neutral-d4) so non-dividers get removed and space is re-colonized.

## protocell_movie.py
- Custom renderer from pack frames: fuel = background brightness, body colour = dominant allele, amphiphile =
  white rim. `packs/ad5-evolve/seed0/protocells.{mp4,png}`, `packs/ad7-gated/seed2/protocells.{mp4,png}`.
  ad5: a mutant shows up as half of an ancestral droplet (t=3700) before taking it over.

## ad7 with 4x dilution (ad7-gated-d4 vs ad7n-neutral-d4), 3+3 seeds, `packs/ad7-gated-d4/alleles.png`
- End [kp0, kp0.5, kp1.5, kp4]: selection [3,0,2,0], [1,4,3,2], [3,3,0,2] (23 droplets); neutral (all kp=0)
  [2,0,0,0], [2,2,0,0], [2,0,0,2] (10 droplets). Membrane alleles take 16/23 and the population is 2.3x larger
  than the membrane-less control, which dwindles under dilution. Allele 1 (predicted optimum) 7/23, allele 2 5/23,
  allele 3 4/23: the optimum is not resolved from this side.

## Fitness landscape and mechanism ablations (single allele, no mutation, seed 0, droplets at t=8000)
- kp: 0 -> 4, 0.2 -> 7, 0.5 -> 12, 1.0 -> 11, 1.5 -> 10, 2.5 -> 9, 4 -> 6 (`screens/ad7_landscape.png`). Single peak.
- Ablate catalyst gating (bc=0) at kp=0.5: 3 droplets (benefit gone; only the fuel cost remains).
- Ablate fuel gating (bu=0) at kp=4: 12 droplets (cost gone; thick = optimum). Both predictions confirmed:
  the optimum = retention benefit (bc) vs uptake cost (bu) of one gating operator.

## ad7t-thick: two-sided test, ancestor = thick membrane allele 3 (kp=4), dil 0.002
- End [kp0, kp0.5, kp1.5, kp4]: [1,5,4,2], [0,7,3,1], [2,2,4,5] (36 droplets). Intermediate alleles 25/36,
  thick ancestor 8/36. `packs/ad7t-thick/seed1/protocells.{mp4,png}`: red thick-shelled small cells are replaced by
  green/yellow thinner-membrane cells that divide. Neutral control (all kp=4) running: ad7tn-neutral.
- ad7tn-neutral (all kp=4, same mutation/dilution), 3 seeds: end [0,2,2,2], [2,1,3,2], [2,3,1,1] = 21 droplets.
  IMPORTANT: mutation churn alone drops the ancestor label to 24% (5/21), about the same as with selection (8/36).
  The real differences vs neutral: population 36 vs 21, intermediate alleles 69% vs 43%. Claim downgraded to Weak.
  CORRECTION (sprint 3, from committee r2): neutral intermediates are 2+2+1+3+3+1 = 12/21 = 57%, not 9/21.
  Per-seed shares overlap (75/91/46% vs 67/50/57%); the intermediate shift is not distinguishable from neutral.
- Landscape seed 1: kp 0/0.5/1.5/4 -> 5/12/12/6 droplets at t=8000 (broad peak 0.5-1.5).

Sprint 2 ended ~18:22 UTC. Report: `REPORT_r2.md`.

## Committee review r1 (read 18:20, after sprint 2) and quick R-arm check
- Decision: CONTINUE, consolidate on ad5 with turnover; arms S/N/R; stop ad4 and ad0/ad1 sweeps; pause motility.
- R arm on ad7 (`linear=1`: CH replaced by linear diffusion of phi at D=M=0.03), seed 0, t=8000: kp=0.5 -> 5 droplets,
  ~no division (CH: 12); kp=4 -> 6 (CH: 6). `screens/R_ad7_kp*.png`. In ad7 the double well matters for division.
- Merge note: the lab branch held an older snapshot of 4 files in this thread dir (add/add conflicts); kept this
  branch's versions.

# Sprint 3 (final; started 19:42 UTC)
Committee r2: CONTINUE on ad7; L6[L3] medium for the ad7 family; L7[L3] Weak; correct the 9/21 count (done above);
move the turnover protocol to ad7. Final deliverables: REPORT_r3, FINAL.md, movies/showcase.mp4.
- ad8-parasite: written at the end of sprint 2 (producer/parasite alleles, fork of ad5), never run. Deleted: the
  autopoiesis thread already has a parasite threshold and the committee asked to log or delete.

## ad9-ledger (protocol world)
- ad7 + harmonic face means in gated_div; rung trait carried by the catalyst (fields a and q = a*rung, same transport,
  so q/a is uniform inside a droplet); in-world tracking every 100 steps logs birth/death/kill/mut/convert/offkind/
  nucleate; mutation only at birth (p=0.1, one daughter, +-1 rung, whole-droplet relabel); Moran dilution
  (cap droplets; each excess -> one uniform random droplet erased); identical-event RNG streams per birth index
  (3 draws per birth) and per kill (1 draw); neutral twin = every rung has the ancestor's kp.
- KP ladder [0, 0.25, 0.5, 1, 1.5, 2.5, 4]. Scaled down from the committee spec to fit the sprint: 128^2 (not 192^2),
  t = 30000 (not >= 40000), landscape at t = 6000.
- Landscape (ad9, single kind, no mutation/dilution, t=6000, 3 seeds; `screens/ad9_landscape.png`, `runs/land_*`):
  births by kp 0/0.25/0.5/1/1.5/2.5/4 = 0.3/4.7/6.7/6.7/6.3/1.7/1.0 (means of 3 seeds); droplets 4.7/9.0/11.7/11.7/11.3/6.7/6.0.
  Plateau 0.5-1.5, both ancestors (0.25 and 2.5) fertile but 2.5 only marginally (births 3, 2, 0).
- Main run attempt 1, cap=12 (kp=2.5 ancestor, seed 0, t=30000): only 9 births, 1 mutation, 1 kill; S and N
  identical end states (12 droplets all rung 5). At carrying capacity births are fuel-limited, so no turnover.
  `runs/cap12/`. Aborted the queue; restarted with cap=6 (below carrying capacity: cells keep dividing and every
  birth forces a Moran kill).
- cap=6 arms done (`runs/{S,N}_a{1,5}_s*`, `screens/ad9_evo.png`, table in REPORT_r3): births = kills, 0 conversions,
  0 off-kind daughters, 2-5 mutations per run. Mean kp never enters 0.5-1.5; S within N's envelope. FAIL at this
  scale; mutation supply is the bottleneck (need ~10x births). The between-droplet term in S is non-zero in 3/6 runs,
  all toward the optimum.
- Sprint 3 ended ~21:00 UTC. FINAL.md and movies/showcase.mp4 delivered.
