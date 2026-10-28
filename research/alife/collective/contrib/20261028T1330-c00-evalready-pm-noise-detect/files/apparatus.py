"""Eval-readiness pilot: PhySim-style apparatus on a labkit world (phase_membrane).

  prep     run the world from noise to t_prep and save the prepared state
  pulse    Gaussian source (rate amp per time unit, width sig px, duration dur) into one
           field at a bath / body-centre / body-rim site; compare with the uninjected twin
  detect   member ensembles from the prepared state under dynamics noise, native world vs
           its deciding ablations; probe arrays like PhySim's devices; energy scores
"""
import argparse, copy, importlib.util, json, sys
from pathlib import Path

import numpy as np
from scipy import ndimage

WORLD = "/home/user/physim/research/alife/threads/autopoiesis/worlds/phase_membrane/world.py"
OUT = Path(__file__).resolve().parent / "out"
FIELDS = ["S", "K", "L", "phi"]
SEEDS = {"native": 7, "chi0": 11, "gate0": 13, "a_half": 17}


def load(overrides=None):
    spec = importlib.util.spec_from_file_location("pmw", WORLD)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.P.update(overrides or {})
    return m


def advance(m, s, n, noise=0.0, rng=None, inj=None, t0=0):
    """n steps; inj = dict(field, y, x, amp, sig, start, dur) as a source amp*gauss per t."""
    dt = m.P["dt"]
    if inj is not None:
        H, W = s["phi"].shape
        yy, xx = np.mgrid[0:H, 0:W]
        dy = (yy - inj["y"] + H / 2) % H - H / 2
        dx = (xx - inj["x"] + W / 2) % W - W / 2
        bump = np.exp(-(dy ** 2 + dx ** 2) / (2 * inj["sig"] ** 2))
    for k in range(n):
        t = (t0 + k) * dt
        if inj is not None and inj["start"] <= t < inj["start"] + inj["dur"]:
            s[inj["field"]] = s[inj["field"]] + inj["amp"] * dt * bump
        if noise > 0:
            for f in FIELDS:
                s[f] = s[f] + noise * np.sqrt(dt) * rng.standard_normal(s[f].shape)
        s = m.step(s)
    return s


def bodies(s):
    lab, n = ndimage.label(s["phi"] > 0.5, structure=np.ones((3, 3)))
    # periodic merge of labels across the edges
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for i, j in zip(a, b):
            if i and j and i != j:
                lab[lab == j] = i
    ids = [i for i in np.unique(lab) if i]
    return lab, ids


def prep(args):
    m = load()
    s = m.init(args.seed, (128, 128))
    rng = np.random.default_rng([99, args.seed])
    s = advance(m, s, int(args.t_prep / m.P["dt"]), noise=args.noise, rng=rng)
    lab, ids = bodies(s)
    areas = {i: int((lab == i).sum()) for i in ids}
    med = np.median(list(areas.values()))
    target = min(ids, key=lambda i: abs(areas[i] - med))
    tm = lab == target
    cy, cx = ndimage.center_of_mass(tm)
    edge = tm & ~ndimage.binary_erosion(tm)
    ey, ex = np.argwhere(edge)[0]
    other = [i for i in ids if i != target]
    oc = ndimage.center_of_mass(lab == max(other, key=lambda i: areas[i]))
    far = ndimage.distance_transform_edt(np.tile(lab == 0, (3, 3)))[128:256, 128:256]
    by, bx = np.unravel_index(np.argmax(far), far.shape)
    sites = dict(centre=[float(cy), float(cx)], rim=[float(ey), float(ex)], bath=[float(by), float(bx)],
                 other=[float(oc[0]), float(oc[1])])
    OUT.mkdir(exist_ok=True)
    np.savez(OUT / f"prep_s{args.seed}.npz", **{f: s[f] for f in FIELDS})
    info = dict(seed=args.seed, t_prep=args.t_prep, noise=args.noise, n_bodies=len(ids),
                target_area=areas[target], median_area=float(med), sites=sites)
    (OUT / f"prep_s{args.seed}.json").write_text(json.dumps(info, indent=1))
    print(json.dumps(info))


def load_prep(seed):
    z = np.load(OUT / f"prep_s{seed}.npz")
    info = json.loads((OUT / f"prep_s{seed}.json").read_text())
    return {f: z[f].copy() for f in FIELDS}, info


def body_at(lab, y, x, r=3):
    H, W = lab.shape
    ys = (np.arange(int(y) - r, int(y) + r + 1)) % H
    xs = (np.arange(int(x) - r, int(x) + r + 1)) % W
    v = lab[np.ix_(ys, xs)]
    v = v[v > 0]
    return int(np.bincount(v).argmax()) if v.size else 0


def pulse(args):
    m = load()
    s0, info = load_prep(args.seed)
    sites = info["sites"]
    twin = copy.deepcopy(s0)
    marks = [100, 300, 1000]
    tw = {}
    t = 0
    for mk in marks:
        twin = advance(m, twin, mk - t, t0=t)
        t = mk
        tw[mk] = copy.deepcopy(twin)
    lab0, _ = bodies(s0)
    tgt = body_at(lab0, *sites["centre"])
    tmask = ndimage.binary_dilation(lab0 == tgt, iterations=4)
    rows = []
    for field in FIELDS:
        for site in ("bath", "centre", "rim"):
            for amp in (0.3, 1.0, 3.0):
                for sig in (2.0, 4.0):
                    y, x = sites[site]
                    inj = dict(field=field, y=y, x=x, amp=amp, sig=sig, start=0, dur=args.dur)
                    s = copy.deepcopy(s0)
                    t = 0
                    row = dict(field=field, site=site, amp=amp, sig=sig, dur=args.dur)
                    for mk in marks:
                        s = advance(m, s, mk - t, inj=inj, t0=t)
                        t = mk
                        lab, ids = bodies(s)
                        labt, idst = bodies(tw[mk])
                        d = np.sqrt(sum(((s[f] - tw[mk][f]) ** 2).sum() for f in FIELDS))
                        dphi = np.abs(s["phi"] - tw[mk]["phi"]) > 0.25
                        n_in = len(set(np.unique(lab[tmask])) - {0})
                        n_in_t = len(set(np.unique(labt[tmask])) - {0})
                        site_body = body_at(lab, y, x, r=2) > 0
                        site_body_t = body_at(labt, y, x, r=2) > 0
                        row[f"t{mk}"] = dict(cells=len(ids), cells_twin=len(idst), diff_l2=round(float(d), 3),
                                             changed_px=int(dphi.sum()), target_parts=n_in,
                                             target_parts_twin=n_in_t, body_at_site=bool(site_body),
                                             body_at_site_twin=bool(site_body_t))
                    rows.append(row)
                    print(json.dumps(row), flush=True)
    (OUT / f"pulse_s{args.seed}_dur{args.dur:g}.json").write_text(json.dumps(rows, indent=1))


def lattice(kind, spacing):
    if kind == "square":  # 13 nodes, L1 shells 0..2
        p = [(iy, ix) for iy in range(-2, 3) for ix in range(-2, 3) if abs(iy) + abs(ix) <= 2]
        return np.array(p, float) * spacing
    v1, v2 = np.array([0.0, 1.0]), np.array([np.sqrt(3) / 2, 0.5])
    p = [a * v1 + b * v2 for a in range(-2, 3) for b in range(-2, 3) if max(abs(a), abs(b), abs(a + b)) <= 2]
    return np.array(p, float) * spacing


def readout(s, devs):
    F = np.stack([s[f] for f in FIELDS])
    N = F.shape[-1]
    out = []
    for c, offs in devs:
        pos = (np.array(c)[None, :] + offs) % N
        out.append(np.stack([ndimage.map_coordinates(F[i], pos.T, order=1, mode="grid-wrap")
                             for i in range(len(FIELDS))]))
    g = np.concatenate([F.mean(axis=(1, 2)), F.var(axis=(1, 2))])
    return np.concatenate([o.ravel() for o in out] + [g])


def run_members(m, s0, members, noise, window, every, devs, seed_base, inj=None):
    R = []
    for k in range(members):
        rng = np.random.default_rng([seed_base, k])
        s = copy.deepcopy(s0)
        t = 0
        rows = []
        while t < window:
            s = advance(m, s, every, noise=noise, rng=rng, inj=inj, t0=t)
            t += every
            rows.append(readout(s, devs))
        R.append(np.stack(rows))
    return np.stack(R)  # (members, times, features)


def energy_score(F, y):
    """F (m, d) forecast members, y (d,) truth; ES = E|X-y| - 0.5 E|X-X'|."""
    a = np.linalg.norm(F - y[None], axis=1).mean()
    b = np.linalg.norm(F[:, None] - F[None], axis=2).mean()
    return a - 0.5 * b


def detect(args):
    s0, info = load_prep(args.seed)
    sites = info["sites"]
    devs = [(sites["centre"], lattice("square", 3.0 * args.scale)), (sites["other"], lattice("hex", 6.0 * args.scale))]
    arms = {"native": {}, "chi0": {"chi": 0.0}, "gate0": {"gate": 0, "gateK": 0}, "a_half": {"a": 2.0}}
    inj = None
    if args.inject:
        y, x = sites["centre"]
        inj = dict(field=args.inject, y=y, x=x, amp=args.amp, sig=2.0, start=0, dur=args.dur)
    E = {}
    for name, ov in arms.items():
        m = load(ov)
        E[name] = run_members(m, s0, args.members, args.noise, args.window, args.every, devs,
                              seed_base=SEEDS[name], inj=inj)
        print(name, E[name].shape, flush=True)
    # truth members: a second native ensemble with different noise seeds
    mN = load()
    T = run_members(mN, s0, args.members, args.noise, args.window, args.every, devs, seed_base=55, inj=inj)
    scale = E["native"].reshape(-1, E["native"].shape[-1]).std(axis=0) + 1e-6
    res = {}
    for name in arms:
        for frac in (0.1, 0.3, 1.0):
            nt = max(1, int(round(frac * T.shape[1])))
            Fz = (E["native"][:, :nt] / scale).reshape(args.members, -1)
            truth = (T[:, :nt] / scale).reshape(args.members, -1) if name == "native" else \
                    (E[name][:, :nt] / scale).reshape(args.members, -1)
            es = np.mean([energy_score(Fz, y) for y in truth])
            res[f"{name}@{frac}"] = round(float(es), 3)
    spread = float(np.linalg.norm((E["native"] - E["native"].mean(0)) / scale, axis=2).mean())
    res["native_member_spread"] = round(spread, 3)
    print(json.dumps(res))
    tag = f"detect_s{args.seed}_n{args.noise:g}_w{args.window}" + (f"_inj{args.inject}" if args.inject else "")
    (OUT / f"{tag}.json").write_text(json.dumps(dict(args=vars(args), res=res), indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["prep", "pulse", "detect"])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--t-prep", type=float, default=4000)
    ap.add_argument("--noise", type=float, default=0.0)
    ap.add_argument("--dur", type=float, default=20)
    ap.add_argument("--members", type=int, default=8)
    ap.add_argument("--window", type=int, default=1000)
    ap.add_argument("--every", type=int, default=25)
    ap.add_argument("--scale", type=float, default=2.0, help="px per PhySim world unit")
    ap.add_argument("--inject", default=None)
    ap.add_argument("--amp", type=float, default=1.0)
    a = ap.parse_args()
    dict(prep=prep, pulse=pulse, detect=detect)[a.cmd](a)
