"""Audit wrapper around the claimed world (20261025T1508-c14-pcell-mwall-b42-metabolic-claim/world.py):
identical dynamics; every 1000 steps it appends population stats (particles, cells, births, deaths,
mean heritable yield y, mean inert marker z) to $AUDIT_LOG, and at t = $AUDIT_SAVE_T it pickles the state
to $AUDIT_SAVE so that a feed-cut fork can be continued from the exact fed trajectory."""
import importlib.util, json, os, pickle, sys
import numpy as np
from scipy import ndimage

_p = "/home/user/physim/research/alife/collective/contrib/20261025T1508-c14-pcell-mwall-b42-metabolic-claim/world.py"
_spec = importlib.util.spec_from_file_location("b42_claimed", _p)
Wm = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(Wm)
META = dict(Wm.META); META["name"] = "pcell-mwall-b42-audit"
P = Wm.P
P.update(json.loads(os.environ.get("WORLD_P", "{}")))
init, fields, particles, damage = Wm.init, Wm.fields, Wm.particles, Wm.damage
LOG = os.environ.get("AUDIT_LOG", ""); SAVE = os.environ.get("AUDIT_SAVE", ""); SAVE_T = int(os.environ.get("AUDIT_SAVE_T", "-1"))


def step(s):
    s = Wm.step(s)
    t = s["t"]
    if LOG and t % 1000 == 0:
        lab, n = ndimage.label(s["phi"] > 0.5)
        rec = {"t": t, "N": int(len(s["py"])), "cells": int(n), "ymean": float(s["y"].mean()) if len(s["y"]) else None,
               "zmean": float(s["z"].mean()) if len(s["z"]) else None, "births": int(s["births"].sum()), "deaths": int(s["deaths"].sum()),
               "S": float(s["S"].mean()), "M": float(s["M"].sum()), "L": float(s["L"].sum()), "F": P["F"]}
        with open(LOG, "a") as f:
            f.write(json.dumps(rec) + "\n")
    if SAVE and t == SAVE_T:
        with open(SAVE, "wb") as f:
            pickle.dump(s, f)
    return s
