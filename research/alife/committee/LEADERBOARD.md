# Leaderboard

Updated 2026-10-24 16:54 UTC. Rungs are committee consensus under [RUBRIC.md](../RUBRIC.md); `L6[L2]` = reproduction of unstructured individuals. Paths are relative to `research/alife/`.

| Rung | Confidence | World | Thread (sprint) | Note | Pack |
|---|---|---|---|---|---|
| L5[L2] | low | ecology | chemotaxis-motility (r1) | Prey-predator pairs, contact 0.93-0.96 vs null ~0.33 (4 seeds). Predators fall 93-95% at k=0 (2 seeds). In matched reruns prey do better WITH predators: an obligate escort or parasite, not demonstrated predation. No cycles. Provisional pending the matched decomposition. | `threads/chemotaxis-motility/packs/ecology` |
| L4b[L2] | high | kstrail | chemotaxis-motility (r1) | Crescent swimmers form spontaneously from noise (spot -> ring -> rupture -> crescent). The chi_h=0 ablation gives static spots. Passes dt/2 and 2x resolution with no heading lock. The swimmer phase coarsens to immotile aggregates by t=1800. L3 Weak (wake, not membrane). Known drift-bifurcation physics. | `threads/chemotaxis-motility/packs/kstrail` |
| L4b[L2] | high | pursuit | chemotaxis-motility (r1) | Non-reciprocal cross-taxis binds chaser-fleer composites (contact 0.76-0.91 vs null 0.27-0.31). A clean 2x2 ablation shows pursuit binds and evasion shapes the bond. L5 Weak: conserved species, so no population dynamics. | `threads/chemotaxis-motility/packs/pursuit` |
| L4b[L2] | medium | toxforage | chemotaxis-motility (r1) | Toxic self-waste acts as size control and keeps 9-14 swimmers with turnover to t=1500. L4c Weak (near-Supported): the judge's n=0 fork kills every body within 200 t and kd=0 gives a sea, but on one seed only. L4a Weak. | `threads/chemotaxis-motility/packs/toxforage` |

Calibration controls: Orbium ~ L4b[L2]; Gray-Scott mitosis ~ L6[L2]; Particle Lenia ring ~ L3 (one static cell); noise ~ L0/L1.
