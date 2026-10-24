# tools (lenia-multichannel)

Run from `research/alife` with the lab env. The catalogue file `chan_found.json` (60 MB, not
committed) is built by parsing `Python/found/*.json` of https://github.com/Chakazul/Lenia; see
NOTEBOOK E1. Re-create it with `parse_catalogue.py` (indices match).

- `engine_src.py`: multi-channel Lenia engine pasted into every world.
- `make_chan_world.py`: world.py from a catalogue creature (optional `--food`, `--jitter`, `--matter`).
- `make_rule_world.py`: world.py from a random-screen rule (noise initial condition).
- `make_eco_world.py`: two-species world (separate rules, shared food, space exclusion).
- `screen_random.py`: random channel/kernel graph families from noise.
- `screen_replicators.py`: random graphs from a small patch, flag growing individual counts.
- `screen_chan.py`, `screen_catalogue_replicators.py`: run catalogue creatures, save strips.
- `quick.py`, `quick_eco.py`, `sweep.py`: fast looks with module-global overrides (`--set`).
- `damage_cell.py`, `extract_cell.py`, `extract_kinds.py`: damage of one cell, cell crops to RLE.
- `mcl.py`: screening copy of the engine.
