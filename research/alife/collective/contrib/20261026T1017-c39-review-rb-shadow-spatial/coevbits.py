"""Coevolving predator-prey particles with heritable bit-string matching genotypes (c38; fork of coev.py).
Genotypes are nb-bit integers stored in trait column 0 (column 1 = 0); mutation flips each bit with prob u at birth;
capture success eps + (1-eps) exp(-h^2/w^2) with h the Hamming distance between predator and prey genotypes.


Prey eat a regrowing food field, move by random walk, divide when their energy passes a threshold
(the daughter's trait is the mother's plus a Gaussian step) and die of starvation or capture.
Predators move toward the nearest prey in sensing range, attack one prey in capture range per step
with success exp(-|pref - trait|^2 / w^2), gain energy on success, divide on an energy threshold
(Gaussian step on pref) and die of starvation. Traits are unbounded 2-vectors; an optional prey cost
multiplies food uptake by exp(-|trait|^2 / (2 S^2)) (S = inf: no cost).
neutral=2: success uses a random living predator's genotype (shuffled twin). neutral=1 is the in-world neutral twin: capture success is the constant p0 regardless of traits.
Every birth and death is logged (time, species, id, parent id, trait) for o_measure.
"""
import numpy as np
from numba import njit

P = dict(L=128.0, G=64, rF=0.02, Fmax=1.0, eat=0.25, cp=0.06, Ediv_p=2.0, step_p=0.6,
         cq=0.025, Ediv_q=4.0, Egain=1.0, step_q=1.0, Rs=6.0, rc=1.0, w=1.0, p0=0.3,
         sig_p=0.12, sig_q=0.12, S=0.0, hT=20.0, eps=0.0, kern=0, nb=20, u=0.003, neutral=0, Np0=1500, Nq0=150, cell=8.0)


@njit(cache=True)
def _build(x, y, n, L, nc, cs):
    head = -np.ones(nc * nc, np.int64); nxt = -np.ones(n, np.int64)
    for i in range(n):
        cx = int(x[i] / cs) % nc; cy = int(y[i] / cs) % nc; c = cy * nc + cx
        nxt[i] = head[c]; head[c] = i
    return head, nxt


@njit(cache=True)
def _mut(g, nb, u):
    x = np.int64(g)
    for b in range(nb):
        if np.random.random() < u:
            x ^= np.int64(1) << b
    return float(x)


@njit(cache=True)
def _ham(a, b, nb):
    x = np.int64(a) ^ np.int64(b); c = 0
    for k in range(nb):
        c += (x >> k) & 1
    return c


@njit(cache=True)
def _run(T, seed, px, py, pE, pt, pid, qx, qy, qE, qt, qid, F, prm, neutral, maxn, log, nlog, rec_every, rec, cnt):
    np.random.seed(seed)
    L, G, rF, Fmax, eat, cp, Edp, sp = prm[0], int(prm[1]), prm[2], prm[3], prm[4], prm[5], prm[6], prm[7]
    cq, Edq, Eg, sq, Rs, rc, w, p0 = prm[8], prm[9], prm[10], prm[11], prm[12], prm[13], prm[14], prm[15]
    sgp, sgq, S, cs, hT, eps, kern, nb, ub = prm[16], prm[17], prm[18], prm[19], prm[20], prm[21], prm[22], int(prm[23]), prm[24]
    qh = np.zeros(maxn)
    nc = int(L / cs); dx = L / G
    np_ = 0
    for i in range(px.shape[0]):
        if pid[i] >= 0: np_ = i + 1
    nq = 0
    for i in range(qx.shape[0]):
        if qid[i] >= 0: nq = i + 1
    nextid = 0
    for i in range(np_): nextid = max(nextid, pid[i] + 1)
    for i in range(nq): nextid = max(nextid, qid[i] + 1)
    alive_p = np.ones(maxn, np.bool_); alive_q = np.ones(maxn, np.bool_)
    nr = 0
    for t in range(T):
        # food regrowth
        for a in range(G):
            for b in range(G):
                F[a, b] += rF * (Fmax - F[a, b])
        # prey: move, eat, pay, divide
        n0 = np_
        for i in range(n0):
            if not alive_p[i]: continue
            px[i] = (px[i] + sp * np.random.randn()) % L; py[i] = (py[i] + sp * np.random.randn()) % L
            gx = int(px[i] / dx) % G; gy = int(py[i] / dx) % G
            u = min(F[gy, gx], eat); F[gy, gx] -= u
            if S > 0:
                u *= np.exp(-(pt[i, 0] ** 2 + pt[i, 1] ** 2) / (2 * S * S))
            pE[i] += u - cp
            if pE[i] < 0:
                alive_p[i] = False
                if nlog < log.shape[0]:
                    log[nlog, 0] = t; log[nlog, 1] = 0; log[nlog, 2] = 0; log[nlog, 3] = pid[i]; log[nlog, 4] = -1
                    log[nlog, 5] = pt[i, 0]; log[nlog, 6] = pt[i, 1]; nlog += 1
            elif pE[i] > Edp and np_ < maxn:
                j = np_; np_ += 1; alive_p[j] = True
                pE[i] *= 0.5; pE[j] = pE[i]
                px[j] = (px[i] + 0.5 * np.random.randn()) % L; py[j] = (py[i] + 0.5 * np.random.randn()) % L
                pt[j, 0] = _mut(pt[i, 0], nb, ub); pt[j, 1] = 0.0
                pid[j] = nextid; nextid += 1
                if nlog < log.shape[0]:
                    log[nlog, 0] = t; log[nlog, 1] = 0; log[nlog, 2] = 1; log[nlog, 3] = pid[j]; log[nlog, 4] = pid[i]
                    log[nlog, 5] = pt[j, 0]; log[nlog, 6] = pt[j, 1]; nlog += 1
        # compact prey
        k = 0
        for i in range(np_):
            if alive_p[i]:
                if k != i:
                    px[k] = px[i]; py[k] = py[i]; pE[k] = pE[i]; pt[k, 0] = pt[i, 0]; pt[k, 1] = pt[i, 1]; pid[k] = pid[i]
                alive_p[k] = True; k += 1
        for i in range(k, np_): alive_p[i] = True; pid[i] = -1
        np_ = k
        head, nxt = _build(px, py, np_, L, nc, cs)
        # predators
        n0 = nq
        for i in range(n0):
            if not alive_q[i]: continue
            if qh[i] > 0:
                qh[i] -= 1
                qE[i] -= cq
                continue
            best = -1; bd = Rs * Rs
            cx = int(qx[i] / cs) % nc; cy = int(qy[i] / cs) % nc
            for oy in range(-1, 2):
                for ox in range(-1, 2):
                    c = ((cy + oy) % nc) * nc + (cx + ox) % nc
                    j = head[c]
                    while j >= 0:
                        if alive_p[j]:
                            ddx = px[j] - qx[i]; ddy = py[j] - qy[i]
                            ddx -= L * np.round(ddx / L); ddy -= L * np.round(ddy / L)
                            d2 = ddx * ddx + ddy * ddy
                            if d2 < bd:
                                bd = d2; best = j
                        j = nxt[j]
            if best >= 0:
                ddx = px[best] - qx[i]; ddy = py[best] - qy[i]
                ddx -= L * np.round(ddx / L); ddy -= L * np.round(ddy / L)
                d = np.sqrt(ddx * ddx + ddy * ddy) + 1e-9
                stp = min(sq, d)
                qx[i] = (qx[i] + stp * ddx / d + 0.2 * np.random.randn()) % L
                qy[i] = (qy[i] + stp * ddy / d + 0.2 * np.random.randn()) % L
                if d - stp <= rc:
                    if neutral == 1:
                        pr = p0
                    else:
                        if neutral == 2:  # shuffled twin: a random predator's genotype, not this one's
                            jq = np.random.randint(0, n0)
                            while not alive_q[jq]:
                                jq = np.random.randint(0, n0)
                            hh = float(_ham(qt[jq, 0], pt[best, 0], nb))
                        else:
                            hh = float(_ham(qt[i, 0], pt[best, 0], nb))
                        pr = eps + (1 - eps) * np.exp(-hh * hh / (w * w))
                    cnt[0] += 1; cnt[1] += pr
                    if np.random.random() < pr:
                        alive_p[best] = False; qE[i] += Eg; qh[i] = hT
                        if nlog < log.shape[0]:
                            log[nlog, 0] = t; log[nlog, 1] = 0; log[nlog, 2] = 2; log[nlog, 3] = pid[best]; log[nlog, 4] = qid[i]
                            log[nlog, 5] = pt[best, 0]; log[nlog, 6] = pt[best, 1]; nlog += 1
            else:
                qx[i] = (qx[i] + sq * np.random.randn()) % L; qy[i] = (qy[i] + sq * np.random.randn()) % L
            qE[i] -= cq
            if qE[i] < 0:
                alive_q[i] = False
                if nlog < log.shape[0]:
                    log[nlog, 0] = t; log[nlog, 1] = 1; log[nlog, 2] = 0; log[nlog, 3] = qid[i]; log[nlog, 4] = -1
                    log[nlog, 5] = qt[i, 0]; log[nlog, 6] = qt[i, 1]; nlog += 1
            elif qE[i] > Edq and nq < maxn:
                j = nq; nq += 1; alive_q[j] = True
                qE[i] *= 0.5; qE[j] = qE[i]; qh[j] = 0
                qx[j] = (qx[i] + 0.5 * np.random.randn()) % L; qy[j] = (qy[i] + 0.5 * np.random.randn()) % L
                qt[j, 0] = _mut(qt[i, 0], nb, ub); qt[j, 1] = 0.0
                qid[j] = nextid; nextid += 1
                if nlog < log.shape[0]:
                    log[nlog, 0] = t; log[nlog, 1] = 1; log[nlog, 2] = 1; log[nlog, 3] = qid[j]; log[nlog, 4] = qid[i]
                    log[nlog, 5] = qt[j, 0]; log[nlog, 6] = qt[j, 1]; nlog += 1
        k = 0
        for i in range(nq):
            if alive_q[i]:
                if k != i:
                    qx[k] = qx[i]; qy[k] = qy[i]; qE[k] = qE[i]; qt[k, 0] = qt[i, 0]; qt[k, 1] = qt[i, 1]; qid[k] = qid[i]; qh[k] = qh[i]
                alive_q[k] = True; k += 1
        for i in range(k, nq): alive_q[i] = True; qid[i] = -1
        nq = k
        # compact prey again (captures)
        k = 0
        for i in range(np_):
            if alive_p[i]:
                if k != i:
                    px[k] = px[i]; py[k] = py[i]; pE[k] = pE[i]; pt[k, 0] = pt[i, 0]; pt[k, 1] = pt[i, 1]; pid[k] = pid[i]
                alive_p[k] = True; k += 1
        for i in range(k, np_): alive_p[i] = True; pid[i] = -1
        np_ = k
        if t % rec_every == 0 and nr < rec.shape[0]:
            rec[nr, 0] = t; rec[nr, 1] = np_; rec[nr, 2] = nq
            m0 = 0.0; m1 = 0.0
            for i in range(np_): m0 += pt[i, 0]; m1 += pt[i, 1]
            rec[nr, 3] = m0 / max(np_, 1); rec[nr, 4] = m1 / max(np_, 1)
            m0 = 0.0; m1 = 0.0
            for i in range(nq): m0 += qt[i, 0]; m1 += qt[i, 1]
            rec[nr, 5] = m0 / max(nq, 1); rec[nr, 6] = m1 / max(nq, 1)
            nr += 1
        if np_ == 0:
            break
    return np_, nq, nlog, nr, nextid


def init(seed, prm=None):
    p = dict(P); p.update(prm or {})
    rng = np.random.default_rng(seed); maxn = 20000
    st = dict(p=p, maxn=maxn,
              px=np.zeros(maxn), py=np.zeros(maxn), pE=np.zeros(maxn), pt=np.zeros((maxn, 2)), pid=-np.ones(maxn, np.int64),
              qx=np.zeros(maxn), qy=np.zeros(maxn), qE=np.zeros(maxn), qt=np.zeros((maxn, 2)), qid=-np.ones(maxn, np.int64),
              F=np.full((p["G"], p["G"]), p["Fmax"]), t=0)
    n, m = p["Np0"], p["Nq0"]
    st["px"][:n] = rng.uniform(0, p["L"], n); st["py"][:n] = rng.uniform(0, p["L"], n); st["pE"][:n] = rng.uniform(0.5, 1.5, n)
    st["pid"][:n] = np.arange(n)
    st["qx"][:m] = rng.uniform(0, p["L"], m); st["qy"][:m] = rng.uniform(0, p["L"], m); st["qE"][:m] = rng.uniform(1, 3, m)
    st["qid"][:m] = np.arange(n, n + m)
    st["seed"] = seed
    return st


def run(st, T, rec_every=50, maxlog=6_000_000):
    p = st["p"]
    prm = np.array([p[k] for k in ("L", "G", "rF", "Fmax", "eat", "cp", "Ediv_p", "step_p", "cq", "Ediv_q", "Egain",
                                   "step_q", "Rs", "rc", "w", "p0", "sig_p", "sig_q", "S", "cell", "hT", "eps", "kern", "nb", "u")], float)
    cnt = np.zeros(2); log = np.zeros((maxlog, 7)); rec = np.zeros((T // rec_every + 2, 7))
    out = _run(T, st["seed"] * 7919 + st["t"], st["px"], st["py"], st["pE"], st["pt"], st["pid"], st["qx"], st["qy"], st["qE"],
               st["qt"], st["qid"], st["F"], prm, int(p["neutral"]), st["maxn"], log, 0, rec_every, rec, cnt)
    np_, nq, nlog, nr, _ = out
    st["t"] += T
    return dict(np=np_, nq=nq, log=log[:nlog], rec=rec[:nr], overflow=nlog >= maxlog, attacks=cnt[0], mean_success=cnt[1] / max(cnt[0], 1))
