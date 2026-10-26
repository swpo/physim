"""ad9-ledger: gated protocells with a logged, birth-coupled mutation ledger (committee r2 protocol).

Fork of ad7-gated (gated diffusion from fisim-beyond-laplacian; self-made amphiphile shell),
with:
  * harmonic face averaging in the gated divergence;
  * heritable trait = kp rung (index into KP ladder), carried by the catalyst: fields a (catalyst)
    and q = a * rung, transported by the same operator, so q/a is constant inside a droplet;
  * in-world droplet tracking every TRK steps (periodic labels, overlap matching) that logs
    births (one component -> >= 2) and deaths;
  * mutation only at birth: with prob pmut one daughter's rung moves +-1 (whole-droplet relabel);
  * Moran dilution: when the droplet count exceeds cap after a birth, one uniformly chosen droplet
    is erased (births = deaths once full);
  * identical-event RNG streams: mutation draws use stream (seed, 'mut') with exactly 3 draws per
    birth, dilution picks use stream (seed, 'dil') with 1 draw per kill, so the neutral twin
    (neutral=1: every rung has the ancestor's kp) replays the same event sequence by birth index.

Equations (c = (1+phi)/2, kp(x) = KP[q/a] in S, KP[rung0] in N):
    dphi = M lap(phi^3 - phi - kappa lap phi) + prod - kd c,     prod = k u c^2 a
    du   = div(Du e^{-bu psi} grad u) + F (1 - u) - prod
    da   = div(Dc e^{-bc psi} grad a) + r c a (1 - a) - g (1 - c) a        (q: same, linear in q)
    dpsi = Dp div(grad psi - chi psi grad|grad phi|^2) + kp(x) prod - gp psi
"""
import numpy as np
from labkit import ops
from labkit.metrics import periodic_label

META = {
    "name": "ad9-ledger",
    "family": "phase-field",
    "parent": "ad7-gated (+ fisim-beyond-laplacian gated diffusion; identical-event RNG idea from fisim xcell-evo2-S)",
    "mutation": "rung trait carried by catalyst; birth-coupled +-1 copy errors; Moran dilution; harmonic gate averaging; event ledger",
    "size": (128, 128),
    "steps_per_frame": 200,
    "dt": 0.5,
    "channels": ["phi (droplet material)", "u (fuel)", "psi (amphiphile)", "a (catalyst)", "rung (kp index)"],
    "matter": [0],
    "threshold": 0.0,
}

KP = [0.0, 0.25, 0.5, 1.0, 1.5, 2.5, 4.0]
P = dict(M=0.03, kappa=1.0, k=0.15, kd=0.02, F=0.004, Du=2.0, bu=0.5, Dc=0.3, bc=3.0, r=0.05, g=0.05,
         Dp=0.3, chi=8.0, gp=0.01, dt=0.5, A=2.0, phi0=-0.95, noise=0.01, seeds=6, r0=6.0,
         rung0=5, neutral=0, pmut=0.1, cap=12, TRK=100, minarea=20, linear=0, harmonic=1)


def kp_of(rung):
    if P["neutral"]:
        return np.full_like(rung, KP[P["rung0"]], dtype=float)
    return np.interp(rung, np.arange(len(KP)), KP)


def gated_div(c, D):
    out = np.zeros_like(c)
    for ax in (-2, -1):
        Dn = np.roll(D, -1, ax)
        Df = 2 * D * Dn / (D + Dn + 1e-12) if P["harmonic"] else 0.5 * (D + Dn)
        fl = Df * (np.roll(c, -1, ax) - c)
        out += fl - np.roll(fl, 1, ax)
    return out


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    phi = P["phi0"] + P["noise"] * rng.standard_normal((H, W))
    a = np.zeros((H, W))
    for _ in range(P["seeds"]):
        m = ops.disk(H, W, rng.integers(0, H), rng.integers(0, W), P["r0"])
        phi[m] = 0.9
        a[m] = 0.9
    ky, kx = ops.wavenumbers(H, W)
    k2 = kx ** 2 + ky ** 2
    dt, M = P["dt"], P["M"]
    s = {"t": 0.0, "n": 0, "phi": phi, "u": np.ones((H, W)), "psi": np.zeros((H, W)), "a": a,
         "q": a * P["rung0"], "k2": k2, "shape": (H, W),
         "rng_mut": np.random.default_rng([seed, 1]), "rng_dil": np.random.default_rng([seed, 2]),
         "den": 1 + dt * M * k2 * (P["A"] + P["kappa"] * k2), "denl": 1 + dt * M * k2,
         "denu": 1 + dt * P["Du"] * k2, "denc": 1 + dt * P["Dc"] * k2, "denp": 1 + dt * P["Dp"] * k2,
         "ledger": [], "prev": None, "nbirth": 0, "nkill": 0, "series": []}
    return s


def _components(s):
    lab, n = periodic_label(s["phi"] > 0)
    area = np.bincount(lab.ravel(), minlength=n + 1)
    a, q = s["a"], s["q"]
    sa = np.bincount(lab.ravel(), weights=a.ravel(), minlength=n + 1)
    sq = np.bincount(lab.ravel(), weights=q.ravel(), minlength=n + 1)
    rung = sq / np.maximum(sa, 1e-9)
    keep = [i for i in range(1, n + 1) if area[i] >= P["minarea"] and sa[i] / area[i] > 0.05]
    return lab, keep, rung, area


def _relabel(s, mask, new):
    s["q"][mask] = s["a"][mask] * new


def _erase(s, mask):
    m = mask | np.roll(mask, 1, 0) | np.roll(mask, -1, 0) | np.roll(mask, 1, 1) | np.roll(mask, -1, 1)
    s["phi"][m] = -1.0
    s["a"][m] = 0.0
    s["q"][m] = 0.0
    s["psi"][m] = 0.0


def _track(s):
    lab, keep, rung, area = _components(s)
    t = s["t"]
    if s["prev"] is not None:
        plab, pkeep, prung = s["prev"]
        both = (plab > 0) & (lab > 0)
        pairs = np.unique(np.stack([plab[both], lab[both]], 1), axis=0) if both.any() else np.zeros((0, 2), int)
        pk, ck = set(pkeep), set(keep)
        pairs = [(p, c) for p, c in pairs if p in pk and c in ck]
        children = {}
        parents = {}
        for p, c in pairs:
            children.setdefault(p, []).append(c)
            parents.setdefault(c, []).append(p)
        for p in pkeep:
            ch = children.get(p, [])
            pr = int(round(prung[p]))
            if len(ch) == 0:
                s["ledger"].append(("death", t, pr))
            elif len(ch) >= 2:
                for c in ch:
                    if int(round(rung[c])) != pr:
                        s["ledger"].append(("offkind", t, pr, int(round(rung[c]))))
                for extra in ch[1:]:
                    s["nbirth"] += 1
                    s["ledger"].append(("birth", t, pr))
                    u1, u2, u3 = s["rng_mut"].random(3)
                    if u1 < P["pmut"]:
                        d = ch[int(u3 * len(ch)) % len(ch)]
                        new = int(np.clip(pr + (1 if u2 < 0.5 else -1), 0, len(KP) - 1))
                        if new != pr:
                            _relabel(s, lab == d, new)
                            rung[d] = new
                            s["ledger"].append(("mut", t, pr, new))
            else:
                c = ch[0]
                if len(parents.get(c, [])) == 1 and int(round(rung[c])) != pr:
                    s["ledger"].append(("convert", t, pr, int(round(rung[c]))))
        for c in keep:
            if c not in parents:
                s["ledger"].append(("nucleate", t, int(round(rung[c]))))
        # Moran dilution: keep count <= cap
        alive = list(keep)
        while len(alive) > P["cap"]:
            j = int(s["rng_dil"].random() * len(alive)) % len(alive)
            v = alive.pop(j)
            s["nkill"] += 1
            s["ledger"].append(("kill", t, int(round(rung[v]))))
            _erase(s, lab == v)
            keep = [x for x in keep if x != v]
    rr = [int(round(rung[c])) for c in keep]
    s["series"].append((t, len(keep), float(np.mean([KP[x] for x in rr])) if rr else float("nan"),
                        np.bincount(rr, minlength=len(KP)).tolist() if rr else [0] * len(KP)))
    s["prev"] = (lab, keep, rung)


def step(s):
    phi, u, psi, a, q, k2, dt, M = s["phi"], s["u"], s["psi"], s["a"], s["q"], s["k2"], P["dt"], P["M"]
    sh = s["shape"]
    c = np.clip((1 + phi) / 2, 0, 1)
    prod = P["k"] * u * c ** 2 * a
    if P["linear"]:
        s["phi"] = ops.irfft2((ops.rfft2(phi) + dt * ops.rfft2(prod - P["kd"] * c)) / s["denl"], sh)
    else:
        s["phi"] = ops.irfft2((ops.rfft2(phi) - dt * M * k2 * ops.rfft2(phi ** 3 - phi - P["A"] * phi)
                               + dt * ops.rfft2(prod - P["kd"] * c)) / s["den"], sh)
    ru = gated_div(u, P["Du"] * np.exp(-P["bu"] * psi)) - P["Du"] * ops.laplacian(u) + P["F"] * (1 - u) - prod
    s["u"] = ops.irfft2((ops.rfft2(u) + dt * ops.rfft2(ru)) / s["denu"], sh)
    Dgc = P["Dc"] * np.exp(-P["bc"] * psi)
    growth = P["r"] * c * (1 - a) - P["g"] * (1 - c)
    ra = gated_div(a, Dgc) - P["Dc"] * ops.laplacian(a) + growth * a
    rq = gated_div(q, Dgc) - P["Dc"] * ops.laplacian(q) + growth * q
    s["a"] = np.clip(ops.irfft2((ops.rfft2(a) + dt * ops.rfft2(ra)) / s["denc"], sh), 0, None)
    s["q"] = np.clip(ops.irfft2((ops.rfft2(q) + dt * ops.rfft2(rq)) / s["denc"], sh), 0, None)
    kpx = kp_of(s["q"] / np.maximum(s["a"], 1e-6))
    gy, gx = ops.grad(phi)
    vy, vx = ops.grad(gy ** 2 + gx ** 2)
    rp = -P["Dp"] * P["chi"] * ops.upwind_flux_div(psi, vy, vx) + prod * kpx - P["gp"] * psi
    s["psi"] = np.clip(ops.irfft2((ops.rfft2(psi) + dt * ops.rfft2(rp)) / s["denp"], sh), 0, None)
    s["t"] += dt
    s["n"] += 1
    if s["n"] % P["TRK"] == 0:
        _track(s)
    return s


def fields(s):
    rung = np.where(s["a"] > 0.05, s["q"] / np.maximum(s["a"], 1e-6), 0.0)
    return np.stack([s["phi"], s["u"], s["psi"], s["a"], rung])


def damage(s, mask):
    _erase(s, mask)
    return s
