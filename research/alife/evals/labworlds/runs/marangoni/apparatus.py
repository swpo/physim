"""Eval-readiness pilot, world 2: PhySim-style apparatus on c34's Marangoni rods.

  prep     run the native world from noise to t_prep (noise-free) and save the prepared state + sites
  pulse    Gaussian source (rate amp per time unit, width sig px, duration dur) into one field at a
           body-centre / body-rim / empty-space site; compare with the uninjected (noise-free) twin
  detect   8-member ensembles from the prepared state under dynamics noise, for a list of arms
           (native world or a deciding ablation); probe arrays like PhySim's devices + global sensor;
           raw readouts saved per arm
  score    energy scores: native forecast vs native truth and vs each ablation, at several windows
World units = grid units (dx = 1): probe spacing 3 / 6 units = 3 / 6 px, injection width 2 px.
"""
import argparse, copy, importlib.util, json, os, time
from pathlib import Path

import numpy as np
from scipy import ndimage

D = Path(__file__).resolve().parent
OUT = D / "out"
BASE = "/home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py"
STATE = ["phi", "q1", "q2", "s", "c"]
OBS = ["phi", "q1", "q2", "s", "c", "vx", "vy"]  # every node reads these (v is derived but observable)
ARMS = {"native": {}, "truth": {}, "passive": {"zeta": 0.0, "mar": 0.0}, "mar0": {"mar": 0.0},
        "kappa0": {"kappa": 0.0}, "zeta0": {"zeta": 0.0}}
ARM_SEED = {"native": 7, "truth": 55, "passive": 11, "mar0": 13, "kappa0": 17, "zeta0": 19}
NOISE_FORMS = {"plain": dict(nfields=STATE, mult=[], cons=[]),
               "phys": dict(nfields=["q1", "q2"], mult=["s", "c"], cons=["phi"])}


def load(overrides=None):
    os.environ["WORLD_P"] = json.dumps(overrides or {})
    spec = importlib.util.spec_from_file_location("mgw", BASE)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    os.environ.pop("WORLD_P", None)
    return m


def noiser():
    spec = importlib.util.spec_from_file_location("mgn", D / "mg_noise.py")
    n = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(n)
    return n


def gauss(shape, y, x, sig):
    H, W = shape
    yy, xx = np.mgrid[0:H, 0:W]
    dy = (yy - y + H / 2) % H - H / 2
    dx = (xx - x + W / 2) % W - W / 2
    return np.exp(-(dy ** 2 + dx ** 2) / (2 * sig ** 2))


def pdist(shape, y, x):
    H, W = shape
    yy, xx = np.mgrid[0:H, 0:W]
    dy = (yy - y + H / 2) % H - H / 2
    dx = (xx - x + W / 2) % W - W / 2
    return np.hypot(dy, dx)


def advance(m, s, n, noise=0.0, form="phys", rng=None, inj=None, t0=0, NZ=None, hook=None, hook_every=50):
    """n steps from step index t0; inj = dict(field, y, x, amp, sig, start, dur): source amp*gauss per time."""
    dt = m.P["dt"]
    bump = gauss(s["phi"].shape, inj["y"], inj["x"], inj["sig"]) if inj is not None else None
    for k in range(n):
        t = (t0 + k) * dt
        if inj is not None and inj["start"] <= t < inj["start"] + inj["dur"]:
            s[inj["field"]] = s[inj["field"]] + inj["amp"] * dt * bump
        if noise > 0:
            s = NZ.add_noise(s, noise, rng, **NOISE_FORMS[form])
        s = m.step(s)
        if hook is not None and (t0 + k + 1) % hook_every == 0:
            if hook(s, t0 + k + 1) is False:
                break
    return s


def bodies(phi, min_area=6):
    lab, n = ndimage.label(phi > 0, structure=np.ones((3, 3)))
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):  # periodic merge
        for i, j in zip(a, b):
            if i and j and i != j:
                lab[lab == j] = i
    ids = [i for i in np.unique(lab) if i]
    small = [i for i in ids if (lab == i).sum() < min_area]
    for i in small:
        lab[lab == i] = 0
    return lab, [i for i in ids if i not in small]


def deepest(mask):
    t = np.tile(mask, (3, 3))
    dt = ndimage.distance_transform_edt(t)[mask.shape[0]:2 * mask.shape[0], mask.shape[1]:2 * mask.shape[1]]
    return np.unravel_index(np.argmax(dt * mask), mask.shape), dt


def prep(args):
    m = load()
    s = m.init(args.seed, (args.size, args.size))
    if args.resite:  # recompute the sites from the saved prepared state (no new simulation)
        z = np.load(OUT / f"prep_s{args.seed}.npz")
        for f in STATE:
            s[f] = z[f].copy()
    else:
        s = advance(m, s, int(round(args.t_prep / m.P["dt"])))
    lab, ids = bodies(s["phi"])
    areas = {i: int((lab == i).sum()) for i in ids}
    med = np.median(list(areas.values()))
    target = min(ids, key=lambda i: abs(areas[i] - med))
    tm = lab == target
    (cy, cx), dtm = deepest(tm)
    edge = tm & ~ndimage.binary_erosion(tm, border_value=1)
    dcen = pdist(tm.shape, cy, cx)
    ey, ex = np.argwhere(edge)[np.argmax([dcen[p[0], p[1]] for p in np.argwhere(edge)])]  # rim = rod tip
    other = max([i for i in ids if i != target], key=lambda i: areas[i])
    (oy, ox), _ = deepest(lab == other)
    far = ndimage.distance_transform_edt(np.tile(lab == 0, (3, 3)))[args.size:2 * args.size, args.size:2 * args.size]
    by, bx = np.unravel_index(np.argmax(far), far.shape)
    sites = dict(centre=[int(cy), int(cx)], rim=[int(ey), int(ex)], bath=[int(by), int(bx)], other=[int(oy), int(ox)])
    OUT.mkdir(exist_ok=True)
    np.savez(OUT / f"prep_s{args.seed}.npz", **{f: s[f] for f in STATE})
    inside = s["phi"] > 0
    lv = {f: dict(inside_mean=round(float(s[f][inside].mean()), 4), outside_mean=round(float(s[f][~inside].mean()), 4),
                  max=round(float(s[f].max()), 4), min=round(float(s[f].min()), 4)) for f in STATE}
    lv["|v|max"] = round(float(np.hypot(s["vx"], s["vy"]).max()), 4) if not args.resite else None
    info = dict(seed=args.seed, size=args.size, t_prep=args.t_prep, n_bodies=len(ids), target_area=areas[target],
                median_area=float(med), target_halfwidth=round(float(dtm.max()), 2),
                bath_dist_to_body=round(float(far.max()), 2), rim_dist_to_centre=round(float(dcen[ey, ex]), 2),
                sites=sites, levels=lv)
    (OUT / f"prep_s{args.seed}.json").write_text(json.dumps(info, indent=1))
    print(json.dumps(info))


def load_prep(m, seed, size):
    z = np.load(OUT / f"prep_s{seed}.npz")
    info = json.loads((OUT / f"prep_s{seed}.json").read_text())
    s = m.init(seed, (size, size))  # spectral grids etc.
    for f in STATE:
        s[f] = z[f].copy()
    return s, info


class Follow:
    """Follow the descendants of one body: every check, the bodies overlapping the 1-px dilation of the
    previous descendant mask."""

    def __init__(self, mask):
        self.mask = mask.copy()
        self.n = 1
        self.maxn = 1
        self.events = []

    def update(self, phi, t):
        lab, ids = bodies(phi)
        grow = ndimage.binary_dilation(self.mask, iterations=1)
        hit = set(np.unique(lab[grow])) - {0}
        n = len(hit)
        if n != self.n:
            self.events.append((round(t, 2), self.n, n))
        self.n = n
        self.maxn = max(self.maxn, n)
        self.mask = np.isin(lab, list(hit)) if hit else np.zeros_like(self.mask)
        return lab, ids


def pulse(args):
    m = load()
    s0, info = load_prep(m, args.seed, args.size)
    sites = info["sites"]
    dt = m.P["dt"]
    marks = [int(round(t / dt)) for t in args.marks]
    every = 50
    lab0, _ = bodies(s0["phi"])
    tgt = lab0[tuple(sites["centre"])]
    # twin
    twin = copy.deepcopy(s0)
    tw, twf = {}, Follow(lab0 == tgt)
    tw_n = {}
    t = 0
    for mk in marks:
        twin = advance(m, twin, mk - t, t0=t, hook=lambda st, k: twf.update(st["phi"], k * dt) and None)
        t = mk
        tw[mk] = {f: twin[f].copy() for f in OBS}
        tw_n[mk] = (twf.n, twf.maxn, list(twf.events))
    scale = {f: float(s0[f].std()) + 1e-9 for f in STATE}
    cases = []
    for field in args.fields:
        for site in args.sites:
            for amp in args.amps:
                cases.append((field, site, amp))
    if args.extra:
        cases += [("phi", "centre", 1e-4), ("vx", "centre", 3.0)]
    if args.cases:
        cases = [(c.split(":")[0], c.split(":")[1], float(c.split(":")[2])) for c in args.cases]
    rows = []
    for field, site, amp in cases:
        t_start = time.time()
        y, x = sites[site]
        inj = dict(field=field, y=y, x=x, amp=amp, sig=args.sig, start=0, dur=args.dur)
        s = copy.deepcopy(s0)
        fol = Follow(lab0 == tgt)
        st = dict(blow=None, vmax=0.0)

        def hook(ss, k):
            fin = np.isfinite(ss["phi"]).all() and np.isfinite(ss["s"]).all() and np.isfinite(ss["q1"]).all()
            if not fin or np.abs(ss["phi"]).max() > args.blow_phi:
                st["blow"] = round(k * dt, 2)
                return False
            st["vmax"] = max(st["vmax"], float(np.hypot(ss["vx"], ss["vy"]).max()))
            fol.update(ss["phi"], k * dt)

        row = dict(field=field, site=site, amp=amp, sig=args.sig, dur=args.dur, blow_phi=args.blow_phi)
        t = 0
        dist = pdist(s0["phi"].shape, y, x)
        for mk in marks:
            if st["blow"] is None:
                s = advance(m, s, mk - t, inj=inj, t0=t, hook=hook)
            t = mk
            key = f"t{mk * dt:g}"
            if st["blow"] is not None:
                row[key] = dict(blowup_at=st["blow"])
                continue
            lab, ids = bodies(s["phi"])
            labt, idst = bodies(tw[mk]["phi"])
            dphi = np.abs(s["phi"] - tw[mk]["phi"])
            ch = dphi > 0.25
            rec = dict(bodies=len(ids), bodies_twin=len(idst), target_desc=fol.n, target_desc_twin=tw_n[mk][0],
                       target_maxdesc=fol.maxn, target_maxdesc_twin=tw_n[mk][1],
                       body_at_site=bool(lab[y, x] > 0), body_at_site_twin=bool(labt[y, x] > 0),
                       changed_px=int(ch.sum()), changed_rmax=round(float(dist[ch].max()), 1) if ch.any() else 0.0,
                       area=int((lab > 0).sum()), area_twin=int((labt > 0).sum()), vmax_so_far=round(st["vmax"], 3))
            for f in STATE:
                df = (s[f] - tw[mk][f]) ** 2
                tot = df.sum()
                if tot > 0:
                    order = np.argsort(dist.ravel())
                    cum = np.cumsum(df.ravel()[order]) / tot
                    r90 = float(dist.ravel()[order][np.searchsorted(cum, 0.9)])
                else:
                    r90 = 0.0
                rec[f"d_{f}"] = float(f"{np.sqrt(tot) / scale[f]:.3g}")
                rec[f"r90_{f}"] = round(r90, 1)
            rec["dmax_phi"] = round(float(dphi.max()), 3)
            row[key] = rec
        row["events"] = fol.events[:12]
        row["twin_events"] = tw_n[marks[-1]][2][:12]
        row["wall"] = round(time.time() - t_start, 1)
        rows.append(row)
        print(json.dumps(row), flush=True)
    tag = "_".join(args.fields) + (f"_{args.tag}" if args.tag else "")
    (OUT / f"pulse_s{args.seed}_{tag}.json").write_text(json.dumps(rows, indent=1))


def lattice(kind, spacing):
    if kind == "square":  # 13 nodes, L1 shells 0..2
        p = [(iy, ix) for iy in range(-2, 3) for ix in range(-2, 3) if abs(iy) + abs(ix) <= 2]
        return np.array(p, float) * spacing
    v1, v2 = np.array([0.0, 1.0]), np.array([np.sqrt(3) / 2, 0.5])
    p = [a * v1 + b * v2 for a in range(-2, 3) for b in range(-2, 3) if max(abs(a), abs(b), abs(a + b)) <= 2]
    return np.array(p, float) * spacing


def readout(s, devs):
    F = np.stack([s[f] for f in OBS])
    N = F.shape[-1]
    out = []
    for c, offs in devs:
        pos = (np.array(c, float)[None, :] + offs) % N
        out.append(np.stack([ndimage.map_coordinates(F[i], pos.T, order=1, mode="grid-wrap") for i in range(len(OBS))]))
    g = np.concatenate([F.mean(axis=(1, 2)), F.var(axis=(1, 2))])
    return np.concatenate([o.ravel() for o in out] + [g])


def detect(args):
    NZ = noiser()
    s_tmp = load()
    s0, info = load_prep(s_tmp, args.seed, args.size)
    sites = info["sites"]
    devs = [(sites["centre"], lattice("square", 3.0 * args.dil)), (sites["other"], lattice("hex", 6.0 * args.dil))]
    every = int(round(args.every / s_tmp.P["dt"]))
    nsteps = int(round(args.window / s_tmp.P["dt"]))
    for arm in args.arms:
        m = load(ARMS[arm])
        R = []
        t0 = time.time()
        for k in range(args.members):
            rng = np.random.default_rng([ARM_SEED[arm], k])
            s = copy.deepcopy(s0)
            rows = []
            t = 0
            while t < nsteps:
                s = advance(m, s, every, noise=args.noise, form=args.form, rng=rng, t0=t, NZ=NZ)
                t += every
                rows.append(readout(s, devs))
            R.append(np.stack(rows))
            print(arm, k, f"{time.time() - t0:.0f}s", "finite" if np.isfinite(R[-1]).all() else "NONFINITE", flush=True)
        tag = f"det_s{args.seed}_{args.form}{args.noise:g}_w{args.window:g}_{arm}"
        np.savez(OUT / f"{tag}.npz", R=np.stack(R), every=args.every, nodes0=len(devs[0][1]), nodes1=len(devs[1][1]),
                 obs=OBS)


def energy_score(F, y):
    a = np.linalg.norm(F - y[None], axis=1).mean()
    b = np.linalg.norm(F[:, None] - F[None], axis=2).mean()
    return a - 0.5 * b


def score(args):
    pre = f"det_s{args.seed}_{args.form}{args.noise:g}_w{args.window:g}_"
    E = {}
    for p in sorted(OUT.glob(pre + "*.npz")):
        z = np.load(p)
        E[p.stem[len(pre):]] = z["R"]
        n0, n1, nobs = int(z["nodes0"]), int(z["nodes1"]), len(z["obs"])
    nf = len(OBS)
    i0 = n0 * nobs
    i1 = i0 + n1 * nobs
    groups = {"all": slice(None), "device0": slice(0, i0), "device1": slice(i0, i1), "global": slice(i1, None)}
    for fi, fname in enumerate(OBS):  # one observed field, both devices + its global mean and variance
        idx = list(range(fi * n0, (fi + 1) * n0)) + list(range(i0 + fi * n1, i0 + (fi + 1) * n1)) + [i1 + fi, i1 + nobs + fi]
        groups[f"field:{fname}"] = np.array(idx)
    nat, tru = E["native"], E["truth"]
    Mm = nat.shape[0]
    scale = nat.reshape(-1, nat.shape[-1]).std(axis=0) + 1e-6
    res = {}
    T = nat.shape[1]
    for wl in args.windows:
        nt = max(1, int(round(wl / args.every)))
        for gname, sl in groups.items():
            Fz = (nat[:, :nt, sl] / scale[sl]).reshape(Mm, -1)
            base = np.mean([energy_score(Fz, y) for y in (tru[:, :nt, sl] / scale[sl]).reshape(Mm, -1)])
            for arm in E:
                if arm in ("native",):
                    continue
                es = np.mean([energy_score(Fz, y) for y in (E[arm][:, :nt, sl] / scale[sl]).reshape(Mm, -1)])
                res[f"{gname}|{arm}|w{wl:g}"] = dict(es=round(float(es), 3), ratio=round(float(es / base), 2))
    spread = float(np.linalg.norm((nat - nat.mean(0)) / scale, axis=2).mean())
    res["native_member_spread"] = round(spread, 3)
    out = OUT / f"score_s{args.seed}_{args.form}{args.noise:g}_w{args.window:g}.json"
    out.write_text(json.dumps(res, indent=1))
    for k, v in res.items():
        if k.startswith("all|") or k.startswith("global|") or k.startswith("device"):
            print(k, v)
    print("native member spread", res["native_member_spread"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["prep", "pulse", "detect", "score"])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--size", type=int, default=128)
    ap.add_argument("--t-prep", type=float, default=300)
    ap.add_argument("--fields", nargs="+", default=["phi", "q1", "s", "c"])
    ap.add_argument("--sites", nargs="+", default=["centre", "rim", "bath"])
    ap.add_argument("--amps", nargs="+", type=float, default=[0.03, 0.3, 3.0])
    ap.add_argument("--extra", action="store_true")
    ap.add_argument("--resite", action="store_true")
    ap.add_argument("--cases", nargs="+", default=None, help="field:site:amp")
    ap.add_argument("--blow-phi", type=float, default=50.0)
    ap.add_argument("--tag", default="")
    ap.add_argument("--sig", type=float, default=2.0)
    ap.add_argument("--dur", type=float, default=20)
    ap.add_argument("--marks", nargs="+", type=float, default=[20, 50, 100])
    ap.add_argument("--noise", type=float, default=0.0)
    ap.add_argument("--form", default="phys")
    ap.add_argument("--arms", nargs="+", default=["native", "truth"])
    ap.add_argument("--members", type=int, default=8)
    ap.add_argument("--window", type=float, default=200)
    ap.add_argument("--windows", nargs="+", type=float, default=[20, 60, 200])
    ap.add_argument("--every", type=float, default=2.0)
    ap.add_argument("--dil", type=float, default=1.0)
    a = ap.parse_args()
    dict(prep=prep, pulse=pulse, detect=detect, score=score)[a.cmd](a)
