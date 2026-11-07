# PhySim worlds as a category of supervenient systems

VW-1 formal note, draft of 2026-11-06. It formalises the agreed definitions, improves them where needed, and maps them to the implementation types. Companion to `spec/DESIGN.md` (VW-0). Numbers marked "closed form" come from `spec/lingauss.py`. The decomposition in Proposition 7 is computed by `note/checks/gap_split.py` (output in `checks/gap_split.json`). Citations are marked VERIFIED (checked by web search for this note) or MEMORY (not checked).

## Summary

**Two layers.** The *semantics* of a world lives in the Markov category BorelStoch. A **level** is an open stochastic system L = (X, U, A, F, μ): a Markov kernel F : X × U ⇝ X, a public *admissibility automaton* A on input histories, and an initial law μ. The *presentation* is what code holds: a pure step f(x, u, ω) with explicit noise ω drawn from keys. Every kernel has presentations, but not a unique one. The freedom is in the couplings between runs that share noise, which is exactly what common-random-number (CRN) branching exploits.

**Morphisms.** A **coarse-graining** is a deterministic causal transducer: memory m, readout y = φ(x, m). The upper level then supervenes on the micro *history*. A **morphism** (Φ, λ) maps states forward and inputs backward. It is **exact** when Φ_*F(x, λu) = F′(Φx, u). Exact morphisms form a symmetric monoidal category **Lev**. Exactness comes in four strengths: pathwise ⇒ strong (lumpability, bisimulation) ⇒ informational closure. Weak lumpability does not imply closure, and closure does not imply that the upper level is Markov.

**Defects.** A real coarse-graining carries a declared defect.
- The *metric defect* δ is a Wasserstein distance to a declared candidate law. It composes affinely, δ(ΨΦ) ≤ Lip(Ψ)·δ(Φ) + δ(Ψ), and propagates over time with the candidate's Lipschitz constant.
- The *closure defect* Γ is a conditional mutual information. It composes by the chain rule, Γ_X(Z) = Γ_Y(Z) + I(x_{≤t}; z_{>t} | y_{≤t}) ≤ Γ_Y(Z) + Γ_X(Y), with no Lipschitz assumption, but only relative to one process law.

**Consequence for VW-0.** The VW-0 gap mixes the coarse-graining's defect with the observation port's noise. On the ring world (τ = 1, whole past), 0.195 of the 0.271 nats belong to the port and 0.076 to the coarse-graining (closed form).

**Worlds, ports, exams.** A **supervenient world** is a chain L0 → … → Lk with ports. The ports form a lens: the forward part is a noisy readout, the backward part a blind, partial placement of inputs. Changing a memoryless apparatus composes lenses; an apparatus with memory is a system and has to be wired in. An exam depends on a world only through its *behaviour*, the family of open-loop input-output laws. Because worlds are Moore systems, that family also fixes the closed-loop law for every agent. Exact morphisms that respect the ports, and exact refinements in particular, therefore leave every score unchanged. The oracle, the gap and the leak condition on hidden state, so they are not behaviour-level.

**Operators.**
- *stack* is post-composition.
- *product* is symmetric monoidal on cores, not on ports.
- *stride* is an action of (ℕ₊, ×) that preserves exactness, amplifies metric defects at most geometrically, and can move closure either way.
- *refine* is pre-composition. The input port is pulled back and the kick must lift.
- *couple* is wiring. It is well defined for Moore systems and preserves exactness when wires read coarse signals only.
- Correlated noise is wiring from a shared noise source.

**Changes from the agreed outline.**
1. Admissibility is an automaton on histories. Information constraints belong to the wiring, not to the level.
2. "Lumpability" must mean *strong* lumpability. The property agents need is closure.
3. The induced law is a Markov projection relative to a declared reference law.
4. Ports are lenses only once observation noise is sampled inside the update.
5. Memory gives supervenience on histories.
6. Morphisms carry a backward input map, which refinement needs.
7. VW-0's data-processing claim for stacking needs a garbling condition.

## 1. Levels

**Conventions.**
- Spaces are standard Borel, with a metric where one is needed.
- A kernel is written K : X ⇝ Y, and L∘K means "K, then L". f_* is pushforward and ⊗ the independent product.
- W_p is the Wasserstein distance and I the mutual information.
- As in VW-0, laws are conditional on an open-loop program π. "Under (μ, π)" names a process law. Pasts and futures are written x_{≤t} and y_{>t}.

**Definition 1 (presentation).** A presentation is a noise space (Ω, ν), a measurable step f : X × U × Ω → X, and an initial map g : Ω₀ → X. A run is x₀ = g(ω₀), x_{t+1} = f(x_t, u_t, ω_{t+1}) with independent ω's. Its *semantics* is the kernel F(x, u) = f(x, u, ·)_*ν together with μ = g_*ν₀.

**Definition 2 (admissibility automaton).** A = (C, c₀, adm, next), with 0 ∈ adm(c) ⊆ U and next : C × U → C. A sequence is admissible if u_t ∈ adm(c_t) at every tick. *Public decidability* (DESIGN §3) means that A makes no reference to X. In VW-0, c = (tick, last non-empty tick, spent budget). min_interval and episode_budget depend on history, so a subset of U cannot express them.

**Definition 3 (level).** L = (X, U, A, F, μ), with F : X × U ⇝ X required on admissible inputs. A presentation is optional extra structure. The trivial level I has one state and one input. "Inputs blind to hidden state" is a constraint on wiring (Section 5), not a property of L.

**Why a Markov category** [F]:
1. Chapman–Kolmogorov is composition.
2. Determinism is intrinsic: f is deterministic iff copy∘f = (f⊗f)∘copy [F, Def. 10.1]. Coarse-grainings must be deterministic.
3. ⊗ *is* independence, so correlated noise has to be some other morphism.
4. VW-0 measures under reference laws. A Markov category provides μ-almost-sure equality [F, Def. 13.1] and conditionals [F, Def. 11.5]. BorelStoch has the latter, which weak exactness and Markov projections need.

**Proposition 1 (presentations versus kernels).**
- (a) Every kernel between standard Borel spaces has a presentation.
- (b) Presentations of one F give equal laws to single runs, but can give different laws to runs that share noise.
- (c) Two copies from one state realise copy∘F with shared noise and (F⊗F)∘copy with independent noise. These agree iff F is deterministic.
- (d) B members with independent noise realise F^{⊗B}.

*Proof.* (a) Noise outsourcing [K]; abstractly, randomness pushback [F, Def. 11.19]. (b) f(x, u, σ_u(ω)), with ν-preserving bijections σ_u, has the same kernel but a different joint law of (f(x, u, ω), f(x, u′, ω)). (c) Definition of determinism. (d) Independence. ∎

*Consequence.* Certificates should have kernel-level estimands. The VW-0 response G is a mean difference, so CRN only reduces its variance. The exception is `replay = "full"`. It hands the agent presentation-level behaviour (rewindable noise), so such a world is defined only together with its presentation (DESIGN Q2).

**Example 1 (A_gliders level 0).**
- X = ℝ₊^{2×128×128} and U = ℝ^{128·128} (one actuator per cell).
- F(x, u) = (F_FL^ξ)^{20}(κ(x, u)): the zero-sum kick κ, then 20 Flow-Lenia substeps with flow noise of std 0.5. The noise is keyed by (stream, seed, member, tick).

## 2. Coarse-grainings and supervenience

**Definition 4 (coarse-graining).** A coarse-graining from L to Y is a transducer Φ = (M, m₀, upd, φ):

m₀ = m₀(x₀), m_{t+1} = upd(m_t, x_{t+1}), y_t = φ(x_t, m_t).

It is memoryless when M = 1. It is *supervenient* if:
- (S1) m₀, upd and φ take no noise argument;
- (S2) upd reads only the new micro state, not inputs or keys;
- (S3) inputs reach upper levels only through x.

Non-injectivity of φ(·, m) is a non-triviality condition, not part of supervenience; the leak certificate quantifies it.

**Proposition 2 (memory).**
- (a) (x_t, m_t) is Markov: the *extended level* L⋉Φ.
- (b) y_{0:t} = G_t(x_{0:t}) for deterministic G_t, so the upper level supervenes on micro *histories*.
- (c) x_{0:∞} ↦ (x, m)_{0:∞} identifies the path laws of L and L⋉Φ. A memory coarse-graining is therefore a span L ← L⋉Φ → Y whose left leg is an isomorphism on paths.
- (d) Transducers compose as cascades: Ψ∘Φ has memory M_Φ × M_Ψ, with Ψ's memory fed φ(x, m_Φ) (VW-0 `stack`). Composition is associative up to the canonical isomorphism of products and unital.

*Proof.* Induction on t, and associativity of products. ∎

*Care.*
- The process y depends on when the observer starts (m₀ is taken at the end of burn-in).
- Memory can dwarf y. Φ_objects (12 slots × 12 features, so y has 144 numbers) keeps a 128×128 label map, 16593 memory numbers in all. That memory is a route by which y can accumulate micro information over time. Φ_coarse (192 block statistics) is memoryless.

## 3. Exact morphisms

**Definition 5 (morphism).** A morphism (Φ, λ) : L → L′ is a deterministic Φ : X → X′ and λ : U′ → U with λ(0) = 0, where λ maps admissible sequences of L′ to admissible sequences of L. It is *exact* if Φ_*F(x, λu′) = F′(Φx, u′) for all x and admissible u′, and Φ_*μ = μ′. The input map points backwards because a coarse input must be realised by a fine one; refinement needs this. Inside one world, λ = id.

**Proposition 3 (Lev).**
- (a) Levels and exact morphisms form a category, with identities (id, id) and composition (Ψ, λ′)∘(Φ, λ) = (ΨΦ, λλ′).
- (b) It is symmetric monoidal under (X×X′, U×U′, A×A′, F⊗F′, μ⊗μ′), with unit I, and tensors of exact morphisms are exact.

*Proof.* (ΨΦ)_*F(x, λλ′u″) = Ψ_*F′(Φx, λ′u″) = F″(ΨΦx, u″). The pushforward of a product law along a product map is the product of the pushforwards. ∎

**Definition 6 (four strengths of exactness)**, for memoryless Φ; a memory Φ is handled through L⋉Φ.
- (E1) *pathwise*: Φ(f(x, u, ω)) = f′(Φx, u, ω) for ν-almost every ω (a semiconjugacy).
- (E2) *strong*: Φ_*F(x, u) depends on x only through Φx (Dynkin's criterion; Kemeny–Snell strong lumpability, with inputs as labels).
- (E3) *weak*: y is Markov for some initial law. A sufficient condition is Rogers–Pitman intertwining [RP]: a kernel Λ : Y ⇝ X concentrated on the fibres of Φ with F∘Λ = Λ∘F′, where F′ := Φ_*∘F∘Λ, and μ = Λ∘ν.
- (E4) *informational closure* under (μ, π) [B, R]: Γ_X(Y) := I(x_{≤t}; y_{>t} | y_{≤t}) = 0 at every t. Here x_{≤t} may be replaced by the Markov state (x_t, m_t).

**Proposition 4.**
1. E1 ⇒ E2 ⇒ E4, the last for every μ and open-loop π.
2. E2 ⇒ E3.
3. E3 ⇏ E4.
4. E4 does not imply that y is Markov.

*Proof.*
1. E1 ⇒ E2: Φ_*F(x, u) = f′(Φx, u, ·)_*ν. E2 ⇒ E4: by induction, law(y_{>t} | x_{≤t}) is the F′-path law from Φx_t, a function of y_t.
2. Under E2, y is Markov for every initial law.
3. Let x_t = (y_t, b_t), b_t i.i.d. fair bits, y_{t+1} = b_t. Then y is i.i.d. and Λ(y) = δ_y ⊗ Bern(½) intertwines, but Γ = I(b_t; y_{t+1}) = log 2. Rosas et al. [R, Thm. 3] prove the same separation for ε-machines.
4. Take y AR(2) started from a deterministic y_{−1} (say 0) and x_t = (y_t, y_{t−1}): then Γ = 0 at every t, but y is not Markov. (With a random y_{−1} the t = 0 term I(y_{−1}; y_{>0} | y_0) is positive; alternatively take the supremum over t ≥ 1.) Closure permits level-1 *memory*. ∎ [Checker: start condition added; the unqualified example fails at t = 0.]

*Reading.*
- An agent needs E4. Composition is cleanest for E2. "Lumpability" in the outline should therefore read *strong*; E3 alone does not make a level.
- For finite X, E2 says that the kernel equivalence of Φ is a Larsen–Skou probabilistic bisimulation [LS] with inputs as labels; the definitions coincide.
- Invariants are exact morphisms to identity-law levels. A_gliders' mass map is E1-exact onto (ℝ², U, id) because the zero-sum kick and reintegration both conserve mass (measured drift 1.9·10⁻¹⁴).
- Symmetries are automorphisms of L0. Periodic Flow-Lenia commutes with torus translations, while Φ_coarse is equivariant only for multiples of its 16-px block. The hidden port permutations are isomorphisms of *interfaces*, not automorphisms of L0.

## 4. Approximate morphisms and their defects

Only L0 has a law. To account for defects, each upper level gets a *declared* law that is never used to simulate. Its canonical choice is the following.

**Definition 7 (Markov projection; metric defect).** Fix a reference law ρ on X, for example the law of x_t under the exam's (μ, π). Let Λ_ρ be the disintegration of ρ along Φ. The *Markov projection* is F′_ρ(y, u) := Φ_*F(Λ_ρ(y), u). For a declared candidate F′, write F_x := Φ_*F(x, u). The *metric defect* is

δ_p(Φ; F′; ρ) := sup_u (∫ W_p(F_x, F′(Φx, u))^p ρ(dx))^{1/p}.

The uniform defect δ_∞ takes the supremum over x. The *fibre oscillation* is ω_ρ := sup_u ∫∫ W₁(F_x, F_x̃) Λ_ρ(Φx, dx̃) ρ(dx).

**Proposition 5 (metric defects).**
- (a) δ = 0 for some F′ and every ρ iff E2 holds.
- (b) *The projection is near optimal:* ω_ρ/2 ≤ inf_{F′} δ₁(Φ; F′; ρ) ≤ δ₁(Φ; F′_ρ; ρ) ≤ ω_ρ.
- (c) *Composition.* Let Φ : X → Y carry candidate F_Y, and let Ψ : Y → Z be L_Ψ-Lipschitz with candidate F_Z. Then
  δ_p(ΨΦ; F_Z; ρ) ≤ L_Ψ·δ_p(Φ; F_Y; ρ) + δ_p(Ψ; F_Z; Φ_*ρ),
  with Ψ's defect measured against F_Y. Grade a morphism by e ↦ L e + δ. Grades compose in the monoid of affine self-maps of [0, ∞), and the grade of a composite is at most the composite of the grades. Lev is the grade-(L, 0) part.
- (d) *Propagation.* Suppose F′ is K-Lipschitz in W_p, and run y′ under F′ from Φ_*ρ₀ with ρ_t = law(x_t). Then e_t := W_p(law Φx_t, law y′_t) satisfies e_{t+1} ≤ K e_t + δ_p(Φ; F′; ρ_t).
- (e) *Products.* With the sum metric, p = 1 and product admissible sets, defects add.

*Proof.*
- (b) Upper bound: convexity of W₁. Lower bound: for x and x̃ in one fibre y, W₁(F_x, F_x̃) ≤ W₁(F_x, F′(y)) + W₁(F′(y), F_x̃); integrate, since (x̃, Φx) has the law of (x, Φx).
- (c) The triangle inequality, W_p(Ψ_*a, Ψ_*b) ≤ L_Ψ W_p(a, b), and Minkowski's inequality.
- (d) Joint convexity of W_p^p under mixtures, and a K-Lipschitz kernel maps couplings to couplings.
- (e) Kantorovich duality with separable test functions gives ≥; the product coupling gives ≤. ∎

*Remarks.*
- F′_ρ depends on ρ (program, time) unless E2 holds. A program-dependent projection is the operational form of the review's weak-lumpability warning.
- VW-0's δ²_T = E‖E[Ψx(T)|x] − E[h0(T)|h0 = Ψx]‖² compares means only. Because ‖mean difference‖ ≤ W₁ ≤ W₂, it lower-bounds the T-step defect (ring, η = 0.3: δ²₁ = 0.230, closed form). That δ_T = 0 does not imply exactness is DESIGN's "and matching noise".
- A_gliders' closure ceilings fall from 0.988 to 0.34 between τ = 1 and τ = 8 for Φ_coarse, and from 0.81 to 0.26 for Φ_objects. This is consistent with the compounding in (d) but does not isolate it: the ceilings use a linear level-1 predictor, so the fall also contains predictor misspecification. [Checker: was "visible empirically".]

**Definition 8 (closure defect).** Under (μ, π), let Γ_X(Y) := sup_t I(x_{≤t}; y_{>t} | y_{≤t}). Suppose Z supervenes on Y: z_{≤t} is a function of y_{≤t}, and z_{>t} is a function of (y_{≤t}, y_{>t}), which allows memory. Define Γ_Y(Z) := sup_t I(y_{≤t}; z_{>t} | z_{≤t}). VW-0's Γ(τ, p) uses a window p and a single future time τ.

**Proposition 6 (closure defects compose).** For supervenient X → Y → Z under one process law, at each t,

I(x_{≤t}; z_{>t} | z_{≤t}) = I(y_{≤t}; z_{>t} | z_{≤t}) + I(x_{≤t}; z_{>t} | y_{≤t}) ≤ Γ_Y(Z) + Γ_X(Y).

So closure is transitive, the total defect is at least the defect relative to the intermediate level, and no Lipschitz assumption is needed. For independent products the conditional informations add at each t, so Γ = sup_t is subadditive, and additive when both suprema are attained at the same t. [Checker: "Γ is additive" held only per t.]

*Proof.* y_{≤t} is a function of x_{≤t}, so I(x_{≤t}; ·) = I(x_{≤t}, y_{≤t}; ·). Apply the chain rule. In the second term, y_{≤t} ⊇ z_{≤t}, and given y_{≤t}, z_{>t} is a function of y_{>t}, so conditional data processing applies. Mutual information is additive over independent pairs. ∎

The VW-0 calibration confirms additivity on concat(ring, random) to 1.8·10⁻¹⁵ nats.

**Proposition 7 (the VW-0 gap = port part + coarse-graining part).** Let o_t = r(y_t, η_t) with i.i.d. η independent of everything else (noise, signs, clip, quantiser). Then

Γ_X(O) = I(y_{≤t}; o_{>t} | o_{≤t}) + I(x_{≤t}; o_{>t} | y_{≤t}),

and the second term is at most Γ_X(Y). The first term, the *port part*, can be positive even when Φ is exact. It is positive whenever the noiseless past y_{≤t} predicts o_{>t} better than the noisy past o_{≤t} does; it vanishes, for example, for i.i.d. y. [Checker: was "positive whenever noise hides y".] The split uses open-loop programs: under a closed-loop agent η_{≤t} reaches x_{>t}.

*Proof.* Proposition 6, using that o_{≤t} is independent of (x_{≤t}, o_{>t}) given y_{≤t}. ∎

Closed form, τ = 1, whole past (`checks/gap_split.py`):

| world | gap | port part | coarse-graining part |
|---|---|---|---|
| ring | 0.2713 | 0.1953 | 0.0759 |
| random | 1.1899 | 0.1654 | 1.0245 |
| stack(ring) | 0.0881 | 0.0602 | 0.0279 |

VW-0 should report both terms. The second needs a predictor given the *noiseless* level-1 past, which is still supervenient information.

## 5. Supervenient worlds, ports as lenses, exams

**Definition 9 (world).** W = (L0, Φ₁…Φ_k, P_in, P_obs).
- L0 is a level with a presentation.
- Each Φ_i is a supervenient transducer Y_{i−1} → Y_i.
- P_in = (A, e, σ_a): the automaton in agent coordinates, the hidden embedding e (a permutation onto the actuable set) and actuation noise.
- P_obs = (P, S, σ_o, clip, quantiser, max_queries) reads level j ≤ k.

Upper levels carry induced processes, with declared laws used only for defect accounting. One tick: check, kick, law, memories, emit o_{t+1}.

**Definition 10 (ports as a lens).**
- The *core* is a stochastic Moore system with interface (Y_j, U₀): state X × M, kernel update, deterministic expose. Systems of this kind are lenses [My, Defs. 1.2.1.2 and 2.2.0.5].
- The ports are a lens P : (Y_j, U₀) ⇆ (O, ℝ^{n_in}). The forward part is the readout. The backward part is the partial map P^♭(y, a) = e(a) (with actuation noise), defined on adm(c).
- The agent sees P∘W.

Myers' stochastic lenses need a deterministic expose map ([My], Remark 2.2.0.6); otherwise lens composition is not well defined. So o_{t+1} is sampled inside the update and stored, after which monadic-lens composition [My, Def. 2.6.4.6] applies. VW-0's keyed noise already does this implicitly.

**Proposition 8.**
- (a) *Blindness* means P^♭ ignores y. *Public decidability* means the domain of P^♭ depends only on c. Together, rejection reveals nothing about hidden state. State-dependent limits belong in κ.
- (b) Changing a memoryless apparatus is lens composition. Stacking a memoryless Ψ is (Ψ, π₂) : (Y_j, U) ⇆ (Y_{j+1}, U), and changing σ_o or the permutations is a lens on (O, ℝ^{n_in}). Replicas are related by an isomorphism of interfaces.
- (c) An apparatus with memory is a system, not a lens, because its output depends on its own state. It is wired in (Section 6.5).

**Definition 11 (behaviour, agent, exam).**
- The behaviour is B_W = {law(o_{0:T} | a_{0:T−1}) : a admissible and open-loop}.
- An agent is a stochastic system with the reversed interface. The closed loop is its wiring with W.
- An exam item is an open-loop context (prefix program, revealed o_{0:P}, test program, queries). Its score is s = E ℓ(pred, o_{P+q}).

**Proposition 9 (exams are evaluations through a lens).**
- (a) s depends on W only through B_W. VW-0's replicate futures reduce variance without changing the expectation.
- (b) *Causality.* If B_W = B_{W′}, then every agent induces the same closed-loop law of (a, o) in W and in W′, for agents that act only through the ports, within one episode, with randomness independent of the world's noise. (Replays and resets that reuse noise are presentation-level, Proposition 1.)
- (c) Suppose (Ψ, λ) : L0′ → L0 is exact, W′ has chain Φ_i∘Ψ, input port λ∘P_in, the same P_obs, and μ = Ψ_*μ′. Then B_{W′} = B_W. Every agent's scores coincide, and so do all behaviour-level quantities: V0, the level-1 error Vε and the designer's level-1 ceiling, the response G and the input capacity.
- (d) Some quantities condition on the hidden state: the oracle Vυ = E Var(o_{t+τ} | x_t), the gap Γ and the observation rate. These are *not* behaviour-level. They are invariant under exact refinement, because the refinement term of the chain rule (Proposition 6) vanishes under E2, but they move under approximate refinement. The leak changes even under exact refinement, since its rank is that of the new hidden state (6/48 against 6/24 in the VW-0 calibration). Skill normalised by the oracle is therefore not comparable across worlds with different base levels. The default normaliser should be behaviour-level.

*Proof.*
- (a) The score is an expectation of a function of (revealed data, future).
- (b) In a Moore system, o_t depends on a_{<t} only. The closed-loop law is ∏_t law(o_t | o_{<t}; a_{<t}) · agent(a_t | o_{≤t}, a_{<t}), and each first factor is a conditional of the open-loop law.
- (c) By E2, Ψx′ has the law of x. Memories and observations are functions of that history plus independent noise.
- (d) The law of o_{t+τ} given x′_t equals its law given Ψx′_t under E2. ∎

Closed-loop exams (DESIGN Q5) need no new world semantics by (b); only the certificates move from conditioning on inputs to directed information.

## 6. Composition operators and their laws

**6.1 Stack** (post-compose a transducer).
- Laws: identity and associativity (Proposition 2(d)).
- Defects: Γ_Y(Z) ≤ Γ_X(Z) ≤ Γ_Y(Z) + Γ_X(Y). This is why VW-0 reports the gap relative to X and relative to level 1.
- *Correction to DESIGN §7.* Data processing gives I(x; z_{≤t}) ≤ I(x; y_{≤t}) for *noiseless* levels only. With a fresh port at the new level, leak and input visibility can rise: Ψ = c·id with c > 1 and unchanged σ_o raises the signal-to-noise ratio by c². The claim needs the new port to be a garbling of the old one. stack(ring)'s fall in leak information (7.43 < 11.85 nats) is consistent with the claim but not guaranteed.

**6.2 Product.**
- Cores tensor, (L0⊗L0′, Φ_i⊗Φ_i′), with the trivial world as unit. This is symmetric monoidal by Proposition 3(b), and defects add (Propositions 5(e) and 6).
- *Ports do not tensor.* VW-0 draws one joint port: block-mixing permutations, summed k, and a shared zero-sum that moves mass between blocks. The product world is isomorphic to the tensor of the worlds only for separable constraints.
- *Noise.* ⊗ requires split keys. A reused key gives copy∘F, the diagonal (Proposition 1(c)).
- *Correlated noise* should be expressed as wiring from a shared noise-source world, a level with no input whose state is the common noise. The tensor stays honest, and the correlation becomes a declared component. The library does not do this yet: `vw.product(..., noise=('correlated', ρ))` is a modified tensor (equal in law to wiring one Gaussian source into two explicit-noise levels, but with no declared source).

**6.3 Stride.** Let S_n(L) = (X, U, A_n, F_0^{n−1}∘F_u, μ), with F_0 = F(·, 0) and the input applied at the first substep.

**Proposition 10.**
- (a) S₁ = id and S_n S_m = S_{nm}: an action of (ℕ₊, ×) reparametrising time.
- (b) Each S_n is an endofunctor on Lev; this uses λ(0) = 0.
- (c) Uniform metric defects grow at most to δ(1 + K + … + K^{n−1}).
- (d) Closure is not monotone in n. In Proposition 4's bit example, Γ = log 2 at n = 1 and Γ = 0 at n = 2. For AR(2) with both coefficients non-zero (started as in Proposition 4.4), Γ = 0 at n = 1 and Γ > 0 at n = 2, because y_{2t−1} is not a function of the strided past.
- (e) Memory coarse-grainings are not natural under stride: S_n(L)⋉Φ ≠ S_n(L⋉Φ). An A_gliders body (median 0.08 px per substep, body length 12.7 px) moves 1.6 px per tick at stride 20 and 16 px at stride 200, where overlap matching fails. The tracker and the automaton's time counters must be re-declared for each stride.

*Proof.* (a) F_0^{n−1}∘(F_0^{m−1}F_u)… collapses to F_0^{nm−1}F_u. (b) Induction over substeps. (c) Proposition 5(d). (d) Direct computation. ∎

**6.4 Refine** (pre-compose with (Ψ, λ) : L₋₁ → L0). The chain becomes Φ₁∘Ψ, …; memories read Ψx; and the input port is pulled back, P_in′ = λ∘P_in, so the agent keeps L0 coordinates. Required:
- (R1) the kick lifts: Ψ(κ₋₁(x, λu)) = κ₀(Ψx, u), which is Ψ(x + Λu) = Ψx + u in VW-0's additive case;
- (R2) the automaton is unchanged;
- (R3) Ψ_*μ₋₁ = μ₀, or holds within the declared defect.

**Proposition 11.**
- (a) Refinement is functorial: (W∘Ψ)∘Ψ′ = W∘(ΨΨ′).
- (b) If (Ψ, λ) is exact, the refinement is invisible to agents and to behaviour-level certificates (Proposition 9(c)). The gap, the oracle and the observation rate are unchanged too (Proposition 9(d)). Ring with an exactly lumpable pair split: gap change 2·10⁻¹⁴ nats; refinement defect I(x₋₁,t; o_{t+1} | x₀,≤t) = −4·10⁻¹⁶ (closed form; VW-0 calibration 1.8·10⁻¹⁵).
- (c) If (Ψ, λ) is approximate, the composite metric defect is at most Lip(Φ)·δ(Ψ; F₀) + δ(Φ; F₁; Ψ_*ρ). The old F₀ becomes the *declared* law of the now-induced L0, which is why defects are defined against candidate laws. For closure, Γ_{X₋₁}(O) = Γ_{X₀}(O) + I(x₋₁,≤t; o_{>t} | x₀,≤t). Ring with η = 0.3: 0.5428 = 0.2758 + 0.2670. Here 0.2758 is measured on the *induced* X₀-process, not on the old world (0.2713).
- (d) *Fine actuation* (a port placed on L₋₁) admits no morphism of worlds in general; only the closed systems can be compared. The old port's meaning need not survive: λ sends a 1-sparse coarse kick to a 2-sparse fine one in the pair-split example.
- (e) State-dependent kicks ("cannot remove matter that is not there") need an explicit κ₋₁ satisfying (R1). VW-0 currently refuses lifted actuation with custom kicks; it should accept κ₋₁ and check (R1).

**6.5 Couple** (wiring diagrams). Boxes are worlds viewed as Moore systems. A wiring is a lens from ⊗_i(Out_i, In_i) to an outer interface.

**Proposition 12.**
- (a) Because every box is Moore (an input at t first shows at t + 1), every wiring defines a world, feedback included. Wiring is associative and unital. Vagner–Spivak–Lerman [VSL] prove the continuous-time version for systems whose outputs depend only on state; Myers [My] treats discrete and monadic systems.
- (b) *Totality.* Inside a world there is no InputViolation. A wire into an input passes through a declared map onto adm (physics, like κ). In `vw.couple` this map is a saturation onto the per-tick constraints (top-k, clip, zero-sum shift, rescale), not the Euclidean projection, and min_interval and the episode budget are not applied. Only the composite's agent-facing port must be publicly decidable.
- (c) *Exactness through wiring.* Suppose each box has an exact (Φ_i, λ_i), each wire reads a signal that factors through the coarse levels, and the fine wiring is λ∘(coarse wiring). Then the coupled coarse-graining is exact: a morphism of wiring-diagram algebras. If a wire reads micro state, closure of the parts does not imply closure of the whole. VW-0's diffusive coupling J is of this kind, and there the gaps stop adding.
- (d) *Noise.* A wired observation is either one measurement read twice (copy after readout) or two measurements. These differ unless the readout is deterministic, so the design must say which.

*Proof of (c).* Φ(F(x, u)) = ⊗_i Φ_i F_i(x_i, λ_i w_i(g(Φx), u)) = ⊗_i F_i′(Φ_i x_i, w_i(g(Φx), u)). ∎

## 7. What existing mathematics offers, and where this departs

- **Factor maps and semiconjugacy** are E1/E2 for deterministic or measure-preserving maps. **Random dynamical systems** [A] (skew products over a noise shift) are the presentation layer. *Departure:* inputs, defects, memory.
- **Lumpability**: strong and weak [KS, §6.4], [BR], intertwining on general spaces [RP], near lumpability [Bu], and KL aggregation [DMM]. *Departure:* input labels, transducer memory, uncountable spaces, and the fact that weak lumpability is not closure (Proposition 4; [R]).
- **Informational closure** [B, P, R]. *Departure:* the chain rule for composition (Proposition 6) and the port/coarse-graining split (Proposition 7).
- **Markov categories** [F, CJ] are the semantic layer. *Departure:* the implementation lives in a finer layer of presentations, where couplings matter.
- **Categorical systems theory**: systems as lenses, stochastic and monadic lenses [My, My2]; wiring diagrams [S13, SR, VSL]; lenses and Poly [S19, NS]; cybernetics [CGHR]. *Departure:* partial backward maps (admissibility), approximately commuting coarse-graining morphisms between systems, closure as a quantity, and exam invariance.
- **Bisimulation** [LS, DEP], behavioural metrics [DGJP], approximate bisimulation [GP], coalgebra [Ru]. An exact coarse-graining's kernel is a bisimulation, and δ is a one-sided analogue of an approximate-bisimulation precision. *Departure:* coarse-grainings are directed and non-injective, their codomain is the observation, and memory and closure have no bisimulation analogue.

## 8. Open questions

1. Is there one defect that composes, propagates and bounds exam skill (for example, a Gaussian bound from Γ to the skill lost against the ceiling)?
2. Defects are relative to the exam's (μ, π). Which reference law makes a world's defect agent-independent under closed-loop agents?
3. Is there a behavioural pseudometric on B_W under which scores are Lipschitz, so that a universality class is a ball?
4. Should trackers be compared with the causal states of y [R], so that a memory of 16593 numbers can be audited for minimality?
5. Autodiff with fixed keys gives the complete-data Fisher information E[Jᵀ Σ_o⁻¹ J], an *upper bound* on the information in o (missing-information principle [OW], Louis's identity [L]). When is the bound enough?
6. Should the RUBRIC dt/2 test be certified as an approximate morphism S₂(L_{dt/2}) → L_dt?
7. Should noise-source worlds be a first-class type?

## 9. Implementation types and the definitions they implement

| type | implements | the contract that enforces it |
|---|---|---|
| `Level` | presentation (Def. 1): `init(params, key)` ↦ μ = g_*ν₀; `step(params, x, noise, u)` ↦ f, with the kick κ inside `step` | pure, float64, noise only from a counter-based `Noise(key, t)`; the law at tick t of a member with key K draws from fold_in(fold_in(K, PROC), t), product factors from `stream(i)`, stride sub-steps from clock t·n + i (32-bit) |
| `CoarseGrain` | transducer (Def. 4): `phi(x, m)`, `init_memory(x)`, `update_memory(m, x_new)` | no key and no input argument (S1–S3 by the signature, by convention: Python cannot stop a closure over a key) |
| `InputPort` | lens backward part plus automaton (Defs. 2, 10) | public state c = (t, last non-empty t, spent); `Admissible.check(a, t, last_t, spent)` raises InputViolation before anything runs; accepted commands are canonicalised to exact zero sum; hidden permutation; actuation noise on its own stream |
| `ObservePort` | lens forward part (Def. 10) | o is a deterministic function of the carry (state, memories, tick, member key), i.e. a deterministic expose of the extended state |
| `World` | Def. 9 and its behaviour B_W | tick order check, kick, law, memory, observe; `vmap` with split keys gives F^{⊗B}; shared keys (designer only) give CRN couplings |
| `product`, `stack`, `stride`, `refine`, `couple` | Section 6 | split keys (or `'shared'`, or a `('correlated', ρ)` modified tensor) and one joint port; cascade memory; `lax.scan` with input at substep 1; `refine(check=)` runs `commutation_error` on the free law (R1 only if `u` is passed; R3 is not checked); `couple` is Moore by construction (the wire reads the state before the laws run) with saturated wires |
| certificates, `Exam` | functionals of B_W, plus hidden-state quantities (oracle, gap, observation rate, leak; Prop. 9(d)) | kernel-level estimands; `Exam` skill is normalised by the oracle by default (hidden-state, Prop. 9(d)); a behaviour-level ceiling must be passed as `ceiling=` |
| Fisher (autodiff) | `vw.fisher` returns the moment lower bound J̄ᵀΣ⁻¹J̄ (J̄ = ∂E o/∂θ by pathwise autodiff with fixed keys, Σ = Cov o) plus the Gaussian covariance term, exact for Gaussian o; the complete-data Fisher E[JᵀΣ_o⁻¹J] of open question 5 (an upper bound) is not what it returns | a θ-free noise law, Σ non-singular, and Φ differentiable almost everywhere (Φ_coarse is; the tracker is not); the unquantised channel |

### Differentiability is a property, not part of the definition

Levels are Markov kernels and coarse-grainings are measurable causal transducers; nothing in Sections 1-6 needs derivatives. Many of the coarse-graining levels that matter are discrete: counting bodies, keeping slot identities, recording a fusion or a fission. Requiring smoothness would exclude them, and a smooth relaxation (soft slots) changes what the level means.

Modules carry a `differentiable` flag. Differentiable modules stay differentiable under stack, product and stride (chain rule), so differentiable worlds form a subcategory. A world is differentiable exactly when every module on the path to the observed level is.

Where derivatives are used:
- **Designer analysis over a few ticks**, such as input sensitivity and actuator design. In a chaotic core, pathwise derivatives agree with finite differences only for one or two ticks (gliders world: median relative error at most 2.2e-4 at 1 tick; disagreement from 4 ticks on). Longer-horizon information quantities use the likelihood-ratio estimator, which needs a differentiable noise density, not differentiable dynamics.
- **Learning a coarse-graining.** An autoencoder or information bottleneck can propose the next level up when the lower dynamics is not known well enough to write that level by hand. Training needs gradients through Φ on sampled states, not through the core, and such learned maps are smooth by construction.

What the implementation does require is that every module be a pure, compiled, batchable function, so that a world is one program. The library marks a module that breaks this (`opaque=True`, a host callback) as opaque. The object tracker `vw.objects.BlobTracker` is pure JAX and not differentiable. With it, the gliders world (`port/aworld.py`, default `tracker='jax'`) is one compiled program, and only its object view is non-differentiable. The numpy tracker remains available as an opaque reference; the JAX tracker matches its decisions exactly.

## References

- [A] L. Arnold, *Random Dynamical Systems*, Springer, 1998. VERIFIED.
- [B] N. Bertschinger, E. Olbrich, N. Ay, J. Jost, "Information and closure in systems theory", 2006. VERIFIED as the origin of informational closure (via citing works); venue (*Explorations in the Complexity of Possible Life*, IOS Press) from MEMORY.
- [BR] C. J. Burke, M. Rosenblatt, "A Markovian function of a Markov chain", Ann. Math. Stat. 29(4):1112–1122, 1958. VERIFIED.
- [Bu] P. Buchholz, "Exact and ordinary lumpability in finite Markov chains", J. Appl. Prob. 31(1):59–75, 1994. VERIFIED.
- [CGHR] M. Capucci, B. Gavranović, J. Hedges, E. F. Rischel, "Towards foundations of categorical cybernetics", EPTCS 372:235–248, 2022. VERIFIED.
- [CJ] K. Cho, B. Jacobs, "Disintegration and Bayesian inversion via string diagrams", MSCS 29:938–971, 2019. VERIFIED.
- [DEP] J. Desharnais, A. Edalat, P. Panangaden, "Bisimulation for labelled Markov processes", Inf. Comput. 179(2):163–193, 2002. VERIFIED.
- [DGJP] J. Desharnais, V. Gupta, R. Jagadeesan, P. Panangaden, "Metrics for labelled Markov processes", TCS 318(3):323–354, 2004. VERIFIED.
- [DMM] K. Deng, P. G. Mehta, S. P. Meyn, "Optimal Kullback–Leibler aggregation via spectral theory of Markov chains", IEEE TAC 56(12), 2011. VERIFIED.
- Dynkin's criterion: attribution via Kemeny–Snell VERIFIED only through a secondary source; the statement is proved here (Proposition 4).
- [F] T. Fritz, "A synthetic approach to Markov kernels, conditional independence and theorems on sufficient statistics", Adv. Math. 370:107239, 2020. VERIFIED, including Defs. 10.1, 11.5, 11.19 and 13.1, and that BorelStoch has conditionals.
- [GP] A. Girard, G. J. Pappas, "Approximation metrics for discrete and continuous systems", IEEE TAC 52(5):782–798, 2007. VERIFIED.
- [K] Noise-outsourcing (functional representation) lemma, O. Kallenberg, *Foundations of Modern Probability*. VERIFIED via citing works; the theorem number depends on the edition.
- [KS] J. G. Kemeny, J. L. Snell, *Finite Markov Chains*, 1960 (2nd ed., Springer, 1976); lumpability in Ch. 6, weak lumpability in §6.4. VERIFIED via secondary sources.
- [L] T. A. Louis, "Finding the observed information matrix when using the EM algorithm", JRSS B 44:226–233, 1982. VERIFIED.
- [LS] K. G. Larsen, A. Skou, "Bisimulation through probabilistic testing", Inf. Comput. 94(1):1–28, 1991. VERIFIED.
- [My] D. J. Myers, *Categorical Systems Theory*, draft of 3 Sept 2023. VERIFIED, including Defs. 1.2.1.2, 2.2.0.5 and 2.6.4.6 and Remark 2.2.0.6.
- [My2] D. J. Myers, "Double categories of open dynamical systems", ACT 2020, arXiv:2005.05956. VERIFIED.
- [NS] N. Niu, D. I. Spivak, *Polynomial Functors: A Mathematical Theory of Interaction*, LMS Lecture Notes 498, CUP, 2025. VERIFIED.
- [OW] T. Orchard, M. A. Woodbury, "A missing information principle: theory and applications", Proc. 6th Berkeley Symp., 1972. VERIFIED.
- [P] O. Pfante, N. Bertschinger, E. Olbrich, N. Ay, J. Jost, "Comparison between different methods of level identification", Adv. Complex Syst. 17(2):1450007, 2014. VERIFIED.
- [Pl] E. Plantec et al., "Flow-Lenia", arXiv:2212.07906. VERIFIED.
- [R] F. E. Rosas, B. C. Geiger, A. I. Luppi, A. K. Seth, D. Polani, M. Gastpar, P. A. M. Mediano, "Software in the natural world: a computational approach to hierarchical emergence", arXiv:2402.09090, 2024. VERIFIED, including eq. 3 and Theorems 1 and 3.
- [RP] L. C. G. Rogers, J. W. Pitman, "Markov functions", Ann. Probab. 9(4):573–582, 1981. VERIFIED (citation and intertwining criterion).
- [Ru] J. J. M. M. Rutten, "Universal coalgebra: a theory of systems", TCS 249(1):3–80, 2000. VERIFIED.
- [S13] D. I. Spivak, "The operad of wiring diagrams", arXiv:1305.0297, 2013. VERIFIED.
- [S19] D. I. Spivak, "Generalized lens categories via functors C^op → Cat", arXiv:1908.02202. VERIFIED.
- [SR] D. I. Spivak, D. Rupel, "The operad of temporal wiring diagrams", arXiv:1307.6894, 2013. VERIFIED (via [VSL]'s reference list).
- [VSL] D. Vagner, D. I. Spivak, E. Lerman, "Algebras of open dynamical systems on the operad of wiring diagrams", TAC 30(51):1793–1822, 2015. VERIFIED (continuous time; outputs depend only on state).
- The commutativity of the Giry monad, used implicitly when applying [My]'s monadic lenses to measurable spaces, is from MEMORY.
