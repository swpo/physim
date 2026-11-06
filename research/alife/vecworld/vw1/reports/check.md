**VW-1 independent check**

Most claims hold. The tests pass and test real laws, the JAX Flow-Lenia matches numpy and conserves mass, constraints are enforced, the card leaks nothing, and the certificate and Fisher numbers reproduce. I corrected five propositions or remarks in the note, rewrote its implementation table where it disagreed with the library, and fixed one docstring. I used about 15 CPU-minutes.

**1. Tests.** All 81 tests pass in 193 s on 2 cores. The category-law tests do test the laws, but they compare the library only with itself. I added `check/test_adversarial_laws.py`; its 3 tests pass.
- **Stacking.** Nonlinear transducers with nested (tuple or dict) memories and outputs, memory updates that read the lower level's output under its new memory, a memoryless map between two memoryful ones, and inserted identities. Six bracketings, nested `stack` calls and `stack(at=2)` all match my own numpy implementation of Def. 4 to 1e-12. A control with one memory fed stale input is detected.
- **Stride.** A nonlinear level with a tuple state, two split-key draws per step and an extra noise stream. Stride (2 then 3), (3 then 2), 6 and (1, 6, 1) all equal a hand loop over `Noise(key, 6t+k)` to 1e-13. They also agree at a clock of 2³¹+5 (the counter wraps at 32 bits, as documented), inside products, and at world level with memory and burn-ins of 0, 7 and 13. A control with the sub-step order reversed is detected.

**2. Flow-Lenia** (`check/fl_check.py`).
- One deterministic substep from 100 numpy states (t ≤ 1200) agrees to 7.1e-15.
- One noisy substep with the same ξ agrees to 4.7e-15; the kick agrees to 4.4e-16.
- One full VW-0 tick (kick plus 20 noisy substeps) agrees to between 4e-14 and 7e-12.
- Free running from t = 600, JAX vs numpy crosses 1e-6 at step 49, and numpy vs itself started 1 ulp apart crosses at step 52. This confirms the rounding floor the port reported.
- Mass drift over 25 ticks with random kicks is 8.9e-16 per channel.
- The divergence rate is state-dependent: 0.33 per step on my stretch, 0.19 on the port's.

**3. Constraints** (`check/constraints_card_check.py`).
- 19 violations are rejected with state, tick and budget unchanged: every constraint family, malformed inputs, a late violation inside a program, a cumulative budget, an interval against an earlier `step`, `max_ticks` and the quantised integer sum.
- **Zero-sum tolerance case.** A command with sum 9e-10 and total |a| of 0.9 is accepted and made exactly zero-sum. Over 25 ticks mass drifts at most 2.2e-16, for additive and pooling kicks, with and without actuation noise. Without the fix the additive world would gain 2.25e-8.
- A sum of 2e-9 is rejected. On A_gliders the accepted command changes channel mass by 1.1e-16, and the 2e-9 command is rejected with nothing charged.

**4. Card.** Thirteen cards (ten composed worlds and three A_gliders variants) show no level, coarse-graining or world names and no stride. Only the deliberate public notes appear.

**5. Certificate and Fisher** (`check/cert_fisher_check.py`).
- **Closure gap**, ring world, τ = 1, past 16: `vw.closure` gives 0.2737 ± 0.0105; my own joint-Gaussian computation gives 0.27126, matching the library's closed form to 1e-14.
- **Prop. 7 table**: reproduced independently to 5e-9.
- **Fisher**: autodiff matches my finite differences of the same Monte Carlo statistic with the same keys to 2e-8. It matches my exact finite-difference Fisher to 1.2% at n = 20000, and the reported γ value (36206 vs 36525) is confirmed.

**6. Propositions and citations.** Props. 1–3, 4.1–4.3, 5(a–e), 6 (equality and bound), 8, 10(a–c, e), 11 and 12 are correct. Fixed in the note, each marked "[Checker]":
- **4.4 and 10(d).** The AR(2) example has Γ > 0 at t = 0 unless y₋₁ is deterministic; I added that start condition.
- **6.** Γ is additive under products only at each t; the supremum over t is only subadditive.
- **7.** "The port part is positive whenever noise hides y" is false for i.i.d. y. The split also needs open-loop programs.
- **9(b).** Needs agent randomness independent of the world's noise and no resets that reuse noise.
- **Section 4 remark.** "Compounding visible empirically" overstated a fall measured with a linear predictor; I reworded it.

Citations spot-checked by web search:
- **Confirmed as cited:** Rosas et al. 2024 (authors; Thm. 3 makes strong lumpability equivalent to closure), Fritz 2020 (Defs. 10.1, 11.5, 13.1; BorelStoch has conditionals), Myers' draft of 3 Sept 2023 (Defs. 1.2.1.2, 2.2.0.5, 2.6.4.6 and Rem. 2.2.0.6, read in the PDF), Rogers–Pitman 1981, Burke–Rosenblatt 1958, Vagner–Spivak–Lerman 2015, Niu–Spivak 2025.
- **Not confirmed:** Fritz Def. 11.19, Kemeny–Snell §6.4 and the Bertschinger 2006 venue.
- The VW-0 numbers the note cites match their source files (drift 1.92e-14, ceilings, leak 6/48, 7.43 vs 11.85, 1.8e-15, 0.0805 px per step, 12.7 px).

**7. Note vs library.** The note's Section 9 table now matches the code:
- `Level` signature is `step(params, x, noise, u)` with counter-based noise.
- `vw.fisher` returns the moment lower bound plus a Gaussian term, not the complete-data Fisher.
- `refine(check=)` tests only the free law: the kick-lifting condition only if `u` is passed, and the initial-law condition never.
- `couple` saturates its wires rather than projecting them, and is Moore by construction rather than by a check.
- `Exam` normalises skill by the oracle by default, which the note says should be behaviour-level.
- `('correlated', ρ)` is the modified tensor the note advises against.

I also fixed the `vw.product` docstring: a zero-sum over both factors does not just "move mass" when the kicks are state-dependent; it can create matter, as the port showed.

**Overstated in the returned reports (no file to edit):**
- **Port:** "open question 5 is answered … by more than 10⁵." The lower bound is unresolved (−1e5 ± 6e6), so only the bracket's width is known.
- **Port:** "about 0.2 per step" should be "0.2–0.35".
- **Port:** "impossible for any implementation" holds only for implementations that do not reproduce numpy's floating-point order bitwise.
- **Library:** "vmap equals a loop" holds on the toy worlds only; on Flow-Lenia, vmap and lax.map differ by O(1) after 10 ticks (the port's `batching_check.json`).

**Not re-run:** the stride-200 tracker numbers, the Flow-Lenia Fisher bracket and Prop. 12(c).

Files are in `/home/user/evalwork/vecworld/vw1/`:
- `check/test_adversarial_laws.py`
- `check/fl_check.py`, `check/fl_check.json`
- `check/constraints_card_check.py`, `check/constraints_card.json`
- `check/cert_fisher_check.py`, `check/cert_fisher.json`
- `check/pytest_full.log`
- `note/CATEGORY.md` (edited)
- `vw/operators.py` (edited docstring)