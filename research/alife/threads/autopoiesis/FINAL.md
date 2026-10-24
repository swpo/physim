# Autopoiesis thread: final summary (3 sprints)

## Best worlds (committee consensus rungs; sprint-3 claims marked as mine)

| world | rung | what it is |
|---|---|---|
| `phase_membrane` | **L6[L3] + L4a** (medium, r2) | Phase protocells form from noise. The membrane is an Allen-Cahn wall whose inside phase is held up by links the cell's own catalyst makes. Links adsorb to the wall (a ring 2.1-2.5x the core), and both daughters inherit the ring (gen 3). 35-41% cuts re-ring. Sprint 3, labkit v0.2 rim cuts on mature cells: a 41% loss recovers to 0.94x and divides, a 21% loss recovers, and 1/3 of targets is lost (`packs/phase_membrane_damage_mature`). The χ=0 control forms and divides just as well, so the ring is a self-made layer but not load-bearing. |
| `phase_protocell_noise` | **L6[L2]** (high) | The same loop without adsorption: 42-46 cells, gen 3-4, dt/2 and 2x resolution converged. |
| `phase_swimdiv` | **L6[L2] + L4b** (medium) | The lab's first dividing swimmers. Per-cell phoresis up the substrate gradient gives crescents with depletion wakes that divide repeatedly. |
| `motile_trait(_tox)` | L6[L2]; L4b[L2] (medium) | Heritable phoretic mobility with a co-mutated neutral tag. Mobility is selected up under self-made toxic waste and down in dense populations, with a tipping point at kd 0.018-0.02. L7 Weak. |
| `membrane_evo` (+`_up`, `_down`) | **L7[L3], my claim (sprint 3, unreviewed)** | Kinds differ only in link yield, the channel is sealed, mutations are whole-cell flips, and identical-event twins share flips and deaths. Over 10 seeds per arm (about 2.5-4 generations), K2 biomass share departs from the twin in 9/10 for both 0.7b (purged through deaths) and 1.3b (sweeps to 85-97% in 8/10 through births). First acquisitions are 1 in 30 runs and conversions ≤ flips in 30/30. A co-mutated neutral tag shows no arm effect. |
| `membrane_kinds` | L7 Contradicted; L5[L3] Weak | The infection law (below). |

## Mechanisms that worked (with ablations)
1. **Membrane = a phase wall tilted by the cell's own product.**
   `dφ = Dp∇²φ + rφ(1−φ)(φ−½+a(L−θ))`. Closure is topological, so the wall cannot have a hole,
   and repair is automatic. Ablation a=0: all domains shrink and die by t≈350.
2. **Gated mobility φ² keeps products in.** gate=0, or K ungated: everything dies; φ≡1: a sea.
   This is the lab's convergent "beyond-Laplacian" operator (also found by fisim and
   active-droplets).
3. **Division by central starvation.** Large cells deplete substrate centrally, L falls below θ,
   and the wall pinches. Cell size rises with feed. Gray-Scott/Zwicker class.
4. **Interface adsorption of the product** (drift χ up ∇[4φ(1−φ)]) makes a material ring. It is
   not needed for life (χ=0 control).
5. **Per-body phoresis gives swimming above a threshold** (1 < μ < 3), and swimming suppresses
   division (a swimmer never starves). Near threshold, swimmers swim and divide.
6. **Sealing horizontal transfer needs both a min face mean for binary gates and fast decay of
   stranded catalyst.** With it (and c2 = c1), conversions drop from 8-26 per run to ≤ flips, and
   selection on a membrane trait shows up through births and deaths (membrane_evo).

## What failed (and why)
- Lattice SCL (numba, McMullin rules + splice): leaky membranes (closure 0.2-0.8), and 30%
  wounds never close. Flexible lattice membranes (bond fluctuation, insertion, reconnection
  fission) shrink inward or shatter.
- A polymer field placed at |∇L|, and Gray-Scott kinetics inside any barrier: freeze or die.
- Local self-repellent propulsion of a phase cell: a divergent local flow tears the wall. Phase
  cells need a rigid-body drive.
- Chemotactic predators that eat substrate starve in the prey's depletion halo.
- Leaky two-kind cells (`phase_kinds`, `membrane_kinds` A/B/B′): the faster kind spreads by
  infection (4-17 conversions per mutation) and can crash the population. **Infection law:**
  with any catalyst leak and c2 > c1, a trace becomes a takeover. Conversions per mutation fall
  with gating (A > B > B′) but reach ~0 only with the sealed channel and c2 = c1.

## What transfers to PhySim worlds
- The **tilted-wall container** (φ with a tilt by any internal product, plus φ²-gated mobility)
  can wrap any reaction-diffusion or Lenia chemistry in a self-maintained, self-repairing,
  dividing compartment. It needs only lap(), a cubic and a mobility-weighted divergence.
- **Gate binary masks with min (or harmonic) face means.** Arithmetic means leak.
- Hidden laws an agent could discover: cell size vs feed; the wall-tilt threshold; the infection
  law (conversion rate vs gate exponent); the sign of selection on link yield vs turnover.

## What a next lab should try
- Map selection on link yield against turnover (about 1 generation does not resolve it; 2.5-4
  does). Add a second heritable axis (growth rate vs link yield) to look for coexistence and
  trade-off-driven diversification (an L8 probe). Replace whole-cell flips by copying errors at
  division.
- Local phoresis (wall slip plus incompressible interior flow) to replace the per-body label.
- Make wall tension depend on the adsorbed ring (budding or pearling division).
- Start from noise with heredity on: let catalyst kinds arise by flip in established cells only.

## Showcase movie
`movies/showcase.mp4` (2.0 MB, 20 s, 128² shown at 512², fixed colour scales over the whole
run): **membrane_evo_up, seed 4, t = 0-40000.** Smoothed noise condenses into a few walled
protocells (the green wall rim is where links accumulate). They grow and divide by central
starvation into a population of blue K1 cells. From t=8000, random whole-cell flips (the same
event stream as the twin run) turn single cells orange (K2, 1.3x link yield, same growth rate).
Orange cells are larger, survive random disk deaths (black holes that appear and refill) and
divide into orange daughters, and by t≈30000 the high-yield lineage holds most of the
biomass, while small blue cells persist between them. Every event is a birth, death, flip or
disk death. Catalyst essentially does not cross between cells (1 conversion against 8 flips in this run's ledger, `runs/evo_hi/up_s4.json`).

## Committee final review (added after the program ended)
Final rungs: membrane_evo L7[L3] (low confidence, disturbance-mediated; the skeptic dissents:
Weak); phase_membrane L6[L3] (medium; the χ=0 ablation backs the ring); mature damage L4a[L3]
(low); phase_membrane_chi0 L6[L2]. Correction to my mechanism: most K2 births coincide with a
disk hit on the parent (30/38 on s4, 43/43 on the skeptic's s11). The r=14 disk is 2.4x a
median K1 cell. High link yield wins because big bodies are cut rather than erased, and their
fragments reseal and regrow. That is real selection, but its sign depends on the disturbance
kernel (consistent with the batch-1 reversal), and the sweep goes through births in 8/10 seeds,
not 9/10. For a future lab: whole-body deaths, a birth-cause ledger, and χ as the heritable trait.
