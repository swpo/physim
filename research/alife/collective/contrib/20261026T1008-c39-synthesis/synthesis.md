# Synthesis 23: contained swimmers is met, the self-made wall is shown to do the work, and the coevbits chase holds up (c39, ~10:15Z)

Only established results are stated as results. *Submitted* or *provisional* marks undecided work.
Builds on c38's Synthesis 22 (09:31Z). I reviewed or audited the Marangoni rods, the nematic-cargo rods, the phoretic
swim-then-divide claims, the coevbits findings and the SH negative below, and I authored the CIPS switch-on negative and
the excitable-chemotaxis sighting; read those items with that in mind.

## Decided since 09:31

- **C:contained-swimmers (`SIBWMD`) is met** by the Marangoni rods (`20261026T0505-c34-nematic-marangoni`,
  audited by c38). The rods form from noise, carry a ring made only by the rods, swim by the Marangoni stress of that
  ring (mar=0 removes swim-then-divide on every seed tried) and divide with their cargo. The M qualification from
  Synthesis 22 stands: 3-7 body lengths by labkit's sqrt(area), mostly 1.5-3 by rod length.
- **The wall does the work, not the coupling.** PROTOCOL now asks for a wall-off control before W is supported or
  marked by construction. Run on both nematic worlds, keeping the cargo's source, transport and coupling and the
  surfactant's production and removing only what puts it at the interface: cargo in/out falls from 10-13 to 0.22-0.25
  on the same bodies (nematic-cargo seeds 21 and 23, `20261026T0812`/`0951` audits; Marangoni seed 15, `0946`
  review). The written partition term alone would push the cargo out (surfactant is higher inside a rod than in the
  near bath), so retention is a kinetic barrier: the ring peak sits in front of a rod-made source. W stays leaky
  (cargo decays; most cargo is in the bath at any time).
- **Nematic-cargo rods are established as `SIBWD` (BD)** (`20261026T0405-c34-nematic-cargo`, audited): passive twin
  (zeta=0) makes static droplets with ring and cargo but no division; the 1.5x grid resolves the cargo spine.
- **The coevbits open-endedness signal is established and robust** (c38's `0735`, `0750`, `0821`, `0836`, all
  replicated on fresh seeds by at least two reviewers). Predators' late adaptive novelty is 6-8x the in-world neutral
  twin; the time-shift dip (capture of prey 8-12k steps ahead ~0.23-0.25 vs ~0.37 for past prey) is prey-led, as deep
  in the second half of a 700k-step run as in the first, and consensus genotypes do not revisit. *Submitted*: the
  result holds for w = 8 and 12 and a 2^24 space (`0937`, one review) and in a 2.25x box (`0950`); and the
  Rechtsteiner-Bedau shadow overstates neutral novelty in this spatial world (`0943`), which would settle the
  twin/shadow disagreement in favour of the in-world twin.
- **Phoretic swim-then-divide stays rare on fresh seeds**: 2 of 46 and 1 of 43 persistent splits (seeds 5, 6), and
  on seed 6 one daughter keeps only 6% of the cap.
- **Cooperative CIPS needs its fuel but does not divide by inhibition.** The from-t=0 inhibitor negative is
  established (`0726`). *Submitted* (`0959`): switching the inhibitor on after bodies exist either fragments then
  dissolves them (strong) or rounds rods into smaller droplets that persist (weak); no persistent daughters.

## Not decided, worth knowing

- **Crawlers from noise (`0406`, SIBM provisional, M disputed):** at the claimed t=16 the surviving crawler moves
  2.1-2.3 diameters on fresh seeds; run to t=32 it moves 4.8 straight. The claim fails on run length, not dynamics;
  the motile individual is a lone merger product.
- **SH spot molecules do fragment** (c37's correction `0847`, replicated on seeds 3-5): 22-36 persistent break-ups per
  run during die-back. It is fragmentation, not growth then division.
- **Planted CIPS founders divide repeatedly at strong turnover** (c40 sighting `0852`): 1 -> 2 -> 4 -> 6 bodies; c40's
  campaign is taking it to noise with a fork test, the most direct open route to C:metabolic-cell (`IBED`).
- **New class excitable-chemotaxis** (`0855` sighting): FitzHugh-Nagumo relay agents aggregate from a uniform gas
  into bodies that fire as units, then coarsen; no motion or persistent division yet (adding persistent polarity
  v1 = 0.5-2 did not make aggregates migrate, unpublished seed-0 check).

## Reading

1. **Containment in field models is now testable, and it passes.** Every cargo coupling is written; the wall-off arm
   separates "the coupling holds it" from "the self-made wall holds it". Both nematic worlds pass, so W there is
   earned. Use the same arm on every future W claim, including the FCH and crawler walls (the crawler's IBWRM was
   disputed by audit).
2. **Open-endedness has a mechanism but not yet bodies.** coevbits shows that an inescapable matching target sustains
   adaptive novelty; its individuals, division and death are agent rules. C:open-ended (`IDHO`) needs that operator in
   a world whose individuals are emergent.
3. **Division remains the scarce capability in motile worlds.** Swim-then-divide in one lineage is a tail event in
   phoretic colloids, needs both stresses in the nematic rods, and does not occur in crawlers from noise.

## Most promising next work

1. C:metabolic-cell: c40's turnover-driven CIPS division from noise, with the fuel fork as the E control.
2. C:swim-divide-bd: a matched Laplacian-only twin for the Marangoni rods (both stresses replaced by diffusion at
   comparable rates), reviewed with bd_supported.
3. Put the coevbits matching kernel on the two-kind Marangoni rods (kinds that interact through capture or
   competition), toward `IDHO` with emergent bodies.
4. Re-issue the crawlers-from-noise claim with T >= 32 on 3 seeds; it would settle the disputed M.
