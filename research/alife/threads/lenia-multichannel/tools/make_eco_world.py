"""Write a two-species world: two catalogue creatures, each with its own channels and rule,
coupled only through a shared food field (build-from-food metabolism) and space exclusion.

python make_eco_world.py catalogue.json IDX_A IDX_B WORLD_ID [--nA 1 --nB 1 --size 192 --food JSON --excl 1.0]
"""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).parent

TEMPLATE = '''"""Two-species multi-channel Lenia ecology.

Species A: Chan (2020) creature '{nameA}' ({codeA}); species B: '{nameB}' ({codeB}), both from
Chakazul/Lenia Python/found (catalogue indices {iA}, {iB}). Each species keeps its own 3 channels and
its own 15-kernel rule; the species never sense each other through kernels. They interact only by
  (1) a shared food field F: matter can only be built from local food (yield Y), food regrows at
      rate rho toward Fmax and diffuses with D;
  (2) space exclusion: positive growth of one species is multiplied by (1 - occupancy of the other)^EXCL,
      occupancy = clip(sum of the other species' channels, 0, 1).
Planted creatures (not spontaneous), small multiplicative jitter per seed.
"""
{engine}

META = {{
    "name": "{name}",
    "family": "lenia",
    "parent": {parent!r},
    "mutation": {mutation!r},
    "size": ({size}, {size}),
    "steps_per_frame": {spf},
    "dt": 0.1,
    "channels": ["A0", "A1", "A2", "B0", "B1", "B2", "F"],
    "matter": [0, 3],   # core channel of each species (halos fuse neighbours otherwise)
    "smooth": 1.0,
}}

R, T = 15, 10
RULE_A = {ruleA}
RULE_B = {ruleB}
CELLS_A = {cellsA}
CELLS_B = {cellsB}
N_A, N_B = {nA}, {nB}
FOOD = {food!r}
EXCL = {excl}
JITTER = 0.05


def _place(A, cr, n, rng, placed):
    H, W = A.shape[1:]
    h, w = cr.shape[1:]
    for _ in range(n):
        for _try in range(100):
            y, x = int(rng.integers(0, H)), int(rng.integers(0, W))
            if all(min(abs(y - py), H - abs(y - py)) > 2.5 * max(h, w) or
                   min(abs(x - px), W - abs(x - px)) > 2.5 * max(h, w) for py, px in placed):
                break
        placed.append((y, x))
        c = np.rot90(cr, int(rng.integers(4)), axes=(1, 2))
        A = np.maximum(A, np.roll(np.pad(c, ((0, 0), (0, H - c.shape[1]), (0, W - c.shape[2]))), (y, x), (1, 2)))
    return A


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    placed = []
    A = _place(np.zeros((3, H, W)), _creature(CELLS_A), N_A, rng, placed)
    B = _place(np.zeros((3, H, W)), _creature(CELLS_B), N_B, rng, placed)
    A = np.clip(A * (1 + JITTER * rng.standard_normal(A.shape)), 0, 1)
    B = np.clip(B * (1 + JITTER * rng.standard_normal(B.shape)), 0, 1)
    ky = 2 * np.pi * np.fft.fftfreq(H)[:, None]
    kx = 2 * np.pi * np.fft.rfftfreq(W)[None, :]
    return {{"A": A, "B": B, "F": np.full((H, W), FOOD.get("F0", 1.0)), "lapK": -(kx ** 2 + ky ** 2),
            "LA": Lenia(RULE_A, 3, size, R, T), "LB": Lenia(RULE_B, 3, size, R, T)}}


def step(s):
    dt = 0.1
    A, B, F = s["A"], s["B"], s["F"]
    occA, occB = np.clip(A.sum(0), 0, 1), np.clip(B.sum(0), 0, 1)
    incs, decs = [], []
    for X, L, occ_other in ((A, s["LA"], occB), (B, s["LB"], occA)):
        G = L.growth(X)
        inc = np.clip(np.minimum(dt * G, 1 - X), 0, None) * (1 - occ_other) ** EXCL
        incs.append(inc)
        decs.append(np.clip(dt * G, None, 0))
    need = (incs[0].sum(0) + incs[1].sum(0)) / FOOD["Y"]
    scale = np.minimum(1, F / np.maximum(need, 1e-12))
    s["A"] = np.clip(A + incs[0] * scale + decs[0], 0, 1)
    s["B"] = np.clip(B + incs[1] * scale + decs[1], 0, 1)
    F = F - need * scale + dt * FOOD["rho"] * (FOOD.get("Fmax", 1.0) - F)
    F = _irfft2(_rfft2(F) / (1 - dt * FOOD["D"] * s["lapK"]), F.shape)
    s["F"] = np.clip(F, 0, None)
    return s


def fields(s):
    return np.concatenate([s["A"], s["B"], s["F"][None]])


def damage(s, mask):
    s["A"][:, mask] = 0
    s["B"][:, mask] = 0
    return s
'''

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cat")
    ap.add_argument("iA", type=int)
    ap.add_argument("iB", type=int)
    ap.add_argument("wid")
    ap.add_argument("--nA", type=int, default=1)
    ap.add_argument("--nB", type=int, default=1)
    ap.add_argument("--size", type=int, default=192)
    ap.add_argument("--spf", type=int, default=10)
    ap.add_argument("--food", default='{"Y": 2, "rho": 0.01, "D": 2}')
    ap.add_argument("--excl", type=float, default=1.0)
    a = ap.parse_args()
    cat = json.load(open(a.cat))
    eA, eB = cat[a.iA], cat[a.iB]

    def rule(e):
        r = [{k: p[k] for k in ("b", "m", "s", "h", "r", "c") if k in p} for p in e["params"]]
        return "[\n" + "".join(f"    {json.dumps(k)},\n" for k in r) + "]"

    def cells(e):
        return "[\n" + "".join(f"    {json.dumps(c)},\n" for c in e["cells"]) + "]"

    out = HERE.parent / "worlds" / a.wid
    out.mkdir(parents=True, exist_ok=True)
    (out / "world.py").write_text(TEMPLATE.format(
        engine=(HERE / "engine_src.py").read_text(), name=a.wid, nameA=eA["name"], codeA=eA["code"],
        nameB=eB["name"], codeB=eB["code"], iA=a.iA, iB=a.iB, parent="mcf-MIRd",
        mutation="two species (separate channel sets and rules) sharing one food field with space exclusion",
        size=a.size, spf=a.spf, ruleA=rule(eA), ruleB=rule(eB), cellsA=cells(eA), cellsB=cells(eB),
        nA=a.nA, nB=a.nB, food=json.loads(a.food), excl=a.excl))
    print(out / "world.py")
