# Toolbox

Operators and measurement code from the first lab that new worlds should borrow rather than rewrite.
Paths are relative to `research/alife/`. Publish new reusable code as a `tool` contribution.

## Operators

### Sealed gated mobility: min face mean plus fast decay outside bodies

`dK/dt = div(D min(g_i, g_j) grad K) + auto*inside - (dK + d_out (1 - inside)) K,  with g = inside = [phi > 1/2]; the face mobility is the MIN of the two cell values, so every face that touches the outside carries zero flux`

Seals a heritable catalyst or label inside its own body. Stranded catalyst outside decays at d_out = 0.2. Use it whenever a kind or allele must not pass between touching field bodies (L7 heredity). The arithmetic gate gave conversions > mutations in 6/6 seeds; the sealed recipe gave conversions <= flips in 30/30 runs.

- code: `threads/autopoiesis/worlds/membrane_evo/world.py :: gate_div (l.81-87); step (inside, decay, gated K/K2/Qt l.106-120)`
- used in: membrane_evo, membrane_evo_up, membrane_evo_down, gated_protocell
- caveats: It is Supported only as the whole sealed-channel recipe: min gate, fast outside decay, and kinds that are neutral inside the cell (c2 = c1). The r2 committee ruled that a tighter gate alone would not stop takeover. The arithmetic mean 0.5(g_i + g_j) leaks 0.5 on every boundary face. The hard indicator [phi > 1/2] is not smooth. The membrane_evo L7 that rests on it is low and disturbance-mediated: the sweep runs through death-disk fragments, and the skeptic dissents (L7 Weak).

### Exponential membrane gate div(D e^{-beta psi} grad c) with harmonic face mean

`dc/dt = div(D e^{-beta psi} grad c) + R;  face coefficient D_f = 2 D_i D_j / (D_i + D_j) (P['harmonic']=1) or (D_i + D_j)/2; fuel bu = 0.5 (weak gate), catalyst bc = 3 (strong gate)`

The body's own shell psi slows whatever crosses it. A weak gate on fuel and a strong gate on catalyst give a permeability/retention trade-off and an interior fitness optimum in shell output, and each side of the trade-off disappears under its own ablation (bc=0: 3 vs 12 droplets; bu=0: 12 vs 6). Use it to contain a fast species with a boundary the body makes itself. Prefer the harmonic mean over the arithmetic one.

- code: `threads/active-droplets/worlds/ad9-ledger/world.py :: gated_div (l.52-59, harmonic switch l.56); arithmetic version threads/active-droplets/worlds/ad7-gated/world.py :: gated_div (l.45-52), called in step (l.90-97)`
- used in: ad7-gated, ad7-gated-d4, ad7t-thick, ad7n-neutral, ad7n-neutral-d4, ad7tn-neutral, ad9-ledger
- caveats: At 1-2 px shell width the grid sets the barrier's strength: kp=4 area fell 30% at dx=0.5, and the harmonic mean changed fitness, not just the profile. Each ablation is 1 seed. There is no control with a uniformly lowered D, so beyond-diffusion stays at 1. An exponential gate never fully seals; for heredity use the min gate. The ad7 founders are planted. The particle analogue (sporecell gate_beta, mobility x e^{-beta n_M}) left rings only on the founders (L6[L3] Contradicted).

### PhySim-genome perm gate (x-genome key perm)

`f += div(D_f e^{-beta max(x_c, 0)} grad f), done as the exact Fourier step with D_f plus an explicit correction div(D_f (e^{-beta max(x_c,0)} - 1) grad f) with an arithmetic face mean; genome entry perm = [[f, c, beta]], where f and c may be channel names`

A membrane channel blocks transport of a fast cargo or marker, and the term vanishes identically at the vacuum. In xcell-a the centre cargo is 1.24 vs 0.43 with the gate off (dt-converged). In xcell-her, beta_h = 0 erases every planted on-lineage (3 judges). Use it to add containment to any blobkit/m4 genome.

- code: `threads/fisim-beyond-laplacian/xgenome.py :: rhs (perm loop l.156-157; _div_face l.47-54; _resolve l.76-87 resolves channel names)`
- used in: xcell-a, xcell-her, xcell-her-sel, xcell-div, xcell-turn, xcell-evo, xcell-evo-N, xcell-evo2-S, xcell-evo2-N, xcell-a-nogate (beta=0), xcell-div-nogate (beta=0)
- caveats: It has only an arithmetic face mean; REPORT recommendation (a) is to make perm first-class with a min or harmonic option. The correction is explicit anti-diffusion bounded by D_f, and it is stable with the exact step at dx 0.5, dt 0.02. The gate-off control kept D=4 (the same fast D), so beyond-diffusion is 1. Always name channels: the r1 bug perm [6,3,5.0] gated the waste by cargo, not membrane, and xcell-turn was retracted. Every xcell world carries its own copy of the stepper (rhs).

### Allen-Cahn wall tilted by the cell's own product, with phi^2-gated mobility

`dphi = Dp lap phi + r phi (1-phi) (phi - 1/2 + a (L - th));  dK = div(DK phi^2 grad K) + auto - kdec K;  dL = div(DL phi^2 grad L) + b K S - dL L;  S fed by F (1 - S)`

This is the autopoietic container. Links that the catalyst makes tilt the double well, so the inside phase spreads; without links, curvature shrinks every domain. phi^2 mobility keeps K and L inside. The wall cannot have a hole, it repairs itself by curvature flow, and the cell divides by central starvation. It forms walled dividing cells from noise (phase_protocell_noise L6[L2] high; phase_membrane L6[L3] medium).

- code: `threads/autopoiesis/worlds/phase_membrane/world.py :: step (tilt l.117; gate g = phi^2 l.94) and mob_div (l.50-56)`
- used in: phase_protocell, phase_protocell_noise, phase_membrane, membrane_kinds, membrane_evo, phase_kinds, phase_trait, motile_trait, phase_protocell_notilt (a=0 ablation), phase_protocell_nogate (gate=0 ablation)
- caveats: The a=0 ablation (domains shrink and all die by t~350) is the researcher's own and was not re-run by the committee; gate=0 leaves all cells dead by t~350-400. mob_div uses an arithmetic face mean of phi^2, so labels leak between touching cells (for heredity use gate_div). The scheme is explicit Euler at dt=1 with clipping. Cell size rises with feed only roughly, and not monotonically at the low end. Transplanting trail propulsion into this cell tore the wall. The tilt was sent to fisim as a genome operator but never implemented there.

### Wall-adsorption drift of the cell's product (chi up the gradient of the wall indicator)

`flux_L = -DL g grad L + DL g chi L grad w,  w = 4 phi (1 - phi),  g = phi^2; the drift term uses first-order upwind`

Collects the cell's own link product in a ring at the wall (rim/core 1.51-1.72, against 1.12-1.14 at chi=0), so the membrane becomes a layer of material. The ring sets cell size (~2x) and division rate (~3x). Use it to turn a phase boundary into a material L3 layer.

- code: `threads/autopoiesis/worlds/phase_membrane/world.py :: step (l.108-114) with upwind_div (l.59-66)`
- used in: phase_membrane, membrane_kinds, membrane_evo, membrane_evo_up, membrane_evo_down, phase_swim, phase_swimdiv, phase_trail, phase_membrane_chi0 (chi=0 control)
- caveats: The ring does work (size and division rate) but is not needed for viability; it is credited under mechanism, not beyond-diffusion. Under rubric v2 the contour 4phi(1-phi) on its own is not a material layer. It was sent to fisim as a genome operator and never implemented there.

### Self-repellent trail propulsion (Keller-Segel with a slow self-secreted repellent)

`drho = Dr lap rho - div(rho (1-rho) (chi_a grad a - chi_h grad h));  da = Da lap a + rho - ka a (fast attractant);  dh = Dh lap h + beta rho - kh h (slow repellent)`

One added slow field makes static KS aggregates swim as crescents (route: spot, ring, rupture, crescent); with chi_h=0 you get 30-60 static spots. It is the base for dividing swimmers (swimfission: Da 4 -> 2) and for predator-prey worlds (pursuit, evopursuit).

- code: `threads/chemotaxis-motility/worlds/kstrail/world.py :: step (l.80-93); init (implicit La/Lh operators l.73-77)`
- used in: kstrail, toxtrail, toxforage, forager, swimfission, swimevo, swimevo_neutral, ecology, pursuit, evopursuit, evopursuit_neutral, evopursuit_nopred
- caveats: Bodies must be unsaturated, the volume-filling face flux must be conservative (MUSCL), and the body radius must be >= 6 px, or the heading locks to the grid. The Laplacian-only slow-inhibitor twin (the known drift bifurcation, Krischer & Mikhailov 1994) was requested in all 3 sprints and never run, so beyond-diffusion is 1. It is validated at 2x resolution. In an Allen-Cahn cell it failed: the divergent flow tears the wall. WORLD_P env overrides are for screening only.

### Conservative volume-filling face flux (MUSCL, van Leer limiter)

`div(rho (1-rho) v) with face flux F_{i+1/2} = v_f rho_L (1 - rho_R) if v_f > 0, else v_f rho_R (1 - rho_L); rho_L and rho_R are van Leer-limited reconstructions; v_f is the face average of the cell-centred v`

Mass-conserving advection that keeps 0 <= rho <= 1, for taxis and motility. Being second order, it cuts the anisotropic numerical diffusion of first-order upwinding, which had made swimmers prefer diagonal headings. Reuse it for any advective body transport (REPORT recommendation (d)).

- code: `threads/chemotaxis-motility/worlds/kstrail/world.py :: vf_flux_div (l.53-65) and _faces (l.43-50)`
- used in: kstrail, toxtrail, toxforage, forager, swimfission, swimevo, swimevo_neutral, ecology, pursuit, evopursuit, evopursuit_neutral, evopursuit_nopred
- caveats: A cell-centred volume-filling factor with clipping lost 80% of the mass; use this face form. It is not in labkit (labkit/ops.py has only the first-order upwind_flux_div), so every chemotaxis world carries a copy. The update is explicit, so CFL applies: |v| dt / dx < 1.

### Toxic-trail homeostat (self-poisoning by the body's own repellent)

`drho += g rho^3/(rh^2 + rho^2) - kd h rho  (h is the body's own slow repellent; switched on at t >= t_on)`

Makes motility a condition of survival: a stalled body sits in its own waste and dies from the inside, while a swimmer leaves the waste behind. This gives intrinsic death and keeps a motile phase alive. Add a consumed, regrowing nutrient (toxforage) and bodies grow and divide.

- code: `threads/chemotaxis-motility/worlds/toxtrail/world.py :: step (kinetics l.99)`
- used in: toxtrail, toxforage, swimfission, swimevo, swimevo_neutral, ecology, evopursuit (pdeath*kd*h), autopoiesis motile_trait_tox (as catalyst decay kd w K)
- caveats: Only within-model ablations exist. The cooperative (Allee) growth term is also what purifies the alleles carried in bodies.

### Non-reciprocal cross-taxis (pursuit and evasion)

`v_prey = chi_a grad a_p - chi_h grad h_p - chi_x grad a_q;  v_pred = chi_a grad a_q - chi_h grad h_q + chi_y grad a_p;  predation -k p q with yield e; in evopursuit chi_x -> chi_x (1 + e fB)`

Predators climb the prey attractant and prey descend the predator attractant. Without pursuit, contact falls to chance (0.58 vs a null of 0.58). Without evasion, predators are carried inside prey. It underlies the evopursuit L5 high sign flip.

- code: `threads/chemotaxis-motility/worlds/pursuit/world.py :: step (l.89-92); also threads/chemotaxis-motility/worlds/evopursuit/world.py :: step (l.113-117)`
- used in: pursuit, ecology, evopursuit, evopursuit_neutral, evopursuit_nopred
- caveats: Only within-model controls exist. Partner abundance was not matched in the 18 fixed-allele arms. ecology's -24% prey effect came from mismatched grids (matched: -7% with predators vs -35% without). The hunters transplant into autopoiesis starved in the prey's depletion halo.

### Allele carried on the body's own flux (upwind allele fraction)

`flux_B = F_total * fB_upwind,  fB = B/(A+B);  dB = Dr lap B - div(flux_B) + gB - ...;  dA uses div(F_total - flux_B)`

Confines a heritable allele to its body by construction: the allele moves only with the body's mass flux, and cooperative growth on own density purifies each body. Use it for heritable traits on advective bodies.

- code: `threads/chemotaxis-motility/worlds/evopursuit/world.py :: allele_flux_div (l.79-86) with vf_face_fluxes (l.69-76)`
- used in: swimevo, swimevo_neutral, evopursuit, evopursuit_neutral, evopursuit_nopred
- caveats: The diffusion term Dr lap B still mixes alleles where bodies touch, and in chemotaxis conversions were comparable to births. Patch mutations swap A <-> B in a disk and are logged in s['mutations'] (ledger()). B wins by retention under consumption (5.8-6.2x), not by exploiting the chase.

### Trait carried on the catalyst's own transport (q = a * trait)

`q = a * rung;  dq = div(Dc e^{-bc psi} grad q) + growth * q, with the same operator and growth rate as a;  trait = q / a`

Makes trait conversions impossible by construction: ad9 had 0 conversions in 12/12 runs. A mutation relabels a whole daughter at birth (_relabel). Use it whenever a continuous field must carry an inherited parameter.

- code: `threads/active-droplets/worlds/ad9-ledger/world.py :: step (l.174-180) and _relabel (l.94-95)`
- used in: ad9-ledger
- caveats: Merges were not logged, so mixed fusions are not certified. With 6 cells and 1-5 mutations per run, the test is underpowered. An earlier analysis counted planted disks separating as births, and the 'broad optimum' claim was withdrawn.

### Build-from-food with maintenance decay (Lenia metabolism)

`inc = clip(min(dt G, 1 - A), 0);  need = sum_c inc / Y;  scale = min(1, F / need);  A <- clip(A + inc*scale + min(dt G, 0) - dt mu A, 0, 1);  F <- F - need*scale + dt rho (Fmax - F), then implicit spectral diffusion D`

Matter can be built only from a local, regrowing food field, and the decay mu makes matter cost maintenance (no free dormancy). In mcfd, turnover 0 / 0.01 / 0.03 gives a dormant lattice / a fed static lattice / intermittent boom-bust, with a sharp threshold between 0.025 and 0.03. Without refill (rho=0), mcf-MIRd went extinct in 3/3 seeds. Use it to add L4c metabolism and turnover to any kernel world.

- code: `threads/lenia-multichannel/worlds/mcfd-MIRd/world.py :: step (conserve branch l.189-202); generator template threads/lenia-multichannel/tools/make_chan_world.py (l.82-94)`
- used in: mcf-MIRd, mcf-MIRd-norefill, mcf-fastcell, mcf-mIRde, mcfd-MIRd, mca-MIRd, mcg-MIRd, mcg-MIRd-neutral, rf-two56-mu0.01, rf-two56-mu0.03, eco-MIRd-Rplus (shared food)
- caveats: Structurally this is a Gray-Scott chemostat: the boom-bust is generic consumer-resource ecology, and the kernel only supplies the individuals. The L4c rows were scored under v1, and every requested starvation fork or local supply cut went unrun. Decay dissipates matter instead of returning it to food, so the ledger is not closed (compare the flow-lenia metabolism). Apart from colonization races, selection acted only where there was turnover.

### Conserved Hill-gated food (closed matter + food ledger)

`q = (A_sum/K_eat)^n;  eat = k_eat phi q/(1+q);  A_c += eat A_c/A_sum - k_dec A_c;  phi += -eat + k_dec sum_c A_c + D_food lap phi`

Open metabolism with an exactly conserved total (matter + food to ~8e-12). Bodies must keep eating to persist, and they can grow, and then divide, only by eating. Hill uptake prevents 'grey goo' tiling. It gives growth-division cycles without a global cap (fl_forager L6[L2]+L4b), and the exact ledger is a ready-made hidden law for an agent to find.

- code: `threads/flow-lenia/worlds/fl_forager/world.py :: metabolism (l.226-238)`
- used in: fl_food, fl_food_r0, fl_food_r8, fl_forager, fl_forager_evo, fl_forager_mut, fl_forager_gene, fl_forager_gene2, fl_cells_food, fl_morph257, fl_predator, fl_predator_gene
- caveats: Linear uptake gives grey goo. Food diffusion is explicit 5-point (stable only for D_food < 0.25 per step). The controls are within-family, so beyond-diffusion is capped at 1.

### Flow-Lenia reintegration tracking with a pressure term

`F_c = (1 - alpha) grad U_c - alpha grad A_sum,  alpha = clip((A_c/theta)^n, 0, 1);  each cell's mass moves as a 2 sigma square to x + clip(dt F, +-(dd - sigma)) and is split over the cells it overlaps (9 targets, np.bincount)`

Mass-conserving transport (to ~1e-12) that gives bounded bodies for almost any rule. The pressure term -alpha grad A keeps rings from breaking into dots (fl_cells). Use it as the conservative advection of REPORT recommendation (d).

- code: `threads/flow-lenia/worlds/fl_forager/world.py :: rt_targets (l.102-122) and step (l.173-223; pressure l.180-182; sobel l.93-99)`
- used in: fl_base, fl_cells, fl_cells_food, fl_food, fl_forager, fl_forager_gene, fl_forager_gene2, fl_ploc, fl_predator, fl_morph257
- caveats: Halving dt is not a convergence test here: dt/2 doubles the numerical diffusion. Test by changing resolution. fl_cells' beaded crown was numerical. The pressure and Hill results are within-family only (beyond-diffusion 1).

### Genes and parameters riding on matter parcels (parameter localization)

`Per-cell parameters P travel in the same reintegration step: 'avg' = mass-weighted mean of the incoming parcels; 'sample' = one incoming parcel chosen with probability proportional to its mass (Gumbel-max key); a body-scale mutation adds log g += N(0, mut_size) in a disk and gives each genotype it hits a new id`

Heritable traits on conserved matter, with genotype ids and a parent table for Muller plots. gene_active=False is the neutral-marker twin.

- code: `threads/flow-lenia/worlds/fl_forager/world.py :: step (localize branches l.194-217); also threads/flow-lenia/worlds/fl_forager_gene2/world.py :: mutate (l.257, own rng_mut stream)`
- used in: fl_ploc, fl_forager_evo, fl_forager_mut, fl_forager_gene, fl_forager_gene2
- caveats: Genes spread by somatic turnover inside fused mosaic bodies (L7 Contradicted; 0 deaths in 13/15 gene2 runs). 'Fusion spreads the gene' was a bookkeeping artefact (r(between, fusion) = -0.90). 'avg' blends genotypes, so use 'sample'.

### Identical-event neutral twins with a state-independent RNG

`Use a separate event stream (e.g. default_rng(seed + 777)). On every step draw the same numbers unconditionally (u, y, x per event type), and only then decide whether each event applies. The arms differ only in one parameter (b2, W[c,h], the kp ladder, gene_active).`

The selected and neutral arms see the same mutation, death and dilution events, so a difference between them comes from the trait, not from diverging random histories. Rubric v2 L7 requires an ancestor-matched neutral arm, ideally a twin of this kind.

- code: `threads/autopoiesis/worlds/membrane_evo/world.py :: step (event block l.126-154; stream s['ev'] created in init l.78); also threads/fisim-beyond-laplacian/worlds/xcell-evo2-S/world.py :: step (wrapper l.259-274, S['krng'])`
- used in: membrane_evo, membrane_evo_up, membrane_evo_down, xcell-evo2-S, xcell-evo2-N, ad9-ledger (rng_mut/rng_dil: 3 draws per birth, 1 per kill; neutral=1), sporecell3, sporecell3-det (chemistry draws all N randoms every call), fl_forager_gene2 (rng_mut; gene_active=False)
- caveats: Events stay matched only while their number does not depend on the state. ad9 replays by birth index, so its twins drift apart once their birth sequences differ, and fl_forager_gene2 picks the location by a mass quantile. particle-life's earlier lysis arms drew random numbers conditionally and diverged before contact. A death disk the size of a body acted as a fission operator and a size filter, which is why membrane_evo's L7 is disturbance-mediated. ad5 uses one shared rng for both the initial condition and the events, so it is not a twin. REPORT recommendation (f): declare such world-level events in META.

### Mutation patches and dilution disks (confined alleles, imposed turnover)

`At rate mut, a disk of radius rm around a random point with c > 0.7 is set to a random other allele. At rate dil, a random disk of radius rd is erased (phi = -1, a = 0; in ad7, psi = 0 too). Every event is logged in s['events'].`

Variation arises during the run and turnover is imposed. With mutual inhibition between alleles (winner-take-all per droplet), alleles stay confined to droplets. This is the origin of the confined-allele method used in 2-4 other threads (ad5-evolve L7[L2] low).

- code: `threads/active-droplets/worlds/ad5-evolve/world.py :: step (mutation l.80-89; dilution l.90-97)`
- used in: ad5-evolve, ad5n-neutral, ad7-gated, ad7t-thick, ad7n-neutral
- caveats: The rng is shared with the initial condition and the site choice depends on the state, so this is not an identical-event twin. Patch flips outnumber births (9 vs 6; in ad7, ~40 vs 6-9). Selection happens only during colonization, against a sterile ancestor, with 0 deaths. ad5's first neutral arm used k=0.13 against an ancestor at 0.10 (unmatched).

### Birth-coupled mutation with a Moran cap (in-world)

`Every TRK steps: periodic labels and overlap matching. For each birth, draw (u1, u2, u3) from rng_mut; with probability pmut, one daughter's rung moves +-1 (whole-droplet relabel). While count > cap, erase a uniformly chosen droplet (rng_dil).`

Kinds change only at birth, as rubric L7 asks; births equal deaths once the box is full; and the world writes its own event ledger.

- code: `threads/active-droplets/worlds/ad9-ledger/world.py :: _track (l.106-159; Moran loop l.149)`
- used in: ad9-ledger
- caveats: Underpowered: 6 cells and 1-5 mutations per run. A census every 100 steps can miss fast merge-split cycles, and merges are not logged.

### Particle chemistry with matter identity (catalytic provenance labels)

`F -> C at rate k_cat x (#C within r_cat); the new C takes the clan label and gene of the nearest catalysing C (the gene flips with probability mu). C -> F at k_dec. C <-> M by neighbour counts. Surface detachment at k_det for body < n_det. Optional contact lysis k_lys and conformity flips k_conf. The total particle number is conserved.`

Gives exact matter-identity lineage: every matter particle carries the clan of the catalyst that made it, so genealogy is exact provenance. Result: catalytic particle cells (sporecell3-det L2 high).

- code: `threads/particle-life/worlds/sporecell3-det/world.py :: chemistry (l.170-223; clan inheritance l.186-194 via nearest_of_type l.129-151)`
- used in: sporecell2, sporecell2-sel, sporecell3, sporecell3-det, sporecell-gene
- caveats: Majority-vote conformity (a flip at rate k_conf where the other kind outnumbers its own) still converted intact cells: 4 conversions against 5 kind-1 births in r3. At a step-safe step, births need a written detachment rule and stop at confluence, so L6[L2] is Weak. Membrane-gated food mobility (gate_beta) left rings only on the founders (L6[L3] Contradicted). The contact-kill rule (k_lys) gives L5 low on a dt map that has not converged. By the end the thread had seven hand-written rules.

### Displacement-capped adaptive sub-stepping (particle integrator numerics gate)

`nsub = ceil(max|v dt| / dx_max); take nsub sub-steps with the forces recomputed; clip any residual displacement > dx_max and count the clips; draw the noise once per step`

A step-safe integrator: the displacement per sub-step stays below dx_max (0.05, against r_max = 1), and nsub_hist, n_clip and max_sub_disp are logged so a judge can check the numerics.

- code: `threads/particle-life/worlds/sporecell3-det/world.py :: step (l.226-259; nsub l.241)`
- used in: sporecell3, sporecell3-det
- caveats: Without it, spore reproduction was integrator overshoot: the per-step displacement was 1.2-1.37 > r_max at dt=0.02. The step-safe control cut free spores from 127 to 3.4. With a clipped integrator, halving dt is not a convergence test.

### Cahn-Hilliard active emulsion with a self-made amphiphile shell

`dphi = M lap(phi^3 - phi - kappa lap phi) + prod - kd c,  prod = k u c^2 sum_i a_i,  c = (1+phi)/2;  dpsi = Dp div(grad psi - chi psi grad|grad phi|^2) + prod * kp(a) - gp psi;  the shell psi gates u (bu) and a (bc)`

Fuel-fed droplets synthesize the amphiphile that coats them, and the shell then gates fuel weakly and catalyst strongly. This gives an interior optimum in shell output (seed 0: 4/7/12/11/10/9/6 droplets at kp 0-4). P['linear']=1 replaces CH with linear diffusion at D=M, which is the Laplacian control.

- code: `threads/active-droplets/worlds/ad7-gated/world.py :: step (CH l.84-89 with the linear switch; psi drift l.99-102) and init (den l.65-71)`
- used in: ad3-membrane, ad3s-soup, ad4-protocell, ad7-gated, ad7-gated-d4, ad7t-thick, ad7n-neutral, ad7tn-neutral, ad9-ledger
- caveats: The founders are planted, and the 2-px shell width is set by the grid. The only Laplacian control that failed (R arm: 5 non-dividing spots vs 12 dividing droplets at kp=0.5; at kp=4, 6 vs 6) is 1 seed at D=M only, while CH's bulk diffusivity is 2M; the 3-seed D=M/2M replication was never run, and the final record keeps beyond-diffusion at 1. ad1-fuel division and ad3 ringing also happen without CH (Gray-Scott mitosis in a CH body). The ad3 shell was inert until ad7 gave it a gating job.

### Front-deposited membrane band plus a Cahn-Hilliard channel (x-genome)

`g(z) = 4 s (1-s),  s = tanh(max(z - thr, 0)/sc);  x_c += M lap[x (x-h) (x-1)] - M k lap^2 x  (the k lap^2 part sits in the exact Fourier factor)`

Deposits a membrane channel only at the activator's front: the drive is zero at the vacuum and in saturated interiors. The CH term caps the membrane at the x=1 well. Together with perm it makes m4 cells that carry a ring which gates their cargo (xcell-a L4b[L3] medium).

- code: `threads/fisim-beyond-laplacian/xgenome.py :: gfun (band l.124-125); rhs (CH term l.146-149); make_state (k^4 in E l.102-105)`
- used in: xcell-a, xcell-her, xcell-div, xcell-evo, xcell-evo2-S, xcell-evo2-N, xcell-turn
- caveats: CH broadens the membrane (8 vs 3 px) rather than sharpening it. Division in xcell-div is Gray-Scott-class (with the gate off, still 8 splits against 13-15). The explicit CH part needs dt M h 8/dx^2 < 1 (at dx=0.33, use dt=0.01). m4 cells have no intrinsic death, so every death in xcell-evo2 had to be imposed.

### Ring-kernel set-point membrane (multi-channel Lenia)

`A_c <- clip(A_c + dt sum_{k: c1=c} h_k G_k(K_k * A_{c0}) / sum h_k, 0, 1); K_k is Chan's shell kernel with ring peaks b inside radius r R; G is a quartic bell`

A ring kernel holds a shell at a set distance from the core, giving static shelled 'cog' cells from noise (r-two56 L3 high, converged at dt/2 and R=15/20). Knockouts: without k4, a sea of shell; without k5, the core dies; without k0, endless worms.

- code: `threads/lenia-multichannel/worlds/r-two56/world.py :: Lenia (growth l.90; RULE l.115-122); engine source threads/lenia-multichannel/tools/engine_src.py :: Lenia`
- used in: r-two56, r-two56-cell, rf-two56-mu0.01, rf-two56-mu0.03
- caveats: Found by 2 of 420 random rules, and 0 cell replicators turned up in 150 screened rules. There is no DoG or Laplacian control (r3: 'the thread's only route to a beyond-diffusion score'). In kernel worlds, boundary features of 1-2 px must survive a >=1.5x resolution continuation. The knockouts are the researcher's r1 ablations.

### labkit spectral and conservative primitives

`ops.wavenumbers(H, W, dx) -> (ky, kx) on the rfft2 grid; ops.lap_symbol = -k^2; ops.rfft2/irfft2 (scipy.fft, WORKERS=2); ops.fft_conv(x, Kf); ops.gauss_kernel; ops.ring_kernel (Lenia shells, gauss or exp core); ops.upwind_flux_div (first-order conservative div(rho v)); ops.laplacian, grad, div (periodic finite differences); ops.disk`

The shared building blocks for every IMEX world below. Import them instead of re-pasting FFT and kernel code.

- code: `labkit/ops.py :: lap_symbol (l.28); wavenumbers (l.13); rfft2/irfft2 (l.20-25); fft_conv (l.109); ring_kernel (l.79); upwind_flux_div (l.51)`
- used in: kstrail and all chemotaxis worlds (lap_symbol, fft_conv, gauss_kernel), ad3-ad9 (wavenumbers, rfft2, upwind_flux_div, disk), lenia r-*/mc* worlds (disk for damage)
- caveats: labkit has no stepper function: the IMEX schemes below live in world files. wavenumbers defaults to dx=1. Only the first-order upwind is provided; the MUSCL volume-filling flux lives in the chemotaxis worlds. WORKERS=2 FFT threads per process (the containers share 4 cores).

### Backward-Euler spectral step for linear diffusion-decay (IMEX)

`precompute L = 1 / (1 - dt (D * lap_symbol - k));  step: x <- irfft2(rfft2(x + dt * source) * L)`

Unconditionally stable linear diffusion and decay for fast signals (attractant, repellent, nutrient), next to an explicit nonlinear body update. The same pattern is used for the Lenia food field.

- code: `threads/chemotaxis-motility/worlds/kstrail/world.py :: init (La, Lh l.73-77) and step (l.90-91)`
- used in: all 12 chemotaxis-motility worlds, mcfd-MIRd and the other food Lenia worlds (F, step l.200)
- caveats: First order in time, and the source is explicit (old rho). The body density itself is explicit Euler with clipping (CFL on chi |grad a| dt).

### Implicit uniform diffusion plus explicit variable-coefficient correction (gated IMEX)

`x <- irfft2((rfft2(x) + dt rfft2(div(D(x) grad x) - D0 lap_fd x + R)) / (1 + dt D0 k^2))`

Stable variable-coefficient (gated) diffusion at large dt: the stiff uniform D0 is implicit, and the gate enters as a bounded explicit correction.

- code: `threads/active-droplets/worlds/ad7-gated/world.py :: step (fuel l.90-93, catalyst l.94-97; denu/denc in init l.70-71)`
- used in: ad7-gated, ad7-gated-d4, ad7t-thick, ad7n-neutral, ad7tn-neutral, ad9-ledger, x-genome perm uses the same split with an exact exponential
- caveats: The correction is anti-diffusive (D(x) <= D0), so it stays stable only while the gated D never exceeds the implicit D0. It mixes a spectral k^2 symbol with a 5-point finite-difference Laplacian, which agree only at long wavelengths.

### Stabilized semi-implicit Cahn-Hilliard step (linear splitting)

`phi_hat <- (phi_hat - dt M k^2 FFT(phi^3 - phi - A phi) + dt FFT(source)) / (1 + dt M k^2 (A + kappa k^2)),  A = 2`

A stable CH step at dt = 0.5 with M = 0.03: the kappa k^4 term and a stabilizing A k^2 are implicit, and the rest of the chemical potential is explicit.

- code: `threads/active-droplets/worlds/ad7-gated/world.py :: step (l.84-89) and init (den l.70)`
- used in: ad0-zwicker, ad1-fuel, ad2-catalysts, ad3-membrane, ad4-protocell, ad5-evolve, ad6-motile, ad7-gated, ad7t-thick, ad9-ledger
- caveats: The stabilizer A adds an artificial time lag, so check convergence in dt. The grid sets the 2-px shell width, and dx changes fitness (kp=4 area -30% at dx=0.5): check dx too.

### Exact exponential Fourier step (blobkit / x-genome convention)

`F <- irfft2(rfft2(F + dt R(F_old)) * E),  E = exp(-(D k^2 + M k_CH k^4) dt);  dx = 0.5, dt = 0.02; noise is added before the diffusion factor`

Exact linear diffusion (and the CH k^4 term) with an explicit reaction that uses the old fields. Parity with blobkit m4 is 3.8e-14 after 1000 steps.

- code: `threads/fisim-beyond-laplacian/xgenome.py :: make_state (E l.100-105) and step (l.171-178)`
- used in: all 16 xcell-* worlds (copied stepper), parity.py regression
- caveats: The reaction is explicit, and the CH explicit part needs dt M h 8/dx^2 < 1. Each world file carries a copy of the stepper, so keep parity.py as the regression test when editing it.

## Trackers and audits

- labkit periodic segmentation: 4-connected components with wrap-around merging, area filter, circular-mean centroids, enclosed holes — labkit/metrics.py :: periodic_label, segment, circ_centroids, holes
- labkit individuals: an outermost component plus everything it encloses (a ring and its core count as ONE individual) — labkit/metrics.py :: individuals, fill_enclosed
- labkit overlap tracker: components followed through frames by pixel overlap with a centroid fallback; split and merge events — labkit/metrics.py :: track
- labkit lineage: lifetimes, persistent splits (absolute K-frame window with the sibling re-merge filter), generations, merge/split ratio, motility — labkit/metrics.py :: lineage_stats
- labkit descendants and individual lineage: track ids reachable through splits and merges; an individual plus merges of its own pieces — labkit/metrics.py :: descendants, individual_lineage
- labkit radial profiles: per-channel means in 25 bins of rho = r/R_eq, rim/core and rim/outside boundary score (MEMBRANE-LIKE at >= 1.5), aggregate over individuals — labkit/metrics.py :: radial_profile, boundary_score, radial_aggregate (driver labkit/run.py :: _radial)
- labkit persistent homology: H0/H1 counts of the superlevel filtration (gudhi periodic cubical complex) — labkit/metrics.py :: persistence_counts
- labkit damage protocol: mature compact target, core/rim/half mask, undamaged comparator, measured loss — labkit/metrics.py :: choose_damage_target, damage_mask, choose_comparator (applied by labkit/run.py :: _apply_damage)
- labkit damage follow-up: the cut individual's pieces, area rel and matter rel tracked with the targeting range — labkit/metrics.py :: follow_individual (driver labkit/run.py :: _damage_followup)
- labkit per-species tracking: segmentation, tracking and lineage run separately on each META species — labkit/run.py :: _species_stats
- labkit particle clusters: periodic radius clustering of particles, with cluster-to-cluster links for tracking — labkit/metrics.py :: particle_clusters, cluster_comps, cluster_links
- labkit evidence pack driver: simulate, analyze, figures and FACTS for one world and seed — labkit/run.py :: run_pack (CLI python -m labkit.run)
- autopoiesis membrane_evo lineage and contagion audit: per-kind births, deaths (split by death disk), merges, flips, CONVERSIONS (1:1 kind change without a flip), first acquisition, off-kind daughters, tag series — threads/autopoiesis/evotrack.py :: bodies (census loop at module level)
- autopoiesis kind tracker: per-kind birth, death, merge and conversion counts by overlap census every 100 steps — threads/autopoiesis/kindtrack.py :: labels (census loop at module level)
- autopoiesis per-channel crop plus line profile through one cell — threads/autopoiesis/chanview.py :: (script)
- active-droplets in-world birth ledger: birth, death, offkind, mut, convert, nucleate and kill events with rung, plus a series of (t, n, mean kp, rung counts) — threads/active-droplets/worlds/ad9-ledger/world.py :: _track
- active-droplets Price-style split: dz_total = dz_mut + dz_conv + dz_between per run, per-rung event tallies, S curves against an identical-event N envelope — threads/active-droplets/evo_analyze.py :: (script)
- active-droplets ledger driver: runs ad9 and saves ledger.json (ledger, series, per-rung counts) and frames.npz — threads/active-droplets/evo_run.py :: (script)
- active-droplets per-allele droplet counts (argmax of mean catalyst per periodic phi>0 component) from live runs or packs — threads/active-droplets/alleles.py :: (script); threads/active-droplets/allele_plot.py :: (script)
- active-droplets protocell movie: fuel background, allele-coloured bodies, amphiphile rim — threads/active-droplets/protocell_movie.py :: (script)
- chemotaxis clean-fission lineage for moving bodies: dense sampling, 2-px dilated overlap links, lone-parent and survival rules, strict largest-parent generations — threads/chemotaxis-motility/fission.py :: label, lone_age (use strict=1)
- chemotaxis merge-aware prey ledger: per-kind clean-fission births, off-kind daughters, deaths, conversions from the world's mutation log — threads/chemotaxis-motility/preytrack.py :: label, lone_age, kind (KNOWN BUG: credits merge products as daughters)
- chemotaxis in-world mutation ledger: (t, site, body area, body B fraction before and after the swap), i.e. a conversion audit — threads/chemotaxis-motility/worlds/evopursuit/world.py :: ledger
- chemotaxis predator exposure per allele (predator density seen by an average unit of each allele) — threads/chemotaxis-motility/exposure.py :: (script)
- chemotaxis pursuit-pair statistic against a rolled-field chance null — threads/chemotaxis-motility/pairing.py :: (script)
- chemotaxis per-species population curves and the prey-predator lag that maximizes cross-correlation — threads/chemotaxis-motility/species.py :: (script)
- chemotaxis per-body allele composition (A, B, mixed counts over time) — threads/chemotaxis-motility/alleles.py :: (script)
- lenia heredity audit: division inheritance of the majority allele, and conversions against mutation events — threads/lenia-multichannel/tools/audit_alleles.py :: cells
- lenia per-division ledger: pure divisions, conversions, mixed-born children on Voronoi territories — threads/lenia-multichannel/tools/division_ledger.py :: snap
- lenia branch-point test: paired S vs N continuation from saved states, comparing whole-territory and old mutation operators — threads/lenia-multichannel/tools/branch_test.py :: territories, readout (states from threads/lenia-multichannel/tools/branch_states.py :: (script); summary in threads/lenia-multichannel/tools/analyze_branch.py :: (script))
- lenia replicator screen: flags random rules whose count of discrete bounded individuals keeps rising — threads/lenia-multichannel/tools/screen_replicators.py :: comps
- flow-lenia level-of-selection Price split (between / within / fusion / nucleation, exact identity) plus a per-kind ledger of births, deaths, flips, conversions, off-kind daughters, and the origin of every final high body — threads/flow-lenia/scripts/audit_gene.py :: audit, plabel
- flow-lenia clean-division chains (parent -> child -> grandchild strips) — threads/flow-lenia/scripts/division_chain.py :: segment, main
- flow-lenia composition heredity at clean divisions (parent vs daughter A0 fraction) — threads/flow-lenia/scripts/morph_heredity.py :: follow, comp
- flow-lenia per-kind mass and body counts for localized worlds; Muller plot of genotype mass by ancestry — threads/flow-lenia/scripts/evo_stats.py :: run, hard_kind; threads/flow-lenia/scripts/muller.py :: (script)
- particle-life merge-aware particle lineage through clan labels (continuation by particle overlap; qualifying births only) — threads/particle-life/lineage2.py :: run, qualify, summary (do not use lineage.py: it ratcheted generations)
- particle-life damage biography at particle resolution with an untouched control cell — threads/particle-life/damage_bio.py :: main
- fisim per-kind heredity: cells per kind, kind switches, splits by parent kind -> daughter kinds — threads/fisim-beyond-laplacian/kinds.py :: label_periodic
- fisim heredity assay of kick-arisen markers: division table from h-on parents, excluding splits near kills, plus conversions of intact cells — threads/fisim-beyond-laplacian/assay.py :: cells, disk; threads/fisim-beyond-laplacian/assay_an.py :: near_kill, lab_of, near_div
- fisim radial profiles of body, membrane and cargo with the gate on/off and CH on/off — threads/fisim-beyond-laplacian/s_profile.py :: (script)
- fisim stepper parity: xgenome.step against blobkit run_genome on m4 (3.8e-14 after 1000 steps) — threads/fisim-beyond-laplacian/parity.py :: (script)
