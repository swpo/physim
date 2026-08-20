"""engine.py — generic canonical-genome simulator for l0-evolver.

GENOME FORMAT (l0/PROGRAM.md canonical, deviation form; DO NOT FORK — when
l0-sampler lands lib/genome.py we import/adapt via get_lib() below):
  G = {"acts":  [{"lam","k1","Du"}...],          # k1 in GENOME form (see below)
       "chans": [{"tau","D","g"}...],            # g = {"kind":"id"} | {"kind":"tanh","thr","sc"}
       "W": n_chan x n_act,  "K": n_act x n_chan,
       "u0": [per-act vacuum root]  (cached; derived),
       "provenance": {...}}
Dynamics (u_i absolute, x_c deviations == 0 at vacuum BY CONSTRUCTION):
  du_i/dt = Du_i lap u_i + lam_i u_i - u_i^3 + k1_i - sum_c K[i,c] x_c
  dx_c/dt = (sum_a W[c,a] g_c(u_a - u0_a) - x_c)/tau_c + D_c lap x_c

Purwins mapping (verified in smoke): k1_genome = k1_purwins - (k3+k4)*u0 and
the M0 vacuum is the MIDDLE root of the genome cubic (activator alone is
self-exciting there; fast w channel stabilizes it) — so vacuum selection is
EXPLICIT (G["u0"]), not "most negative root" (documented deviation from the
G0a sketch in PROGRAM.md; the actual gate is the full-Jacobian dispersion).

Numerics: IMEX-FFT (diffusion exact in Fourier, reaction explicit), dx=0.5,
dt=0.02, periodic — program conventions verbatim (composite/rotor lineage).
"""
import json, os, time
import numpy as np
from scipy import ndimage

BASE = os.path.dirname(os.path.abspath(__file__))
L0 = os.path.dirname(BASE)
CDATA = os.path.join(os.path.dirname(L0), "composite", "data")


def get_lib():
    """Poll for l0-sampler's lib/genome.py; import if present (never fork)."""
    p = os.path.join(L0, "lib", "genome.py")
    if not os.path.exists(p):
        return None
    import importlib.util
    spec = importlib.util.spec_from_file_location("l0lib_genome", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------ genome algebra
def cubic_roots(lam, k1):
    """Real roots of -u^3 + lam*u + k1 = 0, ascending."""
    r = np.roots([-1.0, 0.0, lam, k1])
    return sorted(float(x.real) for x in r if abs(x.imag) < 1e-9)


def genome_vacuum(G):
    """Cached per-act vacuum; validate it solves each cubic."""
    u0 = np.asarray(G["u0"], float)
    for a, act in enumerate(G["acts"]):
        res = -u0[a] ** 3 + act["lam"] * u0[a] + act["k1"]
        assert abs(res) < 1e-7, f"act{a} u0 not a cubic root (res={res})"
    return u0


def g_eval(g, z):
    if g["kind"] == "id":
        return z
    if g["kind"] == "tanh":
        return np.tanh(np.clip(z - g["thr"], 0.0, None) / g["sc"])
    raise ValueError(g["kind"])


def g_slope0(g):
    """dg/dz at z=0 (for linearizations). tanh-with-threshold has slope 0."""
    if g["kind"] == "id":
        return 1.0
    if g["kind"] == "tanh":
        return 0.0 if g["thr"] > 1e-12 else 1.0 / g["sc"]
    raise ValueError(g["kind"])


def jacobian_k(G, q):
    """Full (n_act+n_chan)^2 linearization about the vacuum at wavenumber^2=q."""
    na, nc = len(G["acts"]), len(G["chans"])
    u0 = genome_vacuum(G)
    W = np.asarray(G["W"], float); K = np.asarray(G["K"], float)
    J = np.zeros((na + nc, na + nc))
    for a, act in enumerate(G["acts"]):
        J[a, a] = act["lam"] - 3 * u0[a] ** 2 - act["Du"] * q
        for c in range(nc):
            J[a, na + c] = -K[a, c]
    for c, ch in enumerate(G["chans"]):
        sl = g_slope0(ch["g"])
        for a in range(na):
            J[na + c, a] = W[c, a] * sl / ch["tau"]
        J[na + c, na + c] = -1.0 / ch["tau"] - ch["D"] * q
    return J


def funnel_g0(G, kmax=3.0, nk=181):
    """G0a background dispersion + G0b bistability + G0c tails. Cheap."""
    out = {}
    worst, kw = -np.inf, 0.0
    for k in np.linspace(0, kmax, nk):
        g = float(np.max(np.linalg.eigvals(jacobian_k(G, k * k)).real))
        if g > worst:
            worst, kw = g, float(k)
    out["g0a_maxgrowth"] = worst
    out["g0a_k"] = kw
    out["g0a_pass"] = bool(worst < 0)
    bis = []
    for act in G["acts"]:
        bis.append(len(cubic_roots(act["lam"], act["k1"])) == 3)
    out["g0b_bistable"] = bis
    out["g0b_pass"] = all(bis)
    # G0c per-act tails: Du*s + a - sum_c K_c W_c g'/(1 - A_c s) = 0
    tails = []
    u0 = genome_vacuum(G)
    W = np.asarray(G["W"], float); K = np.asarray(G["K"], float)
    for a, act in enumerate(G["acts"]):
        alin = act["lam"] - 3 * u0[a] ** 2
        terms = []
        for c, ch in enumerate(G["chans"]):
            kw_ = K[a, c] * W[c, a] * g_slope0(ch["g"])
            if abs(kw_) > 1e-14:
                terms.append((kw_, ch["tau"] * ch["D"]))
        # polynomial in s: (Du*s + alin) * prod(1-A_c s) - sum_c kw_c * prod_{c'!=c}(1-A_c' s) = 0
        P = np.polynomial.polynomial
        base = [1.0]
        for _, A in terms:
            base = P.polymul(base, [1.0, -A])
        poly = P.polymul([alin, act["Du"]], base)
        for i, (kw_, A) in enumerate(terms):
            pr = [1.0]
            for j, (_, A2) in enumerate(terms):
                if j != i:
                    pr = P.polymul(pr, [1.0, -A2])
            poly = P.polyadd(poly, P.polymul([-kw_], pr))
        s = np.roots(poly[::-1]) if len(poly) > 1 else np.array([])
        mus = np.sqrt(s.astype(complex))
        # keep decaying-tail branch: Re mu > 0 representative
        mus = np.array([m if m.real >= 0 else -m for m in mus])
        best = None
        for m in mus:
            if 0.02 <= m.real <= 5.0:
                lamb = 2 * np.pi / abs(m.imag) if abs(m.imag) > 1e-9 else None
                cand = dict(re=float(m.real), im=float(abs(m.imag)),
                            wavelength=(float(lamb) if lamb else None))
                # prefer oscillatory in chemistry band, else slowest decay
                if best is None:
                    best = cand
                else:
                    bosc = best["wavelength"] and 3 <= best["wavelength"] <= 30 and 0.1 <= best["re"] <= 1.5
                    cosc = cand["wavelength"] and 3 <= cand["wavelength"] <= 30 and 0.1 <= cand["re"] <= 1.5
                    if (cosc and not bosc) or (cosc == bosc and cand["re"] < best["re"]):
                        best = cand
        tails.append(best)
    out["g0c_tails"] = tails
    return out


# ------------------------------------------------------------------ tracking
def circ_com(wgt, dx):
    tot = wgt.sum()
    if tot <= 0:
        return None
    out = []
    for ax in (0, 1):
        Nax = wgt.shape[ax]
        ang = 2 * np.pi * (np.arange(Nax) + 0.5) / Nax
        prof = wgt.sum(axis=1 - ax)
        z = (prof * np.exp(1j * ang)).sum() / tot
        out.append((np.angle(z) % (2 * np.pi)) / (2 * np.pi) * Nax * dx)
    return tuple(out)


def _find(parent, a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a


def periodic_label(mask):
    lab, n = ndimage.label(mask)
    if n <= 1:
        return lab, n
    parent = list(range(n + 1))
    def union(a, b):
        ra, rb = _find(parent, a), _find(parent, b)
        if ra != rb:
            parent[rb] = ra
    for a, b in zip(lab[0, :], lab[-1, :]):
        if a > 0 and b > 0:
            union(int(a), int(b))
    for a, b in zip(lab[:, 0], lab[:, -1]):
        if a > 0 and b > 0:
            union(int(a), int(b))
    remap, k = {}, 0
    for i in range(1, n + 1):
        r = _find(parent, i)
        if r not in remap:
            k += 1
            remap[r] = k
    lut = np.zeros(n + 1, dtype=lab.dtype)
    for i in range(1, n + 1):
        lut[i] = remap[_find(parent, i)]
    return lut[lab], k


def blob_list(u, thr, dx):
    mask = u > thr
    lab, n = periodic_label(mask)
    out = []
    for i in range(1, n + 1):
        m = lab == i
        wgt = np.where(m, np.clip(u - thr, 0.0, None), 0.0)
        c = circ_com(wgt, dx)
        ys, xs = np.nonzero(m)
        out.append(dict(y=c[0], x=c[1], area=float(m.sum()) * dx * dx,
                        peak=float(u[ys, xs].max())))
    return out


def min_image(d, L):
    return (d + L / 2) % L - L / 2


class Tracker:
    def __init__(self, L, ref_pos=None):
        self.L = L; self.ref = ref_pos; self.prev = None; self.prev_raw = None

    def update(self, bl):
        L = self.L
        if len(bl) == 0:
            self.prev = None; self.prev_raw = None
            return np.zeros((0, 2)), [], []
        if self.prev_raw is None or len(bl) != len(self.prev_raw):
            if self.ref is not None and len(bl) == len(self.ref) and self.prev is None:
                order, used = [], set()
                for (rx, ry) in self.ref:
                    d = [np.hypot(*min_image(np.array([b["y"] - ry, b["x"] - rx]), L))
                         if j not in used else 1e9 for j, b in enumerate(bl)]
                    j = int(np.argmin(d)); used.add(j); order.append(j)
                bl = [bl[j] for j in order]
            else:
                order = np.argsort([b["x"] + 1e-3 * b["y"] for b in bl])
                bl = [bl[i] for i in order]
            raw = np.array([[b["y"], b["x"]] for b in bl])
            unw = raw.copy()
        else:
            raw = np.array([[b["y"], b["x"]] for b in bl])
            used, idx = set(), []
            for pr in self.prev_raw:
                d = np.array([np.hypot(*min_image(raw[j] - pr, L)) if j not in used
                              else 1e9 for j in range(len(raw))])
                j = int(np.argmin(d)); used.add(j); idx.append(j)
            bl = [bl[j] for j in idx]
            raw = raw[idx]
            step = np.array([min_image(raw[i] - self.prev_raw[i], L)
                             for i in range(len(raw))])
            unw = self.prev + step
        self.prev_raw = raw; self.prev = unw
        return unw.copy(), [b["area"] for b in bl], [b["peak"] for b in bl]


# ---------------------------------------------------------------- seeding IC
def fshift(a, dy_px, dx_px):
    if abs(dy_px) < 1e-12 and abs(dx_px) < 1e-12:
        return a
    n0, n1 = a.shape
    ky = np.fft.fftfreq(n0)[:, None]
    kx = np.fft.rfftfreq(n1)[None, :]
    ph = np.exp(-2j * np.pi * (ky * dy_px + kx * dx_px))
    return np.fft.irfft2(np.fft.rfft2(a) * ph, s=a.shape)


def seed_gauss(G, F, seeds, dx, chan_scale=1.0, kick=None):
    """seeds: [(act_index, x, y, amp, sig)]. u-bump plus each channel set to
    chan_scale * its RELAXED response to the frozen bump: x_c solves
    (drive - x)/tau + D lap x = 0  =>  x_hat = drive_hat/(1 + tau*D*k^2)
    (the stamp-math Helmholtz smoothing; chan_scale=0 = Day-0 u-only poke;
    M1 trap doc: pure u-bumps die in slow-tau worlds, relaxed channels fix)."""
    na = len(G["acts"])
    u0 = genome_vacuum(G)
    N = F.shape[-1]
    x = (np.arange(N) + 0.5) * dx
    W = np.asarray(G["W"], float)
    for (ai, px, py, amp, sig) in seeds:
        dX = min_image(x[None, :] - px, N * dx)
        dY = min_image(x[:, None] - py, N * dx)
        bump = amp * np.exp(-(dX ** 2 + dY ** 2) / (2 * sig ** 2))
        F[ai] += bump
    if chan_scale != 0.0:
        kf = 2 * np.pi * np.fft.fftfreq(N, d=dx)
        kr = 2 * np.pi * np.fft.rfftfreq(N, d=dx)
        k2 = kf[:, None] ** 2 + kr[None, :] ** 2
        for c, ch in enumerate(G["chans"]):
            drive = np.zeros_like(F[0])
            for a in range(na):
                if abs(W[c, a]) > 1e-14:
                    drive += W[c, a] * g_eval(ch["g"], F[a] - u0[a])
            dh = np.fft.rfft2(drive) / (1.0 + ch["tau"] * ch["D"] * k2)
            xc = chan_scale * np.fft.irfft2(dh, s=(N, N))
            if kick is not None:
                ang, kd = kick
                a_ = np.deg2rad(ang)
                # channels displaced kick_d OPPOSITE desired direction (M1/M4)
                xc = fshift(xc, -kd * np.sin(a_) / dx, -kd * np.cos(a_) / dx)
            F[na + c] = xc
    return F


def seed_stamp(G, F, stamps, dx):
    """stamps: [(act_index, x, y, stampdict, chan_map[, kick])] — paste
    certified (du,dv,dw,...) deviations; chan_map maps stamp keys -> channel
    indices; optional kick=(angle_deg, kick_d): channel parts pasted displaced
    kick_d OPPOSITE the angle (M4 convention -> blob drifts toward angle)."""
    N = F.shape[-1]
    for entry in stamps:
        ai, px, py, st, chan_map = entry[:5]
        kick = entry[5] if len(entry) > 5 else None
        ns = st["du"].shape[0]
        cy = ns // 2
        gy, gx = py / dx, px / dx
        iy, ix = int(round(gy)) % N, int(round(gx)) % N
        fy, fx = gy - round(gy), gx - round(gx)
        ys = (np.arange(ns) - cy + iy) % N
        xs = (np.arange(ns) - cy + ix) % N
        F[ai][np.ix_(ys, xs)] += fshift(st["du"], fy, fx)
        if kick is None:
            oy_g, ox_g = gy, gx
        else:
            ang, kd = kick
            a_ = np.deg2rad(ang)
            oy_g = gy - kd * np.sin(a_) / dx
            ox_g = gx - kd * np.cos(a_) / dx
        jy, jx = int(round(oy_g)) % N, int(round(ox_g)) % N
        fy2, fx2 = oy_g - round(oy_g), ox_g - round(ox_g)
        ys2 = (np.arange(ns) - cy + jy) % N
        xs2 = (np.arange(ns) - cy + jx) % N
        for key, ci in chan_map.items():
            F[len(G["acts"]) + ci][np.ix_(ys2, xs2)] += fshift(st[key], fy2, fx2)
    return F


def load_stamp(name="stamp_A4_dx05.npz"):
    for root in (os.path.join(BASE, "data"), CDATA):
        p = os.path.join(root, name)
        if os.path.exists(p):
            stf = np.load(p)
            return dict(du=stf["du"], dv=stf["dv"], dw=stf["dw"], u0=float(stf["u0"]))
    raise FileNotFoundError(name)


# --------------------------------------------------------------------- run
def run(G, L=64.0, dx=0.5, dt=0.02, T=500.0, seeds=(), stamps=(),
        chan_scale=1.0, kick=None, noise=0.0, seed=0, rec_tu=5.0,
        thr_frac=0.45, stop_split=False, stop_dead=False, snap_times=(),
        save_fields=False):
    """Integrate genome G. Track blobs per activator. Returns per-act tracks."""
    na, nc = len(G["acts"]), len(G["chans"])
    nf = na + nc
    u0 = genome_vacuum(G)
    N = int(round(L / dx))
    F = np.empty((nf, N, N))
    for a in range(na):
        F[a] = u0[a]
    F[na:] = 0.0
    if seeds:
        F = seed_gauss(G, F, seeds, dx, chan_scale=chan_scale, kick=kick)
    if stamps:
        F = seed_stamp(G, F, stamps, dx)

    W = np.asarray(G["W"], float); K = np.asarray(G["K"], float)
    lam = np.array([a_["lam"] for a_ in G["acts"]])
    k1 = np.array([a_["k1"] for a_ in G["acts"]])
    Dvec = np.array([a_["Du"] for a_ in G["acts"]] + [c_["D"] for c_ in G["chans"]])
    tauv = np.array([c_["tau"] for c_ in G["chans"]])

    # per-act detection thresholds: u0 + thr_frac*(upper_root - u0) if bistable
    thr = np.empty(na)
    for a, act in enumerate(G["acts"]):
        roots = cubic_roots(act["lam"], act["k1"])
        hi = roots[-1] if len(roots) == 3 else u0[a] + np.sqrt(max(act["lam"], 0.2))
        thr[a] = u0[a] + thr_frac * (hi - u0[a])

    kf = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    kr = 2 * np.pi * np.fft.rfftfreq(N, d=dx)
    k2 = kf[:, None] ** 2 + kr[None, :] ** 2
    E = np.exp(-Dvec[:, None, None] * k2[None, :, :] * dt)
    rng = np.random.default_rng(seed)
    sq = np.sqrt(dt)
    steps = int(round(T / dt))
    rec = max(int(round(rec_tu / dt)), 1)

    n0 = [0] * na
    for s in seeds:
        n0[s[0]] += 1
    for s in stamps:
        n0[s[0]] += 1
    trs = [Tracker(L) for _ in range(na)]
    ts, POS, AREA, PEAK, NC = [], [[] for _ in range(na)], [[] for _ in range(na)],         [[] for _ in range(na)], [[] for _ in range(na)]
    snaps = {}; snap_left = sorted(snap_times)
    status = "ok"
    t0 = time.time()
    for t in range(steps + 1):
        tt = t * dt
        if t % rec == 0 or t == steps:
            if not np.isfinite(F).all():
                status = "blowup"; break
            ts.append(tt)
            for a in range(na):
                bl = blob_list(F[a], thr[a], dx)
                unw, ar, pk = trs[a].update(bl)
                POS[a].append(unw); AREA[a].append(ar); PEAK[a].append(pk)
                NC[a].append(len(bl))
            if stop_split and tt > 50.0 and any(
                    n0[a] and NC[a][-1] != n0[a] for a in range(na)):
                status = "census_change"; break
            if stop_dead and len(ts) >= 3 and all(
                    NC[a][-1] == 0 and NC[a][-2] == 0 and NC[a][-3] == 0
                    for a in range(na) if n0[a]):
                dev = max(float(np.max(np.abs(F[a] - u0[a])))
                          / max(thr[a] - u0[a], 1e-9) for a in range(na))
                if dev < 0.5:
                    status = "dead"; break
        while snap_left and tt >= snap_left[0] - 1e-9:
            snaps[snap_left.pop(0)] = F[:na].copy()
        if t == steps:
            break
        R = np.empty_like(F)
        for a in range(na):
            drive = lam[a] * F[a] - F[a] ** 3 + k1[a]
            for c in range(nc):
                if abs(K[a, c]) > 1e-14:
                    drive = drive - K[a, c] * F[na + c]
            R[a] = drive
        for c in range(nc):
            dr = np.zeros((N, N))
            for a in range(na):
                if abs(W[c, a]) > 1e-14:
                    dr += W[c, a] * g_eval(G["chans"][c]["g"], F[a] - u0[a])
            R[na + c] = (dr - F[na + c]) / tauv[c]
        Fn = F + dt * R
        if noise > 0:
            Fn[:na] += noise * sq * rng.standard_normal((na, N, N))
        F = np.fft.irfft2(np.fft.rfft2(Fn) * E, s=(N, N))
    wall = time.time() - t0
    return dict(status=status, u0=u0.tolist(), thr=thr.tolist(), N=N, L=L,
                dx=dx, dt=dt, t=np.array(ts), pos=POS, area=AREA, peak=PEAK,
                ncomp=[np.array(x, int) for x in NC], n0=n0, snaps=snaps,
                fields=(F if save_fields else None), wall_s=wall,
                tu_per_s=(ts[-1] / wall if wall > 0 and ts else None))


# ------------------------------------------------------------------ results
def append_result(record, path=None):
    import fcntl
    path = path or os.path.join(BASE, "results.json")
    lockp = path + ".lock"
    with open(lockp, "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            with open(path) as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        record = dict(record)
        record.setdefault("ts", time.strftime("%Y-%m-%d %H:%M:%S"))
        data.append(record)
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f, indent=1)
        os.replace(tmp, path)
        fcntl.flock(lk, fcntl.LOCK_UN)
    return len(data)
