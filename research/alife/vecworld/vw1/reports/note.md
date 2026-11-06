I've written the formal note at `/home/user/evalwork/vecworld/vw1/note/CATEGORY.md`. It runs about 4900 words before the references (one-page summary plus 12 definitions and 12 propositions), so above the 3000–4000 target; the symbols inflate the count.

I added one closed-form check, `/home/user/evalwork/vecworld/vw1/note/checks/gap_split.py` (output `gap_split.json`). It only reads `spec/`, uses `-B` so nothing was written there, and runs on the shared venv. The venv already existed (another agent made it), so I did not recreate it; JAX was not needed.

## Main definitions and results

- **Two layers.** The meaning of a world lives in a Markov category (BorelStoch). A level is a Markov kernel with inputs, a public admissibility automaton (Def. 2) and an initial law. The code holds a *presentation*: a pure step f(x, u, ω) with keyed noise. Every kernel has presentations, but not a unique one (Prop. 1).
  - Two copies run with shared noise realise copy∘F; with independent noise they realise (F⊗F)∘copy. These agree only for deterministic F.
  - So common random numbers should be variance reduction only. VW-0's `replay="full"` is the one exception: it hands the agent presentation-level behaviour.
- **Coarse-grainings** are deterministic causal transducers (Def. 4) with three supervenience conditions: no noise, no input bypass, memory updated from the new micro state only. With memory, level 1 supervenes on the micro *history*, and the coarse-graining factors through an extended level whose path law matches the original (Prop. 2).
- **Morphisms** (Φ, λ) map states forward and inputs backward. Exact ones form a symmetric monoidal category, Lev (Prop. 3).
- **Four strengths of exactness** (Prop. 4): pathwise ⇒ strong (lumpability, which is bisimulation) ⇒ informational closure.
  - Weak lumpability does not imply closure; my counterexample is a bit copied into y.
  - Closure does not imply Markov: closure allows level-1 memory.
- **Metric defect** against a declared candidate law (Prop. 5).
  - The induced law is a Markov projection, within a factor 2 of the best possible candidate.
  - Defects compose affinely: δ(ΨΦ) ≤ Lip(Ψ)·δ(Φ) + δ(Ψ).
  - Over time they propagate as e_{t+1} ≤ K·e_t + δ_t, and they add under products.
- **Closure defect** composes by the chain rule with no Lipschitz assumption: Γ_X(Z) = Γ_Y(Z) + I(x_{≤t}; z_{>t} | y_{≤t}) ≤ Γ_Y(Z) + Γ_X(Y) (Prop. 6). The catch is that every term is relative to one process law.
- **New result on VW-0's gap** (Prop. 7): it is a port part plus a coarse-graining part. In closed form (τ = 1, whole past):

  | world | gap (nats) | port part | coarse-graining part |
  |---|---|---|---|
  | ring | 0.271 | 0.195 | 0.076 |
  | random | 1.190 | 0.165 | 1.024 |
  | stack(ring) | 0.088 | 0.060 | 0.028 |

  For the ring, most of the "gap" is observation noise, not a failure of level 1 to close.
- **Exact refinement** in closed form: the refinement's own share of the gap is −4e-16 and the gap moves by 2e-14. The leaky refinement (η = 0.3) splits as 0.5428 = 0.2758 + 0.2670.
- **Ports and exams.** The ports form a lens; blindness and public decidability become properties of its backward map (Prop. 8).
  - Exams depend on a world only through its open-loop behaviour, and for these Moore-type worlds that behaviour also fixes every closed-loop law (Prop. 9). Closed-loop exams therefore need no new world semantics.
  - The oracle, the gap and the observation rate condition on hidden state. They survive exact refinement but move under approximate refinement; the leak changes even under exact refinement.
- **Operators.**
  - Stack: associative and unital.
  - Product: monoidal on level 0 and its coarse-grainings, not on ports.
  - Stride: an action of (ℕ₊, ×) that preserves exactness and amplifies defects at most geometrically. Closure can move either way, with an example of each (Prop. 10).
  - Refine: pre-composition with the input port pulled back; the kick must lift (Prop. 11).
  - Couple: wiring diagrams, well defined because worlds are Moore systems. It preserves exactness when every wire reads a coarse signal (Prop. 12).

## What I changed from the agreed outline, and why

1. **Admissibility is an automaton on input histories**, not a subset of U: `min_interval` and `episode_budget` depend on history. The "information constraint" (inputs blind to hidden state) belongs to the agent–world wiring, not to the level.
2. **"Lumpability" must mean strong lumpability.** Weak lumpability is not closure, which agrees with Rosas et al. 2024 (Thm. 3). Closure is what an agent needs; strong exactness is what composes cleanly.
3. **"Induced, never written" is made precise** as a Markov projection relative to a declared reference law. This is why defects need declared candidate laws: under refinement the old level-0 law becomes the declared law of the now-induced level 0.
4. **Ports are lenses only once observation noise is sampled inside the update.** Myers (Remark 2.2.0.6) requires a deterministic expose map for stochastic lens composition.
5. **An apparatus with memory is a system, not a lens**, and is wired in. Memory coarse-grainings are not natural under stride: an A_gliders body moves 1.6 px per tick at stride 20 but 16 px at stride 200, beyond its 12.7 px length, so the tracker's overlap matching breaks.
6. **Morphisms carry an input map pointing backwards**, which lifted actuation needs.
7. **Two corrections to VW-0's DESIGN.md.**
   - Stacking with a fresh observation port can *raise* leak: Ψ = c·id with c > 1 at the same noise. The data-processing claim needs the new port to be a garbling of the old one.
   - Skill normalised by the oracle is not comparable across worlds whose base levels differ.
8. **Correlated noise is wiring from a shared noise-source world**, never a modified tensor.

## Open questions

1. Is there a single defect that composes, propagates and bounds exam skill?
2. Which reference law makes a world's defect independent of the agent under closed-loop agents?
3. Is there a behavioural metric on worlds under which exam scores are Lipschitz, so that a universality class is a ball?
4. Should trackers be audited against the causal states of y? Φ_objects keeps 16593 numbers of memory for a 144-number output.
5. Autodiff Fisher information with fixed keys is the complete-data Fisher information. It is only an *upper bound* on what o carries (missing-information principle, Louis's identity). When is the bound enough?
6. Should the dt/2 numerical-validity test be certified as an approximate morphism under stride?
7. Should noise-source worlds be a first-class type?

The note ends with a table mapping `Level`, `CoarseGrain`, `InputPort`, `ObservePort`, `World`, the five operators, the certificates and autodiff Fisher to these definitions and the contracts that enforce them.

## Citations

I checked almost all citations by web search and marked them VERIFIED. For Fritz, Myers and Rosas et al. I also read the specific definitions, remarks and theorems cited. Three are VERIFIED only through secondary sources: Kemeny–Snell, Dynkin's criterion (whose statement I prove in the note) and the noise-outsourcing lemma. Three items are marked MEMORY: the venue of Bertschinger et al. 2006, the conditional-law part of Rogers–Pitman, and the commutativity of the Giry monad.