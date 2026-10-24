# FINAL: fisim-beyond-laplacian (sprints 1-3)

**Question.** The PhySim/blobkit genome uses cubic activators and linear channels, each with a
Laplacian and only local couplings. Which *minimal* non-Laplacian additions give its blobs sharp,
containing boundaries and life-like organization, while keeping the exact designated vacuum,
IMEX-FFT numerics and interpretable parameters?

## Best worlds (committee consensus rungs)

| world | rung (committee) | what it is |
|---|---|---|
| `xcell-a` | **L4b[L3]**, medium; L4a Weak | An m4 glider carrying a membrane ring and a contained, fast-diffusing cargo. 30% damage heals in ~10 t. |
| `xcell-her` | **L3**, high; heredity of planted kinds Supported; L6 Weak | Membrane cells divide. A bistable marker held by the membrane gate breeds true: 46 divisions, 0 mixed, 0 switches, 3 seeds. |
| `xcell-evo2-S/N` | **L6[L3]**, low | Membrane cells divide through ≥3 generations under imposed dilution (S0 gen 6). Ringed fissions verified by a judge. |
| `xcell-div` | L3; L6 Weak | First dividing membrane cells. Damage unjams a stuck rod. |
| `xcell-turn` | retracted | Waste gated by the wrong channel and planted in founders (my bug). |
| L7 (all attempts) | **Contradicted** | ASSAY_ONE_LINE |

Showcase: `movies/showcase.mp4` (0.8 MB, 12 s). xcell-her seed 0, 160², t = 0-400, with
fixed colour scales over the whole run. Cyan is the body activator u, orange the
Cahn-Hilliard membrane m, magenta the heritable marker h. Ten planted cells (half carry the
marker) grow, elongate and pinch in two, and each daughter re-forms a complete membrane
ring. White (marker-carrying) cells only ever give white daughters, and cyan-centred cells
only cyan ones, until the box fills with a near-hexagonal array of 21 cells of two kinds at
t≈150. Founders and their marker states are planted; division and inheritance are the
dynamics.

## Mechanisms that worked (with the ablation that shows it)

1. **Front-deposited membrane:** a channel driven by `g = 4s(1−s)`,
   `s = tanh(max(z,0)/sc)`. It vanishes at the vacuum and in saturated interiors, so it
   draws a ring exactly at a body's front, including every new front made by division or
   wounding. An optional Cahn-Hilliard term (wells 0/1, k∇⁴ in the exact Fourier step)
   *broadens* and caps the ring: 8 px vs 3 px FWHM, peak 0.56 vs 1.38. It does not sharpen it.
2. **Membrane-gated mobility, `∇·(D e^{−βm} ∇f)`** — the operator that does the work. It
   makes the boundary sharp for a species whose own diffusion length exceeds the cell: cargo
   with D=4 drops from 1.24 to ≈0 across the ring; with β=0 it is 0.44 with a √(Dτ) tail. It
   also keeps a bistable marker inside its cell: with no gate, every planted on-lineage is lost
   (committee re-runs; my L arm at Dh=0.02). Three threads reached the same operator
   independently (autopoiesis φ² gate, active-droplets shell), and the committee calls it the
   lab's first transferable beyond-Laplacian operator.
3. **Division = RD cargo feedback + global cap.** Cargo activates the body (K[u,c]<0), and a
   fast global channel caps the total. Ablations: kc=0 gives 0 splits; β=0 still divides (8
   vs 13-15 splits), so the gate modulates division but does not cause it. dt/2 and dx 0.5→0.33
   give the same sequence. The same genome forms ~26 cells from smoothed noise.
4. **Heredity by bistability + gate.** A marker h with `−h³+h−0.2` is tilted on inside bodies
   (kb≈0.25) and kept in by the gate. It works in a narrow window: kb 0.15 lets domains shrink
   and die; kb ≥0.32 or a marker→body feedback makes the domain invade and stretch cells into
   sterile rods. kb −10% already gives switches (committee).

## What failed (one line each)

- Ring-kernel coupling, porous diffusion, advection by −α∇v, and taxis χ<0 all tile space; taxis χ>0 collapses to one spot.
- The marker feeding the body (kh ≥0.1) makes rods that don't divide ("selection" by sterility).
- Intrinsic turnover: unplanted gated waste, slow global food and slow local food all freeze or starve. m4 cells essentially never die on their own.
- Arisen markers: in sprint 2, 3 on→on+off and 0 on→on+on. A small polar kick has not filled the cell before it pinches. ASSAY_FAIL_LINE
- Selection S vs N (sprint 2): no difference, underpowered (~1 division per cell per 1000 t).

## What transfers to PhySim worlds

- The x-genome spec (`XGENOME_SPEC.md`): four vacuum-exact keys (band g, ch, perm with named
  channels, taxis/kern/porous/adv) on top of blobkit. A genome without them is plain blobkit,
  and parity is 4e-14. `perm` + `band` give an agent a *hidden law* to discover: an invisible
  rim field that changes the diffusivity of other fields.
- Measurables for an agent: a cargo in/out ratio that responds to β, membrane width vs M,
  division count vs kc and the cap K, and marker persistence vs kb. All are clean dose-response
  curves.
- Cautions: world-level Python (kicks, erasure) sits outside the genome. Planting non-body
  channels silently changes outcomes (my xcell-turn bug).

## What a next lab should try

1. **An independent membrane field** that the cell makes (amphiphile shell or tilted Allen-Cahn
   wall), carrying the same gate, so that repair and division of the membrane are its own dynamics.
2. **Heredity that survives a polar mutation:** within-cell purification by cross-inhibition
   (active-droplets mechanism 4), or growth that purifies the body before fission
   (chemotaxis-motility r2). Only then measure selection, using per-kind inter-division times.
3. **Intrinsic death:** a conserved cost that division splits between daughters, to replace disk erasure.
