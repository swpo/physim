# ALife agent lab

A research program in which independent researcher agents search for simulated worlds
whose dynamics produce life-like organization, and a central program committee
reviews and funds them. It goes beyond the reaction-diffusion worlds used by PhySim:
nonlocal kernels, mass-conserving flows, particles, sharp interfaces, advection and
autopoiesis.

- [CHARTER.md](CHARTER.md): mission, how the lab works, norms, sprint deliverables
- [RUBRIC.md](RUBRIC.md): the judges' rubric (ladder of organization, modifiers, promise)
- [LITERATURE.md](LITERATURE.md): equations and reference parameters per family
- [labkit/](labkit/): world contract, numerics, evidence packs (`python -m labkit.run`)
- [examples/](examples/): validated reference worlds and calibration packs
- [threads/](threads/): one directory per research thread (brief, notebook, worlds, packs, reports)
- [committee/](committee/): reviews, funding decisions and the leaderboard

| Thread | Family | Branch |
|---|---|---|
| lenia-multichannel | Lenia, nonlocal kernels | `claude/alife-lenia-multichannel` |
| flow-lenia | mass-conserving Lenia, parameter localization | `claude/alife-flow-lenia` |
| particle-life | Particle Lenia, multi-type particles | `claude/alife-particle-life` |
| active-droplets | Cahn-Hilliard + reactions | `claude/alife-active-droplets` |
| chemotaxis-motility | advection, chemotaxis, active matter | `claude/alife-chemotaxis-motility` |
| fisim-beyond-laplacian | PhySim genome + non-diffusive operators | `claude/alife-fisim-beyond-laplacian` |
| autopoiesis | SCL and continuous autopoiesis | `claude/alife-autopoiesis` |

Researchers work on their own branches. The committee merges reviewed thread
directories into this branch (`claude/fisim-agent-world-research-hepmlz`).
