"""patch_lib.py — PoU patchworlds: map-aware fork of the l0 genome engine.

Partition-of-unity world composition on ONE grid:
    theta(x) = theta_A + rho_B(x) * (theta_B - theta_A),   rho_A + rho_B = 1.

Maps supported (each optional; everything else scalar, verbatim genome.py path):
  act params : lam, k1, u0, Du      (per act i)
  chan params: tau, Dch             (per chan c)
  wiring     : W[(c,a)], K[(i,c)]   (per entry)

Spatially-varying diffusion (litreview R1 reference implementation):
  D(x) = Dbase + dD(x), Dbase = min(map): exact spectral factor for Dbase,
  dD(x) >= 0 in CONSERVATIVE FLUX FORM div(dD grad f), explicit
  (dt*max(dD)*4/dx^2 < 0.5 asserted). Naive D(x)*lap or lap(D*.) are NOT used
  (mass leak / iso-vacuum break — litreview finding 1-2).

Grids: square (N x N) or rectangular (NY x NX) via Lx != L. Tracker wrap uses
Ly; EXACT for Lx == Ly and for Lx == 2*Ly (mod-Ly arithmetic absorbs x-wraps
when per-record steps << Ly/2). Scalar-only path reproduces genome.run_genome
op-for-op (bit-identity gated in P1).

UNITS: engine coords are length units (lu, dx=1-px equivalents); 1 lu = 2 grid
px at dx=0.5. Blob radius ~3 lu, tail wavelength ~11 lu, d*=15.4 lu,
w-halo decay sqrt(Dw*theta)=3.7 lu.
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
def rho_band(shape, dx, x_lo, x_hi, w):
    """rho_B(x,y): ~1 on x-band [x_lo, x_hi] lu, tanh ramps of tanh-width w lu
    (10-90%% transition = 2.197*w). Periodic -> seams at x_lo AND x_hi.
    shape: N or (NY, NX)."""
    NY, NX = (shape, shape) if np.isscalar(shape) else shape
    x = (np.arange(NX) + 0.5) * dx
    r = 0.5 * (np.tanh((x - x_lo) / w) + np.tanh((x_hi - x) / w))
    return np.tile(r[None, :], (NY, 1))


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
    differs between gA and gB (or ALL params if forcemap)."""
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


def blend_scalar(gA, gB, s):
    """Straight-line genome homotopy theta(s) (P0 pre-flight; scalar genome)."""
    g = json.loads(json.dumps(G.genome_json(gA)))
    g["id"] = f"chord[{gA['id']}->{gB['id']}]s{s:g}"
    for i in range(len(g["acts"])):
        for k in ACT_KEYS:
            g["acts"][i][k] = (1 - s) * gA["acts"][i][k] + s * gB["acts"][i][k]
    for c in range(len(g["chans"])):
        for k in ("tau", "D"):
            g["chans"][c][k] = (1 - s) * gA["chans"][c][k] + s * gB["chans"][c][k]
    W = (1 - s) * np.asarray(gA["W"], float) + s * np.asarray(gB["W"], float)
    K = (1 - s) * np.asarray(gA["K"], float) + s * np.asarray(gB["K"], float)
    g["W"], g["K"] = W.tolist(), K.tolist()
    return g


# ------------------------------------------------------------- state/seeding
def state_vacuum_map(g, pmaps, shape):
    NY, NX = (shape, shape) if np.isscalar(shape) else shape
    na, nc = len(g["acts"]), len(g["chans"])
    F = np.zeros((na + nc, NY, NX))
    u0m = (pmaps or {}).get("u0", {})
    for i, a in enumerate(g["acts"]):
        F[i] += u0m.get(i, a["u0"])
    return F


def poke_rect(F, g, act, x, y, amp, sig, dx):
    """Gaussian bump on activator `act`, rectangular-safe (periodic both axes)."""
    NY, NX = F.shape[1], F.shape[2]
    cy = (np.arange(NY) + 0.5) * dx
    cx = (np.arange(NX) + 0.5) * dx
    dyy = G.min_image(cy - y, NY * dx)[:, None]
    dxx = G.min_image(cx - x, NX * dx)[None, :]
    F[act] += amp * np.exp(-(dyy ** 2 + dxx ** 2) / (2 * sig ** 2))
    return F


def dressed_poke(F, g, act, x, y, dx, kick_px=0.0, kdir=(1.0, 0.0), dress=0.6):
    """l0 A1-style dressed poke: u bump + dress*W[c,act] id-channel shadows,
    shadows displaced -kick_px*kdir (blob travels +kdir). Rect-safe."""
    NY, NX = F.shape[1], F.shape[2]
    na = len(g["acts"])
    W = np.asarray(g["W"], float)
    F = poke_rect(F, g, act, x, y, 2.0, 3.0, dx)
    sx, sy = x - kick_px * kdir[0], y - kick_px * kdir[1]
    cy = (np.arange(NY) + 0.5) * dx
    cx = (np.arange(NX) + 0.5) * dx
    dyy = G.min_image(cy - sy, NY * dx)[:, None]
    dxx = G.min_image(cx - sx, NX * dx)[None, :]
    bump = 2.0 * np.exp(-(dyy ** 2 + dxx ** 2) / (2 * 3.0 ** 2))
    for ci, ch in enumerate(g["chans"]):
        if ch["g"] == "id" and W[ci, act] != 0.0:
            F[na + ci] += dress * W[ci, act] * bump
    return F


def paste_rect(F, stamp_fields, field_idx, x, y, dx):
    """Rect-safe sub-pixel stamp paste (FFT shift), periodic."""
    NY, NX = F.shape[1], F.shape[2]
    arr0 = next(iter(stamp_fields.values()))
    ns = arr0.shape[0]
    cy = ns // 2
    gy, gx = y / dx, x / dx
    iy, ix = int(round(gy)) % NY, int(round(gx)) % NX
    fy, fx = gy - round(gy), gx - round(gx)
    ys = (np.arange(ns) - cy + iy) % NY
    xs = (np.arange(ns) - cy + ix) % NX
    for name, fi in field_idx.items():
        F[fi][np.ix_(ys, xs)] += G.fshift(stamp_fields[name], fy, fx)
    return F


def seed_stamp(F, stamp, x, y, dx, kick=None, na=1):
    """A4 stamp: du -> act0; dv,dw -> chans, displaced by kick=(angle_deg, kd_lu)
    OPPOSITE travel direction (composite convention)."""
    paste_rect(F, {"du": stamp["du"]}, {"du": 0}, x, y, dx)
    xx, yy = x, y
    if kick is not None:
        ang, kd = kick
        a = np.deg2rad(ang)
        xx, yy = x - kd * np.cos(a), y - kd * np.sin(a)
    paste_rect(F, {"dv": stamp["dv"], "dw": stamp["dw"]},
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
    """Conservative explicit div(dD grad f), periodic (roll), shape-agnostic."""
    fxp = 0.5 * (dD + np.roll(dD, -1, 1)) * (np.roll(f, -1, 1) - f) / dx
    fyp = 0.5 * (dD + np.roll(dD, -1, 0)) * (np.roll(f, -1, 0) - f) / dx
    return (fxp - np.roll(fxp, 1, 1)) / dx + (fyp - np.roll(fyp, 1, 0)) / dx


# ------------------------------------------------------------- the simulator
def run_patched(g, pmaps=None, F=None, L=96.0, dx=0.5, dt=0.02, T=500.0,
                noise=0.0, seed=0, rec_tu=5.0, thr_frac=0.45, track_acts=None,
                snap_times=(), stop_all_dead=False, stop_explode_n=None,
                save_fields=True, ref_pos=None, rhs_probe=False, kymo_rows=None,
                Lx=None):
    """Map-aware fork of genome.run_genome. pmaps=None/{} == scalar path
    (op-for-op identical to run_genome on square grids; P1-gated).
    Lx != L -> rectangular grid (Ly=L rows, Lx cols); Lx must be L or 2L
    for exact Tracker wraps."""
    t0_wall = time.time()
    pmaps = pmaps or {}
    na, nc = len(g["acts"]), len(g["chans"])
    Lx = L if Lx is None else Lx
    NY, NX = int(round(L / dx)), int(round(Lx / dx))
    assert NX == NY or abs(Lx - 2 * L) < 1e-9, "rect grids: Lx in {L, 2L}"
    if F is None:
        F = state_vacuum_map(g, pmaps, (NY, NX))
    F = np.array(F, float, copy=True)
    assert F.shape == (na + nc, NY, NX)
    W = np.asarray(g["W"], float)
    K = np.asarray(g["K"], float)
    bilin = [tuple(b) for b in g.get("bilin", [])]
    Wm = pmaps.get("W", {})
    Km = pmaps.get("K", {})

    def actpar(key, i, default):
        m = pmaps.get(key, {})
        return m[i] if i in m else default

    lam_l = [actpar("lam", i, g["acts"][i]["lam"]) for i in range(na)]
    k1_l = [actpar("k1", i, g["acts"][i]["k1"]) for i in range(na)]
    u0_l = [actpar("u0", i, g["acts"][i]["u0"]) for i in range(na)]
    tau_l = [pmaps.get("tau", {}).get(c, g["chans"][c]["tau"]) for c in range(nc)]
    anymap = lambda v: isinstance(v, np.ndarray)

    thr_l = []
    for i in range(na):
        lam_i, u0_i = lam_l[i], u0_l[i]
        thr = u0_i + thr_frac * (np.sqrt(np.maximum(lam_i, 1e-9)) - u0_i)
        thr_l.append(thr)

    D_l = ([actpar("Du", i, g["acts"][i]["Du"]) for i in range(na)] +
           [pmaps.get("Dch", {}).get(c, g["chans"][c]["D"]) for c in range(nc)])
    Dbase = np.array([float(np.min(d)) if anymap(d) else float(d) for d in D_l])
    dD_l = [d - Dbase[f] if anymap(d) else None for f, d in enumerate(D_l)]
    ddmax = max([float(np.max(d)) for d in dD_l if d is not None], default=0.0)
    assert dt * ddmax * 4.0 / dx ** 2 < 0.5, f"explicit varD unstable: {ddmax}"

    steps = int(round(T / dt))
    rec = max(int(round(rec_tu / dt)), 1)
    kf = 2 * np.pi * np.fft.fftfreq(NY, d=dx)
    kr = 2 * np.pi * np.fft.rfftfreq(NX, d=dx)
    k2 = kf[:, None] ** 2 + kr[None, :] ** 2
    E = np.exp(-Dbase[:, None, None] * k2[None] * dt)
    id_mask = np.array([c["g"] == "id" for c in g["chans"]])
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

    lam_s = np.array([x if not anymap(x) else np.nan for x in lam_l])[:, None, None]
    k1_s = np.array([x if not anymap(x) else np.nan for x in k1_l])[:, None, None]
    lam_mapped = any(anymap(x) for x in lam_l)
    k1_mapped = any(anymap(x) for x in k1_l)
    u0_mapped = any(anymap(x) for x in u0_l)
    u0s = np.array([x if not anymap(x) else np.nan for x in u0_l])
    U0F = LAMF = K1F = None
    if u0_mapped:
        U0F = np.empty((na, NY, NX))
        for i in range(na):
            U0F[i] = u0_l[i]
    if lam_mapped:
        LAMF = np.empty((na, NY, NX))
        for i in range(na):
            LAMF[i] = lam_l[i]
    if k1_mapped:
        K1F = np.empty((na, NY, NX))
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
        if Km:
            KX = np.zeros((na, NY, NX))
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
                    drive = np.zeros((NY, NX))
                    for a in range(na):
                        wca = Wm.get((c, a), W[c, a])
                        if anymap(wca) or wca != 0.0:
                            drive = drive + wca * Z[a]
                else:
                    drive = np.einsum("a,ayx->yx", W[c], Z)
            else:
                drive = np.zeros((NY, NX))
                for a in range(na):
                    if W[c, a] != 0.0:
                        drive += W[c, a] * np.tanh(
                            np.clip(Z[a] - thr_ch[c], 0.0, None) / sc_ch[c])
            R[na + c] = (drive - X[c]) / tau_l[c]
        for f, dDf in enumerate(dD_l):
            if dDf is not None:
                R[f] += _vardiff(dDf, F[f], dx)
        if rhs_probe and rhs0 is None:
            rhs0 = dict(
                max_abs=[float(np.max(np.abs(R[f]))) for f in range(na + nc)],
                prof_mid=[R[f][NY // 2, :].copy() for f in range(na + nc)])
        Fn = F + dt * R
        if noise > 0:
            Fn[:na] += noise * sq * rng.standard_normal((na, NY, NX))
        F = np.fft.irfft2(np.fft.rfft2(Fn) * E, s=(NY, NX))
    wall = time.time() - t0_wall
    out = dict(status=status, dt=dt, dx=dx, L=L, Lx=Lx, N=NY, NX=NX,
               t=np.array(ts),
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
