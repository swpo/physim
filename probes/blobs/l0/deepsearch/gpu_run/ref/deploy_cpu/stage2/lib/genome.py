"""lib/genome.py — L0 canonical deviation-form genome + general IMEX-FFT simulator.

GENOME (dict, JSON-serializable):
  acts : [ {lam, k1, Du, u0} ]          n_act cubic activators (u_i full fields)
  chans: [ {tau, D, g, thr, sc} ]       n_chan linear channels x_c (DEVIATIONS, ==0 at vacuum)
  W    : n_chan x n_act                 channel drive weights
  K    : n_act x n_chan                 coupling of channels back into activators
  bilin: [ [i, c, c2, coeff], ... ]     OPTIONAL u_i-eq += -coeff * x_c * x_c2
  provenance: {...}

Dynamics:
  du_i/dt = Du_i lap u_i + lam_i u_i - u_i^3 + k1_i - sum_c K[i,c] x_c  (- bilin)
  dx_c/dt = ( sum_a W[c,a] g_c(u_a - u0_a) - x_c ) / tau_c + D_c lap x_c
  g = "id": g(z)=z ;  g = "tanh": g(z)=tanh(max(z-thr,0)/sc)  (bounded deposit; dead
  at linear order when thr>0 -> invisible to G0a/G0c linear screens, documented).

u0_i is the DESIGNATED vacuum: a real root of -u^3+lam*u+k1=0 stored in the genome
(validated at load). NOTE (measured 2026-02-19): the certified M-worlds' vacuum is
the MOST NEGATIVE root of the ORIGINAL cubic -u^3+(lam-k3-k4)u+k1, which in
deviation form (k1_g = k1 - sum K_c*u0) may be middle-or-lowest root of the BARE
cubic -u^3+lam*u+k1_g; root identity in the bare cubic is a free genome choice.

At the vacuum (u_i=u0_i, x_c=0) every drive vanishes for ANY W,K,bilin: the
iso-background trick is structural. bilin terms are quadratic in deviations ->
vacuum-exact and invisible to all linear screens.

Simulator: IMEX-FFT (batched rfft2 over n_act+n_chan stacked fields), dx=0.5,
dt=0.02, L=96 periodic — program conventions (composite/rotor numerics verbatim:
explicit reaction with OLD u in channel drives, then exact diffusion in Fourier).
Tracking: per-activator periodic labeling + circular-mean centroids + greedy
identity matching (composite/sim.py verbatim). Blob identity is MEASURED.

Reference genomes: M0, VVW (M3 MAXC pair), XV (M7 rotor point), BFIELD (M6 g=0.05
point, exact via bilin). Parity gates live in ../parity.py.
"""
import json, os, time
import numpy as np
from scipy import ndimage

BASE = os.path.dirname(os.path.abspath(__file__))          # .../l0/lib
L0DIR = os.path.dirname(BASE)                              # .../l0
CDATA = os.path.join(os.path.dirname(L0DIR), "composite", "data")


# ------------------------------------------------------------- cubic algebra
def cubic_roots(lam, k1):
    """Real roots of -u^3 + lam*u + k1 = 0, sorted ascending."""
    r = np.roots([-1.0, 0.0, lam, k1])
    return sorted(float(x.real) for x in r if abs(x.imag) < 1e-9)


def cubic_disc(lam, k1):
    """Discriminant sign proxy for u^3 - lam*u - k1 (>0 iff 3 distinct real roots)."""
    return 4.0 * lam ** 3 - 27.0 * k1 ** 2


def polish_root(lam, k1, u0, iters=60):
    for _ in range(iters):
        f = -u0 ** 3 + lam * u0 + k1
        fp = -3 * u0 ** 2 + lam
        if abs(fp) < 1e-14:
            break
        du = -f / fp
        u0 += du
        if abs(du) < 1e-15:
            break
    return float(u0)


def act_fu(a):
    return a["lam"] - 3.0 * a["u0"] ** 2


def validate(g, tol=1e-8):
    """Structural checks + u0-is-a-root check. Returns list of problems."""
    probs = []
    na, nc = len(g["acts"]), len(g["chans"])
    W, K = np.asarray(g["W"], float), np.asarray(g["K"], float)
    if W.shape != (nc, na):
        probs.append(f"W shape {W.shape} != ({nc},{na})")
    if K.shape != (na, nc):
        probs.append(f"K shape {K.shape} != ({na},{nc})")
    for i, a in enumerate(g["acts"]):
        f = -a["u0"] ** 3 + a["lam"] * a["u0"] + a["k1"]
        if abs(f) > tol:
            probs.append(f"act{i}: u0 not a root (f={f:.2e})")
        if a["Du"] <= 0:
            probs.append(f"act{i}: Du<=0")
    for c, ch in enumerate(g["chans"]):
        if ch["tau"] <= 0 or ch["D"] < 0:
            probs.append(f"chan{c}: bad tau/D")
        if ch["g"] not in ("id", "tanh"):
            probs.append(f"chan{c}: bad g {ch.get('g')}")
        if ch["g"] == "tanh" and (ch.get("sc", 0) <= 0):
            probs.append(f"chan{c}: tanh needs sc>0")
    for b in g.get("bilin", []):
        i, c, c2, _ = b
        if not (0 <= i < na and 0 <= c < nc and 0 <= c2 < nc):
            probs.append(f"bilin index bad {b}")
    return probs


# ------------------------------------------------------- reference genomes
def _mk_act(lam, k1_orig, Ksum_u0, u0, Du):
    """Fold -sum_c K_c*u0_contrib into k1 (original params -> deviation form)."""
    k1g = k1_orig - Ksum_u0
    return dict(lam=lam, k1=k1g, Du=Du, u0=polish_root(lam, k1g, u0))


def ref_M0():
    lam, k1, k3, k4, tau, theta, Du, Dv, Dw = 2.0, -0.7, 1.0, 1.5, 3.0, 0.7, 1.0, 1.0, 20.0
    r = np.roots([-1.0, 0.0, lam - k3 - k4, k1])
    u0 = sorted(x.real for x in r if abs(x.imag) < 1e-9)[0]
    act = _mk_act(lam, k1, (k3 + k4) * u0, u0, Du)
    return dict(
        id="ref_M0",
        acts=[act],
        chans=[dict(tau=tau, D=Dv, g="id", thr=0.0, sc=1.0),
               dict(tau=theta, D=Dw, g="id", thr=0.0, sc=1.0)],
        W=[[1.0], [1.0]],
        K=[[k3, k4]],
        bilin=[],
        provenance=dict(kind="reference", source="M0 Day-0 blob",
                        orig=dict(lam=lam, k1=k1, k3=k3, k4=k4, tau=tau,
                                  theta=theta, Du=Du, Dv=Dv, Dw=Dw)))


def ref_M4(tau=5.7):
    """M4 family: M0 statics with A=tau*Dv=4 (Dv=4/tau). For G0c shell validation."""
    g = ref_M0()
    g["id"] = f"ref_M4_tau{tau}"
    g["chans"][0]["tau"] = tau
    g["chans"][0]["D"] = 4.0 / tau
    g["provenance"]["source"] = "M4 A=4 family"
    return g


def ref_VVW():
    """M3 MAXC pair: A(k1=-1.0,k4=1.40) + B(k1=-1.0+0.75*UB,k4=2.15), Du=.65,
    shared w (drive (u1+u2)/2), private v_i. Background UB=-0.86756 for both
    species by iso-line construction."""
    lam, k3, tau, theta, Dv, Dw, Du = 2.0, 1.0, 3.0, 0.7, 1.0, 20.0, 0.65
    UB = -0.86756
    k1_1, k4_1 = -1.0, 1.4
    k1_2, k4_2 = -1.0 + 0.75 * UB, 2.15
    a1 = _mk_act(lam, k1_1, (k3 + k4_1) * UB, UB, Du)
    a2 = _mk_act(lam, k1_2, (k3 + k4_2) * UB, UB, Du)
    return dict(
        id="ref_VVW",
        acts=[a1, a2],
        chans=[dict(tau=tau, D=Dv, g="id", thr=0.0, sc=1.0),    # v1
               dict(tau=tau, D=Dv, g="id", thr=0.0, sc=1.0),    # v2
               dict(tau=theta, D=Dw, g="id", thr=0.0, sc=1.0)], # shared w
        W=[[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]],
        K=[[k3, 0.0, k4_1], [0.0, k3, k4_2]],
        bilin=[],
        provenance=dict(kind="reference", source="M3 flavors MAXC pair (A has "
                        "continuum caveat at dx=0.5; B continuum-clean)",
                        orig=dict(UB=UB, k1=[k1_1, k1_2], k4=[k4_1, k4_2])))


def ref_XV(tau1=5.7, tau2=2.5, eta12=0.1, eta21=0.1):
    """M7 rotor point: two private Purwins copies (A_i=4), cross-v eta drive."""
    lam, k1, k3, k4, theta, Du, Dw = 2.0, -0.7, 1.0, 1.5, 0.7, 1.0, 20.0
    r = np.roots([-1.0, 0.0, lam - k3 - k4, k1])
    u0 = sorted(x.real for x in r if abs(x.imag) < 1e-9)[0]
    a1 = _mk_act(lam, k1, (k3 + k4) * u0, u0, Du)
    a2 = dict(a1)
    return dict(
        id=f"ref_XV_tau1{tau1}",
        acts=[a1, a2],
        chans=[dict(tau=tau1, D=4.0 / tau1, g="id", thr=0.0, sc=1.0),   # v1
               dict(tau=tau2, D=4.0 / tau2, g="id", thr=0.0, sc=1.0),   # v2
               dict(tau=theta, D=Dw, g="id", thr=0.0, sc=1.0),          # w1
               dict(tau=theta, D=Dw, g="id", thr=0.0, sc=1.0)],         # w2
        W=[[1.0, eta12], [eta21, 1.0], [1.0, 0.0], [0.0, 1.0]],
        K=[[k3, 0.0, k4, 0.0], [0.0, k3, 0.0, k4]],
        bilin=[],
        provenance=dict(kind="reference", source="M7 rotor RT1 ref point",
                        orig=dict(tau1=tau1, tau2=tau2, eta12=eta12, eta21=eta21)))


def ref_BFIELD(gamma=0.05, tau_b=200.0, D_b=0.0):
    # D_b=0: the BF1/BF2 certified self-launch points ran D_b=0 (dilution curve
    # separately mapped D_b in {0,.5,2}); genome pins the certified point.
    """M6 dynamical-b point (source s2, isok coupling) — EXACT via bilin.
    b-channel: tau=tau_b, D=D_b, g=tanh(max(z-thr)/0.4), W=gamma;
    u-eq += b*(u0-w). In deviations w = u0 + x_w  =>  b*(u0-w) = -x_b*x_w
    -> bilin=[[0, 2, 1, 1.0]]; K[0,b]=0 (b acts ONLY through the vertex)."""
    lam, k1, k3, k4, theta, Du, Dw = 2.0, -0.7, 1.0, 1.5, 0.7, 1.0, 20.0
    tau, Dv = 5.7, 4.0 / 5.7           # M6 ran in the M4 family at tau=5.7
    r = np.roots([-1.0, 0.0, lam - k3 - k4, k1])
    u0 = sorted(x.real for x in r if abs(x.imag) < 1e-9)[0]
    act = _mk_act(lam, k1, (k3 + k4) * u0, u0, Du)
    THR = u0 + 0.45 * (np.sqrt(lam) - u0)
    return dict(
        id=f"ref_BFIELD_g{gamma}",
        acts=[act],
        chans=[dict(tau=tau, D=Dv, g="id", thr=0.0, sc=1.0),            # v
               dict(tau=theta, D=Dw, g="id", thr=0.0, sc=1.0),          # w
               dict(tau=tau_b, D=D_b, g="tanh", thr=float(THR - u0), sc=0.4)],  # b
        W=[[1.0], [1.0], [gamma]],
        K=[[k3, k4, 0.0]],
        bilin=[[0, 2, 1, 1.0]],
        provenance=dict(kind="reference", source="M6 bfield s2 point",
                        orig=dict(gamma=gamma, tau_b=tau_b, D_b=D_b, tau=tau)))


REFS = dict(M0=ref_M0, VVW=ref_VVW, XV=ref_XV, BFIELD=ref_BFIELD, M4=ref_M4)


# ---------------------------------------------------------- tracking (verbatim)
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
    remap = {}
    k = 0
    for i in range(1, n + 1):
        r = _find(parent, i)
        if r not in remap:
            k += 1
            remap[r] = k
    lut = np.zeros(n + 1, dtype=lab.dtype)
    for i in range(1, n + 1):
        lut[i] = remap[_find(parent, i)]
    return lut[lab], k


def blob_list(u, thr, dx, L):
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
        self.L = L
        self.ref = ref_pos
        self.prev = None
        self.prev_raw = None

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
            used = set(); idx = []
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


# ------------------------------------------------------------------- IC helpers
def state_vacuum(g, N):
    na, nc = len(g["acts"]), len(g["chans"])
    F = np.zeros((na + nc, N, N))
    for i, a in enumerate(g["acts"]):
        F[i] += a["u0"]
    return F


def poke(F, g, act, x, y, amp, sig, dx):
    """Gaussian bump on activator `act` (periodic); channels untouched (vacuum)."""
    N = F.shape[1]
    L = N * dx
    c = (np.arange(N) + 0.5) * dx
    dy = min_image(c - y, L)[:, None]
    dxx = min_image(c - x, L)[None, :]
    F[act] += amp * np.exp(-(dy ** 2 + dxx ** 2) / (2 * sig ** 2))
    return F


def fshift(a, dy_px, dx_px):
    if abs(dy_px) < 1e-12 and abs(dx_px) < 1e-12:
        return a
    n0, n1 = a.shape
    ky = np.fft.fftfreq(n0)[:, None]
    kx = np.fft.rfftfreq(n1)[None, :]
    ph = np.exp(-2j * np.pi * (ky * dy_px + kx * dx_px))
    return np.fft.irfft2(np.fft.rfft2(a) * ph, s=a.shape)


def paste_stamp(F, stamp_fields, field_idx, x, y, dx):
    """Paste deviation stamps at physical (x,y), sub-pixel exact.
    stamp_fields: {name: 2D array}; field_idx: {name: target field index}."""
    N = F.shape[1]
    arr0 = next(iter(stamp_fields.values()))
    ns = arr0.shape[0]
    cy = ns // 2
    gy, gx = y / dx, x / dx
    iy, ix = int(round(gy)) % N, int(round(gx)) % N
    fy, fx = gy - round(gy), gx - round(gx)
    ys = (np.arange(ns) - cy + iy) % N
    xs = (np.arange(ns) - cy + ix) % N
    for name, fi in field_idx.items():
        F[fi][np.ix_(ys, xs)] += fshift(stamp_fields[name], fy, fx)
    return F


def load_stamp_A4():
    pth = os.path.join(CDATA, "stamp_A4_dx05.npz")
    stf = np.load(pth)
    return dict(du=stf["du"], dv=stf["dv"], dw=stf["dw"], u0=float(stf["u0"]))


# ------------------------------------------------------------------- simulator
def run_genome(g, F=None, L=96.0, dx=0.5, dt=0.02, T=500.0, noise=0.0, seed=0,
               rec_tu=5.0, thr_frac=0.45, track_acts=None, snap_times=(),
               stop_all_dead=True, stop_explode_n=None, save_fields=False,
               ref_pos=None):
    """Integrate genome g from state F (default vacuum). Per-activator tracking.
    Returns dict with per-act series pos{i}/area{i}/peak{i}/ncomp{i}, status, wall_s.
    stop_explode_n: early-exit status='replicated' if any tracked act's ncomp >= n
    at a record with t>10. stop_all_dead: status='died' if all tracked ncomp==0."""
    t0_wall = time.time()
    na, nc = len(g["acts"]), len(g["chans"])
    N = int(round(L / dx))
    if F is None:
        F = state_vacuum(g, N)
    F = np.array(F, float, copy=True)
    assert F.shape == (na + nc, N, N)
    W = np.asarray(g["W"], float)
    K = np.asarray(g["K"], float)
    bilin = [tuple(b) for b in g.get("bilin", [])]
    lam = np.array([a["lam"] for a in g["acts"]])[:, None, None]
    k1 = np.array([a["k1"] for a in g["acts"]])[:, None, None]
    u0s = np.array([a["u0"] for a in g["acts"]])
    tau_c = np.array([c["tau"] for c in g["chans"]])
    thr_a = np.array([a["u0"] + thr_frac * (np.sqrt(max(a["lam"], 1e-9)) - a["u0"])
                      for a in g["acts"]])
    steps = int(round(T / dt))
    rec = max(int(round(rec_tu / dt)), 1)
    kf = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    kr = 2 * np.pi * np.fft.rfftfreq(N, d=dx)
    k2 = kf[:, None] ** 2 + kr[None, :] ** 2
    Ds = np.array([a["Du"] for a in g["acts"]] + [c["D"] for c in g["chans"]])
    E = np.exp(-Ds[:, None, None] * k2[None] * dt)
    id_mask = np.array([c["g"] == "id" for c in g["chans"]])
    thr_ch = np.array([c.get("thr", 0.0) for c in g["chans"]])
    sc_ch = np.array([c.get("sc", 1.0) for c in g["chans"]])
    rng = np.random.default_rng(seed)
    sq = np.sqrt(dt)
    if track_acts is None:
        track_acts = list(range(na))
    trackers = {i: Tracker(L, ref_pos=(ref_pos or {}).get(i)) for i in track_acts}
    ts = []
    series = {i: dict(pos=[], area=[], peak=[], ncomp=[]) for i in track_acts}
    snaps = {}
    snap_left = sorted(snap_times)
    status = "ok"
    for t in range(steps + 1):
        tt = t * dt
        if t % rec == 0 or t == steps:
            if not np.isfinite(F).all():
                status = "blowup"
                break
            ncs_now = {}
            for i in track_acts:
                bl = blob_list(F[i], thr_a[i], dx, L)
                unw, ar, pk = trackers[i].update(bl)
                series[i]["pos"].append(unw)
                series[i]["area"].append(ar)
                series[i]["peak"].append(pk)
                series[i]["ncomp"].append(len(bl))
                ncs_now[i] = len(bl)
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
        Z = U - u0s[:, None, None]                      # activator deviations
        R = np.empty_like(F)
        KX = np.einsum("ic,cyx->iyx", K, X)
        RU = lam * U - U ** 3 + k1 - KX
        for (i, c, c2, coef) in bilin:
            RU[i] -= coef * X[c] * X[c2]
        R[:na] = RU
        for c in range(nc):
            if id_mask[c]:
                drive = np.einsum("a,ayx->yx", W[c], Z)
            else:
                drive = np.zeros((N, N))
                for a in range(na):
                    if W[c, a] != 0.0:
                        drive += W[c, a] * np.tanh(
                            np.clip(Z[a] - thr_ch[c], 0.0, None) / sc_ch[c])
            R[na + c] = (drive - X[c]) / tau_c[c]
        Fn = F + dt * R
        if noise > 0:
            Fn[:na] += noise * sq * rng.standard_normal((na, N, N))
        F = np.fft.irfft2(np.fft.rfft2(Fn) * E, s=(N, N))
    wall = time.time() - t0_wall
    out = dict(status=status, dt=dt, dx=dx, L=L, N=N, t=np.array(ts),
               thr=thr_a.tolist(), wall_s=wall,
               tu_per_s=(ts[-1] / wall if wall > 0 and ts else None),
               snaps=snaps, fields=F if save_fields else None)
    for i in track_acts:
        s = series[i]
        out[f"pos{i}"] = s["pos"]
        out[f"area{i}"] = s["area"]
        out[f"peak{i}"] = s["peak"]
        out[f"ncomp{i}"] = np.array(s["ncomp"], int)
    return out


# ------------------------------------------------------------------ results IO
def append_result(record, path=None):
    import fcntl
    path = path or os.path.join(L0DIR, "results.json")
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
            json.dump(data, f)
        os.replace(tmp, path)
    return len(data)


def genome_json(g):
    """JSON-safe copy (numpy -> lists/floats)."""
    def conv(o):
        if isinstance(o, dict):
            return {k: conv(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [conv(v) for v in o]
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        return o
    return conv(g)
