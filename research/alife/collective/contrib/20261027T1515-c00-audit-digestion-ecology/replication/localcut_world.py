"""Audit wrapper (replication lens) around the c52 claim world, imported unchanged.

Local ablation of individual predators' supply: at time AB["t"] the prey material (and its catalysis product p) is
deleted inside disks of radius AB["r"] centred on chosen prey bodies, each of which carries exactly one predator.
Every other prey (and every other predator's supply) is left as it is. Waste w is NOT touched, so prey material can
still be remade in the hole at the world's slow rate g w. The predator material is never touched.
Env: AB='{"t": 6000, "r": 9, "pts": [[y, x], ...]}' plus the claim's WORLD_P.
"""
import importlib.util, json, os
import numpy as np

_CLAIM = "/home/user/physim/research/alife/collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py"
_spec = importlib.util.spec_from_file_location("c52_claim_world", _CLAIM)
_w = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_w)

META = dict(_w.META)
META["name"] = "c52-local-prey-cut (audit wrapper)"
P = _w.P
AB = json.loads(os.environ.get("AB", "{}"))
init, fields, q_bath, damage = _w.init, _w.fields, _w.q_bath, _w.damage


def step(s):
    if AB and abs(s["t"] - AB["t"]) < s["par"]["dt"] / 2:
        H, W = s["shape"]
        m = np.zeros((H, W), bool)
        for y, x in AB["pts"]:
            dy = (s["yy"] - y + H / 2) % H - H / 2
            dx = (s["xx"] - x + W / 2) % W - W / 2
            m |= (dy * dy + dx * dx) <= AB["r"] ** 2
        s["pa"] = np.where(m, -1.0, s["pa"])
        s["p"] = np.where(m, 0.0, s["p"])
        s["ab_mask"] = m
    return _w.step(s)
