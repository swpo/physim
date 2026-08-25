"""patch_lib.py — PoU patchworlds: map-aware fork of the l0 genome engine.

Partition-of-unity world composition on ONE grid:
    theta(x) = theta_A + rho_B(x) * (theta_B - theta_A),   rho_A + rho_B = 1.
The blend form is exact for the null test (theta_B == theta_A -> diff 0.0 -> map
is exactly constant).

Maps supported (each optional; everything else scalar, verbatim genome.py path):
  act params : lam, k1, u0, Du      (per act i)
  chan params: tau, Dch             (per chan c)
  wiring     : W[(c,a)], K[(i,c)]   (per entry)

Spatially-varying diffusion: D(x) = Dbase + dD(x), Dbase = min(map) handled
implicitly (exact FFT factor), dD(x) >= 0 handled explicitly in conservative
flux form  div(dD grad f)  (dt*max(dD)*4/dx^2 << 1 checked at run start).
Scalar-only case reproduces genome.run_genome ops 1:1 (bit-identity checked in P1).
"""
import os, sys, json, time
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
L0LIB = os.path.abspath(os.path.join(BASE, "..", "l0", "stage2", "lib"))
if L0LIB not in sys.path:
    sys.path.insert(0, L0LIB)
import genome as G

RESULTS = os.path.join(BASE, "results.json")


def log(rec):
    return G.append_result(rec, path=RESULTS)


# ------------------------------------------------------------- rho builders
def rho_band(N, dx, x_lo, x_hi, w):
    """rho_B(x,y): ~1 on the x-band [x_lo, x_hi], tanh ramps of width w.
    10-90%% ramp width = 2.197*w. Periodic domain -> TWO seams (x_lo and x_hi).
    Returns (N,N) map varying along x only."""
    x = (np.arange(N) + 0.5) * dx
    r = 0.5 * (np.tanh((x - x_lo) / w) + np.tanh((x_hi - x) / w))
    return np.tile(r[None, :], (N, 1))


# ------------------------------------------------------------- genome variants
def ref_M0_k1(k1_orig=-0.7):
    """M0 with shifted ORIGINAL k1 (deviation-form k1_g and u0 recomputed)."""
    lam, k3, k4, Du = 2.0, 1.0, 1.5, 1.0
    r = np.roots([-1.0, 0.0, lam - k3 - k4, k1_orig])
    u0 = sorted(x.real for x in r if abs(x.imag) < 1e-9)[0]
    act = G._mk_act(lam, k1_orig, (k3 + k4) * u0, u0, Du)
    g = G.ref_M0()
    g["acts"] = [act]
    g["id"] = f"M0_k1{k1_orig}"
    g["provenance"]["orig"]["k1"] = k1_orig
    return g


# ------------------------------------------------------------- blending
ACT_KEYS = ("lam", "k1", "u0", "Du")


def blend_genomes(gA, gB, rhoB, forcemap=False):
    """Return (g, pmaps): g = copy of gA; pmaps has a map for every param that
    differs between gA and gB (or for ALL params if forcemap)."""
    assert len(gA["acts"]) == len(gB["acts"]) and len(gA["chans"]) == len(gB["chans"])
    g = json.loads(json.dumps(G.genome_json(gA)))
    g["id"] = f"patch[{gA['id']}|{gB['id']}]"
    pmaps = {}

    def put(kind, idx, a, b):
        a, b = float(a), float(b)
        d = b - a
        if d != 0.0 or forcemap:
            pmaps.setdefault(kind, {})[idx] = a + rhoB * d

    for i, (aA, aB) in enumerate(zip(gA["acts"], gB["acts"])):
        for k in ACT_KEYS:
            put(k, i, aA[k], aB[k])
    for c, (cA, cB) in enumerate(zip(gA["chans"], gB["chans"])):
        assert cA["g"] == cB["g"] == "id", "map engine: id channels only"
        put("tau", c, cA["tau"], cB["tau"])
        put("Dch", c, cA["D"], cB["D"])
    WA, WB = np.asarray(gA["W"], float), np.asarray(gB["W"], float)
    KA, KB = np.asarray(gA["K"], float), np.asarray(gB["K"], float)
    nc, na = WA.shape
    for c in range(nc):
        for a in range(na):
            if WA[c, a] != WB[c, a] or forcemap:
                pmaps.setdefault("W", {})[(c, a)] = WA[c, a] + rhoB * (WB[c, a] - WA[c, a])
    for i in range(na):
        for c in range(nc):
            if KA[i, c] != KB[i, c] or forcemap:
                pmaps.setdefault("K", {})[(i, c)] = KA[i, c] + rhoB * (KB[i, c] - KA[i, c])
    assert not gA.get("bilin") and not gB.get("bilin"), "bilin blending not implemented"
    return g, pmaps


# ------------------------------------------------------------- state/seeding
def state_vacuum_map(g, pmaps, N):
    na, nc = len(g["acts"]), len(g["chans"])
    F = np.zeros((na + nc, N, N))
    u0m = (pmaps or {}).get("u0", {})
    for i, a in enumerate(g["acts"]):
        F[i] += u0m.get(i, a["u0"])
    return F


def seed_stamp(F, stamp, x, y, dx, kick=None, na=1):
    """A4 stamp: du -> act0 at (x,y); dv,dw -> chans, displaced by kick
    (angle_deg, kick_px) OPPOSITE travel direction (composite convention)."""
    G.paste_stamp(F, {"du": stamp["du"]}, {"du": 0}, x, y, dx)
    xx, yy = x, y
    if kick is not None:
        ang, kd = kick
        a = np.deg2rad(ang)
        xx, yy = x - kd * np.cos(a), y - kd * np.sin(a)
    G.paste_stamp(F, {"dv": stamp["dv"], "dw": stamp["dw"]},
                  {"dv": na, "dw": na + 1}, xx, yy, dx)
    return F


def load_stamp():
    pth = os.path.join(os.path.dirname(BASE), "composite", "data", "stamp_A4_dx05.npz")
    stf = np.load(pth)
    return dict(du=stf["du"], dv=stf["dv"], dw=stf["dw"], u0=float(stf["u0"]))


# ------------------------------------------------------------- map-thr blobs
def blob_list_thrmap(u, thrmap, dx, L):
    mask = u > thrmap
    lab, n = G.periodic_label(mask)
    out = []
    for i in range(1, n + 1):
        m = lab == i
        wgt = np.where(m, np.clip(u - thrmap, 0.0, None), 0.0)
        c = G.circ_com(wgt, dx)
        ys, xs = np.nonzero(m)
        out.append(dict(y=c[0], x=c[1], area=float(m.sum()) * dx * dx,
                        peak=float(u[ys, xs].max())))
    return out


def _vardiff(dD, f, dx):
    """Conservative explicit div(dD grad f), periodic (roll)."""
    fxp = 0.5 * (dD + np.roll(dD, -1, 1)) * (np.roll(f, -1, 1) - f) / dx
    fyp = 0.5 * (dD + np.roll(dD, -1, 0)) * (np.roll(f, -1, 0) - f) / dx
    return (fxp - np.roll(fxp, 1, 1)) / dx + (fyp - np.roll(fyp, 1, 0)) / dx


# ------------------------------------------------------------- the simulator
def run_patched(g, pmaps=None, F=None, L=96.0, dx=0.5, dt=0.02, T=500.0,
                noise=0.0, seed=0, rec_tu=5.0, thr_frac=0.45, track_acts=None,
                snap_times=(), stop_all_dead=False, stop_explode_n=None,
                save_fields=True, ref_pos=None, rhs_probe=False, kymo_rows=None):
    """Map-aware fork of genome.run_genome. pmaps=None/{} == scalar path
    (op-for-op identical to run_genome; verified bit-identical in P1)."""
    t0_wall = time.time()
    pmaps = pmaps or {}
    na, nc = len(g["acts"]), len(g["chans"])
    N = int(round(L / dx))
    if F is None:
        F = state_vacuum_map(g, pmaps, N)
    F = np.array(F, float, copy=True)
    assert F.shape == (na + nc, N, N)
    W = np.asarray(g["W"], float)
    K = np.asarray(g["K"], float)
    bilin = [tuple(b) for b in g.get("bilin", [])]
    Wm = pmaps.get("W", {})
    Km = pmaps.get("K", {})

    def actpar(key, i, default):
        m = pmaps.get(key, {})
        return m[i] if i in m else default

    # per-act params as scalar-or-map
    lam_l = [actpar("lam", i, g["acts"][i]["lam"]) for i in range(na)]
    k1_l = [actpar("k1", i, g["acts"][i]["k1"]) for i in range(na)]
    u0_l = [actpar("u0", i, g["acts"][i]["u0"]) for i in range(na)]
    tau_l = [pmaps.get("tau", {}).get(c, g["chans"][c]["tau"]) for c in range(nc)]
    anymap = lambda v: isinstance(v, np.ndarray)

    # threshold (map if lam or u0 mapped)
    thr_l = []
    for i in range(na):
        lam_i, u0_i = lam_l[i], u0_l[i]
        thr = u0_i + thr_frac * (np.sqrt(np.maximum(lam_i, 1e-9)) - u0_i)
        thr_l.append(thr)

    # diffusion: base implicit + explicit deviation
    D_l = ([actpar("Du", i, g["acts"][i]["Du"]) for i in range(na)] +
           [pmaps.get("Dch", {}).get(c, g["chans"][c]["D"]) for c in range(nc)])
    Dbase = np.array([float(np.min(d)) if anymap(d) else float(d) for d in D_l])
    dD_l = [d - Dbase[f] if anymap(d) else None for f, d in enumerate(D_l)]
    ddmax = max([float(np.max(d)) for d in dD_l if d is not None], default=0.0)
    assert dt * ddmax * 4.0 / dx ** 2 < 0.5, f"explicit varD unstable: {ddmax}"

    steps = int(round(T / dt))
    rec = max(int(round(rec_tu / dt)), 1)
    kf = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    kr = 2 * np.pi * np.fft.rfftfreq(N, d=dx)
    k2 = kf[:, None] ** 2 + kr[None, :] ** 2
    E = np.exp(-Dbase[:, None, None] * k2[None] * dt)
    id_mask = np.array([c["g"] == "id" for c in g["chans"]])
    assert id_mask.all() or not (Wm or pmaps.get("tau")), "tanh chans: scalar only"
    thr_ch = np.array([c.get("thr", 0.0) for c in g["chans"]])
    sc_ch = np.array([c.get("sc", 1.0) for c in g["chans"]])
    rng = np.random.default_rng(seed)
    sq = np.sqrt(dt)
    if track_acts is None:
        track_acts = list(range(na))
    trackers = {i: G.Tracker(L, ref_pos=(ref_pos or {}).get(i)) for i in track_acts}
    ts = []
    series = {i: dict(pos=[], area=[], peak=[], ncomp=[]) for i in track_acts}
    snaps = {}
    snap_left = sorted(snap_times)
    status = "ok"
    rhs0 = None
    kymo = {k: [] for k in (kymo_rows or {})}

    # pre-broadcast scalar act params exactly like run_genome (lam[:,None,None])
    lam_s = np.array([x if not anymap(x) else np.nan for x in lam_l])[:, None, None]
    k1_s = np.array([x if not anymap(x) else np.nan for x in k1_l])[:, None, None]
    lam_mapped = any(anymap(x) for x in lam_l)
    k1_mapped = any(anymap(x) for x in k1_l)
    u0_mapped = any(anymap(x) for x in u0_l)
    u0s = np.array([x if not anymap(x) else np.nan for x in u0_l])
    U0F = None
    if u0_mapped:
        U0F = np.empty((na, N, N))
        for i in range(na):
            U0F[i] = u0_l[i]
    LAMF = K1F = None
    if lam_mapped:
        LAMF = np.empty((na, N, N))
        for i in range(na):
            LAMF[i] = lam_l[i]
    if k1_mapped:
        K1F = np.empty((na, N, N))
        for i in range(na):
            K1F[i] = k1_l[i]

    for t in range(steps + 1):
        tt = t * dt
        if t % rec == 0 or t == steps:
            if not np.isfinite(F).all():
                status = "blowup"
                break
            ncs_now = {}
            for i in track_acts:
                if anymap(thr_l[i]):
                    bl = blob_list_thrmap(F[i], thr_l[i], dx, L)
                else:
                    bl = G.blob_list(F[i], thr_l[i], dx, L)
                unw, ar, pk = trackers[i].update(bl)
                series[i]["pos"].append(unw)
                series[i]["area"].append(ar)
                series[i]["peak"].append(pk)
                series[i]["ncomp"].append(len(bl))
                ncs_now[i] = len(bl)
            for fid, row in (kymo_rows or {}).items():
                kymo[fid].append(F[fid][row, :].copy())
            ts.append(tt)
            if stop_all_dead and tt > 10.0 and all(v == 0 for v in ncs_now.values()):
                status = "died"
                break
            if stop_explode_n and tt > 10.0 and any(v >= stop_explode_n
                                                    for v in ncs_now.values()):
                status = "replicated"
                break
        while snap_left and tt >= snap_left[0] - 1e-9:
            snaps[snap_left.pop(0)] = F.copy()
        if t == steps:
            break
        U = F[:na]
        X = F[na:]
        Z = U - (U0F if u0_mapped else u0s[:, None, None])
        R = np.empty_like(F)
        # KX
        if Km:
            KX = np.zeros((na, N, N))
            for i in range(na):
                for c in range(nc):
                    kic = Km.get((i, c), K[i, c])
                    if anymap(kic) or kic != 0.0:
                        KX[i] += kic * X[c]
        else:
            KX = np.einsum("ic,cyx->iyx", K, X)
        RU = (LAMF if lam_mapped else lam_s) * U - U ** 3 \
             + (K1F if k1_mapped else k1_s) - KX
        for (i, c, c2, coef) in bilin:
            RU[i] -= coef * X[c] * X[c2]
        R[:na] = RU
        for c in range(nc):
            row_mapped = any((c, a) in Wm for a in range(na))
            if id_mask[c]:
                if row_mapped:
                    drive = np.zeros((N, N))
                    for a in range(na):
                        wca = Wm.get((c, a), W[c, a])
                        if anymap(wca) or wca != 0.0:
                            drive = drive + wca * Z[a]
                else:
                    drive = np.einsum("a,ayx->yx", W[c], Z)
            else:
                drive = np.zeros((N, N))
                for a in range(na):
                    if W[c, a] != 0.0:
                        drive += W[c, a] * np.tanh(
                            np.clip(Z[a] - thr_ch[c], 0.0, None) / sc_ch[c])
            R[na + c] = (drive - X[c]) / tau_l[c]
        # explicit spatially-varying diffusion correction
        for f, dDf in enumerate(dD_l):
            if dDf is not None:
                R[f] += _vardiff(dDf, F[f], dx)
        if rhs_probe and rhs0 is None:
            rhs0 = dict(
                max_abs=[float(np.max(np.abs(R[f]))) for f in range(na + nc)],
                prof_mid=[R[f][N // 2, :].copy() for f in range(na + nc)])
        Fn = F + dt * R
        if noise > 0:
            Fn[:na] += noise * sq * rng.standard_normal((na, N, N))
        F = np.fft.irfft2(np.fft.rfft2(Fn) * E, s=(N, N))
    wall = time.time() - t0_wall
    out = dict(status=status, dt=dt, dx=dx, L=L, N=N, t=np.array(ts),
               thr=[float(np.mean(th)) for th in thr_l], wall_s=wall,
               tu_per_s=(ts[-1] / wall if wall > 0 and ts else None),
               snaps=snaps, fields=F if save_fields else None, rhs0=rhs0,
               kymo={k: np.array(v) for k, v in kymo.items()})
    for i in track_acts:
        s = series[i]
        out[f"pos{i}"] = s["pos"]
        out[f"area{i}"] = s["area"]
        out[f"peak{i}"] = s["peak"]
        out[f"ncomp{i}"] = np.array(s["ncomp"], int)
    return out
