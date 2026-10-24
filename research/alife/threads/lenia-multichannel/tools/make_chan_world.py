"""Write a self-contained world.py for one creature of Chan's catalogue.

python make_chan_world.py catalogue.json IDX WORLD_ID [--n 3] [--size 192] [--spf 5]
"""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).parent

TEMPLATE = '''"""{doc}"""
{engine}

from labkit import ops  # noqa: E402  (only for disk masks in damage)

META = {{
    "name": "{name}",
    "family": "lenia",
    "parent": {parent!r},
    "mutation": {mutation!r},
    "size": ({size}, {size}),
    "steps_per_frame": {spf},
    "dt": {dt},
    "channels": ["A0", "A1", "A2"][:{C}] + (["F"] if {food!r} else []),
    "matter": list(range({C})),
}}

R, T = {R}, {T}
RULE = {rule}
CELLS = {cells}
N_SEED = {n}
C = {C}
NOISE = 0.6
JITTER = {jitter}   # multiplicative noise on planted creatures, so seeds differ beyond exact symmetries
# Optional metabolism: food field F (diffusing with D, regrowing at rate rho toward Fmax).
#  mode "conserve": matter can only be built from local food (yield Y); see step().
#  otherwise ("gate"): positive growth multiplied by F^gate, eating at eat*mass*F, starving at starve*(1-F).
FOOD = {food!r}


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    if CELLS is None:   # spontaneous: random noise in a square patch covering NOISE of the grid side
        A = np.zeros((C, H, W))
        p = int(NOISE * min(H, W))
        A[:, :p, :p] = rng.random((C, p, p))
        A = np.roll(A, (int(rng.integers(H)), int(rng.integers(W))), (1, 2))
        return _finish(A, size)
    cr = _creature(CELLS)
    A = np.zeros((len(CELLS), H, W))
    h, w = cr.shape[1:]
    placed = []
    for _ in range(N_SEED):
        for _try in range(50):
            y, x = int(rng.integers(0, H)), int(rng.integers(0, W))
            if all(min(abs(y - py), H - abs(y - py)) > max(h, w) * 1.2 or
                   min(abs(x - px), W - abs(x - px)) > max(h, w) * 1.2 for py, px in placed):
                break
        placed.append((y, x))
        c = np.rot90(cr, int(rng.integers(4)), axes=(1, 2))
        A = np.maximum(A, np.roll(np.pad(c, ((0, 0), (0, H - c.shape[1]), (0, W - c.shape[2]))), (y, x), (1, 2)))
    if JITTER:
        A = np.clip(A * (1 + JITTER * rng.standard_normal(A.shape)), 0, 1)
    return _finish(A, size)


def _finish(A, size):
    H, W = size
    st = {{"A": A, "L": Lenia(RULE, C, size, R, T)}}
    if FOOD:
        st["F"] = np.full((H, W), FOOD.get("F0", 1.0))
        ky = 2 * np.pi * np.fft.fftfreq(H)[:, None]
        kx = 2 * np.pi * np.fft.rfftfreq(W)[None, :]
        st["lapK"] = -(kx ** 2 + ky ** 2)
    return st


def step(s):
    L, A = s["L"], s["A"]
    G = L.growth(A)
    if FOOD and FOOD.get("mode") == "conserve":
        # matter is built from food: positive growth is capped by the local food F (yield Y),
        # food spent = matter built / Y; decay just dissipates. Behaviour is unchanged where F is plentiful.
        F = s["F"]
        inc = np.clip(np.minimum(L.dt * G, 1 - A), 0, None)
        dec = np.clip(L.dt * G, None, 0) - L.dt * FOOD.get("decay", 0.0) * A   # optional maintenance cost
        need = inc.sum(0) / FOOD["Y"]
        scale = np.minimum(1, F / np.maximum(need, 1e-12))
        A_new = np.clip(A + inc * scale + dec, 0, 1)
        F = F - need * scale + L.dt * FOOD["rho"] * (FOOD.get("Fmax", 1.0) - F)
        if FOOD["D"] > 0:   # implicit spectral diffusion
            F = _irfft2(_rfft2(F) / (1 - L.dt * FOOD["D"] * s["lapK"]), F.shape)
        s["F"] = np.clip(F, 0, None)
        s["A"] = A_new
    elif FOOD:
        F = s["F"]
        G = np.where(G > 0, G * F ** FOOD["gate"], G) - FOOD["starve"] * (1 - F) * A
        A_new = np.clip(A + L.dt * G, 0, 1)
        mass = A_new.sum(0)
        dF = FOOD["rho"] * (1 - F) - FOOD["eat"] * mass * F
        F = F + L.dt * dF
        if FOOD["D"] > 0:   # implicit spectral diffusion
            F = _irfft2(_rfft2(F) / (1 - L.dt * FOOD["D"] * s["lapK"]), F.shape)
        s["F"] = np.clip(F, 0, 1)
        s["A"] = A_new
    else:
        s["A"] = np.clip(A + L.dt * G, 0, 1)
    return s


def fields(s):
    return np.concatenate([s["A"], s["F"][None]]) if FOOD else s["A"]


def damage(s, mask):
    s["A"][:, mask] = 0
    return s
'''


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cat")
    ap.add_argument("idx", type=int)
    ap.add_argument("wid")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--size", type=int, default=192)
    ap.add_argument("--spf", type=int, default=5)
    ap.add_argument("--food", type=str, default=None, help="JSON dict: gate, starve, rho, eat, D, F0")
    ap.add_argument("--mutation", type=str, default="reference creature in this thread's multi-channel engine")
    ap.add_argument("--parent", type=str, default=None)
    ap.add_argument("--jitter", type=float, default=0.0)
    ap.add_argument("--matter", type=str, default=None, help="python list of channel indices to track")
    a = ap.parse_args()
    e = json.load(open(a.cat))[a.idx]
    T = e["params"][0]["T"]
    rule = [{k: p[k] for k in ("b", "m", "s", "h", "r", "c") if k in p} for p in e["params"]]
    rule_src = "[\n" + "".join(f"    {json.dumps(k)},\n" for k in rule) + "]"
    cells_src = "[\n" + "".join(f"    {json.dumps(c)},\n" for c in e["cells"]) + "]"
    doc = (f"Chan (2020) multi-channel Lenia creature '{e['name']}' (code {e['code']}) from "
           f"Chakazul/Lenia Python/{e['file']}, catalogue index {a.idx}.\n\n"
           f"Positive control for the multi-channel engine: {len(e['cells'])} channels, {len(rule)} kernels, R={e['R']}.\n"
           f"{a.n} planted copies (random rotations); the structure is planted, not spontaneous.")
    out = HERE.parent / "worlds" / a.wid
    out.mkdir(parents=True, exist_ok=True)
    (out / "world.py").write_text(TEMPLATE.format(
        doc=doc, engine=(HERE / "engine_src.py").read_text(), name=a.wid, parent=a.parent or f"Chakazul/Lenia {e['file']}#{e['code']}",
        mutation=a.mutation, food=json.loads(a.food) if a.food else None, size=a.size, spf=a.spf, dt=1.0 / T,
        jitter=a.jitter, C=len(e["cells"]), R=e["R"], T=T, rule=rule_src, cells=cells_src, n=a.n))
    if a.matter:
        src = (out / "world.py").read_text().replace(f'"matter": list(range({len(e["cells"])})),',
                                                     f'"matter": {a.matter},')
        (out / "world.py").write_text(src)
    print(out / "world.py")
