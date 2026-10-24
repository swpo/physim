"""Gene-coloured sheet from a record_gene.py snapshot file: white = ancestral, orange = high g, cyan = low g.

python threads/flow-lenia/scripts/audit_sheet.py RUN.npz OUT.png
"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from labkit import render as R  # noqa: E402

d = np.load(sys.argv[1]); M, Z, T = d["matter"].astype(np.float32), d["logg"].astype(np.float32), d["t"]
pick = np.unique(np.linspace(0, len(T) - 1, 24).round().astype(int))
w = 1 / (1 + np.exp(-Z[pick] / 0.15))
F = np.stack([M[pick] * (1 - w), M[pick] * w], 1)
sc = R.channel_scales(F)
R.contact_sheet([R.composite(R.normalize(f, sc)) for f in F], [f"t={T[k] * 0.2:g}" for k in pick], ncols=6, tile=256,
                title=f"{Path(sys.argv[1]).stem}: matter coloured by log g (cyan low, white ancestral, orange high); fixed scales").save(sys.argv[2])
