"""Evoloop (Sayama 1999): self-replicating, sheathed loops on a 9-state von Neumann cellular automaton.

States: 0 empty, 1 core, 2 sheath, 3-7 signals (7 = straight, 4 = turn, 5/6 arm control), 8 dissolution.
A loop is a square ring of sheath (2) around a core ring that carries a cyclic genome of "170" (extend)
and "140" (turn) triplets; the genome is copied down an arm that builds a daughter of the same size, and
collisions damage loops: damaged structure turns into state 8, which spreads over connected structure
and clears it (an intrinsic death). Variation in loop size arises when collisions corrupt a genome.
Transition table: Golly Rules/Evoloop.rule (Bachmutsky's port of Sayama's table, patched); unlisted
neighbourhoods leave the cell unchanged. The founder is a Langton-type loop of core side m (hole side
m - 4) with an arm, placed at a seed-dependent position and orientation.
WORLD_P (JSON) overrides P.
"""
import numpy as np, itertools, re, os, json as _json

META = {
    "name": "evoloop",
    "family": "cellular-automaton",
    "parent": "new class (Sayama 1999 evoloop; Langton 1984 loops)",
    "mutation": "none (benchmark model); founder loop size m as a parameter",
    "size": (300, 300),
    "steps_per_frame": 200,
    "dt": 1.0,
    "channels": ["loop body (structure, gaps closed, holes filled)", "sheath (state 2)", "genome signals (states 3-7)", "dissolution (state 8)"],
    "matter": [0],
    "smooth": 0.5,
    "periodic": True,
    "radial_channels": [1, 2, 3],
}
P = dict(m=15, founders=2, rule="Evoloop.rule", ms=None)
P.update(_json.loads(os.environ.get("WORLD_P", "{}")))
_HERE = os.path.dirname(os.path.abspath(__file__))


def load_table(path):
    tab = open(path).read().split('@TABLE')[1].split('@')[0]
    nst = None; var = {}; rules = []
    for line in tab.splitlines():
        line = line.split('#')[0].strip()
        if not line: continue
        if line.startswith('n_states'): nst = int(line.split(':')[1]); continue
        if line.startswith('neighborhood'): assert 'vonNeumann' in line; continue
        if line.startswith('symmetries'): assert 'rotate4' in line; continue
        if line.startswith('var'):
            m = re.match(r'var\s+(\w+)\s*=\s*\{(.*)\}', line); vals = []
            for tok in m.group(2).split(','):
                tok = tok.strip(); vals += var[tok] if tok in var else [int(tok)]
            var[m.group(1)] = vals; continue
        toks = [t.strip() for t in line.split(',')] if ',' in line else list(line.replace(' ', ''))  # CNESWC' without commas
        rules.append([(t, list(var[t])) if t in var else (t, None) for t in toks])  # bind variables as defined at this line
    lut = -np.ones(nst ** 5, dtype=np.int16)
    for toks in rules:  # first matching rule wins; a variable repeated in one rule is bound to one value
        vs = dict((t, v) for t, v in toks if v is not None)
        names = list(dict.fromkeys(t for t, v in toks[:5] if v is not None))
        for combo in itertools.product(*[vs[n] for n in names]):
            b = dict(zip(names, combo)); c, n, e, s, w, o = [b[t] if t in vs else int(t) for t, v in toks]
            for nn, ee, ss, ww in [(n, e, s, w), (w, n, e, s), (s, w, n, e), (e, s, w, n)]:
                idx = (((c * nst + nn) * nst + ee) * nst + ss) * nst + ww
                if lut[idx] < 0: lut[idx] = o
    miss = np.where(lut < 0)[0]; lut[miss] = miss // nst ** 4
    return nst, lut.astype(np.uint8)


def make_loop(m):
    """Langton-type loop: core side m (m >= 8), genome (m-2) x 170 + 2 x 140 + (m-4) blanks, arm of m-3 cells."""
    arm = m - 3; g = np.zeros((m + 2, m + arm + 2), np.uint8)
    g[0, 1:m+1] = 2; g[m+1, 1:m+arm+1] = 2; g[1:m+1, 0] = 2; g[1:m, m+1] = 2
    g[2:m, 2] = 2; g[2:m, m-1] = 2; g[2, 2:m] = 2; g[m-1, 2:m] = 2
    s = "170" + "140" * 2 + "1" * (m - 4) + "170" * (m - 3)
    path = [(1, j) for j in range(1, m+1)] + [(i, m) for i in range(2, m+1)] + [(m, j) for j in range(m-1, 0, -1)] + [(i, 1) for i in range(m-1, 1, -1)]
    for (i, j), c in zip(path, s): g[i, j] = int(c)
    g[m, m+1:m+arm+1] = 1; g[m, m+arm+1] = 2; g[m-1, m+1:m+arm+1] = 2
    return g


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    nst, lut = load_table(os.path.join(_HERE, P["rule"]))
    g = np.zeros((H, W), np.uint8)
    r0 = rng.integers(4)
    ms = P["ms"] or [int(P["m"])] * int(P["founders"])  # c27: optional per-founder core sides (competition assay)
    for k, mk in enumerate(ms):  # founders differ by 90 degrees: 180-degree pairs would keep a point symmetry forever
        lp = np.rot90(make_loop(int(mk)), r0 + k)
        i0, j0 = rng.integers(H), rng.integers(W)
        ii = (i0 + np.arange(lp.shape[0]))[:, None] % H; jj = (j0 + np.arange(lp.shape[1]))[None, :] % W
        g[ii, jj] = np.where(lp > 0, lp, g[ii, jj])
    return {"g": g, "lut": lut, "nst": nst, "t": 0}


def step(s):
    g = s["g"]; nst = s["nst"]
    N = np.roll(g, 1, 0); S = np.roll(g, -1, 0); W = np.roll(g, 1, 1); E = np.roll(g, -1, 1)
    s["g"] = s["lut"][(((g.astype(np.int32) * nst + N) * nst + E) * nst + S) * nst + W]
    s["t"] += 1
    return s


def body(g):
    """Loop bodies: structure closed over 1-cell gaps (the genome's empty cells), with enclosed holes filled."""
    from scipy import ndimage
    st = g > 0
    c = ndimage.binary_closing(np.pad(st, 2, mode="wrap"), structure=np.ones((3, 3)))[2:-2, 2:-2] | st
    return ndimage.binary_fill_holes(c)


def fields(s):
    g = s["g"]
    return np.stack([body(g), g == 2, (g >= 3) & (g <= 7), g == 8]).astype(np.float32)


def damage(s, mask):
    s["g"] = np.where(mask, 0, s["g"]).astype(np.uint8)
    return s


def stats(s):
    g = s["g"]
    return {"live": int((g > 0).sum()), "dissolving": int((g == 8).sum())}
