# Autopoiesis, sprint 2 report

The committee's r1 review (queued 17:02) reached this session only at 18:11, after I had run
sprint 2 on my own plan. I then ran the review's main experiment in the remaining time.
Section A is that experiment. Section B is the pre-review work (motility evolution). Not done
from the review: damage of mature cells, a χ=0 ring control, division-axis histograms,
kind-coloured sheets and packs for membrane_kinds, and local phoresis.

## 1. Headline

**Closing the horizontal channel is graded, and it decides the population's fate.** Port: K1/K2
catalyst kinds (c2 = 0.3 vs 0.2) into phase_membrane (χ=2, noise start), as
`worlds/membrane_kinds`. A labkit-independent overlap tracker (`kindtrack.py`) counts
conversions of intact cells, births and deaths per kind. Over 3 seeds × 32k t per arm:

| arm | catalyst mobility / growth | conversions (K1→K2) vs mutations | K2 births | outcome at 32k (K1 / K2 cells) |
|---|---|---|---|---|
| A leaky | D φ², growth ∝ φ | 22/17/20 vs 3/1/5 | 74-102 | K1 extinct, 7-8 K2 cells (100+ K2 deaths: crash) |
| B confined | D φ⁴, growth masked φ<½ | 23/26/25 vs 8/5/10 | 4-8 | 7-12 / 25-33 |
| B′ hard gate | D·[φ>½], growth masked | 13/8/16 vs 8/5/10 | 3-5 | 21-26 / 8-15, no crash |
| C neutral (c2=c1, B) | | 0/0/0 vs 8/5/10 | 0 | 33-34 / 0 (also 0 under B′) |
| D parasite (b2=0, B) | | 10/4/8 vs 8/5/10 | 0 | 1 / 13 / 0 total cells: collapse in 2/3 |

The committee's diagnosis holds: in the leaky world the advantaged kind spreads as an infection
(4-17 conversions per mutation), then crashes the population. Confinement lowers that ratio
(about 3 under B, about 1.6 under the hard gate) and lets the population persist. Even under the
hard gate K2 rises mainly by conversion, not division (3-5 K2 births per seed). So
**L7[L3] is not Supported. It stays Weak**, now with the mechanism identified: catalyst still
crosses between neighbouring cells, which never fuse (merges 0-1), through their φ tails.

## 2. Claims

| world | claimed | strongest evidence | known weaknesses |
|---|---|---|---|
| `membrane_kinds` (arms A/B/B′/C/D) | L7[L3] **Weak**; L5 (infection between cells changes population fate) | `runs/mk/*.json` (13 runs, per-seed event counts and kind series), table above | No packs or colour-by-kind sheets yet, only tracker counts. A conversion counts any 1:1 kind flip, including a cell taken over after its own mutation, so the horizontal share is conversions minus mutations at least. |
| `motile_trait_tox` / `motile_trait` | L7[L3] Weak + L4b (heritable motility vs neutral tag) | section B, `screens/motility_evolution.png`, `screens/motility_regime_shift.png` | Rigid per-cell phoresis. Small populations under toxin. A tipping point at kd 0.018-0.02. Not checked for contagion (same φ² leak as arm A). |

## 3. Mechanisms learned

1. **Horizontal transmission through the φ tail.** With D φ² the catalyst seeps between touching
   cells, and a faster kind wins by infection: in arm A, K1 cells convert 17-22 times while
   K2 cells die 104-133 times. The ratio falls under φ⁴ and the hard gate but does not vanish,
   because a cell's wall region is still φ>½ where it touches a neighbour.
2. **Stochastic-corrector-like protection in the parasite arm.** A link-less K2 kills the cells it
   infects (K2 deaths equal conversions), so K2 never builds a lineage. But conversions still
   reach the population, and it collapses in 2/3 seeds under B. Selection between cells purges
   the parasite only when transmission is vertical (cf. Szathmáry & Demeter 1987; droplet
   division as in Zwicker et al. 2017).
3. **Neutral mutants do not establish** (arm C: 0 K2 cells from 23 mutations under B, 8 under
   B′). Every K2 rise above needs the growth advantage.

## 4. Section B: before the review (motility evolution)

Phoretic mobility μ as a heritable catalyst trait, with a neutral tag at the same mutation rate,
under toxic waste (forked from chemotaxis-motility toxforage). At kd=0.02, μ rises in 5/5
surviving seeds (μ − tag +0.08 to +1.33). At kd=0, μ falls to 1.01-1.22 in 5/5 large
populations. At kd=0.018, 3/3 seeds shift to a dense sessile regime, a tipping point in which
density sets the direction of selection. dt/2 and kd=0.022 agree. Movie:
`packs/motile_trait_tox/movie.mp4`. Negative forks: local trail propulsion (`phase_trail`),
evolutionary rescue (`motile_kinds`), chemotactic predators (`hunters`: they starve in the prey's
halo). Details in NOTEBOOK §11-15.

## 5. Negative results

- Arms B and B′ do not close horizontal transfer: conversions exceed mutations in 6/6 seeds.
- See section B for this sprint's earlier negatives.

## 6. Next sprint

1. Close the channel fully: cross-inhibition between kinds (active-droplets mechanism 4), or
   catalyst bound to links (immobile once inside), then rerun A-D with packs, colour-by-kind
   sheets and kinds.json-style switch counts.
2. Review secondaries for phase_membrane: damage of mature cells on 3 seeds with the hook's
   fraction; a χ=0 control to test whether the ring is load-bearing; division-axis histograms.
3. Re-test the motility trait for contagion with the hard gate.
