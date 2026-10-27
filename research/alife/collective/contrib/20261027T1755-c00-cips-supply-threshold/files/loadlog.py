"""Read a world_ramp.py jsonl log into records, events and per-track histories."""
import json
import numpy as np


def load(path):
    recs, evs, meta = [], [], None
    for line in open(path):
        r = json.loads(line)
        if r["type"] == "rec":
            recs.append(r)
        elif r["type"] == "event":
            evs.append(r)
        else:
            meta = r
    return meta, recs, evs


def tracks(recs):
    """id -> list of (t_rel, kF, area, emax, F_in)."""
    tr = {}
    for r in recs:
        for i, a, em, fi in zip(r["ids"], r["areas"], r["emax"], r["F_in"]):
            tr.setdefault(i, []).append((r["t_rel"], r["kF"], a, em, fi))
    return {k: np.array(v) for k, v in tr.items()}


def series(recs, key):
    return np.array([r["t_rel"] for r in recs]), np.array([r[key] for r in recs], float)
