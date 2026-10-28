"""Eval-readiness pilot: PhySim-style apparatus on c53's fed vortices (adapted from ../apparatus.py).

  prep     run the native world from its own init (seed) to t_prep and save the full prepared state
  pulse    Gaussian source amp*exp(-r^2/2 sig^2) per time unit (sig = 2 world units) into om or Y for dur t at a
           body centre / body rim / empty site; compare with the uninjected twin (no noise)
  detect   8-member ensembles from the prepared state under dynamics noise; native vs its deciding ablations
           (adv 0 = no-advection twin, fork = fuel emptied + regrowth off at window start) and a numerical null
           (dt halved); probe arrays like PhySim's devices plus the global sensor; energy scores

Scale: 1 PhySim world unit = 1 px (the world's own dx); world size 128 x 128 units.
State fields (ports): om (signed vorticity), Y (fuel). Velocity and streamfunction are derived from om.
"""
import argparse, copy, importlib.util, json, os, sys, time
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import ops

ops.WORKERS = 1
WORLD = "/home/user/physim/research/alife/collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py"
OUT = Path(__file__).resolve().parent / "out"
FIELDS = ["om", "Y"]
SIZE = (128, 128)
THR, MINA = 0.06, 6          # the world's META threshold on |om|; labkit's default min area at 128^2
INJ_SIG = 2.0
SEEDS = {"native": 7, "adv0": 11, "fork": 13, "dthalf": 17, "kF0": 19}
ARMS = {"native": {}, "adv0": {"adv": 0.0}, "fork": {"fork": True}, "dthalf": {"dt": 0.01}, "kF0": {"kF": 0.0}}


def load(overrides=None):
    os.environ["WORLD_P"] = "{}"
    spec = importlib.util.spec_from_file_location("fvw", WORLD)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.P.update(overrides or {})
    return m


def rebuild(m, s0):
    """fresh state with m's parameters (operators, par) carrying s0's om, Y, t"""
    s = m.init(0, SIZE)
    for k in ("om", "Y", "t", "eat"):
        s[k] = copy.deepcopy(s0[k])
    return s


def bump_at(y, x, sig=INJ_SIG):
    H, W = SIZE
    c = np.arange(H) + 0.0
    dy = (c - y + H / 2) % H - H / 2
    dx = (np.arange(W) - x + W / 2) % W - W / 2
    return np.exp(-(dy[:, None] ** 2 + dx[None, :] ** 2) / (2 * sig ** 2))


def noise_kick(s, noise, rng, form):
    a = noise * np.sqrt(s["par"]["dt"])
    if form in ("A", "B", "C"):
        s["om"] = s["om"] + a * rng.standard_normal(SIZE)
    if form == "A":
        s["Y"] = s["Y"] + a * rng.standard_normal(SIZE)
    if form == "B":
        s["Y"] = s["Y"] * (1 + a * rng.standard_normal(SIZE))


def advance_time(m, s, T, noise=0.0, rng=None, form="B", inj=None, t_rel0=0.0, hook=None, hook_every=None):
    """advance by T time units; inj = dict(field, bump, amp, start, dur) in window-relative time"""
    dt = s["par"]["dt"]
    n = int(round(T / dt))
    for k in range(n):
        tr = t_rel0 + k * dt
        if inj is not None and inj["start"] - 1e-9 <= tr < inj["start"] + inj["dur"] - 1e-9:
            s[inj["field"]] = s[inj["field"]] + inj["amp"] * dt * inj["bump"]
        if noise > 0:
            noise_kick(s, noise, rng, form)
        s = m.step(s)
        if hook is not None and (k + 1) % hook_every == 0:
            hook(s, t_rel0 + (k + 1) * dt)
    return s


def label_periodic(mask):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    parent = list(range(n + 1))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    H, W = mask.shape
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for sh in (-1, 0, 1):
            bb = np.roll(b, sh)
            for i, j in zip(a, bb):
                if i and j:
                    ri, rj = find(i), find(j)
                    if ri != rj:
                        parent[rj] = ri
    roots = np.array([find(i) for i in range(n + 1)])
    lab = roots[lab]
    ids, cnt = np.unique(lab[lab > 0], return_counts=True)
    keep = ids[cnt >= MINA]
    lab = np.where(np.isin(lab, keep), lab, 0)
    return lab, list(keep)


def circ_centroid(mask):
    H, W = mask.shape
    yy, xx = np.nonzero(mask)
    ay, ax = 2 * np.pi * yy / H, 2 * np.pi * xx / W
    cy = (np.arctan2(np.sin(ay).mean(), np.cos(ay).mean()) / (2 * np.pi) * H) % H
    cx = (np.arctan2(np.sin(ax).mean(), np.cos(ax).mean()) / (2 * np.pi) * W) % W
    return float(cy), float(cx)


def bodies(om):
    lab, ids = label_periodic(np.abs(om) > THR)
    info = {}
    for i in ids:
        mk = lab == i
        info[int(i)] = dict(area=int(mk.sum()), sign=int(np.sign(om[mk].sum())), c=circ_centroid(mk),
                            peak=float(np.abs(om[mk]).max()))
    return lab, info


def pdist(y, x, H=128, W=128):
    yy, xx = np.mgrid[0:H, 0:W]
    dy = (yy - y + H / 2) % H - H / 2
    dx = (xx - x + W / 2) % W - W / 2
    return np.sqrt(dy ** 2 + dx ** 2)


def prep(args):
    m = load()
    s = m.init(args.seed, SIZE)
    s = advance_time(m, s, args.t_prep)
    lab, info = bodies(s["om"])
    areas = np.array([v["area"] for v in info.values()])
    med = float(np.median(areas))
    sites = {}
    for sg, tag in ((1, "p"), (-1, "n")):
        cand = [i for i, v in info.items() if v["sign"] == sg]
        tgt = min(cand, key=lambda i: abs(info[i]["area"] - med))
        mk = lab == tgt
        cy, cx = info[tgt]["c"]
        edge = mk & ~ndimage.binary_erosion(mk)
        ey, ex = np.nonzero(edge)
        dyy = (ey - cy + 64) % 128 - 64
        dxx = (ex - cx + 64) % 128 - 64
        j = int(np.argmax(dxx - 2 * np.abs(dyy)))    # edge pixel in the +x direction from the centroid
        sites[f"centre_{tag}"] = [cy, cx]
        sites[f"rim_{tag}"] = [float(ey[j]), float(ex[j])]
        sites[f"target_{tag}"] = int(tgt)
    other = max([i for i in info if i not in (sites["target_p"], sites["target_n"])], key=lambda i: info[i]["area"])
    sites["other"] = list(info[other]["c"])
    far = ndimage.distance_transform_edt(np.tile(lab == 0, (3, 3)))[128:256, 128:256]
    by, bx = np.unravel_index(np.argmax(far), far.shape)
    sites["empty"] = [float(by), float(bx)]
    OUT.mkdir(exist_ok=True)
    np.savez(OUT / f"prep_s{args.seed}.npz", om=s["om"], Y=s["Y"], eat=s["eat"], t=s["t"])
    uy, ux = m._vel(s)
    pk = {k: info[sites[f"target_{k}"]] for k in ("p", "n")}
    out = dict(seed=args.seed, t_prep=args.t_prep, t_state=s["t"], n_bodies=len(info), median_area=med,
               n_pos=sum(v["sign"] > 0 for v in info.values()), sites=sites, targets=pk,
               empty_dist_to_body=float(far.max()), om_peak_median=float(np.median([v["peak"] for v in info.values()])),
               Y_mean=float(s["Y"].mean()), Y_min=float(s["Y"].min()), Y_at={k: float(s["Y"][int(v[0]) % 128, int(v[1]) % 128])
                                                                          for k, v in sites.items() if isinstance(v, list)},
               u_max=float(np.sqrt(uy ** 2 + ux ** 2).max()), om_mean=float(s["om"].mean()))
    (OUT / f"prep_s{args.seed}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out))


def load_prep(m, seed):
    z = np.load(OUT / f"prep_s{seed}.npz")
    info = json.loads((OUT / f"prep_s{seed}.json").read_text())
    s0 = {"om": z["om"].copy(), "Y": z["Y"].copy(), "eat": z["eat"].copy(), "t": float(z["t"])}
    return rebuild(m, s0), info


class Tracker:
    """follows a same-sign descendant set of one body by mask overlap (checked every 2 t)"""

    def __init__(self, mask, sign):
        self.mask, self.sign, self.n, self.died = mask, sign, 1, None
        self.hist = []

    def update(self, om, t, li=None):
        if self.n == 0:
            self.hist.append((t, 0)); return
        lab, info = li if li is not None else bodies(om)
        grown = ndimage.binary_dilation(self.mask, iterations=1)
        ids = [i for i in np.unique(lab[grown]) if i and info[int(i)]["sign"] == self.sign]
        self.n = len(ids)
        self.mask = np.isin(lab, ids)
        if self.n == 0 and self.died is None:
            self.died = t
        self.hist.append((round(t, 2), self.n))


def pulse(args):
    m = load()
    s0, info = load_prep(m, args.seed)
    sites = info["sites"]
    lab0, inf0 = bodies(s0["om"])
    marks = [20, 50, 100, 200]
    every = int(round(2.0 / m.P["dt"]))
    fields = args.fields.split(",")

    def make_trackers(s):
        tr = {}
        for tag in ("p", "n"):
            tid = sites[f"target_{tag}"]
            tr[tag] = Tracker(lab0 == tid, inf0[tid]["sign"])
        return tr

    # uninjected twin, with snapshots and target tracking
    twin = copy.deepcopy(s0)
    ttw = make_trackers(twin)
    tw = {}
    t = 0.0
    for mk in marks:
        twin = advance_time(m, twin, mk - t, t_rel0=t, hook=lambda s, tt: [x.update(s["om"], tt, li) for li in [bodies(s["om"])]
                                                                           for x in ttw.values()], hook_every=every)
        t = mk
        tw[mk] = copy.deepcopy(twin)
    twin_track = {k: v.hist for k, v in ttw.items()}
    cases = []
    for f in fields:
        sl = ("centre_p", "rim_p", "centre_n", "rim_n", "empty") if f == "om" else ("centre_p", "rim_p", "empty")
        for site in sl:
            for amp in [float(a) for a in args.amps.split(",")]:
                cases.append((f, site, amp))
    if args.chaos:
        cases.append(("om", "empty", 1e-6))
    rows = []
    for f, site, amp in cases:
        y, x = sites[site]
        bump = bump_at(y, x)
        inj = dict(field=f, bump=bump, amp=amp, start=0.0, dur=args.dur)
        s = copy.deepcopy(s0)
        trk = make_trackers(s)
        new_tr = {}
        R = pdist(y, x)
        row = dict(field=f, site=site, amp=amp, dur=args.dur, peak_added=amp * args.dur)
        t = 0.0
        blow = None
        t_start = time.time()
        for mk in marks:
            def hook(ss, tt):
                li = bodies(ss["om"])
                for v in trk.values():
                    v.update(ss["om"], tt, li)
                if "new" in new_tr:
                    new_tr["new"].update(ss["om"], tt, li)
            with np.errstate(all="ignore"):
                s = advance_time(m, s, mk - t, inj=inj, t_rel0=t, hook=hook, hook_every=every)
            t = mk
            fin = bool(np.isfinite(s["om"]).all() and np.isfinite(s["Y"]).all())
            if not fin:
                blow = mk
                row[f"t{mk}"] = dict(finite=False)
                break
            lab, inf = bodies(s["om"])
            labt, inft = bodies(tw[mk]["om"])
            dom = s["om"] - tw[mk]["om"]
            dY = s["Y"] - tw[mk]["Y"]
            e2 = dom ** 2
            order = np.argsort(R.ravel())
            cum = np.cumsum(e2.ravel()[order])
            r90 = float(R.ravel()[order][np.searchsorted(cum, 0.9 * cum[-1])]) if cum[-1] > 0 else 0.0
            ch = np.abs(dom) > 0.03
            # bodies of the twin touched by a difference above half the body threshold
            touched = len(set(np.unique(labt[ch])) - {0})
            uy, ux = m._vel(s)
            site_body = lab[int(round(y)) % 128, int(round(x)) % 128]
            site_body_t = labt[int(round(y)) % 128, int(round(x)) % 128]
            if site == "empty" and mk == marks[0] and site_body and not site_body_t:
                new_tr["new"] = Tracker(lab == site_body, inf[int(site_body)]["sign"])
            d = dict(finite=True, bodies=len(inf), bodies_twin=len(inft), diff_l2_om=float(np.sqrt(e2.sum())),
                     diff_l2_Y=float(np.sqrt((dY ** 2).sum())), r90=r90, changed_px=int(ch.sum()),
                     max_changed_dist=float(R[ch].max()) if ch.any() else 0.0, twin_bodies_touched=touched,
                     om_max=float(np.abs(s["om"]).max()), u_max=float(np.sqrt(uy ** 2 + ux ** 2).max()),
                     Y_max=float(s["Y"].max()), body_at_site=bool(site_body), body_at_site_twin=bool(site_body_t),
                     om_site=float(s["om"][int(round(y)) % 128, int(round(x)) % 128]),
                     om_site_twin=float(tw[mk]["om"][int(round(y)) % 128, int(round(x)) % 128]),
                     Y_site=float(s["Y"][int(round(y)) % 128, int(round(x)) % 128]))
            for tag, v in trk.items():
                d[f"target_{tag}_n"] = v.n
                d[f"target_{tag}_n_twin"] = dict(twin_track[tag]).get(round(float(mk), 2))
            if "new" in new_tr:
                d["new_body_n"] = new_tr["new"].n
            row[f"t{mk}"] = d
        row["blowup_at"] = blow
        row["target_died_at"] = {k: v.died for k, v in trk.items()}
        row["target_died_at_twin"] = {k: ttw[k].died for k in ttw}
        row["target_max_parts"] = {k: max([n for _, n in v.hist] or [0]) for k, v in trk.items()}
        row["target_max_parts_twin"] = {k: max([n for _, n in ttw[k].hist] or [0]) for k in ttw}
        row["target_parts_hist"] = {k: v.hist[::5] for k, v in trk.items()}
        if "new" in new_tr:
            row["new_body_died_at"] = new_tr["new"].died
            row["new_body_hist"] = new_tr["new"].hist[::5]
        row["wall_s"] = round(time.time() - t_start, 1)
        rows.append(row)
        print(json.dumps({k: row[k] for k in row if k not in ("target_parts_hist", "new_body_hist")}), flush=True)
    tag = f"pulse_s{args.seed}_dur{args.dur:g}_{args.fields.replace(',', '')}"
    (OUT / f"{tag}.json").write_text(json.dumps(dict(twin_track=twin_track, rows=rows), indent=1))


def lattice(kind, spacing):
    if kind == "square":  # 13 nodes, L1 shells 0..2
        p = [(iy, ix) for iy in range(-2, 3) for ix in range(-2, 3) if abs(iy) + abs(ix) <= 2]
        return np.array(p, float) * spacing
    v1, v2 = np.array([0.0, 1.0]), np.array([np.sqrt(3) / 2, 0.5])
    p = [a * v1 + b * v2 for a in range(-2, 3) for b in range(-2, 3) if max(abs(a), abs(b), abs(a + b)) <= 2]
    return np.array(p, float) * spacing


def readout(s, devs):
    """PhySim convention: node world position p -> grid coordinate p/dx - 0.5 (cell centres at (i+0.5)dx);
    here a node placed at a pixel's index i reads that pixel, so the device centre is given in pixel indices."""
    F = np.stack([s[f] for f in FIELDS])
    out = []
    for c, offs in devs:
        pos = (np.array(c)[None, :] + offs) % SIZE[0]
        out.append(np.stack([ndimage.map_coordinates(F[i], pos.T, order=1, mode="grid-wrap") for i in range(len(FIELDS))]))
    g = np.concatenate([F.mean(axis=(1, 2)), F.var(axis=(1, 2))])
    return np.concatenate([o.ravel() for o in out] + [g])


def arm_module(name):
    ov = dict(ARMS[name])
    fork = ov.pop("fork", False)
    m = load(ov)
    return m, fork


def run_members(name, s0_raw, members, noise, form, window, every, devs, seed_base, inj=None):
    m, fork = arm_module(name)
    R = []
    for k in range(members):
        rng = np.random.default_rng([seed_base, k])
        s = rebuild(m, s0_raw)
        if fork:
            s["par"]["fork_t"] = s["t"]          # world's own switch: fuel emptied at the first step, regrowth off
        t = 0.0
        rows = []
        while t < window - 1e-9:
            with np.errstate(all="ignore"):
                s = advance_time(m, s, every, noise=noise, rng=rng, form=form, inj=inj, t_rel0=t)
            t += every
            rows.append(readout(s, devs))
        R.append(np.stack(rows))
    return np.stack(R)  # (members, times, features)


def energy_score(F, y):
    a = np.linalg.norm(F - y[None], axis=1).mean()
    b = np.linalg.norm(F[:, None] - F[None], axis=2).mean()
    return a - 0.5 * b


def detect_run(args):
    """run one arm's ensemble (so arms can go to separate processes) and save raw readouts"""
    z = np.load(OUT / f"prep_s{args.seed}.npz")
    info = json.loads((OUT / f"prep_s{args.seed}.json").read_text())
    s0_raw = {"om": z["om"], "Y": z["Y"], "eat": z["eat"], "t": float(z["t"])}
    sites = info["sites"]
    devs = [(sites["centre_p"], lattice("square", 3.0 * args.scale)), (sites["other"], lattice("hex", 6.0 * args.scale))]
    name = args.arm
    sb = SEEDS[name.replace("truth", "native")] if name != "truth" else 55
    base = "native" if name == "truth" else name
    t0 = time.time()
    E = run_members(base, s0_raw, args.members, args.noise, args.form, args.window, args.every, devs, seed_base=sb)
    tag = f"ens_s{args.seed}_{args.form}{args.noise:g}_{name}"
    np.save(OUT / f"{tag}.npy", E)
    print(name, E.shape, f"{time.time() - t0:.0f}s", "finite", bool(np.isfinite(E).all()), flush=True)


def detect_score(args):
    tagb = f"ens_s{args.seed}_{args.form}{args.noise:g}_"
    E = {n: np.load(OUT / f"{tagb}{n}.npy") for n in ["native", "truth"] + args.arms.split(",")}
    nat, T = E["native"], E["truth"]
    nm, nt_all, nf = nat.shape
    scale = nat.reshape(-1, nf).std(axis=0) + 1e-6
    # feature groups: dev0 (2 fields x 13), dev1 (2 x 19), global (4)
    groups = {"all": np.arange(nf), "dev0": np.arange(0, 26), "dev1": np.arange(26, 64), "global": np.arange(64, 68)}
    res = {}
    for win in [float(w) for w in args.windows.split(",")]:
        nt = int(round(win / args.every))
        for gname, gi in groups.items():
            Fz = (nat[:, :nt][:, :, gi] / scale[gi]).reshape(nm, -1)
            base = np.mean([energy_score(Fz, y) for y in (T[:, :nt][:, :, gi] / scale[gi]).reshape(nm, -1)])
            r = {"native_vs_native": round(float(base), 3)}
            for a in args.arms.split(","):
                Az = (E[a][:, :nt][:, :, gi] / scale[gi]).reshape(nm, -1)
                Az = np.where(np.isfinite(Az), Az, 1e6)
                es = np.mean([energy_score(Fz, y) for y in Az])
                r[a] = round(float(es), 3)
                r[f"ratio_{a}"] = round(float(es / base), 2)
            res[f"w{win:g}_{gname}"] = r
    # member spread over time (native, standardized, all features), and truth-vs-native at single times
    spread = np.linalg.norm((nat - nat.mean(0)) / scale, axis=2).mean(0)
    res["native_spread_t"] = {f"{(i + 1) * args.every:g}": round(float(spread[i]), 2) for i in range(0, nt_all, max(1, nt_all // 10))}
    print(json.dumps(res, indent=1))
    (OUT / f"detect_s{args.seed}_{args.form}{args.noise:g}.json").write_text(json.dumps(dict(args=vars(args), res=res), indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["prep", "pulse", "detect_run", "detect_score"])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--t-prep", type=float, default=500)
    ap.add_argument("--noise", type=float, default=0.0)
    ap.add_argument("--form", default="B")
    ap.add_argument("--dur", type=float, default=20)
    ap.add_argument("--fields", default="om,Y")
    ap.add_argument("--amps", default="0.003,0.03,0.3,3")
    ap.add_argument("--chaos", action="store_true")
    ap.add_argument("--members", type=int, default=8)
    ap.add_argument("--window", type=float, default=300)
    ap.add_argument("--windows", default="30,100,300")
    ap.add_argument("--every", type=float, default=2.0)
    ap.add_argument("--scale", type=float, default=1.0, help="px per PhySim world unit")
    ap.add_argument("--arm", default="native")
    ap.add_argument("--arms", default="adv0,fork,dthalf")
    a = ap.parse_args()
    dict(prep=prep, pulse=pulse, detect_run=detect_run, detect_score=detect_score)[a.cmd](a)
