# Second reading of the track 1 and track 2 memos

I read `track1/DESIGN.md`, `track2/EXAM.md` and `inventory/WORLDS.md` and checked them against `vw1/fresh/*/results/summary.json`, the `vw` code, the port and v1's scorer. No new simulation; the new numbers come from rescaling existing summaries and a one-second linear-algebra check.

## 1. Three load-bearing assumptions that our own results contradict

**1a. Open-loop aimed programs will not make actions matter (EXAM §1, §6.2 check 3).**
- **The steering evidence is closed loop.** The "19 of 24" and "35 of 46" results came from a kick re-aimed every tick from the privileged state (`fresh/inputs/scripts/steer.py`). Only 12 targets carry the 46 runs. Clean runs turned toward the source 22 of 23 times (median 13.5°); runs with a fusion or mass change, 13 of 23, near chance.
- **The open-loop version has been measured and barely registers.** `body_x8same` (one body-aimed kick held 8 ticks) is EXAM's class (c). Its median mean shift is ≤ 0.09 of the *oracle* variance. Rescaled by V_oracle/V_best from the closure summary (order of magnitude), that is ≤ 0.7% of the level-1 predictive variance. The 32-cell push (`k32_x1`, nearest to class (d)) reaches ≤ 2.2%.
- **Consequence.** An ignore-actions predictor loses at most about 1–2% MSE, below the paired SE of 64 items. As specified, the exam tests passive prediction.
- **Fix, before any suite.** Measure effect per nat against V_best, not oracle variance. If no admissible open-loop program reaches about 0.1·V_best at h ≤ 8, raise the budgets, admit closed-loop items, or add response items (§5).

**1b. The ceiling is not a ceiling.**
- The checker caveat in the closure summary: ceilings are lower bounds with learning curves "still falling" (at 16 ticks one fit gives 0.24 against the headline 0.136). Predictor quality alone moves c(8) by 0.12 (0.371 to 0.495).
- EXAM §4.2's "closure gap that no level-k predictor can close" therefore includes designer modelling error; an agent can legitimately beat S_ceil. The reward map clip(OES/OES_ceil, 0, 1) would cap reward at the designer's fit. Report OES and OES_ceil side by side instead.
- DESIGN E1's threshold ("beat c(8) = 0.49 by more than 0.1") equals the predictor effect. Hold predictor class, data and epochs fixed across every Φ, and add q = 3 (Φ_coarse's width). E5's "beat c(4) = 0.63" lacks the matched-I₁ condition DESIGN §5 demands.

**1c. The wind channel is an untested actuator.**
- EXAM's nats accounting for the wind is right, but Flow-Lenia is translation-equivariant: a smooth 16-px wind mostly *translates* a 13-px body. Turning needs shear across it, which a block-resolution field barely provides. None of our steering evidence transfers.
- The background wind changes the world (at σ_w = 0.05, an independent random walk of 0.2 px per tick per block), so every certificate in `fresh/` must be recomputed: 47k member-ticks of closure and about 3 CPU-hours of input runs. EXAM should budget this.

## 2. Technical checks

- **KL derivation (EXAM §3.1–3.2): correct.** The chain rule, Girsanov, data processing and I(U;O) ≤ E KL(P_U‖P_0) check. The χ² identity checks: for open-loop shifts, E_0[LR²] = exp(Σ‖Bu_t‖²_{Σ⁻¹}) = e^{2C}. It extends to closed loop under a pathwise cap (exp(2M − 2⟨M⟩) is a supermartingale), which the card's "any admissible program" needs; §3.2 states only open loop. `kl_ring.json` reproduces the table. Caveats:
  1. Bu must lie in range(Σ). Under conservative noise (P0's Q = Lap, transport NCA), mass-changing inputs have infinite KL, so zero-sum is mandatory.
  2. The χ² card guarantee is vacuous at useful budgets: a 1-px block push costs 12.5 nats, allowing √(e^{25} − 1) ≈ 2.7·10⁵ SDs. Print the KL and the linear-Gaussian √(2C), and say the bound is informative only below about 2 nats.
  3. A nats cost is ½(push / natural push SD)², so "information-theoretic versus norm-based" is no dichotomy: the information view *selects* the norm (Σ_a⁻¹).
  4. The efficiency table marginalises the start state, understating efficiency for an agent holding a history.
- **Wind arithmetic: correct** (4f px, 12.5 and 1280 nats). The port's flow noise is std 0.5 per component, channel, cell and substep, before a 4.35-px displacement clip (`flowlenia_jax.py`).
- **Fair energy score: correct**, including v1's self-pair bias (`blobround6_eval._energy_score` includes i = j) and the 5% figure.
- **vw claims: correct.** Public-salt keys (`make_key`); multiplicative, support-only actuation noise; stride input at the first substep; 261 Flow-Lenia parameters.
- **P0: reproduced, but narrower than stated.** The PCA window is alternating (top-to-second eigenvalue ratio 1.054). This rests on conserved noise making the static spectrum rise from 2.5 to 4.2 with wavenumber: the lesson is "reconstruction is blind to dynamics", not "picks the worst feature". The transport-invariance argument needs continuous encoders for its width step.
- **Small fixes.** "19°, 35 of 46" mixes the flank median (19.9°) with the all-runs count (median 20.7°). Mass drift: DESIGN's 1.9e-14 is VW-0's; fresh is 1.84e-14 over 300 ticks; WORLDS' "≤ 1e-16" disagrees with both. Zhang & Liu is dated both 2022 and 2023.

## 3. Contradictions between the memos

1. **Permutations.** DESIGN §5 hides them; EXAM drops them. I side with EXAM, also because companion views with one world seed share the permutation (`fresh/media`).
2. **Certification law.** DESIGN certifies closure under `random_program`; the exam uses classes (a)–(d). Certify under the exam mix.
3. **Input gate.** DESIGN's gate ("blind inputs visible within 1–4 ticks", bits under the L1 `Admissible`) rejects gliders, EXAM's pilot. Restate it in nats, as information efficiency at level k against V_best.
4. **Circulation.** E4's "natural invariant (circulation)" is false: WORLDS measured mean ω drifting (`invariants.json`).
5. **Precision.** DESIGN *defines* GPU worlds in float32; EXAM grades float64 on CPU. Pick one, and use the platform null for law-level agreement.
6. **Actuation.** DESIGN's families declare no actuation channel (EXAM §3.3's rule) and omit particle life, which WORLDS ranks third for its exact Langevin budget.
7. **Citation tags.** EXAM marks as VERIFIED sources checked only in earlier reviews ([M13], [S14], [R24], Alchemy) or via citing papers ([GR07], [PT13]). Under the rules these are MEMORY.

## 4. Citation spot-check (WebSearch/WebFetch, this session)

- **VERIFIED as cited:** Lenggenhager et al., PRX 10:011037; Ferro, QJRMS 140:1917–1923; Yang et al., NSR nwae279; Ziel & Berk, arXiv:1910.07325 ("contradicts other studies" stands); Carnevale et al., PRL 66:2735; Cotton et al., PRL 129:158101.
- **Mislabelled: Chen et al., arXiv:2511.12842** ("Scalable learning of macroscopic stochastic dynamics"). It *identifies closure variables*, trains on small patches (a locality bias) and includes lattice spin systems. It is the closest precedent for the lead's brute-force route, not a reconstruction-led autoencoder, and it undercuts the "only non-CA" gap claim.

## 5. Missing options that matter

**Track 1.**
- **Computational mechanics** is absent from the Φ survey, though `lit2/emergence-closure.md` covers ε-machines. Local causal states (Rupe & Crutchfield 2018, Chaos, arXiv:1801.00515; VERIFIED) are a learned, *local*, closure-defined Φ on lattices: close to "preserve local function" made exact.
- **Stacked chains.** "None learns a stacked chain" ignores NeuralRG (Li & Wang 2018; MEMORY, verified in `lit2/ml-multilevel.md` [25]), which works on static fields. Qualify it to "none for dynamics".
- **Second reading of "preserve local function":** train the encoder jointly with a *local*, equivariant macro predictor (patchnet-style), making locality of the emergent law the bias. Ask the lead which he meant.
- **Crowding.** The transport NCA has no crowding term, so random draws will likely coarsen into point masses. Offer an analogue of Flow-Lenia's −α∇A_sum.

**Track 2.**
- **Response items:** score the predicted mean effect E[o^π] − E[o^0] given a history. It is kernel-level (Prop. 1); designer common random numbers only reduce its variance. It isolates input response from passive chaos.
- **Control items:** "choose an admissible program maximising level-1 statistic f at time q", scored by realised f.
- **Allocation.** With S_ceil ≫ S_oracle, between-item variance dominates: use R = 4, n = 256 for the cost of R = 16, n = 64, and 64-tick replicates only for level-2 cells.

## 6. Cheapest experiments that most reduce uncertainty

- **Track 2: actuation probe, about 20–30 CPU-minutes.** A wind wrapper Level outside `vw`, the 40 saved states (`fresh/inputs/results/states.npz`), twin runs. Compare wind and kick at 2, 12.5 and 50 nats, open-loop aimed and regional, h = 1–16; report effect / V_best per nat, plus one 300-tick background-wind viability run. This decides the actuator, σ_w, the budget scale and whether "actions matter" can pass. If nothing reaches about 0.1·V_best, switch to response or control items before building a suite.
- **Track 1: E1 on real nonlinear data, no new simulation, CPU-minutes.** `fresh/closure/results/sim_{A,B}.npz` hold 36 × 301 level-1 trajectories plus 5 branch replicates of 32 ticks from 144 states. Learn a 2 × 2-block Φ₂ on Φ_coarse's 8 × 8 × 3 field under reconstruction, closure and invariance objectives with a fixed predictor; certify its ceiling against the replicates, and Γ_Y(Z) (Prop. 6) from Y alone. This tests P0's claims and a learned *stacked* Φ at once. Next: an E2-lite screen of 200 transport-NCA draws, with and without crowding, which gives the random-family pass rate and supplies E1's level-0 worlds.
