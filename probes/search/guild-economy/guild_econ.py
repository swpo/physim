"""guild_econ.py — core simulation for the GUILD ECONOMY world search (v2).

Mechanism (one gene axis beyond E2): each cell carries allocation a in [0,1].
Fraction a of a fixed enzyme budget eats raw resource R (producing waste W
as byproduct, yield yW); fraction (1-a) eats waste W. LINEAR PRICES ONLY:
    income = kE*V*(cR*a*R + cW*(1-a)*W)
    rent   = m*V + m2*V*(pathway_R_on + pathway_W_on)   # m2 = expression
             overhead per ACTIVE pathway (on = share > eps); a linear price
             on pathway maintenance, not a curve.
Finite larder E<=cap*V; bankruptcy burns tissue; death below floor;
senescence hazard (turnover); copy inheritance + gaussian mutation on a;
establishment viability gate (child income at local prices must clear
gate*(m+overhead)).

Theory coordinates:
  rho     = cW/cR                (price ratio; W is worth rho x R)
  yW      = waste yield per unit R eaten
  leak    = dW/(0.3*kE)          (abiotic waste decay vs consumption scale)
  margin  = cR*kE/m              (producer income at R=1 in rents)
  sig_mut = mutation sd on a
  over    = m2/m                 (pathway overhead in rents; 0 = pure linear)
Mean-field top law (waste market clearing):
  Q_e/P_e = yW*rho - decay_correction  ->  fr_e = f(rho) demand curve.
"""
import numpy as np

KE = 0.02
M_RENT = 0.0036
EPS_PATH = 0.05


def lap(z):
    return (np.roll(z, 1, 0) + np.roll(z, -1, 0) +
            np.roll(z, 1, 1) + np.roll(z, -1, 1) - 4 * z)


def theory_to_raw(tc):
    p = dict(tc)
    p.setdefault("cap", 0.15)
    p.setdefault("DW", 0.06)
    p.setdefault("DR", 0.06)
    p.setdefault("r0", 0.004)
    p.setdefault("L", 64)
    p.setdefault("hazard", 7e-4)
    p.setdefault("gate", 1.1)
    p.setdefault("over", 0.0)
    p["kE"] = KE
    p["m"] = M_RENT
    p["cR"] = p["margin"] * p["m"] / p["kE"]
    p["cW"] = p["rho"] * p["cR"]
    p["dW"] = p["leak"] * p["kE"] * 0.30
    p["m2"] = p["over"] * p["m"]
    return p


def _paths(A):
    return (A > EPS_PATH).astype(float) + (A < 1 - EPS_PATH).astype(float)


def make_stepper(p, rng):
    """Returns step(state, t) closure. state = [V, E, R, W, A]."""
    cR, cW, kE, m, m2 = p["cR"], p["cW"], p["kE"], p["m"], p["m2"]
    yW, dW, r0 = p["yW"], p["dW"], p["r0"]
    DR, DW, cap, sig = p["DR"], p["DW"], p["cap"], p["sig_mut"]
    hazard, gate = p["hazard"], p["gate"]
    L = p["L"]

    def step(state):
        V, E, R, W, A = state
        uptR = kE * A * V * R
        uptW = kE * (1 - A) * V * W
        R += DR * lap(R) + r0 * (1 - R) - uptR
        np.clip(R, 0, 1, out=R)
        W += DW * lap(W) + yW * uptR - uptW - dW * W
        np.clip(W, 0, None, out=W)
        E += cR * uptR + cW * uptW - (m + m2 * _paths(A)) * V
        neg = E < 0
        V[neg] += E[neg] / 0.05            # bankruptcy burns tissue
        E[neg] = 0
        surplus = np.maximum(E - 0.04 * V, 0)
        used = 0.3 * surplus
        V += np.minimum(2.0 * used, 0.05) * (1 - V)
        np.clip(V, 0, 1, out=V)
        E -= used
        np.minimum(E, cap * V, out=E)      # finite larder
        hz = rng.random((L, L)) < hazard   # senescence turnover
        V[hz] = 0; E[hz] = 0
        dead = V < 0.05
        V[dead] = 0; E[dead] = 0
        alive = ~dead
        energetic = alive & (E > 0.02 * V)
        nEn = np.stack([np.roll(energetic, 1, 0), np.roll(energetic, -1, 0),
                        np.roll(energetic, 1, 1), np.roll(energetic, -1, 1)])
        can = (~alive) & nEn.any(0)
        noise = rng.normal(0, sig, (L, L))
        u = rng.random((L, L))
        if can.any():
            nEv = np.stack([np.roll(E, 1, 0), np.roll(E, -1, 0),
                            np.roll(E, 1, 1), np.roll(E, -1, 1)])
            nA4 = np.stack([np.roll(A, 1, 0), np.roll(A, -1, 0),
                            np.roll(A, 1, 1), np.roll(A, -1, 1)])
            A_par = np.take_along_axis(nA4, nEv.argmax(0)[None], 0)[0]
            child_a = np.clip(A_par + noise, 0.0, 1.0)
            pot = kE * (cR * child_a * R + cW * (1 - child_a) * W)
            need = gate * (m + m2 * _paths(child_a))
            pick = can & (pot > need) & (u < 0.10)
            if pick.any():
                V[pick] = 0.12; E[pick] = 0.02; A[pick] = child_a[pick]
        return state

    return step


def init_state(p, rng):
    L = p["L"]
    gx, gy = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
    V = np.zeros((L, L)); E = np.zeros((L, L))
    # start fields near marginal-viability prices so both guilds are viable
    # from t=0 (otherwise recyclers are wiped and must slowly re-invade)
    Rstar = min((1 + p["over"]) / p["margin"], 0.9)
    Wstar = Rstar / p["rho"]
    R = 0.6 * np.ones((L, L)); W = p.get("W0", Wstar) * np.ones((L, L))
    A = np.full((L, L), 0.5)
    founder_a = np.linspace(0.06, 0.94, 12)
    rng.shuffle(founder_a)
    for av in founder_a:
        cx, cy = rng.integers(6, L - 6, 2)
        mm = (gx - cx) ** 2 + (gy - cy) ** 2 <= 9
        V[mm] = 0.3; A[mm] = av; E[mm] = 0.5 * p["cap"] * 0.3
    return [V, E, R, W, A]


def macro(state):
    V, E, R, W, A = state
    alive = V > 0.05
    Vtot = float(V.sum())
    if Vtot < 1e-9:
        return dict(Vtot=0.0, ncell=0, fr_e=np.nan, fr_b=np.nan,
                    fr_site=np.nan,
                    P_e=0.0, Q_e=0.0, Rm=float(R.mean()), Wm=float(W.mean()),
                    purity=np.nan)
    P_e = float((A * V).sum()); Q_e = float(((1 - A) * V).sum())
    return dict(Vtot=Vtot, ncell=int(alive.sum()),
                fr_e=Q_e / (P_e + Q_e),
                fr_b=float(V[A < 0.5].sum() / Vtot),
                fr_site=float(((A < 0.5) & alive).sum() / alive.sum()),
                P_e=P_e, Q_e=Q_e, Rm=float(R.mean()), Wm=float(W.mean()),
                purity=float((np.abs(A - 0.5) * V).sum() / Vtot * 2))


def bimodality(A, V, nbins=20):
    """V-weighted allocation histogram valley test."""
    alive = V > 0.05
    if alive.sum() < 20:
        return {"bimod": 0.0, "share_lo": 0.0, "share_hi": 0.0}
    h, _ = np.histogram(A[alive], bins=nbins, range=(0, 1), weights=V[alive])
    h = h / h.sum()
    lo_pk = h[:7].max(); hi_pk = h[13:].max(); valley = h[7:13].min()
    bimod = 1.0 - valley / max(min(lo_pk, hi_pk), 1e-9)
    return {"bimod": float(max(bimod, 0.0)),
            "share_lo": float(h[:10].sum()), "share_hi": float(h[10:].sum())}


def contact_enrichment(A, V):
    """P(mixed guild adjacency) / expectation under random mixing."""
    alive = V > 0.05
    g = np.where(alive, (A < 0.5).astype(int), -1)
    pairs_mixed = pairs_alive = 0
    for ax, sh in ((0, 1), (1, 1)):
        a1 = g; a2 = np.roll(g, sh, ax)
        both = (a1 >= 0) & (a2 >= 0)
        pairs_alive += both.sum()
        pairs_mixed += ((a1 != a2) & both).sum()
    fr = (g == 1).sum() / max(alive.sum(), 1)
    exp_mix = 2 * fr * (1 - fr)
    if pairs_alive == 0 or exp_mix < 1e-9:
        return None
    return float(pairs_mixed / pairs_alive / exp_mix)


def block_series(state, L, b=8):
    V, E, R, W, A = state
    Vb = V.reshape(L // b, b, L // b, b).sum((1, 3))
    Qb = ((1 - A) * V).reshape(L // b, b, L // b, b).sum((1, 3))
    return np.where(Vb > 1e-9, Qb / np.maximum(Vb, 1e-9), np.nan)


def block_tau(blocks, dt):
    """L2 timescale: median 1/e ACF time of block recycler-share series."""
    if len(blocks) < 30:
        return None
    arr = np.stack(blocks)
    taus = []
    for i in range(arr.shape[1]):
        for j in range(arr.shape[2]):
            x = arr[:, i, j]
            if np.isnan(x).any() or x.std() < 1e-4:
                continue
            x = x - x.mean()
            n = len(x)
            acf = np.correlate(x, x, "full")[n - 1:]
            acf /= acf[0]
            below = np.where(acf < 1 / np.e)[0]
            if len(below):
                taus.append(below[0] * dt)
    if len(taus) < 8:
        return None
    return float(np.median(taus))


def impulse_tau(p, state, which, seed, T=1200):
    """Micro (L1) timescale: twin-run field impulse decay, common noise."""
    rng1 = np.random.default_rng(seed + 777)
    rng2 = np.random.default_rng(seed + 777)
    s1 = [x.copy() for x in state]
    s2 = [x.copy() for x in state]
    if which == "R":
        s2[2] *= 0.90
    else:
        s2[3] = s2[3] * 1.10 + 0.02
    st1 = make_stepper(p, rng1)
    st2 = make_stepper(p, rng2)
    f = 2 if which == "R" else 3
    devs = [np.abs(s2[f] - s1[f]).mean()]
    for t in range(T):
        st1(s1); st2(s2)
        devs.append(np.abs(s2[f] - s1[f]).mean())
    devs = np.array(devs)
    d0 = devs[0]
    if d0 < 1e-12:
        return None
    below = np.where(devs < d0 / np.e)[0]
    if len(below) == 0:
        return float(T) * 2.0
    return float(below[0])
