"""lcn-colony: the lcn world (world.py, same dynamics and parameters) started from ONE founder body that formed
from full-domain noise in an lcn run (seed 0 or 1, t=1000; founders.json, 4 rods/short worms), planted at the
centre of an empty, food-filled domain (F=1, W=0). Seed k uses founder k%4 rotated by k//4 quarter turns.
Planted founders: a reproduction test, not an S test."""
import json
import os
import importlib.util
import numpy as np

_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("lcn_base", os.path.join(_here, "world.py"))
_b = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_b)

P, step, fields, damage, gated_div = _b.P, _b.step, _b.fields, _b.damage, _b.gated_div
META = dict(_b.META)
META.update({"name": "lcn-colony", "parent": "world.py",
             "mutation": "lcn started from one noise-formed founder in an empty food-filled domain"})
_F = json.load(open(os.path.join(_here, "founders.json")))
_KEYS = sorted(_F)


def init(seed, size):
    H, W = size
    s = _b.init(seed, size)
    crop = np.rot90(np.array(_F[_KEYS[seed % len(_KEYS)]]["A"]), seed // len(_KEYS), axes=(1, 2))
    A = np.zeros((2, H, W))
    h, w = crop.shape[1:]
    A[:, H // 2 - h // 2:H // 2 - h // 2 + h, W // 2 - w // 2:W // 2 - w // 2 + w] = crop
    s["A"], s["F"], s["W"] = A, np.full((H, W), 1.0), np.zeros((H, W))
    s["N0"] = A.sum() / P["Y"] + s["F"].sum()
    return s
