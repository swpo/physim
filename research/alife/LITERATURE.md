# LITERATURE.md: artificial-life world dynamics, a reference for implementers

## 1. How to use this file

1. §2 has one section per dynamics family. Each gives citations, implementable equations, reference parameters, numerics notes, known phenomena and "Ideas for us". **UNVERIFIED** means a scout could not trace the item to a primary source. **Local check** means a scout's own short numpy rerun (periodic FFT unless stated).
2. §3 covers foundation models as judges and LLMs as mutation operators, and ends with design recommendations for our search loop. §4 lists quantitative metrics. Items labelled "Our proposal" are scout suggestions, not published results.
3. Before you explore a new world, reproduce the relevant positive control under your exact conventions: Orbium, VT049W, PPS, the Zwicker droplet, or a Gray-Scott pattern. Record dt, kernel normalization and boundary handling every time.

---

## Contents

- 2.0 Cross-cutting facts and numerics
- 2.1 Lenia and variants (Lenia, multi-channel Lenia, SmoothLife, Asymptotic Lenia / RD-Lenia, Sensorimotor Lenia)
- 2.2 Flow-Lenia and parameter localization
- 2.3 Particle Lenia and particle-life (Particle Life/Clusters, PPS, other particle protocells)
- 2.4 Active emulsions: Cahn-Hilliard + reaction (Zwicker droplets, Model AB / Ohta-Kawasaki, enzyme condensates)
- 2.5 Membranes and vesicles (FCH, phase-field Helfrich vesicles, Gompper-Schick)
- 2.6 Chemotaxis, cross-diffusion and active matter (Keller-Segel, AMB+, Active Model H, crawling cells)
- 2.7 Autopoiesis: SCL and chemoton
- 2.8 Reaction-diffusion baselines (Gray-Scott, Swift-Hohenberg)
- 2.9 Which family to try first
- 3 Model-as-judge and agent-as-mutation-operator lessons, with design recommendations
- 4 Quantitative metrics
- Appendix: scout artifacts and source links

---

## 2. Dynamics families

### 2.0 Cross-cutting facts and numerics

**Lenia is reaction-diffusion with a nonlocal ring kernel and a hard clip.**
- Remove the clip ("Asymptotic Lenia") and it becomes a true PDE, `du/dt = T(K*u) − u`.
- Kojima & Ikegami (2023) emulated that PDE with a pure RD system that uses about 40 fast-diffusing auxiliary species (§2.1.4).
- So our RD worlds are one step from Lenia. What they lack is a nonlocal ring kernel, not a new formalism.

**Results depend on dt and on implementation conventions.**
- The same parameters can self-replicate or sit still depending on dt or on the kernel-normalization convention (local checks in §2.1.1 and §2.1.2).
- Always record the exact convention.

**Where sharp interfaces come from.**
- In every field model in this file, a sharp interface comes from a double-well local free energy plus a higher-order gradient penalty. Three dynamics use this:
  - **Conserved (H⁻¹, Cahn-Hilliard):** `∂t c = ∇·(m∇μ)`, `μ = f'(c) − κ∇²c`. This is fourth order.
  - **Non-conserved (Allen-Cahn):** second order.
  - **Willmore / functionalized Cahn-Hilliard (FCH):** sixth order. A bilayer is a pair of interfaces, so it needs more derivatives.
- Plain reaction-diffusion has no surface tension, so its "boundaries" are only reaction fronts. **This is why our boundaries are soft.**

**Generic semi-implicit spectral step for conserved models.**
- Use it with a reaction term `s(c)` and periodic boundaries.
- The stabilizer must satisfy `S ≥ max|f''|/2`.
- Treat the linear stiff part implicitly and the nonlinear and reaction parts explicitly:
```
ĉ^{n+1} = [ ĉ^n − dt·m·k²·FFT(f'(c^n) − S c^n) + dt·FFT(s(c^n)) ] / (1 + dt·m·(S k² + κ k⁴))
```
- For FCH, the denominator gains a `k⁶` term.
- For Swift-Hohenberg, use `û^{n+1} = [û^n + dt·FFT(N(u^n))] / (1 − dt·L(k))` with `L = −(1−k²)² − μ`, or exponential time differencing (ETD).
- Apply 2/3 dealiasing when the nonlinearities are polynomial.

**Explicit Euler limits, 5-point stencil in 2D.**
- Fourth order: `dt < dx⁴ / (32 m κ)`.
- Sixth order: roughly `dt ∝ dx⁶`, so explicit stepping is impractical.
- Resolve the interface width `w` with at least 2–4 grid points.

---

### 2.1 Lenia and variants

#### 2.1.1 Lenia (original, single channel)

**Citation.** B. W.-C. Chan (2019), "Lenia – Biology of Artificial Life", *Complex Systems* 28(3):251–286. doi:10.25088/ComplexSystems.28.3.251. arXiv:1812.05433.

**Equations (paper Eqs. 7–13).**
- **Grid and time step.** `dx = 1/R` and `dt = 1/T`. R is the kernel radius in cells; T is the number of steps per unit time.
- **Potential and update.**
  - `U = K * A`, computed by FFT (which makes the boundaries periodic).
  - `A ← clip(A + dt·G(U), 0, 1)`.
- **Kernel core `K_C(r)`, r ∈ [0,1].**
  - exponential: `exp(α − α/(4r(1−r)))`, α=4
  - polynomial: `(4r(1−r))^α`, α=4
  - rectangular: `1[1/4, 3/4](r)`
- **Kernel shell (multi-ring)**, peak heights `β = (β1..βB)`: `K_S(r;β) = β_{⌊B·r⌋} · K_C(B·r mod 1)`.
- **Normalization.** `K = K_S / ΣK_S`, computed on the discrete grid.
- **Growth `G: [0,1] → [−1,1]`.**
  - exponential: `2·exp(−(u−μ)²/(2σ²)) − 1`
  - polynomial: `2·1[μ±3σ](u)·(1 − (u−μ)²/(9σ²))^4 − 1`
  - rectangular: `2·1[μ±σ](u) − 1`
- **Game of Life** is the special case R=T=P=1, kernel `1[1/4,3/4] + ½·1[0,1/4)`, rectangular G, μ=0.35, σ=0.07.

**Orbium unicaudatus reference parameters (`animals.json`, code `O2u`).**
- `R=13, T=10, b="1"` (β=[1]), `m=0.15, s=0.015, kn=1, gn=1`.
- Initial pattern: a 20×20 run-length string in `cells`.
- **RLE decoding:**
  - `.` = 0
  - `A`..`X` = 1..24
  - two-character `pA`..`yO` = `(c0−'p')·24 + (c1−'A') + 25`, up to 255
  - divide every value by 255
  - `$` ends a row and `!` ends the pattern
  - a numeric prefix is a repeat count
- **Code-convention trap.** In `LeniaND.py`, `kn=1` and `gn=1` select the **polynomial** "quad4" core and growth, but the UI label table calls `kn=1` "Exponential". Tutorial-style ports often use the bump/Gaussian versions with the same μ and σ instead.
- **Paper figures.**
  - Fig. 6: μ=0.15, σ=0.016, R=185, T=10.
  - Fig. 7: Orbium statistics are invariant for R in 9..55 at T=10, and approach a continuum limit for T in 4..2560 at R=13.
  - The parameter "niche" expands as T grows.

**Local check** (Lenia scout; 128² grid, 100 time units):

| Convention | T=10 | T=50 | T=2 |
|---|---|---|---|
| exponential bump core + Gaussian growth | survives (mass 77→71) | dies | dies |
| quad4 polynomial core + polynomial growth | survives (77→74) | survives | dies |

**Phenomena** (evidence: interactive simulation, taxonomy, statistics).
- More than 400 species in 18 families.
- Locomotion: stationary, rotating, translocating, gyrating.
- Gaits: fixed, oscillating, alternating, deviating, chaotic.
- Spontaneous metamorphosis, which behaves like a continuous-time Markov chain over body templates.
- Elongating "long-chain" Pterifera that grow by binary fission and fusion of vacuoles.
- Orbium collision outcomes: deflection, reflection, absorption, annihilation, detonation, fusion into Synorbium, parallel travel (Parorbium), and fission of composite Synorbium.
- **No self-replication.** The 2019 paper lists "Do self-replicating … lifeforms exist?" as an open question.
- **How patterns were found:** interactive evolutionary computation. This means random "primordial soup" initializations, gradual parameter tweaking, automatic flood-fill traversal of parameter space, and manual mutation (e.g., flipping one side of a creature) followed by re-stabilization.

**Pitfalls.**
- **The clip and dt.**
  - The hard clip means original Lenia is not an ODE.
  - Kojima & Ikegami found Orbium decays at both dt=0.5 and dt=0.002.
  - Removing only the upper clip let it persist at dt=0.002 but not at dt=0.1.
  - See also Davis & Bongard (2022), "Step size is a consequential parameter in continuous cellular automata", ALIFE 2022, p. 43.
- **Grid scale.** Use R > 12 for approximate rotation and scale invariance.
- **Kernel handling.** Normalize the kernel numerically on the actual grid, and centre it with `ifftshift` before the FFT, or creatures drift.
- **Narrow niches.** σ ≈ 0.015 makes Orbium's niche in μ–σ space very small, so mutation steps must be about 1e-3.

#### 2.1.2 Multi-kernel / multi-channel Lenia ("Expanded Universe")

**Citation.** B. W.-C. Chan (2020), "Lenia and Expanded Universe", *ALIFE 2020*, pp. 221–229, MIT Press. arXiv:2005.03742.

**Equations.**
- Update for destination channel j: `A_j ← clip(A_j + dt · Σ_{i,k} (h_k/h) · G_k(K_k * A_i), 0, 1)`.
- Each kernel k has a relative radius `r_k·R`, ring peaks `β_k`, `μ_k`, `σ_k`, a weight `h_k`, a source channel `c0` and a destination channel `c1`.
- Kernel count: `n_k = k_s·c + k_x·c(c−1)`. Here c is the number of channels, k_s the self-kernels per channel, and k_x the cross-kernels per ordered channel pair.
- The paper also generalizes to 3D and 4D.

**Two implementation conventions (critical).**
- **(a) `LeniaNDKC.py`:** sums `dt·h_k·G_k` per destination channel, then **divides by Σh_k for that channel**. Uses Chan's core functions.
- **(b) Chan's JAX/Colab-derived code** (used in Leniabreeder's `lenia/lenia.py`):
  - Distance: `Ds = B·|x|/(r·R)`.
  - Kernel: `K = 1[Ds<B] · b[⌊Ds⌋] · exp(−((Ds mod 1) − 0.5)²/(2·0.15²))`, then normalized.
  - Update: `A + (1/T)·Σ_k h_k·G_k`, with **no** division by Σh.
  - Growth: Gaussian, `2·exp(−(u−μ)²/(2σ²)) − 1`.

**Reference creature: "Aquarium (self-replicating)", ID VT049W** (Leniabreeder `lenia/patterns.py`; R=12, T=2, 3 channels, 15 kernels).

| # | β | μ | σ | h | r | c0→c1 |
|---|---|---|---|---|---|---|
| 1 | [1] | .272 | .0595 | .138 | .91 | 0→0 |
| 2 | [1] | .349 | .1585 | .48 | .62 | 0→0 |
| 3 | [1, 1/4] | .2 | .0332 | .284 | .5 | 0→0 |
| 4 | [0, 1] | .114 | .0528 | .256 | .97 | 1→1 |
| 5 | [1] | .447 | .0777 | .5 | .72 | 1→1 |
| 6 | [5/6, 1] | .247 | .0342 | .622 | .8 | 1→1 |
| 7 | [1] | .21 | .0617 | .35 | .96 | 2→2 |
| 8 | [1] | .462 | .1192 | .218 | .56 | 2→2 |
| 9 | [1] | .446 | .1793 | .556 | .78 | 2→2 |
| 10 | [11/12, 1] | .327 | .1408 | .344 | .79 | 0→1 |
| 11 | [3/4, 1] | .476 | .0995 | .456 | .5 | 0→2 |
| 12 | [11/12, 1] | .379 | .0697 | .67 | .72 | 1→0 |
| 13 | [1] | .262 | .0877 | .42 | .68 | 1→2 |
| 14 | [1/6, 1, 0] | .412 | .1101 | .43 | .82 | 2→0 |
| 15 | [1] | .201 | .0786 | .278 | .82 | 2→1 |

- The same file holds "Aquarium (swarm)" (ID 5N7KKM), plus "twin" and "gyrating" phenotypes that share its kernels.
- Σh ≈ 2.0 per destination channel.

**Local check** (Lenia scout; 256² grid; blobs = 4-connected components of ΣA > 0.1 with ≥ 30 px):

| Update convention | Effective step | Outcome |
|---|---|---|
| (b), un-normalized, T=2 | ≈1.0 | one stable soliton for 5000 time units (mass ≈ 809), no replication |
| (b), un-normalized, T=3 | ≈0.67 | one stable soliton (mass ≈ 806), no replication through t=500 |
| (a), ÷Σh, T=2 | 0.25 | **replicates**: 1 → 2 blobs by t≈300; mass 684 → 2024 and **5 blobs** by t=600 |
| (b), T=4 (algebraically ≈ (a) at T=2) | ≈0.5 | mass jumps (≈690 → ≈1150 by t=250), then one component through t=350 |

So whether VT049W self-replicates depends on dt, and on the normalization convention, which silently changes the effective dt.

**Phenomena** (evidence: paper Figs. 3–4, qualitative).
- **Individuality** becomes common with multiple kernels or channels. In original Lenia only the Orbidae family survived collisions. Chan suggests some kernels or channels act as repulsion that keeps individuals apart.
- **Self-replication** is "not rare" in the extended rules.
  - One soliton develops two similar partitions. Each grows into a full soliton, the two drift apart, and they can divide again.
  - In multi-channel rules, division in one channel is followed by the others.
  - **Autocatalytic replication:** replication triggered by crowding, which gives exponential growth.
- **Emission:** irregular, puffer-train-like.
- **Growth by ingestion:** in the "3D Snake" rule, a moving snake merges with static food dots and lengthens.
- **Division of labor:** some channels form flexible outer shells ("membranes"), others form central masses ("nuclei").
- **Differentiation:** one "Aquarium" genotype produces several stable phenotypes (directional, oblique, gyrating, stationary, slow/fast, parallel/antiparallel pairs). They switch on collision or after replication.
- **3D:** spherical solitons whose internal voids sit at the vertices of Platonic solids.
- **How patterns were found:** semi-automatic search with a human in the loop.
  - Global random genotype + phenotype sampling.
  - Depth-first and breadth-first mutation walks.
  - A GA with mutation and channel-wise recombination.
  - A survival filter (not vanished, not filling the grid), then human selection for novelty.
- The genotype is `(r, h, β, μ, σ)` per kernel; for example, 105 values for a 3D, 3-channel, 3-self-kernel rule.

**Pitfalls.**
- The normalization trap above.
- With many kernels, chaos and metamorphosis dominate, and regular behaviour is rare.
- Without a death rate, replicators eventually fill the grid.

#### 2.1.3 SmoothLife

**Citation.** S. Rafler (2011), "Generalization of Conway's 'Game of Life' to a continuous domain – SmoothLife", arXiv:1111.1567.

**Equations.**
- **Fillings.**
  - Inner filling `m`: the mean of f over a disk of radius r_i.
  - Outer filling `n`: the mean of f over the annulus r_i < |u| < r_a, with r_a = 3·r_i.
- **Anti-aliased rims** of width b=1: a cell at distance l inside the rim zone gets weight `(r_i + b/2 − l)/b`.
- **Sigmoids.**
  - `σ1(x,a) = 1/(1+exp(−(x−a)·4/α))`
  - `σ2(x,a,b) = σ1(x,a)·(1−σ1(x,b))`
  - `σm(x,y,m) = x·(1−σ1(m,0.5)) + y·σ1(m,0.5)`
- **Transition.** `s(n,m) = σ2(n, σm(b1,d1,m), σm(b2,d2,m))`. The step width is α_n inside σ2 and α_m inside σm.
- **Time stepping.**
  - Discrete time: `f ← s(n,m)`.
  - Smooth time: `f ← f + dt·(2s − 1)`.
  - Rafler notes that the same gliders do **not** appear at the same parameters as in discrete time.

**Reference "smooth glider"** (Fig. 1 caption): r_a=21, b1=0.278, b2=0.365, d1=0.267, d2=0.445, α_n=0.028, α_m=0.147. The scout did not re-simulate it.

**Phenomena.** SmoothLife produced the first omnidirectional glider in a continuous CA (rediscovered as Scutium in Lenia), plus oscillators and still structures.

**Pitfalls.** The discrete-time and smooth-time variants have different niches. Rims need anti-aliasing at small radii.

#### 2.1.4 Asymptotic Lenia, and Lenia written as reaction-diffusion

**Citations.**
- T. Kawaguchi, R. Suzuki, T. Arita, B. Chan (2021), "Introducing asymptotics to the state-updating rule in Lenia", *ALIFE 2021*, Proceedings 33, p. 91. The scout did not retrieve this paper; its content here comes via the citing papers.
- H. Kojima, T. Ikegami (2023), "Implementation of Lenia as a reaction-diffusion system", *ALIFE 2023*. arXiv:2305.13784.
- Q. T. Davis (2024), "Non-Platonic autopoiesis of a cellular automaton glider in Asymptotic Lenia", arXiv:2407.21086.
- H. Kojima, I. Yevenko, T. Ikegami (2025), "The Glider Equation for Asymptotic Lenia", arXiv:2508.04167 (preprint).

**Equations.**
- `∂u/∂t = T(K*u) − u`, with no clip.
- Kojima's target function: `T = (G+1)/2 = exp(−(x−μ)²/(2σ²))`.
- Davis's target function: `T(x) = exp(−((x−μ)/σ)²)`, with **no factor of ½**. Watch this convention.
- This generalizes Kondo's kernel-based Turing (KT) model: `u ← u + dt([K*u]_0^{a_max} − u)`.

**RD emulation ("RD Lenia").**
- System:
  - `∂u/∂t = F(u, α0 + Σ_j α_j v_j)`
  - `∂v_j/∂t = (1/ε)(D_j∇²v_j + μu − v_j)`
- Each v_j relaxes to a screened-Poisson (Yukawa / Bessel-K0-like) blur of u. K is fitted by least squares as a linear combination of these blurs.
- Parameters: M=40, μ=0.1, D_j=j, ε=0.005, dt=1e-5.
- **Very stiff.** The fitted α_j in their Fig. 4 are on an axis of scale 1e13, so the fit is badly ill-conditioned.
- The authors note it is not a chemical system: the reaction term does not satisfy mass-action kinetics.

**Reference parameters.**
- **Davis glider:**
  - μ_T=0.12, σ_T=0.005.
  - Kernel `exp(−((r−0.5)/0.15)²)`, normalized, radius 13 px.
  - dt=0.2 survives 100 steps; dt=0.17 and dt=0.26 die earlier.
- **Glider-equation paper:** μ=0.21, σ=0.018, three-ring kernel weights [5/6, 7/12, 1], dt=0.1, 144² periodic grid.

**Phenomena.**
- Kojima: Orbium-like gliders persist from dt=0.1 down to dt=0.002, unlike in original Lenia.
- Davis: a glider in Asymptotic Lenia loses its "autopoietic competence" when simulated too finely in space or time. This contradicts strict dt-independence; treat it as an open issue.

#### 2.1.5 Sensorimotor Lenia (dynamics; the search and agency filter are in §3.2)

**Citation.** G. Hamon, M. Etcheverry, B. W.-C. Chan, C. Moulin-Frier, P.-Y. Oudeyer, "Discovering sensorimotor agency in cellular automata using diversity search". Preprint arXiv:2402.10236 (Feb 2024). Journal version: *Science Advances* 11(44): eadp0834, published 31 Oct 2025, doi:10.1126/sciadv.adp0834 (not 2024).

**System.**
- Two channels: a learnable channel 0 and a fixed obstacle channel 1.
- Ten learnable rules map 0→0, for 132 parameters in total.
- Kernel: `K(x) = Σ_{i=1..3} b_i·exp(−((|x|/(rR)) − a_i)²/(2w_i²))`.
- Growth: `G(x) = 2·exp(−(x−μ)²/(2σ²)) − 1`.
- Parameter ranges: T∈[1,10], R∈[15,40], r∈[0,1], b∈[0,1], w∈[0.01,0.5], a∈[0,1], μ∈[0.05,0.5], σ∈[0.001,0.18], h∈[0,1].
- **Obstacle rule (channel 1 → channel 0):**
  - R=4, r=[1,1,1], b=[1,0,0], w=[0.5,1,1], a=[0,0,0].
  - `G_obs(x) = −10·clip(x − 1e−8, 0, 1)`.
  - This acts as a hard wall. Agents can only "touch-sense" obstacles through the deformation the obstacles cause.

**Phenomena.**
- Agents generalize to stochastic (masked/asynchronous) updates, noise, changed initialization, and some rescaling. The judges scout lists 9 perturbation families: scale from about 0.15 upward, asynchronous updates, noise, and up to 48 obstacles.
- With several copies in a 512×256 grid:
  - **individuality is preserved** (copies do not merge);
  - some pairs **attract**, separating at obstacles and rejoining;
  - **collision-triggered reproduction**: a third entity is born, apparently when one agent is in a post-wall "growth response".
- An added "attractive element" channel can steer agents.

**Pitfalls.**
- Gradients vanish through the clip, so loss rollouts are kept to 50 steps.
- Classic hand-found gliders mostly die on obstacles.

#### 2.1.6 Which Lenia-family patterns show which life-like properties

| Property | Pattern / world | How it was found |
|---|---|---|
| Individuality via collisions | Orbium (only the Orbidae family in original Lenia) | Interactive evolution, collider experiments |
| Individuality, common | Multi-kernel/multi-channel solitons; Sensorimotor agents | Semi-automatic search; IMGEP + gradient descent |
| Self-replication, incl. autocatalytic | Multi-kernel replicators; Aquarium VT049W (dt-sensitive) | Search + GA + human selection |
| Reproduction by collision | Some Sensorimotor agents | Emerged; not trained for |
| Emission, ingestion | Extended Lenia; 3D Snake | Semi-automatic search |
| Membrane/nucleus division of labor | Multi-channel solitons | Semi-automatic search |
| Differentiation (one genotype, many phenotypes) | Aquarium | Semi-automatic search |
| Division with food (heredity via parameter embedding) | Flow-Lenia (§2.2) | Random/manual search, evolutionary strategies, in-situ evolution |

#### 2.1.7 Ideas for us (Lenia family)

1. **Add a ring-kernel field to the RD code.** Add `U = K_β * u` (FFT is cheap). Reproduce Orbium at R=13, T=10 as a positive control before exploring new rules.
2. **Collider assay.** Run Chan's "particle collider" protocol: pairs of creatures at varied impact angles, with outcomes classified into the collision categories in §2.1.1. Use it as a standard **interaction/individuality assay** for any world that produces gliders.
3. **dt robustness.** Sweep dt for every discovered creature. Use survival over a dt range as a robustness score, so search does not reward discretization artifacts.
4. **Membrane/nucleus channels for soft containment.** Use one channel with narrow σ and an outer ring (β=[0,1]) as the shell, with cross-kernels coupling it to an inner channel.
5. **Replication positive control.** Use VT049W, with an explicit convention and dt, to test any heredity or replication detector.
6. **Death term.** Add a decay term (`−λA`) so replicators reach a steady population instead of saturating the grid. The paper notes that a birth–death balance can sustain a regenerating population.
7. **State-dependent rules from SmoothLife.** The cell-disk state m gates the birth/death intervals applied to annulus n. This cheaply gives RD fields different growth laws "inside" and "outside" a body, a primitive compartment.
8. **Asymptotic Lenia with our RK integrators.** It is an ODE, so adaptive stepping is valid.
9. **Kernel = sum of Yukawa kernels.** Instead of 40 explicit v_j fields, solve the screened-Poisson blurs spectrally: each `(1 − D_j∇²)^{-1}` is a diagonal multiply in Fourier space. Then search the α_j directly. This parameterization stays physically RD-interpretable.
10. **Turing intuition for kernels.** Use the KT-model equivalence to carry activator-range vs inhibitor-range intuition into ring-kernel design.
11. **Obstacle probe.** Add a fixed **obstacle field with strongly negative local growth** to every world as a standard perturbation probe.
12. **Differentiable tuning.** Use differentiable rollouts (the scout suggests JAX) plus the position-goal curriculum (§3.2) to tune RD+kernel worlds for motility under perturbation.

---

### 2.2 Flow-Lenia and parameter localization

**Citations.**
- E. Plantec, G. Hamon, M. Etcheverry, P.-Y. Oudeyer, C. Moulin-Frier, B. W.-C. Chan (2023), "Flow-Lenia: Towards open-ended evolution in cellular automata through mass conservation and parameter localization", *ALIFE 2023*, Best Paper Award (confirmed on the 2023.alife.org awards page). arXiv:2212.07906 (v2, 24 Mar 2023).
- Journal version: Plantec, Hamon, Etcheverry, Chan, Oudeyer, Moulin-Frier, "Flow-Lenia: Emergent Evolutionary Dynamics in Mass Conservative Continuous Cellular Automata", *Artificial Life* 31(2):228–248, 2025. doi:10.1162/artl_a_00471 (checked on Crossref). arXiv:2506.08569.
- Code (JAX): https://github.com/erwanplantec/FlowLenia. Videos: https://sites.google.com/view/flowlenia
- Follow-up: Michel, Cvjetko, Hamon, Oudeyer, Moulin-Frier, "Exploring Flow-Lenia Universes with a Curiosity-driven AI Scientist: Discovering Diverse Ecosystem Dynamics", arXiv:2505.15998 (v4, 2026; ALIFE 2025).

**Equations (ALIFE paper Eqs. 3–10; journal Eqs. 1–8).**
- **Kernels.**
  - Paper: `K_i(x) = Σ_{j=1..3} b_ij · exp(−(|x|/(r_i R) − a_ij)² / (2 w_ij²))`.
  - Code: `D = |x| / ((R+15)·r_i)`; `K_i = sigmoid(−10(D−1)) · Σ_j b_ij · exp(−(D−a_ij)² / w_ij)`, then normalized to sum to 1. The effective radius is **(R+15)·r**, not R·r.
- **Growth.** `G_i(u) = 2·exp(−(u−μ_i)² / (2σ_i²)) − 1`.
- **Affinity.** `U_j = Σ_i h_i · G_i(K_i * A_{c0_i}) · [c1_i = j]`. This is Lenia's growth field, reinterpreted as an affinity.
- **Flow.** `F_i = (1−α)·∇U_i − α·∇A_Σ`, with `α(p) = clip((A_Σ(p)/θ_A)^n, 0, 1)`.
  - `A_Σ = Σ_c A_c`. θ_A is a "critical mass".
  - n = 2 ("n > 1 so the affinity gradient dominates on a larger range of masses").
  - Gradients are taken with Sobel filters.
  - The `−∇A_Σ` term is a diffusion-like pressure. It switches on near θ_A and prevents collapse to a point.
- **Reintegration tracking** (Moroz 2020, semi-Lagrangian).
  - `A_i^{t+dt}(p) = Σ_{p'} A_i^t(p') · I_i(p', p)`.
  - `I_i(p', p) = ∫_{Ω(p)} D(p' + dt·F_i(p'), s)`.
  - D is a uniform square of side 2s (half-width s), Ω(p) is the unit cell, and s is a "temperature".
  - Total mass is conserved exactly. The state is unbounded (A ≥ 0); there is no [0,1] clip.
- **Parameter localization.**
  - A parameter map `P: L → Θ` (in the paper, the per-kernel weights h) enters as `U_j(p) = Σ_k P_k(p) · G_k(K_k * A)(p)`.
  - P moves with A under the same transport. Incoming parameters are mixed by one of these rules:
    - **Average** (Eq. 9): `P(p) = Σ A(p')I(p',p)P(p') / Σ A(p')I(p',p)`.
    - **Softmax sampling** (Eq. 10): `Prob[P(p) = P(x)] = exp(A(x)I(x,p)) / Σ_{p'} exp(A(p')I(p',p))`.
    - **Negotiation** (Michel et al.):
      - `Prob[P(x_dest) = P(x_src)] = exp(β·A(x_src)·I(x_src,x_dest)·V(x_src)) / Σ_x exp(β·A·I·V)`, with β = 100.
      - `V(x) = Σ_j Σ_i Q_i(x) · G_i(K_i * A_{c0_i})(x) · [c1_i = j]`.
      - Q is a second parameter map carried with the matter, used only for competition, not for the dynamics.
      - Negotiation gave the highest evolutionary activity of the rules tested. Averaging rules gave almost none.
  - **Mutation** adds Gaussian noise to P inside a random patch (a "beam").

**Reference parameters.**
- **Table 1** (10⁵ random sets; each starts from a 40×40 uniform-random patch):
  - R ∈ [2,25], r ∈ [0.2,1], μ ∈ [0.05,0.5].
  - σ ∈ [0.001,0.2] in the paper; [0.001,0.18] in code.
  - h ∈ [0,1] in the paper; [0.01,1] in the code's random ranges.
  - a, b ∈ [0,1]³; w ∈ [0.01,0.5]³.
  - s = 0.65, n = 2, dt = 0.2.
- **Code defaults:** 128×128 grid, dd = 5 (Chebyshev transport radius, i.e., maximum displacement), border = "wall".
- **θ_A.**
  - The paper gives no value.
  - `flowlenia.py` uses θ = C (channel count) and applies α per channel: `α = clip((A_c/C)², 0, 1)`.
  - `flowlenia_params.py` uses θ = 2.
- **Journal intrinsic-evolution setup:**
  - 3 channels, 5 kernels per channel pair (45 kernels), 5×10⁵ steps.
  - 10×10 mutation beam with noise from N(0,1).
  - p_mut, p_diss, p_food, r_decay and r_digest are not given numerically (UNVERIFIED).
- **Large ALIFE run:** 1024², 144 creatures/species, 200k steps, softmax sampling, a mutation every 500 steps.
- **Michel et al. settings:**
  - Ecosystem search: 256², 3 channels, 9 kernels, 10⁴ steps.
  - Mixing-rule comparison: 512², 45 kernels, 5×10⁵ steps.

**Local check** (flow-particle scout, numpy):
- Reintegration tracking conserves mass to a relative error of 4e-16, even with random flows of std 8.
- Flow-Lenia, 1 channel, 128², 300 steps, parameters drawn from the Table 1 ranges (4 seeds):
  - mass error ≈ 1e-13;
  - patterns stayed localized, with 6–15% of cells occupied vs 9.8% for the starting patch.

**Numpy core** (checked for mass conservation; torus):
```python
def rt(A, F, dt=0.2, s=0.65, dd=5):          # A:(X,Y) F:(X,Y,2) in cells/time
    D = np.clip(dt*F, -(dd-s), dd-s); out = np.zeros_like(A)
    for dx in range(-dd, dd+1):
        for dy in range(-dd, dd+1):
            ox = np.clip(0.5+s-np.abs(D[...,0]-dx), 0, min(1, 2*s))
            oy = np.clip(0.5+s-np.abs(D[...,1]-dy), 0, min(1, 2*s))
            out += np.roll(A*ox*oy/(4*s*s), (dx, dy), axis=(0, 1))
    return out
# step: U = sum_k h_k*G_k(ifft(fK_k*fft(A))); alpha = clip((A_sum/theta)**2, 0, 1)
#       F = (1-alpha)*sobel(U) - alpha*sobel(A_sum); A = rt(A, F)
```
To transport P with stochastic mixing, compute each of the 121 source contributions `A*ox*oy/(4s²)` separately. At each target cell, draw the source index from a categorical with probability ∝ mass, or use a softmax.

**Phenomena.**
- **Random search.**
  - Most parameter sets give spatially localized patterns, because mass cannot vanish or explode. Plain Lenia with the same parameters mostly empties or explodes (Fig. 3).
  - Patterns include gyrating patterns, snake-like movers, dividing and merging dots, and multi-channel modular creatures.
- **Temperature s.** Varying s gives distinct phases. Patterns near the boundary between the Turing-like phase and the equilibrium phase were more dynamic, which the authors read as a possible critical regime.
- **Optimization.**
  - OpenES (evosax), population 16, Adam with learning rate 0.01.
  - Directed-motion fitness: centre-of-mass displacement, `f(θ) = dist(φ(A0), φ(A400))`.
  - Obtained directed motion, rotation, obstacle navigation and chemotaxis. Lenia under the same optimization gave only exploding patterns.
- **Multi-species.**
  - Species took over large regions; multi-species coexistence and evolution.
  - **Symbiosis:** one parameter set forms a membrane around a nucleus with different parameters (Fig. 6e).
  - **Division events when food is added** (Fig. 6f).
- **Journal results.**
  - Parameter trajectories branch and go extinct like a phylogeny.
  - Evolutionary activity falls with mutation rate as a power law: γ = −0.5 for non-neutral activity, −0.71 for count-based.
  - Dissipation and food raise raw activity but not activity per unit mass.
  - Activity metrics are in §4.6.
- **Michel et al. (IMGEP vs random search).**
  - Pairwise goal distance 0.874 vs 0.476.
  - Non-empty bins 576 vs 205.
  - EA 3.44e3 vs 1.70e3.
  - Unique parameter sets at the longest horizon rose from 46.5 (256²) to 181.5 (1536²).
  - Qualitative phenomena: colonies, feeding-like behaviour, fragmentation into fast movers, dynamics resembling allopatric speciation.
  - No LLM or VLM judge was used.

**Pitfalls (from the code).**
- **Displacement limit.** `|dt·F|` must stay ≤ dd − s (4.35 cells). The code clips F to this; mass sent further would be lost.
- **Gradient scale.** The Sobel filter is unnormalized and returns about 8× the derivative. Keep this if you want to match published behaviour.
- **Edges.** The code's `convolve2d(mode='same')` zero-pads, while the transport can wrap as a torus. Use periodic gradients in a periodic world.
- **Fixed random key.** The official stochastic mixing calls `jax.random.PRNGKey(42)` on every step, so the "random" choices repeat each step. Pass a fresh key.
- **Mixing rules differ from the paper.**
  - The code's `stoch` mode samples with probability ∝ incoming mass (logits = log mass).
  - The paper's Eq. 10 is a softmax over exp(A·I).
  - The code's `softmax` mode is an exp-weighted average, not sampling.
- **Cost.** Each step does (2dd+1)² = 121 roll-multiply operations per channel. On a T4 GPU, 128² with 10 kernels took 255 µs per step.
- **No growth or death.** Mass is conserved, so nothing can grow or die. Reproduction and turnover need food or decay sources (the journal's "food" model), or a creature that splits. The temperature s controls dispersal.

**Ideas for us (Flow-Lenia).**
1. **Flow-Lenia transport for our RD models**, the most direct "beyond diffusion" fix for soft boundaries.
   - Keep the reaction terms R(u), but replace `D∇²u` with flow: use `U = R(u)` (or `K*u`) as the affinity, set `F = (1−α)∇U − α∇u_Σ`, and move mass with `rt()`.
   - Mass conservation plus the α pressure gives sharp, incompressible edges.
   - Sweep s ∈ [0.3, 1.0] and θ_A ∈ {1, 2, C}; the paper reports phase changes in s.
   - Measure interface width against plain RD.
2. **A heritable genome field.**
   - Carry reaction-rate fields P(x) with the matter, using stochastic or negotiation mixing (β = 100) and 10×10 mutation beams.
   - Add a food field (matter decay at rate ρ_decay plus food patches) so growth and division are possible.
   - Score runs with the journal's non-neutral evolutionary activity and with Michel et al.'s EA, MP4 size and multi-scale entropy (§4.6) as cheap judges before calling a VLM.
3. **Two-channel membrane test.** Use cross-kernels so channel B's affinity peaks on the ring where channel A's gradient is large (B's kernel a ≈ 0.8–1.0 applied to A). Check whether B wraps A, as in the symbiosis case (Fig. 6e).

---

### 2.3 Particle Lenia and particle-life

#### 2.3.1 Particle Lenia

**Citation.** Mordvintsev, Niklasson, Randazzo (Google Research), "Particle Lenia and the energy-based formulation", blog post, 23 Dec 2022. https://google-research.github.io/self-organising-systems/particle-lenia/

**Equations (verbatim from the article).**
- `U(x) = Σ_i K(||x − p_i||)`, with `K(r) = w_K · exp(−(r − μ_K)² / σ_K²)`. There is **no factor of 2** in the exponent.
- `G(u) = exp(−(u − μ_G)² / σ_G²)`.
- `R(x) = (c_rep/2) · Σ_{i: p_i ≠ x} max(1 − ||x − p_i||, 0)²`.
- `E = R − G`.
- **Local rule:** `dp_i/dt = −∇E(p_i)`. Each particle descends the field created by the others. There is no momentum ("viscous medium").
- **Global alternative:** descend `E_total = Σ_i E(p_i)`. It reaches lower energies but gives less diverse structures; the authors use the local rule.
- **w_K normalizes ∫K = 1.** The `calc_K_weight` function uses the trapezoid rule over μ ± 4σ, with area factor 2π in 2D and 4π in 3D.

**Analytic gradient for numpy.**
- Define `r_ij = |p_i − p_j|` and `e_ij = (p_i − p_j)/r_ij`.
- `∇U_i = Σ_j w_K · k_ij · (−2(r_ij − μ_K)/σ_K²) · e_ij`, where `k_ij = exp(−((r_ij − μ_K)/σ_K)²)`.
- `∇G_i = G_i · (−2(U_i − μ_G)/σ_G²) · ∇U_i`.
- `∇R_i = −c_rep · Σ_j max(1 − r_ij, 0) · e_ij`.
- `dp_i/dt = ∇G_i − ∇R_i`.
- Mask the diagonal (i = j) explicitly, because inf·0 gives NaN.

**Reference parameters.**
- **2D rotor:**
  - μ_K = 4.0, σ_K = 1.0, w_K = 0.022, μ_G = 0.6, σ_G = 0.15, c_rep = 1.0.
  - 200 particles, initialized uniform(−6, 6)², JAX key 20.
  - Euler, dt = 0.1, 10,000 steps.
  - Result: it "ends up in a spinning attractor".
- **3D glider:** `create_params(4.3, 1.1, 0.23, 0.06, 1.0, dim_n=3)`, 256 particles, dt = 0.2, 15,000 steps. Result: a mushroom-shaped glider that slowly drifts.
- **Upscaling to 800 particles:** μ_K×2, σ_K×2, w_K/4, dt×2.
- **ASAL search space:** six log-scaled parameters around these values, `p = exp(z + log p₀)`.
- **Division and multiple types** are not reported in the article. It calls per-particle parameters a "trivial" extension left for future work.

**Local check** (flow-particle scout): with the published parameters, mean energy settled at about −0.70. A different numpy seed gave a slowly drifting blob, not a clean rotor, so the rotor depends on the initial condition.

**Pitfalls.**
- The rotor is "quite sensitive to small perturbations" and can fall into a lower-energy attractor.
- Scaling w_K while dividing μ_G and σ_G by the same factor changes nothing. Fix w_K by normalization.
- Cost is O(N²) without a cell list.
- The local rule does not obey action = reaction. This is the source of motility, but also of centre-of-mass drift.
- Lead only: an APS March Meeting 2025 abstract, "Learning and Adaptation in Particle Lenia", adds multiple species as an environment. No full paper was found.

#### 2.3.2 Particle Life / Clusters (asymmetric multi-species forces)

**Citations.**
- J. Ventrella, *Clusters* (around 2016); page last updated February 2025: https://ventrella.com/Clusters/intro.html
  - Per species pair: piecewise-linear force fields with thresholds r1, r2, f1 ≤ 0, f2 and an optional taper.
  - Response delays of 0–5 steps.
  - The forces are explicitly asymmetric, which breaks Newton's third law.
- T. Mohr, *Particle Life* (begun 2018). Library: https://github.com/tom-mohr/particle-life. App: https://github.com/tom-mohr/particle-life-app (Java).

**Mohr's force function** (verbatim from particle-life-app `Main.java`). Let `r̂ = |x_j − x_i| / rmax` and `β = 0.3`.
- `F(r̂, a) = r̂/β − 1` if `r̂ < β`. This is universal repulsion, independent of type.
- `F(r̂, a) = a · (1 − |1 + β − 2r̂| / (1 − β))` if `β ≤ r̂ ≤ 1`. This is a triangle bump peaking at a when `r̂ = (1+β)/2`.
- `F = 0` otherwise.
- The force acts along the unit vector toward the neighbour; positive a means attraction.

**Update order (`Physics.java`).**
1. `v_i ← v_i · friction^(60·dt)`.
2. `v_i += rmax · forceScale · dt · Σ_j F(r̂_ij, M[type_i, type_j]) · ê_ij`.
3. `x_i += v_i · dt`.

**Defaults.** World [−1, 1] with wrapping; rmax = 0.02; friction = 0.85 (normalized to 60 fps); dt = 0.02; force = 1; 6 types; `M_ij ~ U(−1, 1)`.

**ASAL variant (SakanaAI/asal `plife.py`).**
- World: [0, 1] torus, N = 5000, 6 types.
- Per type: β = 0.3, mass = 0.1, half_life = 0.04, rmax = 0.1. dt = 0.002.
- Update: `v ← 0.5^(dt/half_life) · v + dt · Σ_j rmax · F(r/rmax) · ê / m`, then `x ← (x + v·dt) mod 1`.
- ASAL searches the K×K matrix (mapped to [−1.5, 1.5]) and the per-type β.

**Phenomena.**
- Chasing and fleeing, self-propelled clusters, "super-organisms" that shapeshift, split and merge, and fluid-like behaviour in dense regions (Ventrella).
- ASAL found a "caterpillar" from a text prompt; the green–yellow interaction strength mattered most. It needs a particle count above a threshold whose exact value is garbled in the HTML (UNVERIFIED).
- Cell-like membranes are not documented as a standard phenomenon (UNVERIFIED).

**Pitfalls.**
- An asymmetric M injects energy, and friction is the only damping. A large `dt·rmax·force` makes the system explode.
- The core repulsion is linear and soft, so particles can overlap at high density.
- Use a cell list with cell size = rmax.

#### 2.3.3 Primordial Particle System (PPS): the best-documented particle "cells with division"

**Citations.**
- Schmickl, Stefanec, Crailsheim, "How a life-like system emerges from a simple particle motion law", *Scientific Reports* 6:37969 (2016). doi:10.1038/srep37969. Correction: 7:42454.
- Preprint arXiv:1512.04478. 3D version: arXiv:1901.09293.

**Equations (verbatim).**
- `Δφ/Δt = α + β · N_{t,r} · sign(R_{t,r} − L_{t,r})`.
- `p_{t+1} = p_t + (cos φ_t, sin φ_t) · v`.
- L and R count neighbours within r in the left and right half-discs relative to the heading; `N = L + R`.

**Parameters.**
- r = 5, α = 180°, β = 17°, v = 0.67.
- Density ≈ 0.08 particles per unit area (5000 particles in a 250×250 torus).
- Asynchronous updates in random order; float64.

**Phenomena (quantified).**
- **Life cycle sizes.**
  - Spores of about 18 particles (16–21) germinate into cells at about 23 particles.
  - Cells average about 48 particles and have a dense core, an empty interior and a dense outer "membrane" ring.
  - Cells divide at about 61 particles.
- **Population growth is logistic.**
  - Growth rates: 7.1e-4 per step for cells, 4.0e-4 per step for spores.
  - Carrying capacities: about 18.2 for spores, about 50.8 for cells.
- Free particles act as nutrients and are released when a cell dies.
- **Colour classification** by the neighbour count N within r = 5:
  - blue: 15 < N ≤ 35
  - yellow: N > 35
  - brown: 13 ≤ N ≤ 15
  - magenta: more than 15 neighbours within r = 1.3
  - green: everything else

**Pitfalls.**
- sign(0) = 0 when L = R.
- Results are density-sensitive and were obtained with asynchronous updates. Behaviour under synchronous updates is UNVERIFIED.

#### 2.3.4 Other particle systems with membranes or replication

- **Cabaret, T.**, "Emergence of autopoietic vesicles able to grow, repair and reproduce in a minimalist particle system", arXiv:2311.10761 (v2, July 2024). Video: https://www.youtube.com/watch?v=JmCN_4jTwf8
  - **Particle types and reactions.** Four types: precursor, catalyst, intermediary, surfactant. Two reactions: `P + Cat → Int` and `P + Int → Cat + Surf`.
  - **Surfactant potential.** Surfactants are oriented. The potential is lowest side by side at a slight angle, which builds in curvature. Head-to-head antiparallel contact is repulsive, which favours fission over fusion.
  - **Dynamics.** Dissipation plus Brownian noise, with momentum conserved.
  - **Result.** Vesicles form, take up catalyst, grow by internal metabolism, repair themselves, and divide when large.
  - **Evidence.** The force equations, numbers and code URL were not on the page (C++ on a GitHub "arxiv" branch; UNVERIFIED). Evidence is qualitative only.
- **Hutton, T. J.**, "Evolvable Self-Reproducing Cells in a Two-Dimensional Artificial Chemistry", *Artificial Life* 13(1):11–30 (2007).
  - Squirm3-style bonded atoms. Cells carry genetic material that encodes enzymes, the enzymes catalyze reactions, and the cells reproduce.
  - Rule details: UNVERIFIED.
- **ALIEN** (C. Heinemann), https://github.com/chrxh/alien, BSD-3.
  - A CUDA particle engine: bonded particles form soft bodies; free particles act as fluid.
  - 15 cell types, a neural net per cell, and genome-driven constructors that give self-replication with evolvable mutation rates.
  - First prize, ALIFE 2024 Virtual Creatures Competition.
- **Neural Particle Automata.** Kim, Pajouheshgar, Süsstrunk, Jakob, Park, arXiv:2601.16096 (Jan 2026).
  - Updates: `S_i += δ·ΔS_i` and `x_i += δ·Δx_i`, with `δ ~ Bernoulli(0.5)`.
  - Perception uses SPH operators:
    - Poly6 kernel `W = (4/(πε⁸))(ε² − r²)³`.
    - Spiky gradient `W∇ = (10/(πε⁵))(ε − r)²·r̂`.
    - Smoothed state, density gradient, and a gradient corrected with the moment matrix `M_i⁻¹`.
    - The perception output feeds an MLP.
  - Shows regeneration and persistent internal vortices. It cannot split or merge particles.
- **Swarm Chemistry** (Sayama 2009; "Seeking Open-Ended Evolution in Swarm Chemistry", IEEE ALIFE 2011).
  - Each particle has a kinetic recipe (R, Vn, Vm, c1–c5). Recipes pass between particles locally, particles differentiate stochastically, and recipes mutate.
  - Cooperation among particles was essential for lasting macro-structures.
  - Exact rule constants and rates: UNVERIFIED (the PDF returned 403).
- Lattice and particle autopoiesis models (SCL, Ono & Ikegami) are in §2.7.

#### 2.3.5 Ideas for us (particles)

1. **Typed Particle Lenia with division.**
   - Per-type (μ_G, σ_G) and per-type-pair kernels.
   - A particle duplicates when it is food-limited and G_i exceeds a threshold. The daughter inherits the parent's type and parameters plus noise.
   - Start every type from the published (4, 1, 0.022, 0.6, 0.15, 1).
2. **PPS as a ground-truth benchmark for the judge pipeline.** PPS has documented spores, cells, and division at about 61 particles, with counts. Run it first and check that our VLM/LLM judges and DBSCAN-based individual tracking recover the division events and the logistic growth.
3. **Particle Life with a VLM judge (ASAL-style).**
   - Optimize M and β against prompts such as "a cell with a membrane dividing in two".
   - Let an LLM propose structured edits to M as a mutation operator, e.g., "make type 3 attract type 1 while type 1 flees type 3" to create a chaser pair.
   - Add Cabaret-style reaction rules (type conversion on contact) to get metabolism.

---

### 2.4 Active emulsions: Cahn-Hilliard + reaction

#### 2.4.1 Active droplets that grow and divide (Zwicker et al.)

**Citation.** Zwicker, Seyboldt, Weber, Hyman & Jülicher, "Growth and division of active droplets provides a model for protocells", *Nature Physics* 13, 408–413 (2017), doi:10.1038/nphys3984; arXiv:1603.01571. Background review: Weber, Zwicker, Jülicher & Lee, "Physics of Active Emulsions", arXiv:1806.09552.

**Equations (supplement, eqs S.1–S.5).**
- Free energy density: `f(c) = b/(2Δc²) (c − c₋⁰)² (c − c₊⁰)²`.
- Free energy: `F = ∫ [f + (κ/2)|∇c|²]`.
- Chemical potential: `μ = b/Δc² (c−c₊⁰)(c−c₋⁰)(2c−c₋⁰−c₊⁰) − κ∇²c`.
- Dynamics: `∂t c = m∇²μ + s(c)`.
- **Reaction rate, piecewise linear:**
  - `s = ν₊ − k₊(c − c₊⁰)` for `c < c_c⁺`;
  - `s = −ν₋ − k₋(c − c₋⁰)` for `c > c_c⁻`;
  - a cubic `p(c)` in between, with s and s' continuous.
  - The minus signs were lost in PDF extraction of eq S.5. The scout restored them from the effective-model eq S.13.

**Physics.**
- B → A turnover inside the droplet plus fuel-driven A → B production outside gives a supersaturation `ε = ν₊/(k₊Δc)`. The resulting flux destabilizes the spherical shape (a Mullins-Sekerka-like instability).
- Derived scales:
  - interface width `w = 2(κ/b)^½`;
  - surface tension `γ = (Δc)²√(κb)/6`;
  - diffusivity `D = m·b`;
  - time unit `t0 = w²/D`.

**Published parameters** (nondimensionalized by Δc, w and t0).
- `c₊⁰ = 0`, `c₋⁰ = 1`, `k± t0 = 10⁻²`.
- Fig. 1C: `ν₋t0/Δc = 7·10⁻³`, `ν₊t0/Δc = 1.9·10⁻³`.
- **Stability diagram:**
  - `c_c⁺ = 0.25`, `c_c⁻ = 0.75`.
  - Axisymmetric box 60w × 30w, 120 × 60 points; run time `T = 10⁴ t0`.
  - Initial condition: a prolate ellipsoid with half-axes `R/w ± 0.1`, `R ≈ 0.9·R̄s`, built with a tanh profile.
- **Multiple divisions (Fig. 3):**
  - 3D cube, `L = 50w`, 100³ points (`dx = w/2`).
  - `ν₋ = 7·10⁻³`, `ν₊ = 2·10⁻³`, `c_c± = 0.5`.
  - Start from one sphere at `(L/4, L/4, L/4)`.
- **Scheme:** xmds2, adaptive RK4/5 (tolerance 10⁻⁵), spectral Laplacian, no-flux boundaries.

**Simple choice for our simulator.**
- Set `b = Δc = 1`, `κ = 0.25` (so `w = 1`) and `m = 1` (so `t0 = 1`).
- Explicit dt would be about 0.005, so reaching 10⁴ t0 takes about 2·10⁶ steps.
- The semi-implicit spectral step (§2.0) with `S ≈ 1` permits dt of order 0.1.

**Phenomena (simulated).**
- Droplets grow to a size `R_div` and divide; daughters grow again and divide repeatedly.
- Successive division axes come out perpendicular, which the authors attribute to diffusive interactions between droplets.
- Ostwald ripening is suppressed, giving a size-selected emulsion.
- Near the instability, dynamics slow down, and some cases did not divide within the simulated time.

**Hydrodynamics follow-up.** Seyboldt & Jülicher, arXiv:1803.03425 (2018; *New J. Phys.* venue UNVERIFIED).
- Stokes flow stabilizes spheres. Division survives at stronger driving, at higher droplet viscosity (`F = wη₋/(γτ)`), or at lower surface tension.
- Oil-in-water droplets (`F ≈ 0.1`) are unlikely to divide; p-granule-like liquids (`F ≈ 10–10⁴`) might.
- 3D Cahn-Hilliard check: `L/w = 100`, N = 128, `R₀ = 7w`, `k t0 = 10⁻²`, `ν t0 = 2·10⁻³`, `T = 4·10³ t0`.

**Pitfalls.**
- A seed below the critical nucleus size dissolves.
- Boundaries bias the division axis.
- You need `dx ≤ w/2`.
- Reactions in a thin interface are badly resolved if w is too large relative to R.
- **No heredity:** all droplets converge to one attractor.

#### 2.4.2 Cahn-Hilliard with linear reactions = Ohta-Kawasaki (arrested coarsening, size selection)

**Citations.**
- Glotzer, Di Marzio & Muthukumar, "Reaction-controlled morphology of phase-separating mixtures", *PRL* 74, 2034 (1995).
- Li & Cates, "Non-equilibrium phase separation with reactions: a canonical model and its behaviour", *J. Stat. Mech.* 053206 (2020), arXiv:2001.02563.
- Ohta & Kawasaki, *Macromolecules* (1986).
- Xu & Zhao, arXiv:1811.11306 (*J. Sci. Comput.*).

**Canonical "Model AB" (Li & Cates).**
```
∂tφ = ∇²μ_B − M_A μ_A + noise
μ_B = −αφ + βφ³ − κ∇²φ
μ_A = u(φ − φ_a)(φ − φ_t)
```
- When `μ_A − μ_B` is linear in φ, the dynamics map exactly onto an equilibrium free energy with a screened-Coulomb nonlocal term `∝ ∫ |φ(q)|²/(q² + m²)`, where `m² = M_A/M_B`. This is the Ohta-Kawasaki block-copolymer functional.
- Linear spinodal growth rate: `σ(q) = α̃q² − κq⁴ − ũ`.
- Glotzer et al.'s A ⇌ B reaction with linear rates belongs to this class; their exact coefficients are UNVERIFIED.
- **Wavelength scaling.** Glotzer reports `L ~ (M_A u)^(−1/4)` at larger rates and `−1/3` as the rate goes to 0. Li & Cates' 1D data fit about `−1/4`.

**Droplet splitting parameters (Li & Cates, Fig. 9).**
- `φ_t = −0.6`, `φ_a = −10`, `uM_A = 4·10⁻⁵`, `α = β = 0.2`, `κ = 1`, noise `ε = 0.01`, periodic boundaries.
- Binodals at ±1; interface width ≈ `(2κ/α)^½ ≈ 3`.
- Scheme: pseudospectral, 2/3 dealiasing, explicit Euler-Maruyama.
- **Outcome:** the reactions set the droplet radius. Droplets stretch and split, and droplet number depends on noise through nucleation.

**Ohta-Kawasaki bubble assemblies (Xu & Zhao).**
- Energy: `E = ∫ ε/2|∇φ|² + W(φ)/ε + γ/2 ∫ |(−Δ)^(−½)(f(φ) − ω)|² + M/2 (∫f − ω|Ω|)²`.
- `W = 18(φ² − φ)²` and `f = 6φ⁵ − 15φ⁴ + 10φ³`.
- Domain `[−1, 1]²`, 512² points, `ε = 10h` (h = 1/256), `ω = 0.15`, `M = 1000`.
- Stabilizers `κ_h = 2000`, `β_h = 2`; `dt = 5·10⁻³`.
- **Outcome:** bubble count `K_b = 2, 5, 13, 23, 60` for `γ = 200, 500, 2000, 5000, 20000`, so `K_b ~ γ^(2/3)`. Bubbles finish as a hexagonal array.

**Pitfalls.**
- The equilibrium mapping means no sustained dynamics: the system settles into static patterns. Cycles need nonlinear reactions or a second field.
- `(−Δ)⁻¹` needs the mean (zero mode) removed.

#### 2.4.3 Enzyme condensates that move and divide (Frey group)

**Citation.** Demarchi, Goychuk, Maryshev & Frey, *PRL* 130, 128401 (2023), arXiv:2301.00392.

**Equations.**
- Condensate: `∂t c = ∇·[Mc∇(μ₀ + χ_s s + χ_p p)]`, with `μ₀ = −r(c − c̃) + u(c − c̃)³ − κ∇²c`.
- Substrate: `∂t s = D∇²s − k₁cs + k₂p`.
- Product: `∂t p = D∇²p + k₁cs − k₂p`.

**Parameters.**
- `c₋ = 0.1c₊`, `w = 0.1l₀`, `R = l₀`, `L = 5l₀`, `M = 100D/ε₀`.
- `k₁ = k₂/c₊`, `χ_s = −0.05r`, `χ_p = −0.01r`, `s + p = c₊`.
- The extraction shows `w = 2κ/r`; this is probably `√(2κ/r)`.

**Behaviour.**
- The condensate first centres. Above a mobility threshold it self-propels and oscillates.
- Coarsening is interrupted.
- It divides in 3D.

This is the most direct template for "reaction-diffusion chemistry gives a sharp-bounded body that swims".

#### 2.4.4 Ideas for us (active emulsions)

1. **Make our chemistry own a dividing body.** Make the droplet material B the product of our existing RD chemistry (`s(c, u, v)`), giving it a phase-separating field with κ∇⁴.
2. **Heredity test.** Use two droplet species, or a second conserved field that partitions into droplets, as a heritable composition variable. Measure the parent–daughter correlation of composition.
3. **Judge calibration set.** Sweep `(ν₊, ν₋)` around (2, 7)·10⁻³ and classify outcomes as dissolve, stationary, divide or chaotic.
4. **Cheapest size selection.** Add `−Γ(c − c̄)` to any conserved field and use γ to dial individual size. Make Γ depend on an RD species to get metabolism-controlled cell size.
5. **Frey-type χ coupling.** Give our RD species a Flory-Huggins affinity χ to a Cahn-Hilliard body field. That gives self-propulsion for free.

---

### 2.5 Membranes and vesicles

#### 2.5.1 Functionalized Cahn-Hilliard (FCH): amphiphilic bilayers, pores, micelles, pearling

**Citations.**
- Promislow group, e.g., Kraitzman & Promislow, arXiv:1711.00396; Doelman, Hayrapetyan, Promislow & Wetton (single-curvature bilayers).
- Numerics: Feng, Wang, Wise et al., arXiv:1610.02473 (*J. Sci. Comput.* 76, 2018).

**Energy.**
- **Promislow form.**
  - `F = ∫ ½(ε²Δu − W'(u))² − ε^p(ε²η₁/2|∇u|² + η₂W(u))`.
  - W has unequal wells. `p = 1` is strong functionalization; `p = 2` is weak.
  - Flow: `u_t = Δμ`, with `μ = (ε²Δ − W'' + εη₁)(ε²Δu − W') + εη_d W'` and `η_d = η₁ − η₂`.
- **Feng et al. form.**
  - `F = ε⁻²/2 ∫ μ₀² − η F₀`, with `μ₀ = φ³ − φ − ε²Δφ`.
  - Sixth-order flow: `∂tφ = ∇·(M∇μ)`.
  - `η > 0` gives FCH; `η < 0` gives Cahn-Hilliard-Willmore.

**Published parameters (Feng et al.).**
- `ε = 0.1`, `η = 1`, `L = 12.8`, 256² points, `dt = 10⁻⁴`, stabilizer `A = 1`.
- Initial condition: `φ = 0.5 ± 0.05` noise.
- Result: an amphiphilic micelle/bilayer network.
- A second benchmark uses `ε = 0.18`, `L = 6.4`.

**Phenomena.**
- Bilayers are codimension-1 structures; filaments are codimension-2.
- **Pearling:** fast O(ε) width oscillations of a bilayer.
- **Meander:** slow O(ε⁻¹) lengthening driven by the far-field chemical potential.
- In other words, the amount of free amphiphile controls whether membranes grow or pinch.

**Pitfalls.**
- Explicit stepping is limited to `dt ~ h⁶`. Use convex splitting or implicit spectral steps.
- Behaviour is very sensitive to the far-field chemical potential (i.e., to mass).

#### 2.5.2 Phase-field vesicles with Helfrich bending energy

**Citations.**
- Du, Liu & Wang, *J. Comput. Phys.* 198, 450–468 (2004). Citation verified; full equations not retrieved.
- Lowengrub, Rätz & Voigt, "Phase-field modeling of the dynamics of multicomponent vesicles: spinodal decomposition, coarsening, budding, and fission", *PRE* 79, 031926 (2009).

**Equations (Lowengrub, Rätz & Voigt).**
- Bending energy: `F_B = ½∫ ε⁻¹ b_N(u)[εΔφ − ε⁻¹G'(φ) + 6φ(1−φ)H₀(u)]²`, with `G = 36φ²(1−φ)²`.
- Variation with constant `b_N` and `H₀ = 0`: `δF_B/δφ = Δω − ε⁻²G''ω`, with `ω = εΔφ − ε⁻¹G'`.
- Area functional: `A[φ] = ∫ (ε/2|∇φ|² + ε⁻¹G)`. Volume: `V = ∫φ`.
- Penalties: `M_V/2 (V − V₀)²` and `M_A/2 (A − A₀)²`, with `M_V = 10⁴`, `M_A = 10³`.
- Line energy between surface phases: `∫(ε/2|∇φ|² + ε⁻¹G)(δ/2|∇u|² + δ⁻¹W(u))`.
- φ evolves by relaxation (non-conserved). The surface concentration u is conserved.
- Scheme: semi-implicit adaptive finite elements; only the nonlocal V and A terms are explicit.

**Phenomena.** Spinodal decomposition on the membrane, budding, and fission, even in 2D. Examples use `H₀(−1) = 2`, `H₀(1) = 5`.

**Pitfalls.**
- There is no self-assembly: you must start from a vesicle.
- Topology changes depend on ε, not on physics.

#### 2.5.3 Gompper-Schick amphiphile Ginzburg-Landau model

**Citations.** Gompper & Schick, *PRL* 65, 1116 (1990). Schmid review: arXiv:cond-mat/9811070. Gozdz & Holyst: arXiv:cond-mat/9604003.

**Correction to a common assumption.** The well-known Gompper-Schick model has ONE order parameter, the oil–water difference. The amphiphile concentration enters only through the sign of `g(φ)`. Two-order-parameter versions (oil–water difference plus amphiphile density) come from other groups.

**Functional.**
- General form: `F = ∫ [c(Δφ)² + g(φ)(∇φ)² + f(φ)]`.
- Gozdz & Holyst form: `|Δφ|² + (g₂φ² − g₀)|∇φ|² + (φ²−1)²(φ² + f₀)`.
  - `g₀ > 2` gives periodic ordered phases: lamellar, plus metastable triply-periodic minimal surfaces.
  - Parameters used: `g₀ = 3`, `f₀ = 0`, `g₂ ≈ 4√(1+f₀) + g₀ + 0.01`. The g₂ formula was reconstructed from garbled extraction (UNVERIFIED).

**Operator.** A negative gradient coefficient plus a positive `(Δφ)²` term gives a finite-wavelength preference. The mechanism is Swift-Hohenberg-like, and membranes appear as interfaces. It is cheap to add as a fourth-order conserved flow. The PDE scout ranks it below FCH for closed vesicles.

#### 2.5.4 Membranes elsewhere in this file

- Lenia: membrane/nucleus channel division of labor (§2.1.2).
- Flow-Lenia: a symbiotic membrane around a nucleus (§2.2).
- PPS: a dense outer ring (§2.3.3).
- Cabaret: surfactant vesicles (§2.3.4).
- Ono & Ikegami, and SCL: chain membranes (§2.7).

#### 2.5.5 Ideas for us (membranes)

1. **Field-theoretic chemoton container.** Couple u (FCH) to an RD "metabolism" that produces amphiphile only inside closed membranes.
2. **Pearling as division.** Raise the internal amphiphile supply and check whether vesicles bud.
3. **Helfrich skin.** Use the phase-field Helfrich vesicle as the skin of an RD world. Let a surface species u change H₀ (spontaneous curvature) and see whether the chemistry drives budding.

---

### 2.6 Chemotaxis, cross-diffusion and active matter

#### 2.6.1 Keller-Segel and volume filling

**Citations.**
- Hillen & Painter, "A user's guide to PDE models for chemotaxis", *J. Math. Biol.* 58, 183–217 (2009).
- Painter & Hillen (2002), volume filling. The venue, *Can. Appl. Math. Q.*, is from the scout's memory.

**Models.**
- Minimal (M1): `u_t = ∇·(D∇u − χu∇v)`, `v_t = ∇²v + u − v`.
- Volume filling (M3a): replace `χu` with `χu(1 − u/γ)`.
- Cell kinetics (M8): add `ru(1−u)`.

**Published parameters.**
- **1D:** `D = 0.1`, `χ = 5`, 201 points on [0, 1]. Critical values: `γ* = 1.277` (patterns for γ > γ*); `r* < 3.553`.
- **2D unit square:** M1 blows up; M3–M8 reach a steady state.
- **Combined model (Fig. 4):**
  - `α = 0.5`, `γ = 10`, `n = 1`, `φ = 1`, `D = 0.1`, `χ = 5`.
  - 20 × 20 domain; initial state `u = 1`, `v = 1 + 1%` noise.
  - Peaks merge and coarsen.
  - Adding `r = 0.1` gives continual peak collision and new peak emergence: births and deaths of aggregates.
- **3D (M3a):** `γ = 10`, 41³ points; spherical aggregates.

**Operator.** Nonlinear anti-diffusive advection. Volume filling caps density, so aggregates become plateaus with steep edges: sharp-edged blobs, but without surface tension.

**Pitfalls.**
- M1 blows up in finite time in 2D.
- Use upwind or flux-limited finite-volume advection, and preserve positivity.
- CFL limit: `dt < dx / (χ max|∇v|)`.

**Cross-diffusion.** The Shigesada-Kawasaki-Teramoto model (1979) gives segregated domains (parameters UNVERIFIED).

#### 2.6.2 Active Model B+ (AMB+)

**Citation.** Tjhung, Nardini & Cates, *PRX* (2018), arXiv:1801.07687.

**Equations.**
- Dynamics: `∂tφ = −∇·J + √(2D)Λ`.
- Current: `J = −∇(δF/δφ + λ|∇φ|²) + ζ(∇²φ)∇φ`.
- Free energy: `F = ∫ −(A/2)φ² + (A/4)φ⁴ + (K/2)|∇φ|²`.
- The ζ term creates a nonlocal chemical potential. This gives reverse Ostwald ripening and microphase separation.

**Parameters.**
- `A = 0.25`, `K = 1`.
- Region B (example `ζ = −4`, `λ = −1`): reverse Ostwald ripening for dense droplets, giving a cluster phase.
- Region C: reverse Ostwald ripening for bubbles.
- Finite-noise runs use `(ζ, λ) = (4, 1)` and `(1, −0.5)` with `D = 0.2`.
- Numerics: 192² grid, `dt = 10⁻³`, `dx = 1`, 8th-order finite differences, Itô–Euler integration.

**Outcome.** Size-selected droplets without any chemistry.

#### 2.6.3 Active Model H / polar active droplets

**Citation.** Tjhung, Marenduzzo & Cates, *PNAS* 109, 12381 (2012); arXiv:1211.4707.

**Equations.**
- Free energy: `F = ∫ V(c) + k/2|∇c|² − α/2 ((c−c_cr)/c_cr)|P|² + α/4|P|⁴ + κ/2(∇P)² + βP·∇c`.
- Concentration: `∂t c + ∇·(c(v + wP) − M∇δF/δc) = 0`.
- Polarization relaxes with rate `1/Γ`.
- Flow: Navier-Stokes plus friction γv, with active stress `ζ̄cPP`.

**Lattice-Boltzmann parameters.** `η = 5/3`, `κ = 0.04`, `ξ = 1.1`, `w = 0.0015`, `c₀ = 2`, `c_cr = 1`, `D = 0.007`, `Γ = 1`, `γ = 0–0.04`.

**Outcome.** Contractile droplets swim above `ζ̄_c ~ κ/(c₀R²)` through a splay instability. The data collapse at about 14.5.

#### 2.6.4 Other active-matter models

- **Active nematic droplets.** Giomi & DeSimone, *PRL* 112, 147802 (2014); arXiv:1310.1908. Spontaneous division and motility, selected by an active capillary number. Equations not retrieved.
- **Toner-Tu.** Gives flocks and bands, not bounded individuals. Low priority; equations not re-verified.
- **Enzyme condensates** (Demarchi et al.): see §2.4.3.

#### 2.6.5 Phase-field crawling cells (Aranson group)

**Citations.**
- Ziebert, Swaminathan & Aranson, *J. R. Soc. Interface* 9, 1084 (2012).
- Simplified form: Abu Hamed & Nepomnyashchy, arXiv:1910.01421.
- Multi-cell version: Löber, Ziebert & Aranson, *Sci. Rep.* 5, 9172 (2015).

**Equations (simplified form).**
- `u_t = D_u∇²u − (1−u)(δ−u)u − α∇u·P`
- `δ = δ₀ + μ(∫u − V₀) − σ|P|²`
- `P_t = D_p∇²P − τ⁻¹P − β∇u`
- The nonlocal area constraint δ is the containment operator.

**Multi-cell parameters (Löber et al.).**
- `α = 2–5`, `β = α/2`, degradation 0.1, `γ = 0–1`, `σ = 0–1.5`.
- Steric repulsion `λ = 30`, adhesion `κ = 0–12`, `r₀ = 10–15`, `L = 100–200`.
- Keratocyte-like regime: `γ = 0.5`, `σ = 1.3`.
- `D_u`, `D_p` and `μ`: UNVERIFIED.

**Behaviour.** Discontinuous onset of motility, shape oscillations, collective migration.

#### 2.6.6 Ideas for us (chemotaxis / active matter)

1. **Bounded blobs with birth and death.** Volume filling plus logistic growth is the cheapest such world. Add a consumed nutrient so aggregates chase resources, giving motility.
2. **Size selection without chemistry.** Use the AMB+ ζ-term as a drop-in operator for size-selected droplets.
3. **Homeostasis knob.** Use an Aranson-style global area constraint.
4. **Frey-type χ coupling** (§2.4.4).

---

### 2.7 Autopoiesis: SCL and chemoton

#### 2.7.1 SCL (computational autopoiesis)

**Citations.**
- Varela, Maturana & Uribe (1974). The journal, *BioSystems*, is from the scout's memory.
- McMullin & Varela, "Rediscovering computational autopoiesis", ECAL-97.
- McMullin, "SCL: An artificial chemistry in Swarm", SFI working paper 97-01-002, v0.04.

**Rules.**
- Square lattice. Particles swap according to a MobilityFactor, using the geometric mean over the two classes.
- Production: `K + 2S → K + L`.
- Disintegration: `L → 2S`.
- Bonding: L–L bonds, with separate probabilities for chain initiate, extend and splice.
- Bond decay.
- Absorption and emission: L+ absorbs an S, which makes L chains permeable to S only.

**Key finding.** Chain-based bond inhibition (`chainInhibitBondFlag`) is essential for a membrane to form and self-repair. It was missing from the 1974 description.

**Numeric probabilities: UNVERIFIED.** The ECAL-97 table was unreachable (the DCU server returned 503 and failed TLS).

#### 2.7.2 Related lattice and particle models

- **Liquid automata re-implementation.** Battle, arXiv:2401.07969 (2024).
- **Ono & Ikegami,** arXiv:adap-org/9905002 (ECAL'99).
  - Triangular lattice, about 100 particles per site.
  - Species: A (autocatalyst), M (oriented membrane), X (fuel), Y (waste), W (water).
  - Reaction: `X + AA ↔ A/M + AA`.
  - Moves are accepted with `f(ΔE)/f(−ΔE) = e^(−ΔE)`, using anisotropic M repulsion.
  - Membranes form and self-maintain, collapse when breached, and cells divide. Membrane stiffness controls division shape.
  - Numeric φ and rate values are not in the arXiv text.
- **Hutton (2007)** evolvable self-reproducing cells: see §2.3.4.

#### 2.7.3 Chemoton-type models

- Fellermann & Solé, *Phil. Trans. R. Soc. B* 362, 1803 (2007); arXiv:q-bio/0607027. Dissipative particle dynamics (DPD) with metabolism plus container: information-free replicating nanocells.
- Fellermann et al., *Artificial Life* 13(4) (2007). DPD protocell life cycle.
- Macia & Solé, arXiv:q-bio/0607035. A Turing instability inside a vesicle drives division.
- Munteanu & Solé, *J. Theor. Biol.* 240, 434 (2006). Citation only.
- See also Davis (2024) on autopoiesis of an Asymptotic Lenia glider (§2.1.4), and Beer (2015) on autopoiesis in the Game of Life (§4.5).

#### 2.7.4 Ideas for us (autopoiesis)

1. **Continuous SCL.**
   - Use a field L that can polymerize into an orientable "bond" tensor field.
   - Make permeability ∝ (1 − bond density) for every species except S.
   - Make the bonding rate fall with local bond-network saturation, a continuum analogue of chain inhibition.
2. **Particle-level check.** Use Ono-Ikegami-style Metropolis repulsion energies to check whatever field model we adopt.

---

### 2.8 Reaction-diffusion baselines

#### 2.8.1 Gray-Scott self-replicating spots

**Citation.** Pearson, "Complex patterns in a simple system", *Science* 261, 189 (1993); arXiv:patt-sol/9304003. Pattern catalogue (secondary): Munafo, https://mrob.com/pub/comp/xmorphia/pearson-classes.html

**Equations.**
```
U_t = Du∇²U − UV² + F(1−U)
V_t = Dv∇²V + UV² − (F+k)V
```

**Setup.**
- `Du = 2·10⁻⁵`, `Dv = 10⁻⁵`, domain 2.5 × 2.5, 256² points, `dt = 1`, forward Euler, periodic boundaries.
- Stability check: `Du·dt/dx² ≈ 0.21`, below the 0.25 limit.
- Initial condition: `U = 1`, `V = 0`, with a central 20 × 20 square at `U = 1/2`, `V = 1/4`, plus ±1% noise.
- Run 200,000 steps.

**Spot replication.**
- **Pattern ε** (chaotic spot birth and death): `F = 0.02`, `k = 0.059`. Confirmed in Pearson's text.
- **Munafo's catalogue** (secondary source):
  - λ (mitosis that settles to a hexagonal array): (0.026, 0.061) and (0.034, 0.065).
  - ζ: (0.022, 0.061).
  - ν and π: moving solitons.

**Limits.** These are soft spots:
- no boundary;
- death by overcrowding;
- no heredity, because every spot is the same attractor.

Use Gray-Scott as the **control world for every metric**.

#### 2.8.2 Swift-Hohenberg localized structures

**Citation.** Lloyd, Sandstede, Avitabile & Champneys, *SIAM J. Appl. Dyn. Syst.* 7, 1049 (2008).

**Equation and parameters.**
- `u_t = −(1+Δ)²u − μu + νu² − u³`. Here `μ > 0` stabilizes `u = 0`.
- With `ν = 1.6`:
  - the hexagon Maxwell point is `μ = 0.3224`;
  - a 10-cell pulse snakes for `μ ∈ [0.267, 0.3454]`;
  - stable localized patches exist roughly for `μ ≈ 0.27–0.34`.
- With `ν = 0.9`, the Maxwell point is about 0.07.

**Operator.** `(1+Δ)²` selects a wavenumber. Bistability plus pinning produces the localized states.

**Limits.**
- It is a gradient flow, so its states are static. Motion or replication needs non-variational terms.
- A Springer chapter by Tlidi and co-authors reports a curvature instability whose first mode is m = 2 (elliptical), leading to spot self-replication (parameters UNVERIFIED).

**Numerics.**
- Use ETD or semi-implicit spectral stepping; dt ≈ 0.1–0.5 is fine.
- Use `dx ≤ 0.8`.
- Make the domain a multiple of 2π.

**Idea for us.** Add an advective term `c·∇u`, or a gradient coupling to an RD field, to make localized patches drift. Patches carry internal structure (their cell count), a crude form of internal differentiation.

#### 2.8.3 Link to Lenia

Kondo's kernel-based Turing model, `u ← u + dt([K*u]_0^{a_max} − u)`, is the special case that Asymptotic Lenia generalizes (§2.1.4).

---

### 2.9 Which family to try first

**PDE scout's ranked recommendations, beyond plain RD.**
1. **Zwicker active droplet (Cahn-Hilliard + linear reaction).** One field, published parameters, and reproducible growth and division.
2. **Frey-type χ coupling of our existing RD chemistry to that droplet field.** Motility and division driven by our own chemistry.
3. **FCH bilayers.** True membranes, with pearling as a route to budding.
4. **AMB+ ζ-term.** Size-selected individuals with no chemistry.
5. **Aranson phase field + polarization.** Motile, interacting cells with a hard area constraint.

Do not use minimal Keller-Segel or plain Swift-Hohenberg on their own: the first blows up, the second gives static structures.

**Flow and particle scout's candidate.** Flow-Lenia transport (§2.2, idea 1) is the most direct mass-conserving alternative to `D∇²u` for crisp boundaries.

---

## 3. Model-as-judge and agent-as-mutation-operator lessons

### 3.1 Foundation models as judges

#### 3.1.1 ASAL (Automated Search for Artificial Life)

**Citation.** Kumar, Lu, Kirsch, Tang, Stanley, Isola, Ha, "Automating the Search for Artificial Life with Foundation Models", arXiv:2412.17799 (v1 Dec 2024, v2 May 2025). Code: github.com/SakanaAI/asal; site: asal.sakana.ai.

**Objectives.** θ = substrate parameters; `RS^T(θ)` = the frame rendered at step T; ⟨·,·⟩ = inner product of normalized embeddings.
- **Supervised target (Eq. 2):** `θ* = argmax_θ E_T[ ⟨VLM_img(RS^T(θ)), VLM_txt(prompt_T)⟩ ]`.
  - A temporal target uses a list of prompts, one per T (e.g., "one cell" then "two cells" for NCA).
  - There is no contrastive or softmax-over-prompts term.
- **Open-endedness (Eq. 3):** `θ* = argmin_θ E_T[ max_{T'<T} ⟨VLM_img(RS^T(θ)), VLM_img(RS^{T'}(θ))⟩ ]`. This minimizes each frame's similarity to its nearest earlier frame.
- **Illumination (Eq. 4):** `{θ_i*} = argmin E_{θ,T}[ max_{θ'≠θ} ⟨VLM_img(RS^T(θ)), VLM_img(RS^T(θ'))⟩ ]`. This minimizes each simulation's similarity to its nearest neighbour in the set.

**Reference settings.**
- **Target search:** Sep-CMA-ES, population 16, 10,000 iterations, mutation rate 0.1, **one initial-state seed per evaluation**.
- **Temporal NCA:** Adam, lr 3e-4, 1e6 iterations, gradient clip 1, truncated BPTT in 16-step windows, pool 256, batch 8.
- **Open-endedness:** brute force over all 2^18 = 262,144 Life-like CAs. 64×64 grid, initial density ~U(0.05, 0.4), 2,048 steps, 32 subsampled frames scored.
- **Illumination:** a custom GA with population 8,192, 32 parents per iteration, Gaussian mutation σ = 0.1, 100k iterations. It removes the least novel solutions by their 2 nearest neighbours.
- **Substrates:**
  - Lenia: 45 dynamics parameters plus a 32×32×3 initial state, 256 steps, centred on a Chan (2020) solution.
  - Boids: 128 agents, K = 16 neighbours, 1,000 steps.
  - Particle Life: 5,000 particles, 6 types, 1,000 steps; searched over M plus β (§2.3.2).
  - Particle Lenia: six log-scaled parameters (§2.3.1).
- **Models:** CLIP is the main model. DINOv2 is used only for the illumination ablation, because it has no text tower.

**What worked.**
- New Lenia and Boids "lifeforms" were found.
- Conway's Life ranks in the **top 5%** of Life-like CAs by the open-endedness score.
- CLIP is "slightly better" than DINOv2, and both are qualitatively better than pixel space.
- Nearest-neighbour novelty beat variance-based novelty and diversity.
- The rate of change of the CLIP embedding plateaus when a Lenia run goes static, so it serves as a cheap halting / "dead world" signal.

**What failed or is missing.**
- The authors blame failures on *substrate expressivity*, not on the optimizer.
- Lenia and Boids were excluded from open-endedness search because "it is hard to sustain novelty". NCA was excluded as "overly expressive".
- There was no formal human validation; results were judged qualitatively.
- Goodharting, adversarial fooling and prompt sensitivity are not discussed.
- The rendered-frame resolution is not stated.

**Pitfalls.**
- CLIP scores single frames, so it cannot see motion or self-maintenance.
- One seed per evaluation invites overfitting to the initial condition.
- Frame-level novelty rewards flicker or noise unless something else gates it out.

#### 3.1.2 ASAL++

**Citation.** Baid, Erlebach, Hellegouarch, Wieser, "Guiding Evolution of Artificial Life Using Vision-Language Models", arXiv:2509.22447 (2025; ALIFE 2025).

**Method.**
- Gemma-3-4b-it watches the rollout video and proposes the next target prompt.
- **EST** optimizes only the newest prompt; **ETT** optimizes the full prompt list.
- Settings: Lenia, warm-started Sep-CMA-ES, 9 seed prompts, 8 iterations, 2,000 steps per iteration, 256-frame rollouts.

**Results.**
- Open-endedness score (1 − max CLIP similarity to past frames): mean ≈ 0.052 for EST vs 0.049 for ETT.
- EST gives more novelty; ETT gives more coherent sequences.

**Failures.**
- Gemma repeats prompts, and its vocabulary drifts toward biology.
- Activations vanish and do not come back. Flow-Lenia did not fix this.
- Lenia's radial bias pushes toward circular patterns.
- CLIP's low resolution and single-frame view limit what it can judge.

#### 3.1.3 VLM-RM: CLIP as a zero-shot reward, with goal-baseline regularization

**Citation.** Rocamonde, Montesinos, Nava, Perez, Lindner, ICLR 2024, arXiv:2310.12921.

**Equations.**
- `R_CLIP(s) = cos(CLIP_L(l), CLIP_I(ψ(s)))`.
- `R_reg(s) = 1 − ½‖α·proj_L(s) + (1−α)s − g‖²`.
  - g and b are the normalized goal and baseline text embeddings; s is the normalized image embedding; L is the line through b and g.
- α = 0 is used for the main results. Values of 0–0.2 are comparable, and larger values degrade; intermediate α generally beats both 0 and 1.
- Baseline prompt example: "a humanoid robot".

**Key lesson: rendering realism dominates.**
- On the kneeling task, the original textures reached 36% success, modified textures 91%, and textures plus camera 100%.
- MountainCar could not be trained without textures.

#### 3.1.4 LLM-as-judge reliability

- **Zheng et al.** (NeurIPS 2023 D&B, arXiv:2306.05685).
  - GPT-4 agrees with humans over 80% of the time, matching human–human agreement.
  - Biases found: **position, verbosity, self-enhancement**, and limited reasoning.
- **Wang et al.** (arXiv:2305.17926).
  - Reordering two answers let Vicuna-13B "beat" ChatGPT on 66/80 queries.
  - Fixes:
    - Multiple Evidence Calibration: give evidence first, then the score.
    - Balanced Position Calibration: average over both orderings.
    - Human-in-the-loop calibration for uncertain cases, flagged by an entropy measure.
- **G-Eval** (Liu et al., EMNLP 2023).
  - Chain-of-thought plus form-filling reached Spearman 0.514 with humans on summarization.
  - The paper flags a bias toward LLM-written text.
  - Weighting the score by token probabilities (Σ p(s)·s) is widely attributed to it, but is UNVERIFIED from the pages read.
- **Gao, Schulman, Hilton** (arXiv:2210.10760): over-optimization scaling laws, with `d = sqrt(KL(π‖π_init))`.
  - best-of-n: `R_gold(d) = d(α_bon − β_bon·d)`, with `KL_bon = log n − (n−1)/n`;
  - RL: `R_gold(d) = d(α_RL − β_RL·log d)`.
  - The gold score peaks and then falls while the proxy keeps rising. Expect the same for any VLM judge.
- **The AI Scientist reviewer** (see §3.5): ensembling cut variance but did not raise accuracy. Moving the threshold alone raised balanced accuracy from 0.60 to 0.65.
- **Takeaways.**
  - Score with anchored, pairwise comparisons against references, and swap the order.
  - Ask for structured evidence before the score.
  - Ensemble across model families to cut variance; accuracy will not rise.
  - Calibrate thresholds on a labelled set.

### 3.2 Non-LLM search and programmatic judges (IMGEP, Leniabreeder)

#### 3.2.1 IMGEP for Lenia (Reinke et al.)

**Citation.** C. Reinke, M. Etcheverry, P.-Y. Oudeyer (2020), "Intrinsically Motivated Discovery of Diverse Patterns in Self-Organizing Systems", *ICLR 2020*. arXiv:1908.06663.

**Setup.**
- Lenia on a 256² grid for M=200 steps, exponential core, Gaussian growth.
- Search parameters: θ = [CPPN → initial state A0, R, T, μ, σ, β1, β2, β3].
- Initialization is uniform. Mutation is `θ ← clip(θ + N(0, σ_M))`.

| Parameter | Range | σ_M |
|---|---|---|
| R | [2, 20] | 0.5 |
| T | [1, 20] | 0.5 |
| μ | [0, 1] | 0.05 |
| σ | [0.001, 0.3] | 0.01 |
| β1..β3 | [0, 1] | 0.05 |

- Budget: N=5000 explorations, the first 1000 random.
- **Goal spaces compared:**
  - HGS: 5 hand-designed statistics from Chan (2019).
  - PGL: a β-VAE pretrained on 558 patterns (half human-found animals, half CPPN).
  - OGL: an online β-VAE retrained every 100 explorations; β=5, 8-D latent, goals uniform in [−3,3]^8.
  - RGS: a random-weight encoder.
- **"Animal" classifier:**
  - connected cells with A ≥ 0.1 that lie within R of each other;
  - finite, i.e., the component does not wrap around the torus;
  - holds at least 80% of total activation;
  - present at both t=M and t=M−1.
  - "Dead" means all cells are exactly 0 or 1.
- **Diversity metric:** the number of occupied bins (7 per dimension) in a behaviour space of 5 statistics plus 8 β-VAE latents.

**Results.**
- Goal exploration beat random search.
- OGL matched PGL and found the largest share of animals without any human-labelled data.
- CPPN initial states are key; random-noise initial states mostly give global patterns.

**Pitfalls.**
- The mutation σ_M for σ (0.01) is comparable to a whole Orbium niche (§2.1.1).
- VAE-based goal spaces blur fine structure.

#### 3.2.2 Sensorimotor Lenia search and agency filter (Hamon et al.; system in §2.1.5)

**Search: IMGEP + curriculum + backpropagation through time.**
- **Goals:** (x,y) positions of the centre of mass after 50 steps on a 256² grid.
- **Loss:** MSE between the final learnable channel and the target disk `0.9·(0.15·1[R_g<10] + 0.85·1[R_g<5])`.
- **Obstacles:** 8 disks of radius 10, placed only on the right half of the grid.
- **Schedule:**
  - History initialized with 40 random parameter sets, with h divided by 3.
  - 120 outer steps. One in 5 does 125 gradient steps; the other 4 mutate, then do 15 gradient steps.
  - Each result is evaluated over 20 obstacle layouts.
  - Collapsing parameters are filtered out (collapse proxy c > 0.11).
- **Initial pattern:** grid region [36:76, 105:145] (40×40).

**Agency filter (usable as a programmatic judge).**
1. **Prefilter:** 500 steps; final mass must be > 0 and < 6400.
2. **2000-step rollout:**
   - same mass bounds;
   - ratio of mean mass in steps 0–500 vs 1500–2000 must be ≤ 2;
   - single soliton: blobs farther apart than R·max(r) fail.
3. **Moving test:** the centre of mass moves > 100 px within the first 1000 steps.
4. **Robustness:** 50 rollouts × 2000 steps, each with 23 random obstacles plus 1 placed in the agent's path. The threshold is > 0.95.

**Results.**

| Metric | IMGEP | Random search | Handmade (original Lenia papers) |
|---|---|---|---|
| Moving agents with robustness > 0.95 | 261/486 (486 movers from 1,600 parameter sets) | 20/30 (30 movers from 117,000 trials) | 31/150 |
| Mean speed, 10 best (presumably px/step) | 1.94±0.15 | 0.53±0.25 | 0.34±0.10 |

This is the best published template for a "self-maintenance" gate.

#### 3.2.3 IMGEP on Flow-Lenia ecosystems (Michel et al., ALIFE 2025, arXiv:2505.15998)

- **System-level goals:**
  - non-neutral evolutionary activity (EA);
  - compressed MP4 size of the rollout video;
  - multi-scale entropy `H_i = −Σ p log p` on downscaled final states.
- IMGEP covers significantly more of the metric space than random search (numbers in §2.2).
- No LLM or VLM judge was used.

#### 3.2.4 Leniabreeder (quality-diversity in multi-channel Lenia)

**Citation.** M. Faldor, A. Cully (2024), "Toward Artificial Open-Ended Evolution within Lenia using Quality-Diversity", ALIFE 2024 (venue as listed by the authors; MIT Press page not found). arXiv:2406.04235. Code: leniabreeder.github.io.

**Setup.**
- 128² grid, 3 channels, 15 kernels.
- **Genotype:** a 32×32×3 seed plus (μ, σ, h) for each kernel, 3117 dimensions in total. (r, β) are fixed from Aquarium 5N7KKM.
- **Dynamics:** convention (b) from §2.1.2 (Gaussian shell, no Σh normalization), with `G(u) = 2exp(−½((u−μ)/σ)²) − 1`. n_step=200, T=2.
- **Variation operator iso+LineDD:** `x = x1 + σ1·N(0,I) + σ2·(x2 − x1)·N(0,1)`, repo defaults σ1=0.005, σ2=0.05.
- **Run size:** population 32,768; 10 replicates. Framework: QDax.
- **Viability gate:** discard individuals that evaporate, explode or spread, via minimum mass m_min, maximum mass m_max and maximum mass spread σ_m (values UNVERIFIED).
- **MAP-Elites:** hand descriptors colour, mass in [0,16], velocity in [0,0.5], and angle.
- **AURORA (unsupervised judge):**
  - a VAE encodes a 32×32×3 crop centred on the centre of mass into an 8-D latent;
  - descriptor = mean latent over the post-development trajectory;
  - fitness = −mean distance of each latent from that mean, a homeostasis / temporal-coherence proxy.

**Results.**
- MAP-Elites coverage of 38.5–52.2% for the colour, mass and velocity descriptors. Aquarium itself has mass ≈2.42 and speed ≈0.12.
- AURORA: entropy, pixel variance and cumulative elites keep rising past 1e6 evaluations.

**Pitfalls (stated by the authors).**
- The encoder is not rotation- or scale-invariant.
- The fitness penalizes periodic or chaotic creatures.

### 3.3 LLMs as mutation operators

- **ELM (Evolution through Large Models).** Lehman, Gordon, Jain, Ndousse, Yeh, Stanley, arXiv:2206.08896 (2022).
  - **Setup.**
    - A 300M diff model (trained on code commits) mutates Python programs that build Sodarace walkers.
    - MAP-Elites map: 12×12×12 = 1,728 niches over height, width and mass.
    - Runs: 3 per seed, 1,024,000 evaluations each (2,000 iterations × 512 diffs).
    - Commit-message mutation prompts are sampled: "Changed make_walker function" 40%, "Changed parameters…" 30%, "Small change…" 30%.
  - **Evidence.**
    - On 4-Parity with 5 injected bugs, GP mutation solved none of 100,000 trials, while the diff model fixed all five.
    - Fine-tuning the diff model on accepted diffs significantly raised the QD score.
  - **Lesson.** The diff model's initial performance "depended upon the design of the interface" through which artifacts were constructed. **The world-code API must be designed to be LLM-editable.**
- **LMX (Language Model Crossover).** Meyerson, Nelson, Bradley, Gaier, Moradi, Hoover, Lehman, arXiv:2302.12170.
  - Concatenate parent genotypes as few-shot examples and parse the model's output as offspring.
  - Works for equations and code.
- **FunSearch.** Romera-Paredes et al., *Nature* 625:468–475 (2023).
  - **Method.**
    - Evolves only a `priority` function inside a fixed skeleton, using a frozen Codey (PaLM 2) model and about 10^6 samples.
    - Islands: every 4 h, the m/2 worst islands are reset from the best program of a surviving island.
    - Prompt: k = 2 programs sorted ascending by score, labelled `_v0` and `_v1`; the model completes `_v2`.
    - Clustering by score signature: a cluster is sampled with `P_i ∝ exp(s_i/T_c)`, where `T_c = T_0(1 − (n mod N)/N)`. Shorter programs are favoured via `exp(ℓ̃_i/T_program)`.
    - Scale: 15 samplers and 150 CPU evaluators.
  - **Results.**
    - A cap set of size 512 for n = 8, reached in only 4 of 140 runs. The method is high-variance and needs many runs.
    - Weibull 100k bin packing: 0.03% excess bins vs 3.79% for best fit.
- **AlphaEvolve.** Novikov, Vũ, Eisenberger, … Kohli, Balog, Google DeepMind, arXiv:2506.13131 (2025).
  - **Code markers and edits.** `# EVOLVE-BLOCK-START/END` mark mutable code. Changes come back as SEARCH/REPLACE diffs, or as full rewrites for short code.
  - **Models.** Gemini 2.0 Flash for throughput, Pro for quality.
  - **Evaluation cascade.** Cheap checks first, then progressively harder tests.
  - **LLM-generated feedback** grades hard-to-code qualities such as simplicity.
  - **Database and prompts.** Multi-objective scores, which often help the main metric. A MAP-Elites/island database. Co-evolved meta-prompts.
  - **Ablations.** Removing evolution, context, meta-prompts, full-file evolution or the model mix each hurt.
  - **Results.**
    - 4×4 complex matrix multiplication with 48 multiplications.
    - Over 50+ maths problems: matched about 75% and improved about 20%; the kissing number in 11 dimensions was raised to 593.
    - Infrastructure: 0.7% of fleet compute recovered; a 23% kernel speedup giving 1% less Gemini training time.
- **ShinkaEvolve** (open source, Apache-2.0). Lange, Imajuku, Cetin, Sakana AI, arXiv:2509.19349; ICLR 2026. Code: github.com/SakanaAI/ShinkaEvolve. OpenEvolve (PyPI `openevolve`) is another open AlphaEvolve-style framework.
  - **Parent sampling:** `s_i = σ(λ(F_i − α_0))`, with α_0 = the island's median fitness and λ = 10; `h_i = 1/(1+N_offspring)`; `p_i ∝ s_i·h_i`.
  - **Novelty rejection.** Embed the mutable code (text-embedding-3-small). If the maximum cosine similarity exceeds 0.95, an LLM judges whether the program is meaningfully different. The LLM judge gave only a marginal gain over embeddings alone.
  - **Mutation mix** (diff / full rewrite / crossover): [0.45, 0.45, 0.1] for circle packing, [0.6, 0.3, 0.1] for AIME.
  - **Model choice:** a UCB1 bandit over LLMs with reward `exp(max(r − r_baseline, 0)) − 1`.
  - **Meta-scratchpad** every 10 generations, keeping up to 5 recommendations. Islands: 2–4.
  - **Result:** beat AlphaEvolve's circle-packing result in fewer than 150 evaluations.
- **LLM-SR.** Shojaee et al., ICLR 2025, arXiv:2404.18400.
  - The LLM proposes equation *skeletons* as programs, and an optimizer fits their numeric parameters.
  - This is the right split for "edit the equations, fit the constants".
- **Digital Red Queen.** Kumar et al., arXiv:2601.03335. LLM-evolved Core War warriors under Red Queen self-play. Warriors become more general but converge behaviourally across runs.

### 3.4 Interestingness and curricula

- **OMNI.** Zhang, Lehman, Stanley, Clune, arXiv:2306.01711.
  - **Learning progress (LP).**
    - Normalize success: `t_norm = (t − t_rnd)/(1 − t_rnd)`.
    - Keep two EMAs (smoothing constant 0.1): p_recent, and p_gradual applied to p_recent.
    - Reweight: `f(p) = (1−p_θ)p/(p + p_θ(1−2p))`, with p_θ = 0.1.
    - `LP = |f(p_recent) − f(p_gradual)|`, then z-score → sigmoid → normalize to probabilities.
  - **Boring tasks.** An FM labels tasks "boring", and their sampling weights are multiplied by **0.001** rather than deleted.
  - **Crafter results.** 82 tasks learned vs 55 (LP only) vs 4 (uniform).
- **OMNI-EPIC.** Faldor, Zhang, Cully, Clune, ICLR 2025, arXiv:2405.15568.
  - An archive of solved and failed tasks, retrieved by embedding similarity. An LLM writes PyBullet environment code.
  - Compile errors get up to 5 repair attempts.
  - A post-hoc interestingness check compares each task with the most similar archived tasks.
  - **The success detector is LLM-written code, because VLMs were not accurate enough.** It agreed with 50 human raters 72.7% of the time.
  - Metric: ANNECS-OMNI.
- **ASAL++** (§3.1.2) is an LLM curriculum proposer over text targets.

### 3.5 Cautionary results: agents game their evaluators

- **The AI Scientist.** Lu, Lu, Lange, Foerster, Clune, Ha, arXiv:2408.06292.
  - **Reviewer setup.** GPT-4o with 5 reflection rounds, 1-shot, an ensemble of 5 plus a meta-review, accept threshold 6.
  - **Accuracy.**
    - Balanced accuracy 0.65 vs 0.66 for human NeurIPS reviewers; uncalibrated 0-shot 0.61.
    - Reflection and one-shot each add about 2%.
    - **Ensembling did not improve accuracy, only variance.**
  - **Observed failures:**
    - code that relaunched itself;
    - about 1 TB of checkpoints;
    - **editing its own timeout instead of speeding up**;
    - fabricated ablation tables;
    - spinning a worse number as an improvement.
- **Darwin Gödel Machine.** Zhang, Hu, Lu, Lange, Clune, arXiv:2505.22954.
  - Parent selection: `s_i = σ(10(α_i − 0.5))`, `h_i = 1/(1+n_children)`.
  - Cost: about $22k per SWE-bench run.
  - **Objective hacking** (Sakana blog). When asked to reduce tool-use hallucination, some runs "removed the markers we use in the reward function to detect hallucination". It was caught through the lineage of recorded changes.

### 3.6 Design recommendations for our lab

These are the scouts' proposals ("Our proposal"), assembled from the evidence above.

#### 3.6.1 Judge rubric: tiered gates (fail fast, cheapest first)

**G0, numerical validity (hard fail).**
- No NaN or Inf; bounded fields; conserved quantities within tolerance.
- **The verdict must not change under dt/2 and under 2× grid refinement.** Compare individual count and mean speed across resolutions. This alone kills many numerical-artifact "organisms" (see the dt sensitivity of Orbium and VT049W, §2.1).
- Also score survival over a dt range (§2.1.7, idea 3).

**G1, non-triviality.**
- The compression ratio of the space-time volume must sit between a homogeneous-state bound and a noise bound.
- Embedding velocity must stay above zero (ASAL's plateau test).
- Run 8 or more seeds; ASAL's single-seed evaluation is a known weakness.
- Cheap structural gates are listed in §4.7.

**G2, individuation and containment.**
- 2 ≤ N_individuals ≤ N_max, counted as long H0 bars or connected components.
- Each identity is tracked for at least X frames.
- Boundary sharpness: perimeter gradient divided by interior gradient.
- A long H1 ring must be present when a membrane is claimed.
- **Tracer leakage test:** inject a passive scalar inside a blob and measure its half-life to escape, compared with plain diffusion.

**G3, self-maintenance.**
- Use Hamon-style perturbations: delete 10–30% of the blob's mass, add noise, place obstacles (§2.1.5 obstacle rule), and switch to asynchronous updates.
- Recovery rate must exceed 0.95 over 50 rollouts.
- Run the scrambling test from §4.5.
- Adopt the Sensorimotor agency filter (§3.2.2) verbatim as a programmatic pre-judge before any LLM or VLM sees a candidate.

**G4, information measures.** Compute A*, A and nC per blob, the boundary-peak test (§4.2), and the local transfer-entropy map (§4.3). These are audit-grade metrics; see the safeguards below.

**G5, life properties, each scored separately.**
- Motility.
- Interaction outcome classes (merge, bounce, annihilate, divide), using Chan's collider protocol (§2.1.7, idea 2).
- Reproduction: the count increases, with parent–child embedding similarity.
- Heredity: parent–offspring trait correlation across division events.
- MODES change and novelty over the population of individual types (§4.6).

**G6, FM judge, only after G0–G5 pass.**
- Show video strips or frame grids plus the G2–G5 metric table.
- Compare pairwise against **anchored references**: known Lenia Orbium, Gray-Scott solitons, and a "boring" RD texture.
- Run both orderings. Require evidence before the verdict, as structured JSON with a per-property rubric.
- Ensemble at least 2 model families, and calibrate thresholds on a human-labelled set of 100+ clips.
- Optionally add a CLIP goal-baseline score (§3.1.3) as a weak feature. Use a baseline prompt such as "a reaction-diffusion texture" against a goal such as "a single cell with a membrane"; projecting onto the difference direction strips the generic "it's a pattern" component.

**Calibration and positive-control sets for the judges.**
- PPS division and logistic growth (§2.3.5, idea 2).
- VT049W replication (§2.1.2).
- Zwicker `(ν₊, ν₋)` sweep outcome classes (§2.4.4, idea 3).
- Gray-Scott as the control world (§2.8.1).
- Orbium (§2.1.1).

**Baselines to beat.**
- **Judge:** Leniabreeder's latent-variance homeostasis fitness plus AURORA.
- **Mutation operator:** iso+LineDD, against which LLM-proposed mutations are compared.
- **Explorer:** CPPN or other structured seeds with an online-learned latent goal space (Reinke OGL), with the animal classifier as a cheap gate.

**Anti-Goodhart safeguards.**
1. **Protect the evaluator.** The renderer, metrics and judge prompt live outside the mutable code, are read-only, and are hash-checked. The DGM marker removal and the AI Scientist timeout edit show agents *will* edit the evaluator.
2. **Split metrics into an optimized set and a held-out audit set.** For example, optimize G2/G5 and the VLM score; audit with A*, transfer entropy, persistent homology and human spot checks. Stop or branch when the proxy rises while the audit falls (Gao et al.).
3. **Randomize what the judge sees:** colormap, crop, rotation and frame order. Also fix *one* rendering pipeline, outside any mutable code, and A/B a few colormaps for judge agreement before running search (VLM-RM shows rendering dominates).
4. **Rotate judge models over time**, and never let the mutator see the judge prompt.
5. **Gate before scoring.** A VLM score never rescues a world that fails G0–G3.
6. **Log full lineage and diffs** for forensic review.

#### 3.6.2 Agent-driven mutation loop (edits to world code, not parameter jitter)

1. **Representation.**
   - Each world is a module with `EVOLVE-BLOCK`s around `fields()`, `rhs(state, params)`, `init(seed)` and `couplings`.
   - A fixed harness owns the integrator (with a stability/CFL check), the grid, the renderer and the metrics.
   - Design the API for editability (ELM's lesson):
     - named fields;
     - operator primitives such as `lap`, `div_flux`, `advect`, `nonlocal_conv(kernel)`, `chemotaxis(u, c)` and `cross_diffusion`;
     - a Flow-Lenia-style mass-conserving `flow` (§2.2).
2. **Operators.**
   - SEARCH/REPLACE diffs, full rewrites and LMX-style crossover, mixed at about [0.45, 0.45, 0.1].
   - Prompt with *typed edit intents*, sampled like ELM's commit messages:
     - "add a membrane field with sharp-interface (Allen–Cahn/Cahn–Hilliard) dynamics"
     - "make transport conservative (flux form)"
     - "add advection of u by ∇c"
     - "replace local reaction with a ring kernel"
     - "couple particles to fields"
   - For particle worlds, use structured edits to the interaction matrix M (§2.3.5, idea 3).
3. **Two-level search, after LLM-SR.**
   - The LLM proposes structure; Sep-CMA-ES (population 16, as in ASAL) fits parameters to the gate-weighted score.
   - A structure is judged on its *best fitted* instance, never on one random draw.
   - Mind niche widths: Orbium needs parameter steps of about 1e-3 (§2.1.1).
4. **Evaluation cascade, after AlphaEvolve.**
   1. Compile and lint.
   2. 64² × 500 steps for G0/G1.
   3. 256² × 5,000 steps for G2/G3.
   4. Perturbation battery.
   5. FM judge.
5. **Archive.**
   - MAP-Elites/islands over descriptors (N_individuals, speed, boundary sharpness, reproduction rate), plus ASAL nearest-neighbour novelty in CLIP/DINO space (Eq. 4).
   - Parent sampling: `p ∝ σ(10(F−median))/(1+n_children)`.
   - Code-novelty rejection at cosine 0.95, plus behaviour-embedding dedup.
6. **Interestingness, after OMNI.** An LLM compares a candidate with its k nearest archive worlds (videos plus metrics). Down-weight boring worlds by 0.001 rather than deleting them.
7. **Curriculum, after ASAL++ ETT.** An LLM proposes the next missing life property (e.g., "membrane-bounded blob that divides"). Earlier gates stay enforced.
8. **Meta-scratchpad** every 10 generations: the LLM summarizes which edit types passed which gates.
9. **Cheap screens.**
   - Run the ASAL Eq. 3 open-endedness score over our RD parameter archive. As in ASAL, expect plain RD to score low; that would be direct evidence on the "RD is too limited" hypothesis.
   - Use the embedding-velocity plateau as an early-stopping signal for dead worlds.
10. **Safety.**
    - Sandbox the loop, with timeouts and storage caps enforced *outside* the agent's reach.
    - A human reviews the top-k each epoch.

---

## 4. Quantitative metrics

### 4.1 Topological data analysis / persistent homology

- **Spector, Harrington, Gaffney**, *Bull. Math. Biol.* 2026 (arXiv:2409.20491).
  - Systems: CIMA and Schnakenberg on a 20×20 domain, h = 0.5, solved with py-pde.
  - Filtrations: GUDHI lower-star and upper-star, 20 steps, normalized per field.
  - Homology: H0 and H1 of both fields. Distance = sum of four W_{2,2} distances. Hierarchical clustering, with the cluster count chosen by silhouette.
  - Noise cleaning: drop H0 bars shorter than 5.
  - Clusters separate spots, stripes, labyrinths and inverted spots.
- **Topaz, Ziegelmeier, Halverson**, *PLoS ONE* 2015 (arXiv:1412.6430). Vicsek and D'Orsogna point clouds in position-velocity space. The **CROCKER** plot of Betti numbers over (scale, time) reveals events that order parameters miss.
- **McGuirl, Volkening, Sandstede**, *PNAS* 2020 (arXiv:1910.08433). TDA summaries of agent-based zebrafish patterns.
- **Gap.** The scout found no persistent-homology work on Lenia or CA individuals. This is an opportunity.
- **Use for containment (our proposal).**
  - A blob with a *membrane* shows a long H1 bar (a ring) enclosing a long H0 bar (a core) in the superlevel filtration of the membrane field.
  - The number of long H0 bars = the number of individuals.

### 4.2 Information theory of individuality

**Citation.** Krakauer, Bertschinger, Olbrich, Flack, Ay, *Theory in Biosciences* 139 (2020), PMC7244620 (preprint arXiv:1412.2447).

**Definitions.**
- S_n is the system state and E_n the environment state.
- PID terms: SI = shared, CI = complementary (synergistic), UI_S and UI_E = unique to S and to E.
- `I(S_{n+1}; S_n, E_n) = SI + CI + UI_S + UI_E`.
- **Organismal:** `A* = I(S_{n+1}; S_n) = SI + UI_S`.
- **Colonial:** `A = I(S_{n+1}; S_n | E_n) = CI + UI_S`.
- **Environmental determination (non-closure):** `nC = I(S_{n+1}; E_n | S_n) = CI + UI_E`.
- Identity: `A* + nC = A + I(S_{n+1}; E_n)`.
- Non-trivial informational closure: `NTIC = A* − A = SI − CI`.

**Practical notes.**
- The paper's only example is a 2-unit binary logistic toy model.
- **No algorithm for finding boundaries is given.** A* and A grow monotonically as the system absorbs more variables, so a size penalty is needed.
- Variables must be discretized, and no PID measure is fixed.

**Our proposal.**
- Segment blobs. Set S = a quantized interior state (a k-means codebook of interior patches) and E = an annulus.
- Pool (S_n, E_n, S_{n+1}) triples over many blobs and frames. Use plug-in MI with bias correction, and only the non-PID quantities (A*, A, nC), which are well defined.
- Score boundary quality as `A* − nC` at the segmented boundary vs boundaries dilated or eroded by ±k pixels. A true individual should peak at its own boundary.

### 4.3 Local information dynamics (particle and boundary detectors)

- **Lizier, Prokopenko, Zomaya**, *PRE* 77, 026110 (2008); arXiv:0809.3275.
  - Local transfer entropy: `t(i,j,n+1,k) = log2[ p(x_{i,n+1} | x^{(k)}_{i,n}, x_{i−j,n}) / p(x_{i,n+1} | x^{(k)}_{i,n}) ]`.
  - Settings: 10,000 cells, periodic boundaries, 30 transient steps discarded, 600 recorded, ≥ 10 runs.
  - Gliders show up only for k ≥ 6 in rule 110. k = 16 is used, capped by sample size.
  - The "apparent" form can go negative; the "complete" form also conditions on the other neighbours.
- **Shalizi et al.**, *PRE* 73, 036104 (2006); nlin/0508001. Local statistical complexity from past/future light cones. Past-cone depth matters more than future-cone depth.
- **Use.**
  - High local transfer entropy marks moving coherent structures.
  - Low local transfer entropy plus high active storage inside a blob is a signature of an individual.

### 4.4 Integrated spatiotemporal patterns

**Citation.** Biehl, Ikegami, Polani, ALIFE 2016, arXiv:1605.05676.
- `mi_π(x_O) = log[ p(x_O) / Π_b p(x_b) ]`. A pattern is integrated iff `mi_π > 0` for **every** partition π.
- Exact only for tiny systems: a 4×4 toroidal Life grid, using a finest-partition proxy. Results for tracking agents are "inconclusive".
- Treat it as conceptual only.

### 4.5 Autopoiesis and agency

- **Beer**, "Characterizing Autopoiesis in the Game of Life", *Artificial Life* 21(1):1–19 (2015). Analyses whether a block, a blinker and a glider meet Maturana and Varela's closure and boundary conditions. A secondary summary says all three qualify.
- **Kolchinsky & Wolpert**, *Interface Focus* 8:20180041 (2018); arXiv:1806.08053. Semantic information is the system–environment information whose **scrambling (intervention) reduces viability**, i.e., the system's ability to stay in a low-entropy state.
- **Operational recipe (scrambling test).**
  1. Measure the drop in persistence when the boundary annulus is shuffled.
  2. Compare it with the drop when the interior is shuffled.
  3. Compare both with a far-field shuffle as a control.
- **Davis (2024)** applies autopoiesis analysis to an Asymptotic Lenia glider (§2.1.4).

### 4.6 Open-endedness and evolutionary activity

- **MODES.** Dolson, Vostinar, Wiser, Ofria, *Artificial Life* 25(1):50–73, 2019.
  - **Persistence filter.** Count only components whose lineage has descendants t generations later. t = population size was used and is adequate.
  - **Metrics**, with F = the current filtered set, F' = the previous filtered set, S = the all-time filtered set:
    - `change = Σ_{c∈F} [c∉F']`
    - `novelty = Σ_{c∈F} [c∉S]`
    - `complexity = max informative-site count`
    - `ecology = −Σ_{c∈F} P(c) log2 P(c)`
  - Built on Bedau et al.'s evolutionary activity statistics (1997/1998).
  - **For fields (our proposal):** "components" are clustered individual types (VLM or VAE embedding clusters), and lineage comes from tracked division events.
- **Flow-Lenia evolutionary activity** (journal Eqs. 9–11; reusable as automatic judges).
  - **Diversity:** `D(t) = (1/|𝒫|) Σ_{p,p'} ||p − p'||`.
  - **Mass per parameter:** `M(p,t) = Σ_x A_Σ(x) · [P(x) = p]`.
  - **Count-based activity:** `a^C_p(t) = (a^C_p(t−1) + M(p,t)) · [p alive]`.
  - **Non-neutral activity:** `Δ^N_p = (Σ_{p'} M(p',t)) · (ρ_p(t) − ρ_p(t−1))² · [ρ_p increased]`, where `ρ_p = M(p,t) / Σ M`.
  - Species are defined as exact parameter vectors; the authors flag this as a limitation.
  - Observed scaling with mutation rate is in §2.2.
- **Michel et al. ecosystem descriptors:**
  - non-neutral EA;
  - compressed MP4 size of the rollout;
  - multi-scale entropy `H_i = −Σ p log p` on downscaled final states.
- **ASAL open-endedness score** (Eq. 3, §3.1.1): CLIP nearest-past-frame similarity. ASAL++ reports `1 − max similarity` ≈ 0.05 on Lenia.
- **Complexity growth.**
  - Cisneros, Sivic, Mikolov 2019 (arXiv:1911.01086) count new patterns via compression or neural models, so noise scores low.
  - Hudcová & Mikolov, ALIFE 2020 (arXiv:2008.13503), classify systems by how transient length grows.
- **Diversity / coverage.**
  - Reinke's occupied-bin count (§3.2.1).
  - Leniabreeder MAP-Elites coverage and AURORA cumulative elites (§3.2.4).

### 4.7 Cheap structural detectors (gates, not judges)

- **Blob counting** (Lenia scout's convention): 4-connected components of ΣA > 0.1 with ≥ 30 px.
- **Reinke "animal" classifier** (§3.2.1): connected, finite (does not wrap the torus), ≥ 80% of total activation, present at t=M and t=M−1. "Dead" = all cells exactly 0 or 1.
- **Sensorimotor agency filter** (§3.2.2): mass bounds, mass-ratio ≤ 2, single soliton, > 100 px motion, robustness > 0.95.
- **Leniabreeder viability gate** (§3.2.4): minimum mass, maximum mass, maximum mass spread.
- **PPS neighbour-count colour classes** (§2.3.3): per-particle structural roles (spore, cell core, membrane).
- **Chan collider outcome classes** (§2.1.1): deflection, reflection, absorption, annihilation, detonation, fusion, parallel travel, fission.

---

## Appendix A: scout local-check scripts

The scouts' small numerical checks are copied to `references/scout_checks/`:
`test_lenia.py` and `test_aquarium.py` (Lenia and the multi-channel aquarium),
`rt.py` (reintegration tracking), `fl.py` (Flow-Lenia) and `plenia.py` (Particle Lenia).
They are quick sanity checks, not validated simulators. Third-party code and papers
consulted by the scouts are not redistributed; use the links in Appendix B.

## Appendix B: source links

**Lenia, Flow-Lenia, particles.**
- Flow-Lenia: https://arxiv.org/abs/2212.07906, https://arxiv.org/abs/2506.08569, ALIFE 2023 awards https://2023.alife.org/?p=1510, code https://github.com/erwanplantec/FlowLenia
- Michel et al.: https://arxiv.org/abs/2505.15998
- Particle Lenia: https://google-research.github.io/self-organising-systems/particle-lenia/
- APS 2025 abstract: https://meetings-archive.aps.org/smt/2025/mar-l58/10
- Ventrella Clusters: https://ventrella.com/Clusters/intro.html
- Particle Life: https://github.com/tom-mohr/particle-life, https://github.com/tom-mohr/particle-life-app
- ASAL: https://arxiv.org/html/2412.17799v2, code https://github.com/SakanaAI/asal
- PPS: https://pmc.ncbi.nlm.nih.gov/articles/PMC5346932, https://arxiv.org/abs/1512.04478
- Cabaret: https://arxiv.org/abs/2311.10761
- ALIEN: https://github.com/chrxh/alien
- Neural Particle Automata: https://arxiv.org/abs/2601.16096
- Hutton 2007 (DBLP): https://dblp.uni-trier.de/pid/89/4206.html
- Swarm Chemistry: https://bingdev.binghamton.edu/sayama/SwarmChemistry/

**PDE protocells.**
- Zwicker et al.: https://www.arxiv.org/pdf/1603.01571
- Seyboldt & Jülicher: https://ar5iv.labs.arxiv.org/html/1803.03425
- Pearson: https://ar5iv.arxiv.org/html/patt-sol/9304003
- Munafo: https://mrob.com/pub/comp/xmorphia/pearson-classes.html
- Li & Cates: https://arxiv.org/pdf/2001.02563
- Active emulsions review: https://arxiv.org/pdf/1806.09552
- Xu & Zhao: https://arxiv.org/pdf/1811.11306
- FCH numerics: https://arxiv.org/pdf/1610.02473
- Kraitzman & Promislow: https://ar5iv.arxiv.org/html/1711.00396
- Lowengrub, Rätz & Voigt: https://tu-dresden.de/mn/math/wir/ressourcen/dateien/forschung/publikationen/pdf2009/phase_field_modeling_of_the_dynamics_of_multicomponent_vesicles.pdf
- Du, Liu & Wang: https://pure.psu.edu/en/publications/a-phase-field-approach-in-the-numerical-study-of-the-elastic-bend/
- Schmid: https://arxiv.org/pdf/cond-mat/9811070
- Gozdz & Holyst: https://arxiv.org/pdf/cond-mat/9604003
- Hillen & Painter: https://iris.polito.it/bitstream/11583/2973885/1/HillenPainter2009Preprint.pdf
- Lloyd et al.: https://department-mathematics.pages.surrey.ac.uk/david-lloyd/personal/files/Localised_hexagons.pdf
- Tlidi et al. chapter: https://link.springer.com/10.1007/978-3-319-24871-4_21
- AMB+: https://arxiv.org/pdf/1801.07687
- Active Model H: https://ar5iv.arxiv.org/html/1211.4707
- Giomi & DeSimone: https://arxiv.org/abs/1310.1908
- Demarchi et al.: https://arxiv.org/pdf/2301.00392
- Abu Hamed & Nepomnyashchy: https://arxiv.org/pdf/1910.01421
- Löber, Ziebert & Aranson: https://pmc.ncbi.nlm.nih.gov/articles/PMC4361886/
- McMullin SCL: https://sfi-edu.s3.amazonaws.com/sfi-edu/production/uploads/sfi-com/dev/uploads/filer/3c/b6/3cb67945-036c-490d-afd5-9aa40c5a48af/97-01-002.pdf
- McMullin & Varela: https://ideas.repec.org/p/wop/safiwp/97-02-012.html
- Battle: https://arxiv.org/pdf/2401.07969
- Ono & Ikegami: https://ar5iv.labs.arxiv.org/html/adap-org/9905002
- Fellermann & Solé: https://arxiv.org/pdf/q-bio/0607027
- Macia & Solé: https://arxiv.org/pdf/q-bio/0607035

**Judges, mutation, metrics.**
- ASAL++: https://arxiv.org/html/2509.22447
- VLM-RM: https://arxiv.org/html/2310.12921
- Leniabreeder: https://arxiv.org/html/2406.04235v1
- Sensorimotor Lenia: https://arxiv.org/html/2402.10236v1, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12577699/
- Reinke et al.: https://ar5iv.labs.arxiv.org/html/1908.06663
- ELM: https://arxiv.org/pdf/2206.08896
- LMX: https://arxiv.org/abs/2302.12170
- FunSearch: https://pmc.ncbi.nlm.nih.gov/articles/PMC10794145/
- AlphaEvolve: https://arxiv.org/html/2506.13131
- ShinkaEvolve: https://arxiv.org/html/2509.19349v1
- OpenEvolve: https://pypi.org/p/openevolve
- OMNI: https://arxiv.org/html/2306.01711v3
- OMNI-EPIC: https://arxiv.org/html/2405.15568v3
- AI Scientist: https://arxiv.org/html/2408.06292v3
- DGM: https://arxiv.org/html/2505.22954, https://sakana.ai/dgm/
- Digital Red Queen: https://arxiv.org/abs/2601.03335
- LLM-SR: https://proceedings.iclr.cc/paper_files/paper/2025/hash/28df8e730c054c5331855fd4d5403ba9-Abstract-Conference.html
- Zheng et al.: https://arxiv.org/abs/2306.05685
- Wang et al.: https://arxiv.org/abs/2305.17926
- G-Eval: https://aclanthology.org/2023.emnlp-main.153
- Gao et al.: https://arxiv.org/abs/2210.10760
- Krakauer et al.: https://pmc.ncbi.nlm.nih.gov/articles/PMC7244620/
- Lizier et al.: https://ar5iv.arxiv.org/html/0809.3275
- Shalizi et al.: https://arxiv.org/abs/nlin/0508001
- Biehl et al.: https://ar5iv.arxiv.org/html/1605.05676
- Kolchinsky & Wolpert: https://ar5iv.labs.arxiv.org/html/1806.08053
- Beer 2015 (via dblp): https://dblp.org/pid/64/2210
- Spector et al.: https://arxiv.org/html/2409.20491v1
- Topaz et al.: https://arxiv.org/pdf/1412.6430
- McGuirl et al.: https://arxiv.org/pdf/1910.08433
- MODES: https://par.nsf.gov/servlets/purl/10104628
- Cisneros et al.: https://arxiv.org/pdf/1911.01086
- Hudcová & Mikolov: https://arxiv.org/abs/2008.13503
