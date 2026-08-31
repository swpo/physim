"""refpipes.py — Track A scripted REFERENCE PIPELINES (W2). No learning.

All pipelines consume ONLY the agent-facing surface (anonymous streams,
global mean/var, budget counters) + the announced contract specs. Truth
enters only in adequacy.py scoring.

R1 geometry bootstrap : corr->MDS embedding, adjacency graph, lattice class,
                        motion-basis recovery by interpolant matching.
R2 particulateness    : bimodality per port, s-event stats, blob size via
                        ring profile + dilation scan.
R3 closed-loop track  : P-controller on ring asymmetry in R1 coords.
R4 contracts          : P1 CRPS forecasts (persistence / AR2 / informed),
                        P2 event-rate forecast, P3 injection response.
"""
import numpy as np
from scipy.interpolate import RBFInterpolator

CTRL_TU = 5.0
MAX_STEP = 1.5


# ------------------------------------------------------------------ helpers
def classical_mds(D, ndim=2):
    D = np.asarray(D, float)
    k = len(D)
    D2 = D ** 2
    J = np.eye(k) - np.ones((k, k)) / k
    B = -0.5 * J @ D2 @ J
    w, V = np.linalg.eigh(B)
    idx = np.argsort(w)[::-1][:ndim]
    w = np.clip(w[idx], 0, None)
    return V[:, idx] * np.sqrt(w)[None, :]


def corr_to_dist(C):
    """Chordal correlation distance: sqrt(2(1-r)). Monotone in true distance
    for smooth decaying correlations; ~ d/ell at short range (the range that
    matters — long distances get fixed by the geodesic step)."""
    d = np.sqrt(np.clip(2.0 * (1.0 - C), 0.0, None))
    np.fill_diagonal(d, 0.0)
    return d


def geodesic_mds(D, n_nn=4, ndim=2):
    """Isomap-lite: kNN graph on D, shortest paths, classical MDS."""
    from scipy.sparse.csgraph import shortest_path
    k = len(D)
    Wg = np.full((k, k), np.inf)
    for i in range(k):
        order = np.argsort(D[i])
        for j in order[1:n_nn + 1]:
            Wg[i, j] = Wg[j, i] = D[i, j]
    Gd = shortest_path(Wg, method="D", directed=False)
    if not np.isfinite(Gd).all():
        Gd = np.where(np.isfinite(Gd), Gd, D * 2.0)
    return classical_mds(Gd, ndim)


def gap_adjacency(Dm, max_deg=6, gamma=1.30):
    """Adjacency from a raw distance matrix: per-node largest-relative-gap
    neighbor cut, union-symmetrized, then filtered by pairwise-normalized
    edge length (edge <= gamma * geomean of the two nodes' NN distances)."""
    k = len(Dm)
    A = np.zeros((k, k), bool)
    for i in range(k):
        order = np.argsort(Dm[i])
        order = order[order != i]
        v = Dm[i][order]
        best_j, best_gap = 1, 0.0
        for j in range(1, min(max_deg, len(v) - 1) + 1):
            g = (v[j] - v[j - 1]) / max(v[j - 1], 1e-12)
            if g > best_gap:
                best_gap, best_j = g, j
        A[i, order[:best_j]] = True
    dmin = np.where(np.eye(k, dtype=bool), np.inf, Dm).min(1)
    lim = gamma * np.sqrt(dmin[:, None] * dmin[None, :])
    return (A | A.T) & (Dm <= lim)


def classify_lattice(X, adj, center=None):
    """{tri,square,hex} from interior-node degrees + edge angle structure.
    Uses the center node (max degree in a >=2-ring patch is interior)."""
    deg = adj.sum(1)
    if deg.max() == 0:
        return "unknown"
    i = int(center if center is not None else np.argmax(deg))
    if deg[i] < 2:
        i = int(np.argmax(deg))
    nb = np.nonzero(adj[i])[0]
    v = X[nb] - X[i]
    ang = np.sort(np.arctan2(v[:, 0], v[:, 1]))
    gaps = np.degrees(np.diff(np.concatenate([ang, [ang[0] + 2 * np.pi]])))
    gaps = gaps[gaps > 15.0]           # merge near-duplicate directions
    n_dir = len(gaps)
    # vote: number of distinct NN directions at the most-connected node
    by_dir = {6: "hex", 4: "square", 3: "tri"}.get(n_dir)
    # second vote: max interior degree
    by_deg = {6: "hex", 4: "square", 3: "tri"}.get(int(deg.max()))
    if by_dir and by_deg == by_dir:
        return by_dir
    return by_dir or by_deg or "unknown"


def gauss_crps(mu, sig, y):
    """CRPS of N(mu, sig^2) forecasts vs obs y (elementwise)."""
    sig = np.maximum(np.asarray(sig, float), 1e-6)
    z = (np.asarray(y, float) - mu) / sig
    from scipy.stats import norm
    return sig * (z * (2 * norm.cdf(z) - 1) + 2 * norm.pdf(z)
                  - 1.0 / np.sqrt(np.pi))


# -------------------------------------------------------------- observation
class History:
    """Read log: irregular times, streams (n_ports, k) per device."""

    def __init__(self):
        self.t = []
        self.streams = []          # list of {dev: (nf,k)}
        self.glob = []             # (nf,2)

    def add(self, obs):
        s0 = next(iter(obs["streams"].values()))
        if s0 is None or not np.isfinite(np.asarray(s0)).any():
            return False
        self.t.append(obs["t"])
        self.streams.append({d: np.array(v) for d, v in obs["streams"].items()})
        self.glob.append(np.array(obs["global_stats"]))
        return True

    def mat(self, dev):
        """(T, nf, k) matrix of reads for device dev."""
        return np.stack([s[dev] for s in self.streams])

    def times(self):
        return np.asarray(self.t)


def burst_schedule(i0, i1, n_reads, burst=10):
    """Read indices: bursts of `burst` consecutive steps spread over [i0,i1)."""
    n_reads = max(int(n_reads), 0)
    if n_reads <= 0:
        return set()
    nb = max(n_reads // burst, 1)
    reads = set()
    starts = np.linspace(i0, max(i1 - burst, i0), nb).astype(int)
    for s in starts:
        for j in range(burst):
            if s + j < i1 and len(reads) < n_reads:
                reads.add(s + j)
    return reads


# ============================================================ R1: geometry
def r1_geometry(env, hist, dev, probe_cfg=None):
    """Passive part: embedding + adjacency + lattice from history reads.
    Returns state dict; motion probe done separately (needs live control)."""
    M = hist.mat(dev)                       # (T, nf, k)
    nf, k = M.shape[1], M.shape[2]
    tarr = hist.times()
    # frame-to-frame diffs within consecutive-read bursts
    dt = np.diff(tarr)
    consec = dt <= CTRL_TU + 1e-6
    dM = (M[1:] - M[:-1])[consec]           # (Td, nf, k)
    Ds, ws = [], []
    port_q = np.zeros(nf)
    for p in range(nf):
        for A in (dM[:, p, :], M[:, p, :] - M[:, p, :].mean(0)):
            if len(A) < 8 or A.std() < 1e-6:
                continue
            C = np.corrcoef(A.T)
            if not np.isfinite(C).all():
                continue
            off = C[~np.eye(k, dtype=bool)]
            rng_q = off.max() - off.min()
            med = np.median(off)
            # informative: structured (range) + mostly-positive short-range
            # correlations, not saturated (all ~1 = smooth global mode)
            q = rng_q * (off > 0.05).mean()
            if med > 0.985 or rng_q < 0.05:
                q = 0.0
            port_q[p] = max(port_q[p], q)
            if q > 0:
                d = corr_to_dist(C)
                Ds.append(d / np.median(d[d > 0]))
                ws.append(q)
    if not Ds:
        return dict(ok=False, why="no informative port")
    D = np.average(np.stack(Ds), axis=0, weights=ws)
    D = 0.5 * (D + D.T)
    X = geodesic_mds(D)
    adj = gap_adjacency(D)
    # center stream = max correlation-degree node (min mean distance)
    center = int(np.argmin(D.mean(1)))
    lat = classify_lattice(X, adj, center=center)
    Xc = X - X[center]
    nn_emb = np.linalg.norm(Xc[:, None] - Xc[None, :], axis=2)
    np.fill_diagonal(nn_emb, np.inf)
    return dict(ok=True, X=Xc, D=D, adj=adj, lattice=lat, center=center,
                nn_scale=float(nn_emb.min()), port_q=port_q,
                n_diff=int(len(dM)))


def port_contrast(s, ports):
    """Spatial structure metric: max over ports of node std / (|median|+1)."""
    vals = []
    for p in ports:
        v = s[p]
        if np.isfinite(v).all():
            vals.append(v.std())
    return max(vals) if vals else 0.0


def r1_seek_structure(env, r1, dev, hist_contrast, max_steps=4,
                      thresh_q=0.75, ledger=None):
    """Walk (anonymous axis alternation) until local spatial structure is in
    view: port contrast > quantile of history contrasts. Returns spend."""
    q = r1["port_q"]
    ports = [int(p) for p in np.argsort(q)[::-1][:3] if q[p] > 0]
    thr = np.quantile(hist_contrast, thresh_q) if len(hist_contrast) else 0.0
    spend = dict(reads=0, motion=0.0)
    dirs = [np.array([1.5, 0.0]), np.array([0.0, 1.5]),
            np.array([1.5, 0.0]), np.array([0.0, -1.5])]
    obs = env.step({}, read=True)
    spend["reads"] += 1
    if port_contrast(np.array(obs["streams"][dev]), ports) >= thr:
        return spend, True
    i = 0
    while i < max_steps:
        d = dirs[(i // 3) % len(dirs)]
        obs = env.step({dev: dict(move=tuple(d))}, read=True)
        if not obs["rejected"] and ledger is not None:
            ledger.append(np.array(d))
        spend["reads"] += 1
        spend["motion"] += float(np.abs(d).sum())
        c = port_contrast(np.array(obs["streams"][dev]), ports)
        if c >= thr:
            return spend, True
        i += 1
    return spend, False


def r1_motion_probe(env, r1, dev, n_rep=2, dm=1.5, hist=None,
                    max_env_steps=None):
    """Recover motion basis B_emb (action units -> embedding displacement).
    Per rep and axis: measure world drift with a hold-still pair, then probe
    legs [+dm,-dm,-dm,+dm]; each successful leg yields (est - drift)*sg/dm.
    Legs fail independently (no all-or-nothing). dm adapts down (halves)
    when legs fail from decorrelation (fast/striped worlds: E2 lesson).
    Returns (B or None, quality, spend)."""
    X = r1["X"]
    spend = dict(reads=0, motion=0.0, steps=0)
    q = r1["port_q"]
    ports = [int(p) for p in np.argsort(q)[::-1][:4] if q[p] > 0]
    hist_contrast = []
    if hist is not None:
        M = hist.mat(dev)
        for j in range(len(M)):
            hist_contrast.append(port_contrast(M[j], ports))
    hist_contrast = np.asarray(hist_contrast)
    ledger = getattr(env, "_move_ledger", None)

    def seek():
        sk, found = r1_seek_structure(env, r1, dev, hist_contrast,
                                      ledger=ledger)
        spend["reads"] += sk["reads"]
        spend["motion"] += sk["motion"]
        spend["steps"] += sk["reads"]
        return found

    ests = [[], []]
    wq = [[], []]
    dm_cur = dm
    for rep in range(n_rep):
        for axis in range(2):
            if max_env_steps is not None and                     spend["steps"] + 12 > max_env_steps:
                break
            seek()
            obs = env.step({}, read=True)
            spend["reads"] += 1
            spend["steps"] += 1
            s_prev = np.array(obs["streams"][dev])
            # hold-still drift pair
            obs = env.step({}, read=True)
            spend["reads"] += 1
            spend["steps"] += 1
            s_cur = np.array(obs["streams"][dev])
            drift, dq = _match_shift(X, s_prev, s_cur, ports, r1["nn_scale"])
            if drift is None:
                drift = np.zeros(2)
            s_prev = s_cur
            legs = []
            signs = (+1.0, -1.0, -1.0, +1.0)
            for sg in signs:
                a = np.zeros(2)
                a[axis] = sg * dm_cur
                obs = env.step({dev: dict(move=tuple(a))}, read=True)
                if not obs["rejected"] and ledger is not None:
                    ledger.append(a.copy())
                spend["reads"] += 1
                spend["motion"] += dm_cur
                spend["steps"] += 1
                s_cur = np.array(obs["streams"][dev])
                est, qual = _match_shift(X, s_prev, s_cur, ports,
                                         r1["nn_scale"])
                legs.append((sg, est, qual))
                s_prev = s_cur
            n_fail = sum(1 for _, e, _q in legs if e is None)
            if n_fail == 0:
                # signed sum cancels LINEAR drift exactly (best when the
                # world moves steadily: E3 swarm lesson)
                comb = sum(sg * e for sg, e, _q in legs) / 4.0
                ests[axis].append(comb / dm_cur)
                wq[axis].append(float(np.mean([q_ for _, _, q_ in legs])))
            else:
                for sg, e, q_ in legs:      # per-leg salvage (E2 lesson)
                    if e is not None:
                        ests[axis].append(sg * (e - drift) / dm_cur)
                        wq[axis].append(0.5 * q_)
            if n_fail >= 3 and dm_cur > 0.4:
                dm_cur *= 0.5            # decorrelation: smaller steps
    B = np.zeros((2, 2))
    okq = []
    for axis in range(2):
        if len(ests[axis]) >= 1:
            E = np.stack(ests[axis])
            B[:, axis] = np.median(E, axis=0)     # robust to drift outliers
            if len(E) >= 2:
                mad = np.median(np.abs(E - B[:, axis][None, :]))
                scale = np.linalg.norm(B[:, axis]) + 1e-12
                consistency = float(np.clip(1.0 - mad / scale, 0.0, 1.0))
            else:
                consistency = 0.8                 # single clean combination
            okq.append(consistency * float(np.mean(wq[axis])))
    qual = float(np.mean(okq)) if okq else 0.0
    ok = (len(okq) == 2 and np.abs(np.linalg.det(B)) > 1e-9
          and qual > 0.05)
    return (B if ok else None), qual, spend


def _match_shift(X, s0, s1, ports, nn_scale, n_iter=4):
    """Displacement est with s1(node) ~ interp_s0(X + est): iterated
    Lucas-Kanade on RBF interpolants (linearize, LSQ over nodes+ports,
    re-evaluate). est = device displacement in EMBEDDING coordinates
    (derivation: X = s Ro p, sensor at world c+p reads f(c+p); after device
    move d it reads f(c+d+p) = interp_s0(X + s Ro d))."""
    itps, chans = [], []
    for p in ports:
        f0, f1 = s0[p], s1[p]
        if f0.std() < 3e-3 or not (np.isfinite(f0).all()
                                   and np.isfinite(f1).all()):
            continue
        # pattern persistence: consecutive reads must correlate (rejects
        # white-noise ports and fields that decorrelate within one step)
        c01 = np.corrcoef(f0, f1)[0, 1]
        if not np.isfinite(c01) or c01 < 0.6:
            continue
        try:
            itp = RBFInterpolator(X, f0, kernel="thin_plate_spline",
                                  smoothing=1e-8)
        except Exception:
            continue
        itps.append(itp)
        chans.append(p)
    if not itps:
        return None, 0.0
    # interior evaluation mask (avoid TPS extrapolation)
    Rpatch = np.linalg.norm(X, axis=1).max() * 0.75 + 1e-9
    inner = np.linalg.norm(X, axis=1) <= Rpatch
    if inner.sum() < 5:
        inner = np.ones(len(X), bool)
    h = 0.05 * nn_scale
    delta = np.zeros(2)
    err0 = None
    for it in range(n_iter):
        G_rows, r_rows = [], []
        for itp, p in zip(itps, chans):
            Q = X[inner] + delta
            f_pred = itp(Q)
            gy = (itp(Q + [h, 0.0]) - itp(Q - [h, 0.0])) / (2 * h)
            gx = (itp(Q + [0.0, h]) - itp(Q - [0.0, h])) / (2 * h)
            resid = s1[p][inner] - f_pred
            w = 1.0 / max(s1[p][inner].std(), 1e-6)
            G_rows.append(np.stack([gy, gx], 1) * w)
            r_rows.append(resid * w)
            if it == 0 and err0 is None:
                err0 = 0.0
            if it == 0:
                err0 += float(((resid * w) ** 2).sum())
        G = np.concatenate(G_rows)
        rvec = np.concatenate(r_rows)
        try:
            step, *_ = np.linalg.lstsq(G, rvec, rcond=None)
        except np.linalg.LinAlgError:
            return None, 0.0
        step = np.clip(step, -nn_scale, nn_scale)
        delta = delta + step
        if np.linalg.norm(delta) > 3.0 * nn_scale:
            return None, 0.0
        if np.linalg.norm(step) < 1e-3 * nn_scale:
            break
    # quality: residual reduction vs no shift
    err1 = 0.0
    for itp, p in zip(itps, chans):
        resid = s1[p][inner] - itp(X[inner] + delta)
        w = 1.0 / max(s1[p][inner].std(), 1e-6)
        err1 += float(((resid * w) ** 2).sum())
    gain = 1.0 - err1 / max(err0, 1e-12)
    if gain < 0.10:
        return None, 0.0
    return delta, float(gain)


# ------------------------------------------------- R1b: dilation radial probe
def r1_dilation_probe(env, r1, dev, n_cyc=2, dg=0.12, spread=3):
    """Radial structure from dilation wiggles. Cycle [+dg,-dg,-dg,+dg]:
    signed sum of stream deltas cancels field drift, leaves 4*dg*r_i*grad_r f.
    |resp| averaged over cycles+ports ranks nodes by RADIUS. Returns dict:
    rho (k,), center, rings (label per node), ring_radii, lattice_vote,
    spend. Ends at the starting dilation."""
    X = r1["X"]
    k = X.shape[0]
    q = r1["port_q"]
    ports = [int(p) for p in np.argsort(q)[::-1][:5] if q[p] > 0]
    spend = dict(reads=0, motion=0.0)
    signs = (+1.0, -1.0, -1.0, +1.0)
    logacc = np.zeros(k)
    wacc = 0.0
    for cyc in range(n_cyc):
        obs = env.step({}, read=True)
        spend["reads"] += 1
        s_prev = np.array(obs["streams"][dev])
        for sg in signs:
            obs = env.step({dev: dict(dilate=sg * dg)}, read=True)
            spend["reads"] += 1
            spend["motion"] += dg
            s_cur = np.array(obs["streams"][dev])
            if cyc == 0 and sg == signs[0]:
                legs = []
            legs.append((sg, s_cur - s_prev))
            s_prev = s_cur
        legs = legs[-4:]
        comb = sum(sg * d_ for sg, d_ in legs) / (4.0 * dg)   # (nf, k)
        for p in ports:
            v = np.abs(comb[p])
            if not np.isfinite(v).all():
                continue
            scale = np.median(v) + 1e-9
            logacc += np.log(v / scale + 1e-3)
            wacc += 1.0
        # decorrelate cycles: let the world move on (no reads, no cost)
        if cyc < n_cyc - 1:
            for _ in range(spread):
                env.step({}, read=False)
    if wacc == 0:
        return dict(ok=False, why="no dilation response", spend=spend)
    rho = np.exp(logacc / wacc)
    center = int(np.argmin(rho))
    # ring clustering on sorted rho: cut at largest relative gaps
    order = np.argsort(rho)
    vals = rho[order]
    # normalize so ring-1 ~ 1: first non-center cluster
    gaps = np.diff(np.log(vals[1:] + 1e-9))
    # number of rings unknown (2..5): choose cuts = largest gaps with
    # monotone-cluster constraint; simple approach: kmeans-like 1D split
    rings = _ring_cluster(vals)
    ring_lab = np.empty(k, int)
    ring_lab[order] = rings
    n_per = [int((ring_lab == j).sum()) for j in range(ring_lab.max() + 1)]
    ring_rad = [float(np.mean(rho[ring_lab == j]))
                for j in range(ring_lab.max() + 1)]
    # lattice vote from ring-1 coordination + radius ratio
    vote = None
    if len(n_per) >= 2:
        n1 = n_per[1]
        vote = {6: "hex", 4: "square", 3: "tri"}.get(n1)
        if len(n_per) >= 3 and ring_rad[1] > 0:
            ratio = ring_rad[2] / ring_rad[1]
            by_ratio = ("hex" if abs(ratio - np.sqrt(3)) <
                        abs(ratio - np.sqrt(2)) else "square")
            if vote is None:
                vote = by_ratio
    return dict(ok=True, rho=rho, center=center, ring_lab=ring_lab,
                n_per_ring=n_per, ring_radii=ring_rad, lattice_vote=vote,
                spend=spend)


def _ring_cluster(vals, max_rings=6):
    """1D clustering of sorted radial scores: cut at big relative gaps.
    vals sorted ascending. Returns ring index per sorted position."""
    n = len(vals)
    lv = np.log(vals + 1e-9)
    gaps = np.diff(lv)
    # candidate cuts: gaps above 60% of the max gap, at most max_rings-1
    thr = 0.35 * gaps.max()
    cuts = [i for i in np.argsort(gaps)[::-1] if gaps[i] >= thr]
    cuts = sorted(cuts[:max_rings - 1])
    rings = np.zeros(n, int)
    r = 0
    prev = 0
    for c in cuts:
        rings[prev:c + 1] = r
        r += 1
        prev = c + 1
    rings[prev:] = r
    return rings


def r1_refine_with_rings(r1, dil):
    """Fuse embedding angles with dilation radii: node i at radius
    ring_radii[ring(i)] (normalized so ring1 = embedding nn scale), angle
    from the embedding relative to the dilation center. Updates X, center,
    adj, lattice, nn_scale in a copy of r1."""
    X0 = r1["X"]
    c = dil["center"]
    Xc = X0 - X0[c]
    rho1 = dil["ring_radii"][1] if len(dil["ring_radii"]) > 1 else 1.0
    rr = np.asarray(dil["ring_radii"]) / max(rho1, 1e-9)
    ang = np.arctan2(Xc[:, 0], Xc[:, 1])
    rad = rr[dil["ring_lab"]]
    X = np.stack([rad * np.sin(ang), rad * np.cos(ang)], 1)
    X[c] = 0.0
    d = np.linalg.norm(X[:, None] - X[None, :], axis=2)
    np.fill_diagonal(d, np.inf)
    adj = gap_adjacency(np.where(np.isfinite(d), d, 0.0)
                        + np.where(np.isfinite(d), 0.0, 0.0))         if False else gap_adjacency(_finite(d))
    out = dict(r1)
    lat = dil.get("lattice_vote") or classify_lattice(X, adj, center=c)
    out.update(X=X, center=c, adj=adj, lattice=lat,
               nn_scale=float(d.min()), rings=dil["ring_lab"],
               dil_rho=dil["rho"])
    return out


def _finite(d):
    dd = d.copy()
    dd[~np.isfinite(dd)] = 0.0
    return dd


# ---------------------------------------------------- R1c: template snapping
TEMPLATES = {
    10: ("tri", (1, 3, 6)),
    13: ("square", (1, 4, 4, 4)),
    19: ("hex", (1, 6, 6, 6)),
    25: ("squareC", (1, 4, 4, 4, 8, 4)),
}


def template_offsets(k):
    """Canonical offsets for the k-node template, ring-major order."""
    from device import lattice_offsets
    lat, counts = TEMPLATES[k]
    n_rings = dict(tri=3, square=3, hex=3, squareC=3)[lat]
    offs = lattice_offsets(lat, n_rings)
    return lat, counts, offs


def rot2(theta, reflect=False):
    c, s = np.cos(theta), np.sin(theta)
    Rm = np.array([[c, -s], [s, c]])
    if reflect:
        Rm = Rm @ np.array([[1.0, 0.0], [0.0, -1.0]])
    return Rm


def lattice_symmetries(offs, tol=1e-6):
    """All O(2) ops (rotations+reflections on a fine grid) mapping the
    template point set to itself. Returns list of 2x2 matrices."""
    sym = []
    d0 = np.sort(np.linalg.norm(offs, axis=1))
    for refl in (False, True):
        for ang in np.arange(0, 360, 15) * np.pi / 180:
            Rm = rot2(ang, refl)
            Q = offs @ Rm.T
            # match Q to offs
            dd = np.linalg.norm(Q[:, None] - offs[None, :], axis=2)
            if (dd.min(1) < 1e-6).all():
                sym.append(Rm)
    return sym


def r1_template_snap(r1, dil, k):
    """Snap the geometry estimate to the k-node template (k is DISCLOSED as
    the per-port channel count — the pipeline hypothesizes the roster of
    standard patches). Node coords = geodesic embedding (angles + radii),
    center from dilation rho (fallback: embedding eccentricity); assignment
    by rotation/scale-scanned Hungarian matching on the embedding. Returns
    refined r1 dict incl. assign (stream slot -> canonical offset index)."""
    from scipy.optimize import linear_sum_assignment
    if k not in TEMPLATES:
        return None
    lat, counts, offs = template_offsets(k)
    radii_t = np.sort(np.unique(np.round(np.linalg.norm(offs, axis=1), 6)))
    center = int(dil["center"]) if (dil and dil.get("ok")) else r1["center"]
    Xc = r1["X"] - r1["X"][center]
    # normalize embedding scale: median node radius -> median template radius
    r_emb = np.linalg.norm(Xc, axis=1)
    scale0 = np.median(np.linalg.norm(offs, axis=1)) / max(
        np.median(r_emb), 1e-9)
    best = None
    for refl in (False, True):
        for a in np.arange(0, 360, 5) * np.pi / 180:
            Rm = rot2(a, refl)
            for sc in (0.85, 1.0, 1.18):
                T = (offs @ Rm.T)
                Xs = Xc * (scale0 * sc)
                cost = np.linalg.norm(Xs[:, None] - T[None, :], axis=2)
                # soft ring prior from dilation rho ranking
                if dil and dil.get("ok"):
                    rho = dil["rho"]
                    order = np.argsort(rho)
                    lab = np.empty(k, int)
                    i0 = 0
                    for j, cnt in enumerate(counts):
                        lab[order[i0:i0 + cnt]] = j
                        i0 += cnt
                    ringT = np.searchsorted(radii_t + 1e-6,
                                            np.linalg.norm(T, axis=1))
                    cost = cost + 0.35 * (
                        np.abs(ringT[None, :] - lab[:, None]))
                ri, ci = linear_sum_assignment(cost)
                c_tot = cost[ri, ci].sum()
                if best is None or c_tot < best[0]:
                    best = (c_tot, ci.copy())
    c_tot, assign = best
    X_snap = offs[assign]
    d = np.linalg.norm(X_snap[:, None] - X_snap[None, :], axis=2)
    np.fill_diagonal(d, np.inf)
    adj = d <= (d.min() + 1e-6)
    ring_snap = np.searchsorted(radii_t + 1e-6,
                                np.linalg.norm(X_snap, axis=1))
    out = dict(r1)
    out.update(X=X_snap, adj=adj, lattice=lat,
               center=int(np.argmin(np.linalg.norm(X_snap, axis=1))),
               nn_scale=float(d.min()), assign=assign,
               snap_cost=float(c_tot / k), rings=ring_snap)
    return out


# ======================================================= R2: particulateness
def bimodality_coeff(x):
    x = np.asarray(x, float).ravel()
    if x.std() < 1e-9:
        return 0.0
    z = (x - x.mean()) / x.std()
    n = len(z)
    skew = np.mean(z ** 3)
    kurt = np.mean(z ** 4)
    return (skew ** 2 + 1) / max(kurt, 1e-9)


def r2_particulate(hist, r1, dev):
    """Bimodality per port, event stats, blob-pass detection on center node.
    Polarity-aware: a port is flipped if its minority (excursion) side is
    LOW — localized objects are then dips; work with the flipped sign so
    'above thr' always means 'object present'. Event port = most bimodal
    with a MINORITY excursion (on_frac < 0.5 after polarity fix)."""
    M = hist.mat(dev)                        # (T, nf, k)
    nf, k = M.shape[1], M.shape[2]
    bim = np.zeros(nf)
    stats = []
    for p in range(nf):
        A = M[:, p, :]
        if A.std() < 1e-9:
            stats.append(None)
            continue
        z = (A - A.mean()) / A.std()
        skew = float(np.mean(z ** 3))
        sign = 1.0 if skew >= 0 else -1.0     # excursions on the heavy tail
        As = A * sign
        lo, hi = np.percentile(As, [5, 99])
        thr = 0.5 * (lo + hi)
        x = As > thr
        on_frac = float(x.mean())
        bim[p] = bimodality_coeff(A)
        stats.append(dict(sign=sign, thr=float(thr), on_frac=on_frac))
    # event port: bimodal, sparse-ON, with real crossings
    scores = np.full(nf, -1e9)
    for p in range(nf):
        if stats[p] is None:
            continue
        of = stats[p]["on_frac"]
        if of <= 1e-4 or of > 0.55:
            continue
        scores[p] = bim[p] - 0.3 * of
    p_ev = int(np.argmax(scores))
    if scores[p_ev] <= -1e8:
        p_ev = int(np.argmax(bim))
        if stats[p_ev] is None:
            stats[p_ev] = dict(sign=1.0, thr=0.0, on_frac=1.0)
    st = stats[p_ev]
    A = M[:, p_ev, :] * st["sign"]
    thr = st["thr"]
    x = A > thr
    up = (~x[:-1] & x[1:]).sum()
    on_frac = float(x.mean())
    cnt = x.sum(1)
    fano = float(cnt.var() / max(cnt.mean(), 1e-9))
    c = r1["center"] if r1.get("ok") else 0
    xc = A[:, c] > thr
    passes = int((~xc[:-1] & xc[1:]).sum())
    verdict = bool((bim.max() > 0.55) and (on_frac < 0.55) and (fano > 0.5)
                   and up >= 2)
    # per-port table (for track-port selection etc.)
    table = []
    T = M.shape[0]
    for p in range(nf):
        if stats[p] is None:
            table.append(None)
            continue
        Ap = M[:, p, :] * stats[p]["sign"]
        xp = Ap > stats[p]["thr"]
        n_up_pn = float((~xp[:-1] & xp[1:]).sum() / max(k * (T - 1), 1))
        table.append(dict(sign=stats[p]["sign"], thr=stats[p]["thr"],
                          on_frac=stats[p]["on_frac"], bim=float(bim[p]),
                          up_rate=n_up_pn))
    return dict(bim=bim, p_event=p_ev, sign=st["sign"], thr=float(thr),
                n_up=int(up), on_frac=on_frac, fano=fano,
                center_passes=passes, particulate=verdict, table=table)


def pick_track_port(r2, s_now=None):
    """Port for closed-loop tracking: bimodal, LOCALIZED (small on-frac),
    MOBILE (crossing rate); when a current read s_now (nf,k) is given,
    in-view signal breaks ties (scene-aware). Returns (port, sign, thr)."""
    best, out = -1e9, None
    for p, st in enumerate(r2.get("table") or []):
        if st is None:
            continue
        if not (0.003 <= st["on_frac"] <= 0.40):
            continue
        # coherent passages are RARE crossings; churn (noise) is frequent.
        up = st["up_rate"]
        sc = (st["bim"] + 3.0 * np.sqrt(min(up, 0.06))
              - 2.0 * max(up - 0.06, 0.0) - st["on_frac"])
        if s_now is not None and np.isfinite(s_now[p]).all():
            v = st["sign"] * s_now[p]
            if v.max() > st["thr"]:
                sc += 0.5                      # object in view right now
        if sc > best:
            best = sc
            out = (p, st["sign"], st["thr"])
    if out is None:
        out = (r2["p_event"], r2.get("sign", 1.0), r2["thr"])
    return out


class OnlineThreshold:
    """Running percentile threshold: thr = lo + blend*(hi-lo) over samples
    seen so far (window-capped), lo/hi = p5/p99.5. blend=0.7 keeps the
    threshold in the object CORE (mid-range sits in diffusive skirts —
    measured E1 failure mode: tracker locks onto skirt overlaps)."""

    def __init__(self, init_samples, cap=20000, blend=0.7):
        self.buf = list(np.asarray(init_samples, float).ravel()[-cap:])
        self.cap = cap
        self.blend = blend

    def update(self, samples):
        self.buf.extend(np.asarray(samples, float).ravel().tolist())
        if len(self.buf) > self.cap:
            self.buf = self.buf[-self.cap:]

    def thr(self):
        lo, hi = np.percentile(self.buf, [5, 99.5])
        return lo + self.blend * (hi - lo)


def r2_size_scan(env, r1, r2, dev, max_wait=40, scan=(-0.25, -0.25, 0.5, 0.25, 0.25)):
    """Wait for a blob on center node, then dilation-scan to estimate radius.
    Returns dict with radius in DILATION-SCALED ring units (agent units) +
    the log the evaluator converts with secret ds. Costs reads+motion."""
    X, c = r1["X"], r1["center"]
    ringR = np.linalg.norm(X - X[c], axis=1) / max(r1["nn_scale"], 1e-9)
    p, thr = r2["p_event"], r2["thr"]
    sgn = r2.get("sign", 1.0)
    spend = dict(reads=0, motion=0.0)
    hit_t = None
    for i in range(max_wait):
        obs = env.step({}, read=True)
        spend["reads"] += 1
        s = np.array(obs["streams"][dev]) * sgn
        if s[p, c] > thr:
            hit_t = obs["t"]
            break
    if hit_t is None:
        return dict(ok=False, why="no blob pass", spend=spend)
    profs = []       # (dilation_mult, profile)
    dil_mult = 1.0
    dil_net = 0.0
    for dg in (0.0,) + scan:
        act = {dev: dict(dilate=dg)} if dg else {}
        obs = env.step(act, read=True)
        spend["reads"] += 1
        spend["motion"] += abs(dg)
        if dg and not obs["rejected"]:
            dil_net += dg
        dil_mult = np.exp(dil_net)
        s = np.array(obs["streams"][dev]) * sgn
        if s[p, c] <= thr:
            break
        profs.append((dil_mult, s[p]))
    # restore dilation to pre-scan value (agent-side bookkeeping)
    if abs(dil_net) > 1e-9:
        obs = env.step({dev: dict(dilate=-dil_net)}, read=False)
        spend["motion"] += abs(dil_net)
    if not profs:
        return dict(ok=False, why="blob left", spend=spend)
    # half-max radius per profile, in units of (current spacing)*ring
    rads = []
    for mult, sp in profs:
        prof = sp - thr
        half = 0.5 * max(prof[c], 1e-9)
        rr = ringR * mult                       # node radius in base-ds units
        order = np.argsort(rr)
        rs, vs = rr[order], prof[order]
        # first crossing below half
        below = np.nonzero(vs < half)[0]
        if len(below) == 0 or below[0] == 0:
            continue
        j = below[0]
        r_half = np.interp(half, [vs[j], vs[j - 1]], [rs[j], rs[j - 1]])
        rads.append(r_half)
    if not rads:
        return dict(ok=False, why="profile flat", spend=spend)
    return dict(ok=True, t=hit_t, r_est_ds=float(np.median(rads)),
                n_prof=len(rads), port=int(p), spend=spend)


# ========================================================== R3: tracking
def r3_track(env, r1, r2, B_emb, dev, n_steps, duty=1.0, kp=0.8,
             coast_max=6, hist=None, blend=0.7, excursion_cap=22.0):
    """WATCH/TRACK state machine (validated on E1 cache, sweep 2026-08-31):
    WATCH: hold still until the track port shows a super-threshold pattern
           (threshold = p5 + blend*(p99.5-p5) online percentile — the CORE
           band; mid-range thresholds lock onto diffusive skirt overlaps).
    TRACK: P-controller (kp, deadband 0.2nn) on the intensity-weighted patch
           centroid with velocity lead + prediction-gated association
           (2.0nn) + coasting through dropouts (<=coast_max reads).
    Measured on E1 s928: once locked, same-blob retention ~100% over 750tu;
    acquisition waits for a passage (no reliable open-loop pursuit from
    >2 patch radii — an honest limitation, reported not hidden)."""
    X, c = r1["X"], r1["center"]
    s_now = None
    if hist is not None and len(hist.streams):
        s_now = np.asarray(hist.streams[-1][dev])
    p, sgn, thr0 = pick_track_port(r2, s_now=s_now)
    othr = OnlineThreshold([thr0 - 0.5, thr0 + 0.5], blend=blend)
    if hist is not None:
        othr = OnlineThreshold(sgn * hist.mat(dev)[:, p, :], blend=blend)
    thr = othr.thr()
    Binv = np.linalg.pinv(B_emb)
    every = max(int(round(1.0 / max(duty, 1e-6))), 1)
    log = dict(t=[], locked_read=[], err=[], state=[], spend_reads=0,
               spend_motion=0.0, port=int(p), sign=float(sgn))
    led = getattr(env, "_move_ledger", None)
    nn = r1["nn_scale"]
    Xc = X - X[c]

    state = "watch"
    vel = np.zeros(2)
    err = None
    last_err = None
    coast = 0
    a_net = np.zeros(2)          # net commanded displacement (control units)

    for i in range(n_steps):
        read = (i % every == 0) if state == "track" else True
        a = np.zeros(2)
        if state == "track" and err is not None:
            aim = err + vel                     # velocity lead
            if np.linalg.norm(aim) > 0.2 * nn:
                a = kp * (Binv @ aim)
        a = np.clip(a, -MAX_STEP, MAX_STEP)
        # leash: do not wander beyond excursion_cap net control units
        if np.linalg.norm(a_net + a) > excursion_cap:
            if np.dot(a, a_net) > 0:
                a = np.zeros(2)
        act = {dev: dict(move=tuple(a))} if np.abs(a).sum() > 1e-9 else {}
        obs = env.step(act, read=read)
        if act and not obs["rejected"]:
            log["spend_motion"] += float(np.abs(a).sum())
            a_net += a
            if led is not None:
                led.append(np.asarray(a, float).copy())
        if read:
            log["spend_reads"] += 1
            s = np.array(obs["streams"][dev])
            good = np.isfinite(s).all()
            if good:
                othr.update(sgn * s[p])
                thr = othr.thr()
            w = np.clip(sgn * s[p] - thr, 0.0, None) if good else None
            if w is not None and (w > 0).all():
                w = w - w.min()
            if w is not None and state == "track" and err is not None:
                pred = err + vel
                gate = np.exp(-np.linalg.norm(Xc - pred, axis=1) ** 2
                              / (2 * (2.0 * nn) ** 2))
                w = w * gate
            if w is not None and w.sum() > 1e-6:
                e = (w[:, None] * Xc).sum(0) / w.sum()
                if state == "track" and last_err is not None:
                    vel = 0.6 * vel + 0.4 * (e - last_err)
                if state == "watch":
                    vel = np.zeros(2)
                state = "track"
                last_err = e
                err = e
                coast = 0
                log["locked_read"].append((obs["t"], True))
            else:
                if state == "track":
                    coast += 1
                    if coast <= coast_max and last_err is not None:
                        err = last_err + vel * coast
                    else:
                        state = "watch"
                        err = None
                        last_err = None
                        vel = np.zeros(2)
                log["locked_read"].append((obs["t"], False))
        else:
            if err is not None:
                err = err + vel
        log["t"].append(obs["t"])
        log["err"].append(None if err is None else np.asarray(err).copy())
        log["state"].append(state)
    return log


# ====================================================== R4: contracts P1-P3
def _backtest_sigma(series, times, predictor, H, max_origins=20):
    """Backtest predictor at horizon H over the series; per-channel RMSE.
    Subsamples origins for tractability."""
    step = max(int(round(H / CTRL_TU)), 1)
    cand = [i for i in range(len(series) - step)
            if abs((times[i + step] - times[i]) - H) < 1e-6]
    if len(cand) > max_origins:
        cand = [cand[j] for j in
                np.linspace(0, len(cand) - 1, max_origins).astype(int)]
    errs = []
    for i in cand:
        mu = predictor(series[: i + 1])
        errs.append(series[i + step] - mu)
    if not errs:
        return None
    E = np.stack(errs)
    return np.sqrt((E ** 2).mean(0)) + 1e-4


def p1_persistence(hist, dev, horizons):
    M = hist.mat(dev)
    T, nf, k = M.shape
    S = M.reshape(T, nf * k)
    t = hist.times()
    out = {}
    for H in horizons:
        mu = S[-1]
        sig = _backtest_sigma(S, t, lambda s: s[-1], H)
        if sig is None:
            sig = S[-20:].std(0) + 1e-3
        out[H] = (mu, sig)
    return out


def _ar2_forecast(s, nstep):
    """Per-column AR(2) via least squares; forecast nstep ahead.
    Stationarity-clamped AND range-clamped (linear AR on short histories
    can still explode multiplicatively over long horizons)."""
    T, C = s.shape
    if T < 8:
        return s[-1]
    y = s[2:]
    A = np.stack([s[1:-1], s[:-2]], axis=2)         # (T-2, C, 2)
    mu = s.mean(0)
    yc = y - mu
    Ac = A - mu[None, :, None]
    out = np.empty(C)
    for cc in range(C):
        M_ = Ac[:, cc, :]
        try:
            coef, *_ = np.linalg.lstsq(M_, yc[:, cc], rcond=None)
        except np.linalg.LinAlgError:
            coef = np.array([1.0, 0.0])
        if abs(coef[0]) + abs(coef[1]) > 1.95:
            coef = coef / (abs(coef[0]) + abs(coef[1])) * 1.95
        x1, x2 = s[-1, cc] - mu[cc], s[-2, cc] - mu[cc]
        for _ in range(nstep):
            x1, x2 = coef[0] * x1 + coef[1] * x2, x1
        out[cc] = x1 + mu[cc]
    lo = s.min(0) - 3.0 * s.std(0) - 1e-6
    hi = s.max(0) + 3.0 * s.std(0) + 1e-6
    return np.clip(out, lo, hi)


def p1_ar2(hist, dev, horizons):
    M = hist.mat(dev)
    T, nf, k = M.shape
    S = M.reshape(T, nf * k)
    t = hist.times()
    dt_med = np.median(np.diff(t)) if len(t) > 1 else CTRL_TU
    out = {}
    for H in horizons:
        nstep = max(int(round(H / dt_med)), 1)
        mu = _ar2_forecast(S, nstep)
        sig = _backtest_sigma(S, t, lambda s: _ar2_forecast(s, nstep), H)
        if sig is None:
            sig = S[-20:].std(0) + 1e-3
        out[H] = (mu, sig)
    return out


def p1_informed(hist, dev, horizons, r1, track_log):
    """Geometry+tracking-informed: advect the last spatial pattern by the
    tracked target velocity (embedding units/tu). Self-gating: only used
    when the calibration is TRUSTED (snapped template + decent snap cost)
    and the measured velocity is significant; falls back to AR2 otherwise
    (measured: advection on a bad chart is catastrophically wrong)."""
    M = hist.mat(dev)
    T, nf, k = M.shape
    t = hist.times()
    ar2 = p1_ar2(hist, dev, horizons)
    if not r1.get("ok") or "assign" not in r1 or             r1.get("snap_cost", 9e9) > 0.9:
        return ar2
    errs = [(tt, e) for tt, e in zip(track_log["t"], track_log["err"])
            if e is not None]
    if len(errs) < 8:
        return ar2
    tt = np.array([e[0] for e in errs[-12:]])
    ee = np.stack([e[1] for e in errs[-12:]])
    if tt[-1] - tt[0] < 1e-9:
        return ar2
    v = np.polyfit(tt - tt[0], ee, 1)[0] if len(tt) >= 3 else np.zeros(2)
    # gate: displacement over the SHORTEST horizon within the chart, and
    # motion must exceed noise (fit residual)
    fit = np.polyval(np.polyfit(tt - tt[0], ee, 1), (tt - tt[0])[:, None])
    resid = float(np.sqrt(np.mean((ee - fit) ** 2)))
    disp_min = np.linalg.norm(v) * min(horizons)
    if disp_min < max(0.5 * r1["nn_scale"], 2.0 * resid) or             np.linalg.norm(v) * max(horizons) > 3.5 * r1["nn_scale"]:
        return ar2      # static target, noisy velocity, or off-chart advection
    X = r1["X"]
    s_last = M[-1]                        # (nf,k)
    out = {}
    for H in horizons:
        mu = np.empty((nf, k))
        for p in range(nf):
            try:
                itp = RBFInterpolator(X, s_last[p],
                                      kernel="thin_plate_spline",
                                      smoothing=1e-8)
                mu[p] = itp(X - v[None, :] * H)
            except Exception:
                mu[p] = s_last[p]
        mu = mu.reshape(-1)
        out[H] = (mu, ar2[H][1])
    return out


# ---------------------------------------------------------------- P2 events
def count_events(A, thr):
    """A (T,k) stream matrix; upward crossings per frame summed over nodes."""
    x = A > thr
    up = (~x[:-1] & x[1:])
    return up.sum(1)                       # (T-1,)


def p2_forecast(hist, dev, p_ev, thr, win_tu, n_win, duty, sign=1.0):
    """Predict event counts in the next n_win windows of win_tu.
    Returns dict variant -> (n_win,) predicted rates."""
    M = hist.mat(dev)
    t = hist.times()
    A = M[:, p_ev, :] * sign
    # windowed observed rates, duty-corrected (crossings need consecutive reads)
    dt = np.diff(t)
    consec = dt <= CTRL_TU + 1e-6
    x = A > thr
    up = (~x[:-1] & x[1:]).sum(1) * consec       # only trust consecutive pairs
    frames_per_win = max(int(round(win_tu / CTRL_TU)), 1)
    # windows over the observed span
    edges = np.arange(t[0], t[-1] + win_tu, win_tu)
    rates = []
    for w0, w1 in zip(edges[:-1], edges[1:]):
        sel = (t[:-1] >= w0) & (t[:-1] < w1)
        n_pairs = (sel & consec).sum()
        if n_pairs == 0:
            rates.append(np.nan)
        else:
            rates.append(up[sel].sum() * frames_per_win / n_pairs)
    rates = np.asarray(rates, float)
    valid = rates[np.isfinite(rates)]
    mean_r = float(valid.mean()) if len(valid) else 0.0
    last_r = float(valid[-1]) if len(valid) else 0.0
    # trend from last 6 valid windows
    out = {}
    out["persistence"] = np.full(n_win, last_r)
    out["mean"] = np.full(n_win, mean_r)
    if len(valid) >= 4:
        v = valid[-6:]
        slope = np.polyfit(np.arange(len(v)), v, 1)[0]
        out["informed"] = np.clip(last_r + slope * np.arange(1, n_win + 1),
                                  0, None)
    else:
        out["informed"] = out["persistence"]
    return out


# --------------------------------------------------------------- P3 response
def p3_template_predict(calib_resps, ann, n_frames, k, nf):
    """calib_resps: list of dicts(amp, dur, resp (T,nf,k) possibly with NaN
    rows for unread frames). ann: dict(amp, dur). Linear amplitude scaling."""
    if not calib_resps:
        return None
    T = n_frames
    acc = np.zeros((T, nf, k))
    wacc = np.zeros((T, 1, 1))
    for cr in calib_resps:
        scale = (ann["amp"] * ann["dur"]) / max(cr["amp"] * cr["dur"], 1e-9)
        R = cr["resp"][:T]
        m = np.isfinite(R[:, 0, 0])
        # fill missing frames by linear interpolation over time
        Rf = R.copy()
        idx = np.nonzero(m)[0]
        if len(idx) < 2:
            continue
        for j in range(T):
            if not m[j]:
                Rf[j] = Rf[idx[np.abs(idx - j).argmin()]]
        acc[:len(Rf)] += Rf * scale
        wacc[:len(Rf)] += 1.0
    if wacc.max() == 0:
        return None
    return acc / np.maximum(wacc, 1)
