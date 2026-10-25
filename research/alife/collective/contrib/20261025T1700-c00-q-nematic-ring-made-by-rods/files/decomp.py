"""Is rod motion self-propulsion? The Brinkman-Stokes solve is linear in the force, so the flow
splits exactly into the part each rod's own forces make (forces in its Voronoi cell) and the part
its neighbours make. For each rod: U_tot = mean fluid velocity over the rod (phi > 0), U_self =
the same for the flow made by its own cell's forces, U_nbr = U_tot - U_self; also U_self from
the active stress alone. Checked against the rod's actual centroid velocity over 1 time unit.
usage: decomp.py world.py seed frame1 frame2 ...   (frames of 100 steps; world dt from WORLD_P)"""
import sys, importlib.util
import numpy as np
from numpy.fft import fft2, ifft2
from scipy import ndimage
sys.path.insert(0, "/home/user/physim/research/alife"); sys.dont_write_bytecode = True
from labkit import metrics as M

spec = importlib.util.spec_from_file_location("w", sys.argv[1]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
seed = int(sys.argv[2]); snaps = sorted(int(x) for x in sys.argv[3:])
P = W.P; spf = 100
st = W.init(seed, W.META["size"]); H, Wd = st["phi"].shape
kx, ky, k2, da = st["kx"], st["ky"], st["k2"], st["da"]


def forces(phi, q1, q2, zeta=None):
    zeta = P["zeta"] if zeta is None else zeta
    Ph, Q1, Q2 = fft2(phi), fft2(q1), fft2(q2)
    mu = P["a"] * (phi ** 3 - phi) - P["k"] * ifft2(-k2 * Ph).real
    px, py = W._d(Ph, kx), W._d(Ph, ky)
    cap = (mu * px, mu * py)
    act = (-zeta * (W._d(Q1, kx) + W._d(Q2, ky)), -zeta * (W._d(Q2, kx) - W._d(Q1, ky)))
    return cap, act


def stokes(fx, fy):
    Fx, Fy = fft2(fx), fft2(fy)
    kf = (kx * Fx + ky * Fy) / st["k2s"]
    den = P["xi"] + P["eta"] * k2
    Vx = (Fx - kx * kf) / den * da; Vy = (Fy - ky * kf) / den * da
    Vx[0, 0] = Vy[0, 0] = 0
    return ifft2(Vx).real, ifft2(Vy).real


def owners(inside):
    lab, n = M.periodic_label(inside)
    tile = np.tile(inside, (3, 3))
    _, idx = ndimage.distance_transform_edt(~tile, return_indices=True)
    sl = (slice(H, 2 * H), slice(Wd, 2 * Wd))
    iy, ix = idx[0][sl] % H, idx[1][sl] % Wd
    return lab, n, np.where(inside, lab, lab[iy, ix])


def centroid(m):
    ys, xs = np.nonzero(m)
    ay, ax = 2 * np.pi * ys / H, 2 * np.pi * xs / Wd
    cy = (np.arctan2(np.sin(ay).mean(), np.cos(ay).mean()) % (2 * np.pi)) * H / (2 * np.pi)
    cx = (np.arctan2(np.sin(ax).mean(), np.cos(ax).mean()) % (2 * np.pi)) * Wd / (2 * np.pi)
    return cy, cx


allrows = []
f = 0
for target in snaps:
    while f < target:
        for _ in range(spf):
            st = W.step(st)
        f += 1
    phi, q1, q2 = st["phi"].copy(), st["q1"].copy(), st["q2"].copy()
    inside = phi > 0
    lab, n, own = owners(inside)
    cap, act = forces(phi, q1, q2)
    fx, fy = cap[0] + act[0], cap[1] + act[1]
    vx, vy = stokes(fx, fy)
    # actual centroid velocity over 1 time unit
    st2 = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in st.items()}
    nsteps = int(round(1.0 / P["dt"]))
    for _ in range(nsteps):
        st2 = W.step(st2)
    lab2, n2 = M.periodic_label(st2["phi"] > 0)
    rows = []
    for j in range(1, n + 1):
        m = lab == j
        if m.sum() < 12:
            continue
        o = own == j
        sx, sy = stokes(fx * o, fy * o)
        ax_, ay_ = stokes(act[0] * o, act[1] * o)
        Ut = np.array([vy[m].mean(), vx[m].mean()]); Us = np.array([sy[m].mean(), sx[m].mean()])
        Ua = np.array([ay_[m].mean(), ax_[m].mean()]); Un = Ut - Us
        ids, cnt = np.unique(lab2[m & (lab2 > 0)], return_counts=True)
        if len(ids) == 0:
            continue
        m2 = lab2 == ids[np.argmax(cnt)]
        c1, c2 = centroid(m), centroid(m2)
        Uc = np.array([M._wrap(c2[0] - c1[0], H), M._wrap(c2[1] - c1[1], Wd)]) / (nsteps * P["dt"])
        cos = lambda a, b: float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))
        rows.append(dict(frame=target, area=int(m.sum()), Ut=np.linalg.norm(Ut), Us=np.linalg.norm(Us), Ua=np.linalg.norm(Ua), Un=np.linalg.norm(Un),
                         Uc=np.linalg.norm(Uc), cos_c_t=cos(Uc, Ut), cos_s_t=cos(Us, Ut), cos_c_s=cos(Uc, Us)))
    allrows += rows
    a = lambda k: np.array([r[k] for r in rows])
    print(f"frame {target} (t={target * spf * P['dt']:.0f}): {len(rows)} rods; median |U_centroid| {np.median(a('Uc')):.4f}, |U_tot| {np.median(a('Ut')):.4f}, |U_self| {np.median(a('Us')):.4f} (active-only {np.median(a('Ua')):.4f}), |U_nbr| {np.median(a('Un')):.4f}; "
          f"|U_self|>|U_nbr| in {np.mean(a('Us') > a('Un')):.2f}; median cos(U_centroid, U_tot) {np.median(a('cos_c_t')):.2f}, cos(U_centroid, U_self) {np.median(a('cos_c_s')):.2f}")
a = lambda k: np.array([r[k] for r in allrows])
print(f"ALL {len(allrows)} rod-snapshots: median |U_self|/|U_tot| {np.median(a('Us') / a('Ut')):.2f}; |U_self|>|U_nbr| in {np.mean(a('Us') > a('Un')):.2f}; median cos(U_centroid, U_self) {np.median(a('cos_c_s')):.2f}; median |U_centroid|/|U_tot| {np.median(a('Uc') / a('Ut')):.2f}")
