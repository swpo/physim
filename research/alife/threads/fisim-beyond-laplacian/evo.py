"""xcell-evo genome: xcell-her minus the unused hdep channel, plus one membrane-gated waste
channel for turnover. Arms: S (gated h, marker boosts cargo production), N (gated h, neutral),
L (no gate on h, Dh lowered). All perm/taxis entries use channel names."""
import json
import numpy as np


def genome(arm="N", kb=0.25, kc=0.25, wch=0.2, kw=0.15, tw=40.0, Dw=2.0, beta=5.0,
           Dh=0.3, DhL=0.05, k1h=-0.2, Kg=1.0):
    with open("/home/user/physim/packages/blobkit/blobkit/data/worlds/m4.json") as f:
        m4 = json.load(f)
    body = dict(m4["acts"][0], name="u")
    roots = np.roots([-1.0, 0.0, 1.0, k1h])
    u0h = float(min(r.real for r in roots if abs(r.imag) < 1e-9))
    h = dict(name="h", lam=1.0, k1=k1h, Du=(DhL if arm == "L" else Dh), u0=u0h)
    ch = lambda name, tau, D, g="id", **e: dict(name=name, tau=tau, D=D, g=g, thr=0.0, sc=1.0, **e)
    chans = [dict(m4["chans"][0], name="v"), dict(m4["chans"][1], name="w"),
             dict(name="m", tau=2.0, D=0.0, g="band", thr=0.0, sc=0.6, ch={"M": 1.0, "k": 1.0, "h": 0.5}),
             ch("glob", 10.0, 100.0), ch("bdep", 1.0, 0.5), ch("c", 5.0, 4.0), ch("q", tw, Dw)]
    #      drive from:  u     h
    W = [[1, 0],                       # v
         [1, 0],                       # w
         [2, 0],                       # m   (band of the body front)
         [1, 0],                       # glob
         [1, 0],                       # bdep (tilts h on inside bodies)
         [1, wch if arm == "S" else 0.0],  # c (cargo); S: the marker adds cargo production
         [1, 0]]                       # q (waste)
    #        v    w    m    glob  bdep  c    q
    K = [[1.0, 1.5, 0.0, Kg,  0.0, -kc, kw],
         [0.0, 0.0, 0.0, 0.0, -kb, 0.0, 0.0]]
    perm = [["c", "m", beta], ["q", "m", beta]] + ([] if arm == "L" else [["h", "m", beta]])
    return dict(id=f"xcell-evo-{arm}", acts=[body, h], chans=chans, W=W, K=K, bilin=[], perm=perm,
                provenance=dict(kind="fisim-beyond-laplacian sprint 2", arm=arm))
