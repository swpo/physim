"""Write worlds/<id>/world.py: a self-contained labkit world embedding the x-genome stepper.

    python mkworld.py <id> <parent> "<mutation>" genome.json [--n N] [--T T] [--frames F] [--soup n]
"""
import argparse, json, pathlib, textwrap

HERE = pathlib.Path(__file__).parent
ap = argparse.ArgumentParser()
ap.add_argument("id"); ap.add_argument("parent"); ap.add_argument("mutation"); ap.add_argument("genome")
ap.add_argument("--n", type=int, default=160); ap.add_argument("--spf", type=int, default=100)
ap.add_argument("--soup", type=int, default=8); ap.add_argument("--acts", default=None)
ap.add_argument("--doc", default="")
ap.add_argument("--dress", default=None, help="json list of channel indices that get the blobkit dressed poke (default: all id channels driven by the poked act)")
ap.add_argument("--channels", default=None)
ap.add_argument("--render", default=None, help="json list of state indices returned by fields()")
a = ap.parse_args()
g = json.load(open(a.genome))
core = (HERE / "xgenome.py").read_text().split('"""', 2)[2]
na, nc = len(g["acts"]), len(g["chans"])
chans = json.loads(a.channels) if a.channels else [f"u{i}" for i in range(na)] + [f"x{c}" for c in range(nc)]
acts = json.loads(a.acts) if a.acts else list(range(na))
render = json.loads(a.render) if a.render else list(range(na + nc))
dress = json.loads(a.dress) if a.dress else None
src = f'''"""{a.id}: extended PhySim/blobkit genome world (thread fisim-beyond-laplacian).

{textwrap.fill(a.mutation, 88)}
{a.doc}
Numerics: blobkit conventions (dx=0.5, dt=0.02, explicit reaction with old fields, exact
linear diffusion [+ Cahn-Hilliard k^4] in Fourier space). Stepper copied from
threads/fisim-beyond-laplacian/xgenome.py (parity with blobkit m4: 4e-14 after 1000 steps).
"""
import json
import numpy as np
import scipy.fft as sfft

GENOME = json.loads(r"""{json.dumps(g)}""")

META = {{
    "name": "{a.id}",
    "family": "fisim-extended-rd",
    "parent": "{a.parent}",
    "mutation": {json.dumps(a.mutation)},
    "size": ({a.n}, {a.n}),
    "steps_per_frame": {a.spf},
    "dt": 0.02,
    "channels": {json.dumps(chans)},
    "smooth": 1.0,
    "periodic": True,
}}
SOUP_N = {a.soup}
SOUP_ACTS = {acts}
RENDER = {render}            # state indices shown/measured by labkit (all others are hidden)
DRESS = {dress}            # channels given the dressed poke at t=0 (None = all id channels; others start at vacuum)
{core}

def init(seed, size):
    N = size[0]
    dx = 0.5
    rng = np.random.default_rng(seed)
    g = GENOME
    S = make_state(g, N, seed=seed)
    F = S["F"]
    L = N * dx
    na = len(g["acts"])
    W = np.asarray(g["W"], float)
    pts = []
    for _ in range(5000):
        p = rng.uniform(0, L, 2)
        if all(np.hypot(*(((p - q) + L / 2) % L - L / 2)) >= 14.0 for q in pts):
            pts.append(p)
            if len(pts) == SOUP_N:
                break
    for k, p in enumerate(pts):
        a = SOUP_ACTS[k % len(SOUP_ACTS)]
        ang = rng.uniform(0, 2 * np.pi)
        poke(F, a, p[0], p[1], 2.0, 3.0, dx)
        tmp = np.zeros_like(F)
        poke(tmp, 0, p[0] - 0.5 * np.sin(ang), p[1] - 0.5 * np.cos(ang), 1.2, 3.0, dx)
        for c, ch in enumerate(g["chans"]):
            if ch["g"] == "id" and W[c, a] != 0 and (DRESS is None or c in DRESS):
                F[na + c] += W[c, a] * tmp[0]
    F[:na] += 0.01 * rng.standard_normal(F[:na].shape)
    return S


def fields(S):
    F = S["F"].copy()
    F[:S["na"]] -= S["u0"]          # report deviations: vacuum = 0 in every channel
    return np.clip(F[RENDER], 0, None)   # positive parts of deviations (vacuum = 0)


def matter(Fd):
    return np.clip(Fd[0], 0, None)


def damage(S, mask):
    S["F"][:, mask] = 0.0
    S["F"][:S["na"], mask] = S["u0"][:, 0, 0][:, None]
    return S
'''
out = HERE / "worlds" / a.id / "world.py"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(src)
print("wrote", out)
