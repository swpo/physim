# Rubric changes

Each revision names the concrete counterexample that prompted it. Earlier verdicts
stand under the version they used. Sprint 1 reviews used v1. Sprint 2 reviews onward use v2.

## v1 to v2 (24 October 2026, after the sprint 1 reviews)

All seven sprint 1 directors raised rubric issues. The changes below adopt the ones raised
with a concrete example, usually by more than one director.

| Rule | Change | Counterexample that prompted it |
|---|---|---|
| L3: material channel | A boundary computed as an algebraic function of the order parameter or body field is capped at Weak unless an ablation shows it does work. | autopoiesis `phase_protocell`: its "wall" channel is 4phi(1-phi), a contour of phi by construction. fisim `xcell-a`: membrane m = 4s(1-s) of the body passes only because its gate ablation shows containment. |
| L3: self-made interface layers | A quasi-equilibrium layer of an independently produced and transported species counts for the rung; whether it does work is scored under the modifiers. | active-droplets `ad3-membrane`: the psi shell is 98% explained by \|grad phi\|^2 + c, yet it is self-made, removed at chi=0, and wraps every daughter. |
| L3: conditional layers | A layer set by a local environment rule and lost population-wide is Weak. | particle-life `sporecell`: the M ring is a food-contact label that every cell loses at depletion while the cells live on. |
| L3: sub-kernel features | 1-2 px boundary features in kernel worlds must survive a >= 1.5x resolution continuation. | lenia-multichannel MIRd+: the "halo" is isolated 1-2 px dots at kernel radius 15. |
| L4a: target and twin | Damage a mature, non-dividing individual with an undamaged twin on >= 2 seeds, and report the actual erased fraction. | `--damage` hit the largest component, which in dividing worlds is usually mid-division (autopoiesis, active-droplets, chemotaxis). FACTS reported 49/475 px when the world hook erased ~36% (autopoiesis). |
| L4a: debris | Erased matter must leave the individual's reach. | particle-life `sporecell`: the cut turned debris into food at the wound, so regrowth was confounded. |
| L4c: ablation type | A global feed cut is not sufficient. Require an abrupt fork with individuals dying, a local supply cut, or a per-individual flux budget, run on the claimed world. | active-droplets `ad1-fuel` (F=0 would kill any RD spot). lenia `mcfd-MIRd` (the ablation was run on the parent world). chemotaxis `toxforage` (gradual r=0 left survivors living on leftover food). |
| L5: matched controls | The ablation must be matched (grid, duration, seeds), and the sign of the effect on each partner reported. | chemotaxis `ecology`: the prey effect reversed sign when two judges ran a matched control (-7% with predators vs -35% without, against the researcher's unmatched -24%). |
| L5: cycles | Peak spacing across >= 3 seeds plus a grid-size check before calling it a cycle. | lenia `mcfd-MIRd`: peak spacing 530/290/260, a ~650 t static plateau on seed 11, damping at 192². |
| L6: founder generations | From planted founders, Supported needs max_generation >= 3; from noise-formed founders, >= 2. | fisim `xcell-div`/`xcell-her`: max gen 2 from planted founders is one counted generation; two of three judges had accepted it. |
| L6: reticulate genealogy | Report merge/split ratio; above 50% caps confidence at medium. Lineage must be merge-aware. | flow-lenia `fl_forager` (merges about 80% of splits). particle-life `sporecell-gene` "gen 9" was a split/re-merge ratchet. |
| L7: contagion | Kinds may change only at mutation or birth. Report conversions of intact individuals per mutation; horizontal sweeps are L5 (infection). | autopoiesis `phase_kinds`: 45 intact K1 cells converted without division against 8 mutations, and K2 still swept with mutation off. |
| L7: neutral arm | The neutral arm must match the ancestor's baseline fitness (ideally an identical-event twin). Report per-kind births, deaths, flips and off-kind daughters. Colonization-only selection with 0 deaths caps confidence at low. | active-droplets `ad5-evolve`: neutral at k=0.13 against an ancestor at 0.10, and a matched neutral showed the ancestor is sterile. |
| Numerics (Flow-Lenia) | dt/2 at fixed reintegration spread is not a convergence test; use a resolution change with kernels and flow scaled. | flow-lenia: halving dt doubles numerical diffusion in reintegration tracking. |
| Beyond-diffusion modifier | Scoring >= 2 needs a matched Laplacian-only control that fails. | active-droplets `ad1-fuel`: two judges replaced Cahn-Hilliard with linear diffusion, and the droplets still hollowed and divided (Gray-Scott mitosis in a CH body). |
| L2: churn populations | When tracked identities churn through collisions, L2 can rest on body lifetime between collisions, judged from images. | chemotaxis `toxforage`/`ecology`: plainly discrete swimmers with 0 persistent tracks. |

labkit v0.2 adds the measurements these rules rely on: per-channel radial boundary
profiles, an absolute lineage window with a sibling re-merge filter and merge/split
ratio, damage aimed at mature compact individuals with a measured erased fraction, and
per-species tracking.
