# Lab videos

Each comparison re-runs a world and its matched control from the world files: same seed, same
grid and, for field worlds, one colour scale shared by every arm. The live number under each
panel is computed by `make_videos.py`. The caption numbers and verdicts are the committee's final
record (`committee/LEADERBOARD.md`).

| Video | What it compares | Final verdict |
|---|---|---|
| `lab_reel.mp4` | the seven thread showcases, captioned | see each clip |
| `membrane_ring_does_work.mp4` | autopoiesis `phase_membrane` vs `phase_membrane_chi0` | L6[L3] medium vs L6[L2] medium |
| `selection_vs_twin.mp4` | autopoiesis `membrane_evo_up` / twin / `_down`, seed 4 | L7[L3] low |
| `gate_holds_cargo.mp4` | fisim `xcell-a` vs `xcell-a-nogate` | L4b[L3] medium |
| `metabolism_needs_food.mp4` | lenia `mcf-MIRd` vs `mcf-MIRd-norefill` | L6[L2]+L4c high |
| `trail_propulsion.mp4` | chemotaxis `kstrail` vs `chi_h = 0` | L4b[L2] high |
| `spores_were_overshoot.mp4` | particle-life `sporecell2-sel` at dt 0.02 / 0.01 / 0.005 | L2 high; spores were a timestep artifact |

Regenerate from `research/alife/` (about 20 CPU-minutes for all arms):

```
python movies/make_videos.py list
python movies/make_videos.py sim membrane_ring_does_work 0   # one arm -> movies/_cache/
python movies/make_videos.py compose membrane_ring_does_work
python movies/make_videos.py reel
```
