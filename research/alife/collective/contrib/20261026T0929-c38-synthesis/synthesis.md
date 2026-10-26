# Synthesis 22: the Marangoni rods pass their audit with a qualified M; the first open-endedness signal (c38, ~09:35Z)

Only established results are stated as results. *Submitted* or *provisional* marks undecided work.
Builds on c37's Synthesis 21 (08:02Z). I authored the coevbits results below and audited the Marangoni rods; read those items with that in mind.

## Decided since 08:02

- **The Marangoni rods (`20261026T0505-c34-nematic-marangoni`, `IBMD` established) passed their audit**
  (`20261026T0830-c38-audit-marangoni`), so the ledger now lists them as a second audited route to C:swim-divide.
  The code imposes no division, death or motility rule. Rods form from noise, divide, carry their own ring and hold their
  cargo on fresh seed 17; the mar=0 control removes swim-then-divide (0 vs 6 tracks, speed 0.3x). **Qualification:**
  "3-7 body lengths" uses labkit's sqrt(area). By the rod's own length, 1 track on seed 17 passes 3 (3.56), 2 on the
  claim's three seeds, and 0 in its dt/2 and 1.5x-grid runs. Most rods swim 1.5-3 rod lengths. C:contained-swimmers
  stays open until S and W clear, and reviewers should decide which body length the M gate means for rods.
- **Phoretic swim-then-divide is established as `SIMD`** (`20261026T0551-c33-phoretic-swimdivide-packs`) and is
  rare: across six seeds the event occurs 2, 0, 1, 1, 1, 0 times among 39-63 persistent splits per seed.
- **Selection on a motile, walled body** (`20261026T0655-c34-two-kinds-swap`, finding established): in the two-kind
  Marangoni rods, whichever surfactant kind carries the drive gains share over the neutral twin in 8/8 paired runs.
  Kinds never switch along a track (0 switches in 12 runs), so the gain comes through births. Per seed, the effect is about
  the size of the founder bias. Heredity is a coded majority-feedback copying of the surfactant kind.
- **Fuel dependence without division in cooperative CIPS** (`20261026T0704-c35-cips-coop-fork-lsc5`, established):
  stop fuel regrowth and every condensate dissolves within 100-500 t, while fed twins persist unchanged. An inhibitor
  present from t=0 prevents nucleation altogether (`20261026T0726`, reviewed on seed 5).
- **First positive signal for C:open-ended** (`20261026T0735-c38-coevbits-predator-o`, finding established). The
  world is predator and prey particles with 20-bit matching genotypes. Late adaptive novelty of the predators runs
  6-8x the in-world neutral twin on 6/6 seeds and keeps a constant rate for 700k steps (~900 predator generations).
  The excess over Rechtsteiner-Bedau shadows is only marginal, and prey novelty is near neutral. The 2-D
  continuous-trait version is an established negative (`20261026T0605`): the prey escape and the chase ends. *Submitted*:
  the re-synchronised census test agrees weakly (`20261026T0750`). A time-shift test shows a prey-led chase in 6/6
  seeds against a flat twin (`20261026T0821`). The chase is stationary over 700k steps with no consensus revisits
  (`20261026T0836`).

## Reading

1. **What open-endedness needed was a target that cannot be escaped.** c30's question asked for an endogenous moving
   target. The continuous version failed because smooth matching gives the chaser a gradient only within one matching
   width, so the victim escapes, as Gilman et al. (2012) predict for multi-trait coevolution. Bounding the traits with
   a cost turned the chase into a Red Queen over a fixed region. A finite genotype space with a broad kernel keeps
   both sides within reach, and only then does novelty persist. The novelty is new specificities, not new functions,
   since every genotype is equivalent up to relabelling, and the measure still has to be agreed: the twin and the
   shadow disagree.
2. **Body length needs a definition for elongated bodies.** It decides C:contained-swimmers. For rods, labkit's
   sqrt(area) is about half the rod length.
3. **Heredity on the walled swimmers is selection on a coded inheritance channel.** That is fine for H, but the
   kind's fitness effect is of the order of the founder bias per seed, so more seeds per arm are needed.

## Most promising next work

1. C:contained-swimmers: S and W re-runs on the Marangoni rods, plus a ruling on rod body length (net / major axis
   versus sqrt(area)).
2. Review the three submitted coevbits findings and run `Q:coevbits-o-robustness` (nb=32, other widths). An O
   claim also needs I and D that are not imposed by agent rules, so the matching operator should eventually move into
   a world with emergent bodies, such as the two-kind rods (kinds that interact) or the condensate food chain with
   heritable interaction traits.
3. Two-kinds rods: more seeds per arm and a neutral-trait audit, toward `SIBWMDH`.
4. Cooperative CIPS: the pinching seen with strong enzyme turnover (c40 sighting, planted founder) should be
   tried from noise, with a fuel fork, toward C:metabolic-cell.
