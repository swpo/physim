# Candidate level-0 worlds and coarse-grainings for supervenient worlds

Inventory of 2026-11-07, for track 1 ("more worlds"), with what track 2 needs to know about each world's noise and inputs. A world here is a level-0 law F0 with hidden θ, plus a coarse-graining Φ (VW-1 types, `vw1/note/CATEGORY.md`). Citation marks: **V** = verified this session, **V-earlier** = verified in the named earlier review, **M** = from memory.

New measurements (one thread, nice 10, shared 4-core box, wall time ±30%; files are in this folder):
- `timing.py` → `timing.json`: per-step cost of every world.
- `invariants.py` → `invariants.json`: invariant drift in short free runs of the collective worlds.
- `kl_inject.py` → `kl_inject.json`: the KL cost of a v1 injection read as a Gaussian mean shift.

## 1. Findings that apply to every world

**Noise.** The four collective worlds are deterministic after their initial random field. The only exception is the vortex world's mutation event, one uniform draw every 50 t. Their noise exists only in the PhySim v1 LabWorld declarations, which are additive, proportional (σξx) or conserved (divergence of a white flux), each smoothed with ℓ = 2 px. The VW-0 Flow-Lenia worlds are deterministic too. The VW-1 port adds flow noise of std 0.5.

**Inputs as a shift before Gaussian noise** (x′ = f(x) + Bu + η, charge ½‖Bu‖²_Σ⁻¹; this matches the matched actuation channel in `track2/EXAM.md` §3.3):
- *Additive fields are natural actuators:* vortex ω, the phase field φ, nematic Q, Gray-Scott u and v.
- *Proportional fields* (vortex fuel Y; membrane S, K and L; every CIPS field) give a state-dependent charge, infinite at x = 0. Make their noise log-normal and actuate log x, giving the exact charge ½‖Δ log x‖²/σ². Clip after the noise.
- *Inputs must be smoother than the noise.* For width w ≤ ℓ the charge diverges under grid refinement. v1's inject bump has width INJ_SIGMA = 2 = ℓ.
  - On vortex ω (σ = 0.003, dt 0.02, gain 0.01), one unit pulse costs 1.7·10⁵ nats at w = 2 and 1.4·10⁴ nats at w = 3.
  - Spreading it over a 50-step tick divides the charge by 50.
  - So the v1 devices have no usable information meaning; each world must declare its actuation channel and noise scale.

**Conserved quantities, measured:**
- Flow-Lenia mass: drift ≤ 10⁻¹⁶ in the JAX port.
- CIPS ∫e: constant over 1000 steps. Turnover d(e₀ − e) preserves the mean because the initial mean is e₀.
- Fed-vortex circulation is **not** conserved: mean ω drifts 0 → −0.002 in 80 t, because gain and decay act on ω. Track 1's E4 should not count it as an invariant.
- Rods: mean φ relaxes towards φ_b = −0.6 (chemostat).
- phase_membrane: nothing is conserved (∫φ goes 1427 → 6361 → 1533).

**Hidden θ.** Every collective world's parameter point is published in its claim and suite. Hiding the weights therefore means drawing θ from a prior around the defaults, inside a band where the behaviour survives. That band must be mapped per world.

## 2. The collective's grand-challenge worlds

### 2.1 Fed vortices with heredity (c53, G:SIDH)

*Law.* A 2D incompressible fluid in which vorticity grows only where it eats a regrowing fuel. Labels a and b are copied where vortices eat. Mutation swaps a and b in a 6-px disk every 50 t. Kind b gains 20% more per unit fuel.
- **State and cost:** ω, Y, a, b: 4×128² float64. 2.4 ms/step at dt 0.02. About 37 CPU-s per generation *(estimate: generation 9–10 by t = 3000)*.
- **JAX port:** easy, since the law is pseudo-spectral. Mutation becomes `jax.random.categorical` over the eating mask.
- **Conserved quantities:** none. The law is equivariant under the lattice Euclidean group, with ω flipping sign under reflection.
- **Noise and inputs:** v1 noise is additive on ω and proportional on Y. A smooth ω stir (w > ℓ, spread over a tick) is an exact Gaussian channel.
- **Coarse-grainings:**
  - L1a: pooled ω and Y.
  - L1b: a vortex tracker giving position, circulation, size, sign and label share. This shows individuals, fission and heredity.
  - L2: count and kind-b share, which shows *selection*: b rises to 0.86–0.93 against 0.38–0.60 in the neutral twin.
  - Candidate laws: point vortices with merger rules (cf. Carnevale et al. 1991, **V**) and replicator dynamics.
- **Likely closure:** motion is near-closed given neighbours. Growth needs fuel, so pair L1b with pooled Y, as gliders paired coarse with objects. L2 should be good at long horizons, with finite-population noise (25–35 vortices).
- **Risks:** a reticulate genealogy (merge/split about 0.9–1.0); mixed labels (purity 0.58–0.73); fission needs neighbour strain; the fitness effect is written into the law; one parameter point.

### 2.2 phase_membrane (lab 1, SIBD)

*Law.* An Allen–Cahn phase whose inside is held up by links L. The links are made by an autocatalyst K from a fed substrate S and drift into the wall. Cells condense from noise and divide by central starvation.
- **State and cost:** S, K, L, φ: 4×128² float64. 1.0 ms/step at dt 1, the cheapest collective world. About 0.3–1 CPU-s per division cycle *(estimate)*.
- **JAX port:** trivial (`roll` stencils and an upwind flux).
- **Conserved quantities:** none.
- **Noise and inputs:** additive on φ, proportional on S, K and L. The actuators are φ (carving a wall) and S (feeding), once S's noise form is changed.
- **Coarse-grainings:** pooled fields; cells (φ > 0.5) with area, K and L content, wall integrity and S uptake. This shows individuals, *metabolism* and division. L2: count and size distribution.
- **Likely closure:** grow-then-split is a size-structured population law (growth-fragmentation). Cells compete for S, so pair the cell level with pooled S.
- **Risks:** 9–22 cells per box; frequent merges and deaths; explicit Euler at dt 1 (the suite used 0.5).

### 2.3 CIPS-iso (c40, SIBED)

*Law.* Enzyme condensates form by catalysis-induced phase separation (Cotton, Golestanian & Agudo-Canalejo 2022, **V**). Consumed fuel caps their size, so they divide by pinching. An amphiphile layer is made by catalysis and is one-way coupled.
- **State and cost:** e, p, F, s: 4×192² float64. 4.4 ms/step at dt 0.1. About 3 CPU-min per generation.
- **JAX port:** easy to moderate. It has 9-direction MUSCL fluxes, and the harmonic limiter's 10⁻³⁰⁰ guard underflows in float32.
- **Conserved quantities:** ∫e.
- **Noise and inputs:** proportional everywhere; actuate log F (feeding or starving).
- **Coarse-grainings:** bodies with area, layer and local fuel; counts. This shows division, metabolic dependence (a fuel moat kills in 25–50 t) and a boundary layer.
- **Likely closure:** good but *empty*. Division stops once the box fills (16–17 bodies, no deaths), so free level-1 dynamics become stationary.
- **Risks:** the cost; the layer is about one pixel thick, and peak and timing are not converged.

### 2.4 Marangoni rods (c34, SIBWMD)

*Law.* Active-nematic Cahn–Hilliard droplets on a Brinkman–Stokes fluid (after Giomi & DeSimone 2014, **M**). A self-made surfactant ring drives a Marangoni stress and holds a cargo.
- **State and cost:** φ, q₁, q₂, s, c: 5×128² float64. 12.8 ms/step at dt 0.05, the most expensive. 40–90 CPU-s per generation.
- **JAX port:** moderate. About 25 FFTs per step, and exp(κs) with κ = 20 risks overflow in float32; validation is the real cost.
- **Conserved quantities:** none exactly.
- **Noise and inputs:** conserved noise on φ (a flux shift is an exact channel), additive on Q, proportional on s and c.
- **Coarse-grainings:** rods with centroid, Q-orientation, length, velocity, ring and cargo. This shows motility, containment, inheritance of contents and division.
- **Likely closure:** short-horizon. The flow is chaotic and heading depends on the internal Q texture.
- **Risks:** the cost; motility is a minority trait (5 of 61 dividing tracks).

## 3. VW-0 Flow-Lenia worlds (Plantec et al. 2023, **V-earlier**, `hierarchical_worlds_litreview.md`)

One port serves all three: `flowlenia_jax.make_level(name)`. State: 2×128² float64, mass conserved per channel. Measured cost per substep (one tick is 20 substeps): A 7.9 ms, B 5.2 ms, C 5.7 ms. The matter kick is singular with respect to the flow noise (KL = ∞), so track 2 proposes a coarse "wind" channel.
- **A_gliders (done).** Measured closure ceilings:
  - coarse: 0.99, 0.85 and 0.49 at τ = 1, 4 and 8, and 0.08 at 32;
  - objects: 0.83 and 0.63 at τ = 1 and 4.
- **B_swarm.** About 14 bodies, 214 tracks, only 4 long (212 splits, 196 merges). Identity barely persists, so the natural level 1 is pooled density. It is a control in which an object level is the wrong Φ.
- **C_cells.** 3–7 large cells (39 px) that crawl, fuse and divide. It needs 256² for statistics. It tests whether a closure method transfers within one law family.

Add B and C as nearly free *variants*, not as new families.

## 4. Classic families worth adding

Reference JAX float64 steps are in `timing.py`.

### 4.1 Gray-Scott, and neural reaction–diffusion

Spots grow to a critical size and divide (Pearson 1993, **V**), also in experiments (Lee et al. 1994, **V**). A "pipette" steers them: feeding attracts, overfeeding splits (Froese, Virgo & Ikegami 2014, **V-earlier**, `lit_alife-embodied.md`).
- **State and cost:** 2×N². 2.9 ms/step at 256², about 0.75 ms at 128².
- **Conserved quantities:** none.
- **Noise and inputs:** additive noise; feeding u is an exact channel.
- **Coarse-grainings:** a spot tracker (replicating particles) and spot counts.
- **Likely closure:** good.
- **θ:** four rates, or an MLP reaction term f_θ(u, v) with diffusion kept. This is the bridge to arbitrary dynamics with a physics skeleton.
- **Risks:** a famous parameter map; some regimes freeze; no heredity.

### 4.2 Lattice Boltzmann and lattice gas

Lattice gases reproduce Navier–Stokes (Frisch, Hasslacher & Pomeau 1986, **V**). Fluctuating LB noises the non-conserved modes and satisfies the fluctuation–dissipation theorem at all wavevectors (Adhikari et al. 2005, **V**).
- **State and cost:** D2Q9: 9×128²; 1.8 ms/step.
- **Conserved quantities:** mass and momentum.
- **Noise and inputs:** a declared Gaussian body force makes agent forces an exact shift. FHP noise is Bernoulli, so its charge is a Bernoulli KL.
- **Coarse-grainings:** pooled ρ and u (closed by conservation laws), then vortices.
- **Likely closure:** excellent; the LES gap is a difficulty knob.
- **Use:** the calibration world.
- **Risks:** no individuals; turbulence must be forced.

### 4.3 Ising/Potts and the cellular Potts model

The cellular Potts model sorts cells by differential adhesion (Graner & Glazier 1992, **V**). Also relevant: Glauber dynamics (**M**), Kadanoff block spins (**M**), and models A and B (Hohenberg & Halperin 1977, **M**).
- **State and cost:** 128² int8 or int32. 0.21 ms per sweep.
- **Noise and inputs:** intrinsic noise. A local field h is the input; its charge is a sum of Bernoulli KLs, which is computable.
- **Coarse-grainings:** block spins and domains. In the cellular Potts model the label *is* the identity, so the object level is exact.
- **Risks:** relaxational near-equilibrium dynamics; division must be added by rule.

### 4.4 Particle life, and boids/Vicsek

In Clusters the forces between types are asymmetric and "break Newton's third law"; Clusters inspired Mohr's Particle Life (Ventrella, **V**). Related: Particle Lenia's rotor is "quite sensitive to small perturbations" (**V-earlier**), and Vicsek alignment (1995, **V**). Tools: JAX MD neighbour lists (**V**); ASAL already ships particle life and boids (**V-earlier**).
- **State and cost:** N×2 plus types. 7.1 ms/step at N = 1024 with all pairs.
- **Conserved quantities:** particle number per type. Momentum is not conserved (active matter).
- **Noise and inputs:** overdamped Langevin noise makes a regional force an *exact* shift. The charge Σ‖F dt‖²/2σ² grows with the number of particles pushed. This is the cleanest budget here.
- **Coarse-grainings:** per-type densities; contact-graph clusters as organisms (composition, heading, spin); size distributions.
- **Learned coarse-grainings:** level 0 is a *set*, so a learned Φ must be permutation-invariant. This is the lead's "biases define Φ" with a new bias.
- **θ:** a K×K matrix with a natural prior.
- **Risks:** most draws are gas or crystal, so screening is needed; reproduction is rare.

### 4.5 Neural CA

Sources: growing NCA (Mordvintsev et al. 2020, **V-earlier**) and CAX (Faldor & Cully, arXiv:2410.02651, **V**). The law *is* a network, so θ is literally its weights.
- **State and cost:** 16×64²; 1.0 ms/step.
- **Conserved quantities:** none unless imposed (track 1's transport NCA conserves mass).
- **Coarse-grainings:** learned autoencoders. Track 1's pilot found that a closure objective recovers pooling for conservative dynamics while PCA does not: cosine to uniform 0.89 at τ = 1 and 0.9999 at τ = 64 (`track1/pooling_tau.json`).
- **Risks:** most draws die, explode or freeze.

## 5. Ranking: the first worlds to bring into the vw types after gliders

1. **Fed vortices with heredity.**
   - Cheap, with an easy spectral port.
   - Additive ω noise makes the stirring budget exact.
   - Three levels with classical candidate laws: fields → point vortices → kind shares.
   - The first *selection* target at level 2.
   - SIDH held through 3 supporting reviews (3 more for the base world), and an existing suite.
   - Agrees with track 1's E4.
2. **phase_membrane.**
   - The cheapest world and a trivial port.
   - Adds membranes, metabolism and growth-then-division.
   - First change the noise forms and test dt 0.5 against 0.25.
3. **Particle life with Langevin noise.**
   - The black-box bridge: a weight prior, an exact budget, and a permutation-invariant Φ.
   - Fallback: **Gray-Scott with a neural reaction term**, which also feeds track 1's autoencoder pilots.

Add B_swarm and C_cells now. Defer CIPS-iso (cost, stationary free dynamics) and the rods (cost, stiffness, short closure) until there is a GPU path. Lattice Boltzmann and Ising are worth a day each as calibration worlds later.

## 6. Table

| World | State | Measured cost (1 thread) | Event timescale | JAX port | Conserved | Noise; Gaussian-shift input? | Natural Φ | Closure guess | Rank |
|---|---|---|---|---|---|---|---|---|---|
| Fed vortices | 4×128² f64 | 2.4 ms/step | ~37 s/gen (est.) | easy | none | add. ω, prop. Y; yes on ω | pooled ω,Y; vortices; kind share | good with fuel | 1 |
| phase_membrane | 4×128² f64 | 1.0 ms/step | ~0.3–1 s/division (est.) | trivial | none | add. φ, prop. S,K,L; yes on φ | pooled; cells; counts | good with pooled S | 2 |
| CIPS-iso | 4×192² f64 | 4.4 ms/step | ~3 min/gen (est.) | moderate | ∫e | prop. all; log F | bodies; counts | good, stationary | defer |
| Marangoni rods | 5×128² f64 | 12.8 ms/step | 40–90 s/gen (est.) | moderate–hard | none exact | cons. φ, add. Q; flux on φ | rods (+Q) | short | defer |
| A_gliders | 2×128² f64 | 7.9 ms/substep | 0.14 s/tick | done | mass | flow 0.5; wind channel | pooled; objects | c(4) 0.85 / 0.63 | done |
| B_swarm | 2×128² f64 | 5.2 ms/substep | 0.10 s/tick | done | mass | as A | pooled density | objects poor | variant |
| C_cells | 2×128² f64 | 5.7 ms/substep | 0.11 s/tick | done | mass | as A | few cell slots | untested | variant |
| Gray-Scott / neural RD | 2×N² f64 | 2.9 ms (256²) | seconds/division (est.) | trivial | none | add.; yes | spots; counts | good | 3 (alt) |
| Lattice Boltzmann / FHP | 9×128² f64 / bits | 1.8 ms/step | — | trivial | mass, momentum | random force; yes | pooled ρ,u; vortices | excellent | later |
| Ising / cellular Potts | 128² int8/int32 | 0.21 ms/sweep | — | trivial | M (Kawasaki) | intrinsic; Bernoulli KL | block spins; cells | relaxational | later |
| Particle life | N×2 f64 + types | 7.1 ms (N=1024) | ~10³ steps (est.) | easy | number per type | Langevin; yes, exact | densities; clusters | unknown | 3 |
| Neural CA | 16×64² f64 | 1.0 ms/step | — | trivial | none | if declared; yes | learned AE | unknown | track 1 E2 |

## References

**Verified this session:**
- Pearson 1993, Science 261:189.
- Lee, McCormick, Pearson & Swinney 1994, Nature 369:215.
- Frisch, Hasslacher & Pomeau 1986, PRL 56:1505.
- Adhikari et al. 2005, EPL 71:473.
- Graner & Glazier 1992, PRL 69:2013.
- Carnevale et al. 1991, PRL 66:2735.
- Vicsek et al. 1995, PRL 75:1226.
- Cotton et al. 2022, PRL 129:158101.
- Ventrella, Clusters (ventrella.com/Clusters).
- Schoenholz & Cubuk, JAX MD (arXiv:1912.04232).
- Faldor & Cully, CAX (arXiv:2410.02651).

**Verified in earlier reviews:**
- Flow-Lenia and Growing NCA (`hierarchical_worlds_litreview.md`).
- Particle Lenia, Froese et al. 2014 and ASAL (`lit_alife-embodied.md`).

**From memory:**
- Glauber 1963.
- Kadanoff 1966.
- Hohenberg & Halperin 1977.
- Giomi & DeSimone 2014.

**Internal:**
- The claims under `collective/contrib`.
- `gc_suites/*/capabilities.json`.
- `vw1/fresh/closure/results/summary.json`.
- `program/track1/DESIGN.md`, `program/track2/EXAM.md`.
