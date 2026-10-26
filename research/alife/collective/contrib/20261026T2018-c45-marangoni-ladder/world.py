"""Active nematic droplets: Cahn-Hilliard droplets that carry their own nematic order and
stir themselves through an active stress, on a Brinkman-Stokes fluid (c11).

c34 variant (Q:nematic-ring-made-by-rods): the surfactant s is made ONLY on rod pixels,
src = ks * [phi > 0] (src_mode="rod"; src_mode="c11" restores c11's ks (1+phi)/2, which the
chemostat bath at phi ~ -0.65 keeps on), so every molecule of the ring is made by an individual.
gm > 0 (c34, gated growth): the surfactant ring lowers the droplet's Cahn-Hilliard mobility where it sits,
M_eff = M / (1 + gm s), so the ring throttles the mass flux by which a rod grows (and its shape relaxes);
gm = 0 is the passive-ring world exactly. Stabilised splitting: implicit M, explicit div((M_eff - M) grad mu).
Marangoni (c34): mar != 0 adds the tangential stress of a surfactant-dependent tension sigma = sigma0 - mar s,
f_M = -mar |grad phi| (I - n n) grad s, n = grad phi / |grad phi| (mar > 0: s lowers the tension); mar = 0 is the
world without it. This is the only way s acts back on the rods.
Cargo (c34): a species c made on rod pixels (kc [phi>0]), decaying at kcd, advected by the flow, with chemical
potential ln c + kappa s, so the rod's own surfactant ring excludes it: dc/dt = Dc lap c + Dc kappa div(c grad s)
- div(v c) + kc [phi>0] - kcd c. kappa = 0 is the wall ablation. c acts back on nothing.
Adsorption strength chis is a free parameter (default 5, c11 used 3). The 1.5x-grid test should
scale noise with dx (noise_area=True keeps the white-noise power per unit area fixed).

After Giomi & DeSimone, PRL 112, 147802 (2014) ("Spontaneous division and motility in active
nematic droplets"), simplified to a dry-friction Stokes fluid so that the flow is one
spectral solve per step. 2D periodic, pseudo-spectral.

phi: droplet phase (+1 inside, -1 outside), model H:
    dphi/dt + v.grad phi = M lap mu + kr (phi_b - phi),   mu = a (phi^3 - phi) - k lap phi
Q = [[q1, q2], [q2, -q1]]: nematic order, ordered only inside droplets:
    dQ/dt + v.grad Q - [Q, W] = lam_f E (inside) + G H,
    H = -c (phi_c - phi) Q - c |Q|^2 Q + L lap Q  (|Q|^2 = q1^2 + q2^2)
Fluid (Brinkman-Stokes, incompressible):
    (xi - eta lap) v + grad p = f,  f = mu grad phi (capillary) + div(-zeta Q) (active stress)
zeta > 0 extensile. The only source of motion is the droplets' own active stress, which is
proportional to their own order Q; outside droplets Q relaxes to 0. Ablation: zeta = 0
(passive nematic emulsion: coarsening only). WORLD_P (JSON) overrides P.

TURNOVER (c45, Q:marangoni-turnover-persistence): every DIL_EVERY frames (DIL_EVERY*steps_per_frame steps) a trait-blind
dilution: label the bodies (phi > 0, components merged across periodic edges), sort them by raster order of their first
pixel, draw 256 uniforms from an RNG seeded only by the run seed and the event index, and remove body i if u_i < p_dil:
inside the body dilated by 2 px, phi is set to the mean phi of the bath (outside all bodies) and Q and s to 0. Nothing reads
a body's kind, speed, size or age. The kr chemostat term then restores the mean, so the survivors grow. Defaults here:
CARGO=0, p_dil=0.08, DIL_EVERY=10. REDIST=1 adds the removed matter back uniformly over the domain at once
(phi mean conserved by the event). If the environment variable TURNOVER_LOG is set, each event appends one JSON line
(step, number of bodies, removed indices and areas).

LADDER (c45, Q:marangoni-heritable-ladder): K=3 surfactant kinds s0, s1, s2, transported identically; the rod's source is
split by its local composition with majority feedback (as c34's two kinds): src_k = ks [phi>0] f_k^2 / sum_j f_j^2,
f_k = (s_k + e) / (sum_j s_j + K e). Kind k has Marangoni coefficient MARS[k] (ladder 20, 40, 60; the identical-event
twin gives every kind 40), the stress is made from sum_k MARS[k] s_k. Initial s_k: independent white noise of amplitude s0.
Mutation: at every frame boundary the bodies are labelled (as for the dilution) and 256 uniforms drawn from an RNG seeded
only by (seed, 9191, frame); body i mutates if u_i < mu: its kind (largest body-summed s_k) becomes k-1 or k+1 with equal
odds (a second uniform; at the ends the only neighbour), and all surfactant of every kind inside the body dilated by 3 px
is moved to the new kind. Nothing reads a body's speed, size, age or kind except the flip itself. MUT_LOG (env) logs events.
Defaults here: p_dil 0.10 with REDIST=1 (20261026T1924-c45-marangoni-turnover-long), mu 1e-3.
"""
import json, os
import numpy as np
from numpy.fft import fft2, ifft2
from scipy import ndimage

META = {
    "name": "active-nematic-marangoni-ladder",
    "family": "active-nematic",
    "parent": "collective/contrib/20261026T0505-c34-nematic-marangoni/world.py",
    "mutation": "three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover",
    "size": (128, 128),
    "steps_per_frame": 100,
    "dt": 0.05,
    "channels": ["phi (droplet)", "order |Q|", "s0 (mar 20)", "s1 (mar 40)", "s2 (mar 60)"],
    "matter": [0],
    "threshold": 0.0,
    "smooth": 0.5,
    "periodic": True,
    "radial_channels": [0, 1, 2, 3, 4],
}

P = dict(dx=1.0, dt=0.05, a=1.0, k=1.5, M=1.0, S=2.0, c=1.0, phi_c=0.0, G=0.5, L=1.0,
         lam_f=0.5, zeta=0.8, eta=1.0, xi=0.02, phi0=-0.4, noise=0.2, qnoise=0.05, kr=0.012, phi_b=-0.6, Ds=0.5, chis=3.0, ks=0.02, kds=0.02,
         src_mode="rod", noise_area=False, gm=0.0,
         CARGO=1, Dc=1.0, kc=0.02, kcd=0.005, kappa=20.0, mar=40.0)
P["chis"] = 5.0

P.update(dict(CARGO=0, p_dil=0.10, DIL_EVERY=10, REDIST=1, MARS=[20.0, 40.0, 60.0], mu=1e-3, s0=0.01, ecop=1e-3))
P.update(json.loads(os.environ.get("WORLD_P", "{}")))
if P["noise_area"]:
    P["noise"] = P["noise"] / P["dx"]


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    dx = P["dx"]
    phi = P["phi0"] + P["noise"] * rng.standard_normal((H, W))
    q1 = P["qnoise"] * rng.standard_normal((H, W))
    q2 = P["qnoise"] * rng.standard_normal((H, W))
    ky = 2 * np.pi * np.fft.fftfreq(H, d=dx)[:, None] * np.ones((1, W))
    kx = 2 * np.pi * np.fft.fftfreq(W, d=dx)[None, :] * np.ones((H, 1))
    k2 = kx ** 2 + ky ** 2
    kmax = np.pi / dx
    da = ((np.abs(kx) < 2 / 3 * kmax) & (np.abs(ky) < 2 / 3 * kmax)).astype(float)
    k2s = k2.copy(); k2s[0, 0] = 1.0
    return {"seed": int(seed), "i": 0, "nev": 0, "phi": phi, "q1": q1, "q2": q2, "kx": kx, "ky": ky, "k2": k2, "k2s": k2s, "da": da,
            "vx": np.zeros((H, W)), "vy": np.zeros((H, W)), "t": 0.0, "s": np.zeros((H, W)), "c": np.zeros((H, W)), "sk": [P["s0"] * rng.random((H, W)) for _ in range(3)]}


def _d(f_hat, k):
    return ifft2(1j * k * f_hat).real


def _cargo(c, sf, vx, vy, phi, dt, dx):
    """Finite-volume cargo step (positive): Slotboom flux J = -Dc exp(-kappa s) grad(c exp(kappa s)) with the face weight
    2 / (exp(kappa s_i) + exp(kappa s_j)), first-order upwind advection by the face-averaged flow, source and decay."""
    e = np.exp(P["kappa"] * sf); u = c * e
    out = np.zeros_like(c)
    for ax, v in ((1, vx), (0, vy)):
        ej = np.roll(e, -1, ax); uj = np.roll(u, -1, ax); cj = np.roll(c, -1, ax)
        fl = -P["Dc"] * 2.0 / (e + ej) * (uj - u) / dx
        vf = 0.5 * (v + np.roll(v, -1, ax))
        fl = fl + np.where(vf > 0, vf * c, vf * cj)
        out -= (fl - np.roll(fl, 1, ax)) / dx
    return np.maximum(c + dt * (out + P["kc"] * (phi > 0) - P["kcd"] * c), 0)


def _bodies(phi):
    """Labels of phi > 0 merged across periodic edges, renumbered 1..n in raster order of each body's first pixel."""
    lab, n = ndimage.label(phi > 0)
    if n == 0:
        return lab, 0
    par = list(range(n + 1))
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    for a, b in ((lab[:, 0], lab[:, -1]), (lab[0, :], lab[-1, :])):
        for x, y in zip(a, b):
            if x and y:
                rx, ry = find(x), find(y)
                if rx != ry: par[max(rx, ry)] = min(rx, ry)
    root = np.array([find(a) for a in range(n + 1)])
    lab = root[lab]
    first = {}
    for idx, v in enumerate(lab.ravel()):
        if v and v not in first: first[v] = idx
    order = sorted(first, key=first.get)
    remap = np.zeros(n + 1, int)
    for k, v in enumerate(order): remap[v] = k + 1
    return remap[lab], len(order)


def _dilute(s):
    phi = s["phi"]
    lab, n = _bodies(phi)
    u = np.random.default_rng([s["seed"], 4242, s["nev"]]).random(256)
    s["nev"] += 1
    rm = [i for i in range(1, min(n, 256) + 1) if u[i - 1] < P["p_dil"]]
    bath = phi[lab == 0].mean() if (lab == 0).any() else phi.mean()
    m0 = s["phi"].sum()
    areas = []
    for i in rm:
        m = np.pad(lab == i, 2, mode="wrap")
        m = ndimage.binary_dilation(m, iterations=2)[2:-2, 2:-2]
        areas.append(int((lab == i).sum()))
        s["phi"][m] = bath; s["q1"][m] = 0.0; s["q2"][m] = 0.0; s["s"][m] = 0.0
        for sk in s["sk"]: sk[m] = 0.0
    if P["REDIST"] and rm:
        # the removed body matter returns at once, spread uniformly over the domain (fresh medium; trait-blind)
        s["phi"] += (m0 - s["phi"].sum()) / s["phi"].size
    log = os.environ.get("TURNOVER_LOG")
    if log:
        with open(log, "a") as fh:
            fh.write(json.dumps({"step": s["i"], "frame": s["i"] // META["steps_per_frame"], "n": n, "removed": rm, "areas": areas}) + "\n")
    return s


def _mutate(s):
    frame = s["i"] // META["steps_per_frame"]
    lab, n = _bodies(s["phi"])
    rng = np.random.default_rng([s["seed"], 9191, frame])
    u, v = rng.random(256), rng.random(256)
    ev = []
    for i in range(1, min(n, 256) + 1):
        if u[i - 1] >= P["mu"]:
            continue
        body = lab == i
        k = int(np.argmax([sk[body].sum() for sk in s["sk"]]))
        k2 = 1 if k == 0 else (1 if k == 2 else (0 if v[i - 1] < 0.5 else 2))
        m = np.pad(body, 3, mode="wrap")
        m = ndimage.binary_dilation(m, iterations=3)[3:-3, 3:-3]
        moved = sum(sk[m] for sk in s["sk"])
        for j, sk in enumerate(s["sk"]):
            sk[m] = moved if j == k2 else 0.0
        ev.append({"body": i, "from": k, "to": k2, "area": int(body.sum())})
    log = os.environ.get("MUT_LOG")
    if log and ev:
        with open(log, "a") as fh:
            fh.write(json.dumps({"frame": frame, "n": n, "events": ev}) + "\n")
    return s


def step(s):
    dt, kx, ky, k2, da = P["dt"], s["kx"], s["ky"], s["k2"], s["da"]
    phi, q1, q2 = s["phi"], s["q1"], s["q2"]
    Ph, Q1, Q2 = fft2(phi), fft2(q1), fft2(q2)
    # chemical potential and capillary force
    mu = P["a"] * (phi ** 3 - phi) - P["k"] * ifft2(-k2 * Ph).real
    px, py = _d(Ph, kx), _d(Ph, ky)
    fx = mu * px - P["zeta"] * (_d(Q1, kx) + _d(Q2, ky))
    fy = mu * py - P["zeta"] * (_d(Q2, kx) - _d(Q1, ky))
    if True:
        Shm = fft2(sum(m * sk for m, sk in zip(P["MARS"], s["sk"]))); sx, sy = _d(Shm, kx), _d(Shm, ky)
        g = np.sqrt(px * px + py * py); nx, ny = px / (g + 1e-6), py / (g + 1e-6)
        sn = nx * sx + ny * sy
        fx = fx - g * (sx - nx * sn)
        fy = fy - g * (sy - ny * sn)
    Fx, Fy = fft2(fx), fft2(fy)
    kf = (kx * Fx + ky * Fy) / s["k2s"]
    den = P["xi"] + P["eta"] * k2
    Vx = (Fx - kx * kf) / den * da
    Vy = (Fy - ky * kf) / den * da
    Vx[0, 0] = Vy[0, 0] = 0
    vx, vy = ifft2(Vx).real, ifft2(Vy).real
    # velocity gradients
    dxvx, dyvx, dxvy, dyvy = _d(Vx, kx), _d(Vx, ky), _d(Vy, kx), _d(Vy, ky)
    om = 0.5 * (dxvy - dyvx)
    Exx, Exy = 0.5 * (dxvx - dyvy), 0.5 * (dyvx + dxvy)
    # phi: advection explicit, CH stabilised semi-implicit
    adv_phi = vx * px + vy * py
    nl = P["a"] * (phi ** 3 - phi) - P["S"] * phi
    rhs = Ph - dt * fft2(adv_phi) * da - dt * P["M"] * k2 * fft2(nl) * da
    if P["gm"] > 0:
        mu_f = fft2(mu)
        dM = P["M"] / (1 + P["gm"] * s["s"]) - P["M"]
        gx, gy = dM * _d(mu_f, kx), dM * _d(mu_f, ky)
        rhs = rhs + dt * (1j * kx * fft2(gx) + 1j * ky * fft2(gy)) * da
    rhs[0, 0] += dt * P["kr"] * P["phi_b"] * phi.size
    Ph = rhs / (1 + dt * P["M"] * (P["k"] * k2 ** 2 + P["S"] * k2) + dt * P["kr"])
    # Q: bulk terms explicit, L lap implicit
    inside = 0.5 * (1 + np.clip(phi, -1, 1))
    QQ = q1 * q1 + q2 * q2
    bulk = -P["c"] * (P["phi_c"] - phi) - P["c"] * QQ
    r1 = -(vx * _d(Q1, kx) + vy * _d(Q1, ky)) - 2 * om * q2 + P["lam_f"] * inside * Exx + P["G"] * bulk * q1
    r2 = -(vx * _d(Q2, kx) + vy * _d(Q2, ky)) + 2 * om * q1 + P["lam_f"] * inside * Exy + P["G"] * bulk * q2
    imp = 1 + dt * P["G"] * P["L"] * k2
    Q1 = (Q1 + dt * fft2(r1) * da) / imp
    Q2 = (Q2 + dt * fft2(r2) * da) / imp
    # surfactant: made inside droplets, decays, adsorbs at the interface (drift up grad w, w = 1 - phi^2)
    w = 1 - np.clip(phi, -1, 1) ** 2
    Wh = fft2(w)
    wx, wy = _d(Wh, kx), _d(Wh, ky)
    e = P["ecop"]; tot = sum(s["sk"]) + 3 * e
    f2 = [((sk + e) / tot) ** 2 for sk in s["sk"]]; f2s = sum(f2)
    new = []
    for sk, fk in zip(s["sk"], f2):
        Skh = fft2(sk)
        fxs = P["Ds"] * P["chis"] * sk * wx + vx * sk
        fys = P["Ds"] * P["chis"] * sk * wy + vy * sk
        src = P["ks"] * (phi > 0) * fk / f2s - P["kds"] * sk
        Skh = (Skh + dt * (-(1j * kx * fft2(fxs) + 1j * ky * fft2(fys)) + fft2(src)) * da) / (1 + dt * P["Ds"] * k2)
        new.append(np.maximum(ifft2(Skh).real, 0))
    s["sk"] = new
    s["s"] = sum(new)
    s["phi"], s["q1"], s["q2"] = ifft2(Ph).real, ifft2(Q1).real, ifft2(Q2).real
    s["vx"], s["vy"], s["om"] = vx, vy, om
    s["i"] += 1
    if P["mu"] > 0 and s["i"] % META["steps_per_frame"] == 0:
        s = _mutate(s)
    if P["p_dil"] > 0 and s["i"] % (P["DIL_EVERY"] * META["steps_per_frame"]) == 0:
        s = _dilute(s)
    return s


def fields(s):
    om = s.get("om", np.zeros_like(s["phi"]))
    return np.stack([s["phi"], np.sqrt(s["q1"] ** 2 + s["q2"] ** 2)] + list(s["sk"])).astype(np.float32)


def stats(s):
    return {"vmax": round(float(np.hypot(s["vx"], s["vy"]).max()), 4), "mean_phi": round(float(s["phi"].mean()), 4)}
