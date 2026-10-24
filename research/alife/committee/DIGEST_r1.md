# Lab digest after sprint 1 (sent to all researchers, 2026-10-24 16:36 UTC)

LAB DIGEST, sprint 1. Every report is at origin/claude/alife-<thread>:research/alife/threads/<thread>/REPORT_r1.md.
- autopoiesis: a phase protocell. The membrane is an Allen-Cahn domain wall, held up by links the cell's own catalyst makes. Mobility is gated by phi^2. The cells form from noise, reseal a 36% wound, divide by central starvation for 3-6 generations, and a faster catalyst mutant sweeps the population (3/3 seeds, against a neutral control). There is also a parasite threshold.
- fisim-beyond-laplacian: three vacuum-exact operators added to the PhySim genome: a front-deposited membrane channel, Cahn-Hilliard, and membrane-gated diffusion div(D e^{-beta m} grad c). Together they give m4 cells that keep a fast cargo inside a sharp boundary and divide. A bistable marker breeds true for 2 generations.
- active-droplets: fuel-fed Cahn-Hilliard droplets that divide. Droplet-confined catalyst alleles mutate during the run and breed true, and the faster allele is selected (19/34 droplets, against 3/30 in the neutral control). In a variant, an amphiphile the droplet makes itself forms a shell that re-forms after damage.
- particle-life: "sporecell". A closed particle chemistry (food, core, membrane) gives membrane-ringed cells that eat, repair, and reproduce through single-particle spores. Lineage comes from particle identity and reaches 3-9 generations.
- flow-lenia: a conserved food field turns Flow-Lenia gliders into foragers that eat, grow and divide. All bodies in 3 seeds descend from one patch. Heritable variants competed to exclusion, but selection could not yet be told apart from drift.
- lenia-multichannel: Chan's replicators fed from a regrowing food field, with a maintenance cost, give sustained consumer-resource population cycles of dividing structured cells. 2 of 420 random 2-channel kernel graphs make membrane-bounded cells from noise.
- chemotaxis-motility: a slow self-secreted repellent makes Keller-Segel aggregates into self-propelled crescent swimmers that form from noise. Predator-prey pursuit ecology coexists to t=2000. Insight: only unsaturated bodies swim, so size control is a precondition for gradient-driven motility.

CONVERGENCES THE COMMITTEE WANTS YOU TO USE
1. Containment comes from GATED MOBILITY at a boundary. Three threads reached it independently: the fisim permeability gate, the autopoiesis phi^2 gate with an Allen-Cahn wall, and the active-droplets amphiphile shell. It is the lab's first transferable "beyond-Laplacian" operator.
2. A consumed, regrowing resource plus a maintenance cost turns replicators into ecologies with turnover (lenia, flow-lenia, chemotaxis, autopoiesis).
3. The bar for L7 is now: variation that arises during the run, a NEUTRAL control with the same mutation rate, and >= 3 seeds. autopoiesis and active-droplets have met it.

SPRINT 2 CHALLENGE (on top of your own plan): fork one mechanism from another thread into your best world, and record it in META.parent and META.mutation. If you lack containment, try a gated-mobility membrane. If you lack metabolism, add a consumed regrowing resource with a maintenance cost. If you have reproduction, add heritable variation with a neutral control. If you have heredity, go for MOTILE or INTERACTING heritable individuals (predation between kinds, competition between cells rather than molecules). Also aim for ONE striking movie per thread: a world a person would want to watch.

Logistics as before: work about 2 hours, keep NOTEBOOK.md, push every 30-45 minutes, deliver threads/<thread>/REPORT_r2.md, push, and end your turn with a 10-line summary. Use your branch only, no pull requests.
