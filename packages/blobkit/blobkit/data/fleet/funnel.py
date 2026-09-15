"""lib/funnel.py — G0 algebraic funnel (microseconds/candidate; order G0b->G0a->G0c).

G0b BISTABLE: each act's bare cubic -u^3+lam*u+k1 has 3 distinct real roots
    (disc = 4 lam^3 - 27 k1^2 > 0, lam > 0).
G0a VACUUM STABLE: J(k) of the full linearization about the designated vacuum
    (z_i = u_i-u0_i, x_c):
      dz_i/dt = (fu_i - Du_i k^2) z_i - sum_c K[i,c] x_c
      dx_c/dt = (sum_a W[c,a] gp_c z_a - x_c)/tau_c - D_c k^2 x_c
    gp_c = g_c'(0): 1 for g="id", 0 for g="tanh" with thr>0 (one-sided saturating
    deposit is DEAD at linear order — sampling REQUIRES thr>0 on tanh channels so
    the linear screens stay exact).
    margin = max over k in [0,kmax] of max Re eig J(k). PASS iff margin < 0.
    Near-zero margins (|margin| < 0.01) logged as "excitable shelf" (NOTE: a slow
    linearly-dead tanh channel contributes its trivial -1/tau_b eigenvalue, which
    can dominate the margin — flag is heuristic).
    ROOT POLICY (measured 2026-02-19, deviates from spec's "most-negative root"):
    u0 is a GENE. In deviation form u0 enters the channel drives g(u-u0), so each
    root designation is a DIFFERENT dynamical system — designation belongs to the
    SAMPLER, not the funnel. Measured: M0's certified vacuum -0.70354 is the
    MIDDLE root of its bare cubic (most-negative-root heuristic mis-designates,
    and best-margin designation gave wavelength 16.3 instead of the certified
    10.9). funnel(g) RESPECTS g's stored u0; enumerate_vacua()/pick_root() are
    sampler helpers.
G0c SPATIAL TAILS (per activator, self-block): steady modes e^{mu x}, s=mu^2:
      Du_i s + a_i - sum_c K[i,c] W[c,i] gp_c / (1 - A_c s) = 0,  A_c = tau_c D_c
    Polynomial in s of degree 1+n_id. mu = +-sqrt(s). Complex mu => oscillatory
    tails, shell wavelength 2 pi/|Im mu|; report the slowest-decaying oscillatory
    mode (min |Re mu| with Im!=0) and slowest real mode. Chemistry-candidate box:
    3 <= wavelength <= 30 and 0.1 <= |Re mu| <= 1.5 and oscillatory mode dominates
    (decays no more than 2x faster than the slowest monotone mode).
    VALIDATION: M4 (A=4) genome must predict shell wavelength 10.9 +- 0.3.
"""
import numpy as np

import genome as G

KMAX = 3.0
NK = 121
EXCITABLE_BAND = 0.01


def gprime0(ch):
    if ch["g"] == "id":
        return 1.0
    return 0.0          # tanh with thr>0: dead at linear order (enforced)


def g0b(g):
    """Bistability per act. Returns (passed, [disc_i])."""
    discs = []
    ok = True
    for a in g["acts"]:
        d = G.cubic_disc(a["lam"], a["k1"])
        discs.append(float(d))
        if not (a["lam"] > 0 and d > 0):
            ok = False
    return ok, discs


def jac_k(g, u0s, k):
    na, nc = len(g["acts"]), len(g["chans"])
    W = np.asarray(g["W"], float)
    K = np.asarray(g["K"], float)
    q = k * k
    J = np.zeros((na + nc, na + nc))
    for i, a in enumerate(g["acts"]):
        J[i, i] = a["lam"] - 3.0 * u0s[i] ** 2 - a["Du"] * q
        for c in range(nc):
            J[i, na + c] = -K[i, c]
    for c, ch in enumerate(g["chans"]):
        gp = gprime0(ch)
        for a in range(na):
            J[na + c, a] = W[c, a] * gp / ch["tau"]
        J[na + c, na + c] = -1.0 / ch["tau"] - ch["D"] * q
    return J


def g0a_margin(g, u0s=None, kmax=KMAX, nk=NK):
    """(margin, k_at_max) for the designated (or supplied) vacuum."""
    if u0s is None:
        u0s = [a["u0"] for a in g["acts"]]
    worst, kw = -np.inf, 0.0
    for k in np.linspace(0.0, kmax, nk):
        ev = np.linalg.eigvals(jac_k(g, u0s, k))
        m = float(ev.real.max())
        if m > worst:
            worst, kw = m, float(k)
    return worst, kw


def enumerate_vacua(g, kmax=KMAX, nk=NK, max_combos=9):
    """SAMPLER HELPER: u0 designation is a GENE. Enumerate joint root combos
    (exact for n_act<=2) with their G0a margins, sorted by margin (best first).
    Returns [(u0s, margin, k_at)] or None if any act lacks a real root."""
    roots_per_act = []
    for a in g["acts"]:
        rr = G.cubic_roots(a["lam"], a["k1"])
        if not rr:
            return None
        roots_per_act.append(rr)
    combos = [[]]
    for rr in roots_per_act:
        combos = [c + [r] for c in combos for r in rr]
        if len(combos) > max_combos:
            combos = combos[:max_combos]
    tried = []
    for u0s in combos:
        m, kw = g0a_margin(g, u0s, kmax, nk)
        tried.append((list(map(float, u0s)), float(m), float(kw)))
    tried.sort(key=lambda x: x[1])
    return tried


def g0c_tails(g, act):
    """Spatial-tail eigenvalues for activator `act` (self-block).
    Returns dict(osc=(re,im,wavelength)|None, mono_re|None, all_mu)."""
    a = g["acts"][act]
    afu = a["lam"] - 3.0 * a["u0"] ** 2
    Du = a["Du"]
    K = np.asarray(g["K"], float)
    W = np.asarray(g["W"], float)
    terms = []          # (KW_c, A_c) for linearly-alive channels with KW != 0
    for c, ch in enumerate(g["chans"]):
        kw = K[act, c] * W[c, act] * gprime0(ch)
        if kw != 0.0:
            terms.append((kw, ch["tau"] * ch["D"]))
    # P(s) = (Du s + a) prod(1 - A_c s) - sum_c KW_c prod_{c'!=c}(1 - A_c' s)
    def polymul(p, q):
        return np.polynomial.polynomial.polymul(p, q)
    base = np.array([afu, Du])                     # a + Du s (coef order: s^0, s^1)
    prod_all = np.array([1.0])
    for (_, A) in terms:
        prod_all = polymul(prod_all, np.array([1.0, -A]))
    P = polymul(base, prod_all)
    for j, (kw, _) in enumerate(terms):
        pr = np.array([1.0])
        for jj, (_, A2) in enumerate(terms):
            if jj != j:
                pr = polymul(pr, np.array([1.0, -A2]))
        P = np.polynomial.polynomial.polysub(P, kw * pr)
    roots_s = np.polynomial.polynomial.polyroots(P)
    mus = []
    for s in roots_s:
        mu = np.sqrt(complex(s))
        for m in (mu, -mu):
            mus.append(m)
    osc = None          # slowest-decaying oscillatory (Re<0 branch, Im!=0)
    mono = None         # slowest-decaying monotone (Re<0, Im~0)
    for m in mus:
        re, im = m.real, m.imag
        if re >= -1e-12:
            continue
        if abs(im) > 1e-9:
            if osc is None or -re < -osc[0]:
                osc = (float(re), float(abs(im)))
        else:
            if mono is None or -re < -mono:
                mono = float(re)
    out = dict(all_s=[(float(s.real), float(s.imag)) for s in roots_s])
    if osc:
        out["osc_re"] = osc[0]
        out["osc_im"] = osc[1]
        out["wavelength"] = float(2 * np.pi / osc[1])
    else:
        out["osc_re"] = None
        out["osc_im"] = None
        out["wavelength"] = None
    out["mono_re"] = mono
    return out


def chemistry_box(tails):
    """Chemistry-candidate test on one act's tails.
    V3 (stage-2 lock, controller-approved): wavelength + |Re| box ONLY. The v2
    osc-dominance clause (|Re osc| <= 2|Re mono|) had a measured RECALL BUG:
    it rejected ALL 15 alive VVW-family jitters (12 with certified-style bonds)
    in stage 1. Osc-dominance is still logged via mono_re for post-hoc study."""
    if tails["wavelength"] is None:
        return False
    wl, re = tails["wavelength"], abs(tails["osc_re"])
    return bool(3.0 <= wl <= 30.0 and 0.1 <= re <= 1.5)


def funnel(g, log_all_roots=False):
    """Full G0 funnel on genome g AT ITS STORED u0 designation (u0 is a gene).
    Returns record dict with stage, margins, tails. Does not mutate g."""
    rec = dict(stage="none")
    ok_b, discs = g0b(g)
    rec["g0b_disc"] = discs
    rec["g0b"] = bool(ok_b)
    if not ok_b:
        rec["stage"] = "fail_g0b"
        return rec
    u0s = [a["u0"] for a in g["acts"]]
    margin, k_at = g0a_margin(g, u0s)
    rec["g0a_margin"] = float(margin)
    rec["g0a_k"] = float(k_at)
    if log_all_roots:
        tried = enumerate_vacua(g)
        rec["g0a_all_roots"] = tried
    rec["g0a"] = bool(margin < 0.0)
    rec["excitable_shelf"] = bool(abs(margin) < EXCITABLE_BAND)
    if margin >= 0.0:
        rec["stage"] = "fail_g0a"
        return rec
    tails = [g0c_tails(g, i) for i in range(len(g["acts"]))]
    rec["g0c"] = [dict(osc_re=t["osc_re"], osc_im=t["osc_im"],
                       wavelength=t["wavelength"], mono_re=t["mono_re"])
                  for t in tails]
    rec["chem_box"] = [chemistry_box(t) for t in tails]
    rec["g0c_any_osc"] = any(t["wavelength"] is not None for t in tails)
    rec["g0c_any_chem"] = any(rec["chem_box"])
    rec["stage"] = "pass"
    return rec
