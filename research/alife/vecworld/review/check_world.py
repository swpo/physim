"""Independent checks of the A_gliders two-level world (reviewer's code).

1. level-0 mass conservation (law with VW-0 noise; stress test with huge flows)
2. kick: per-channel mass and positivity under admissible inputs; zero-sum tolerance loophole
3. input constraints: violating inputs through step() and run()
4. permutations: obs = quantise(h1[out_map]); input -> in_map cell; card contents
5. supervenience: replay the tracker from the saved h0 history; Phi_coarse and Phi_objects
   recomputed from h0 with my own code; bit-for-bit reproduction of base_000 and one branch
"""
import json
import math
import os
import sys
import time

import numpy as np
import scipy.ndimage as ndi

INT = "/home/user/evalwork/vecworld/integrate"
sys.path.insert(0, INT)
import lenia_world as LW          # noqa: E402
vw = LW.vw
OUT = "/home/user/evalwork/vecworld_integrate_review/check_world.json"
res = {}
t_start = time.time()

specs, parts = LW.make_specs("A_gliders")
l0, tr = parts["l0"], parts["tracker"]
C, H, W, HW = l0.C, l0.H, l0.W, l0.HW
w = vw.VectorWorld(specs["objects"], world_seed=0)
inv = LW.inverse_in_map(w)


# ------------------------------------------------------------------ my own Phi implementations
def my_coarse(h0, G=8):
    A = h0.reshape(C, H, W)
    b = H // G
    means = np.array([[A[c, i * b:(i + 1) * b, j * b:(j + 1) * b].mean() for i in range(G) for j in range(G)]
                      for c in range(C)]).ravel()
    S = A.sum(0)
    m2 = np.array([(S[i * b:(i + 1) * b, j * b:(j + 1) * b] ** 2).mean() for i in range(G) for j in range(G)])
    return np.concatenate([means, m2])


def my_components(h0, blur, thr, m_min):
    """Periodic 8-connected components of blur(A_sum) > thr (union-find over the wrap edges)."""
    A = h0.reshape(C, H, W)
    S = A.sum(0)
    mask = ndi.gaussian_filter(S, blur, mode="wrap") > thr
    lab, n = ndi.label(mask, structure=np.ones((3, 3)))
    par = list(range(n + 1))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    def union(a, b):
        if a and b:
            ra, rb = find(a), find(b)
            if ra != rb:
                par[ra] = rb
    for x in range(W):                       # top/bottom edge, incl. diagonals
        for dx in (-1, 0, 1):
            union(lab[0, x], lab[H - 1, (x + dx) % W])
    for y in range(H):
        for dy in (-1, 0, 1):
            union(lab[y, 0], lab[(y + dy) % H, W - 1])
    root = np.array([find(i) for i in range(n + 1)])
    L = root[lab]
    comps = []
    yy, xx = np.mgrid[0:H, 0:W]
    for r in np.unique(L[L > 0]):
        sel = L == r
        m = S[sel].sum()
        if m < m_min:
            continue
        ty, tx = 2 * np.pi * yy[sel] / H, 2 * np.pi * xx[sel] / W
        cy = math.atan2((S[sel] * np.sin(ty)).sum(), (S[sel] * np.cos(ty)).sum()) * H / (2 * np.pi) % H
        cx = math.atan2((S[sel] * np.sin(tx)).sum(), (S[sel] * np.cos(tx)).sum()) * W / (2 * np.pi) % W
        comps.append((m, cy, cx))
    return comps


# ------------------------------------------------------------------ 5. reproduction + supervenience
d0 = np.load(f"{INT}/data/A_gliders/base_000.npz")
b0 = np.load(f"{INT}/data/A_gliders/branch_000.npz")
seed = tuple(int(x) for x in d0["seed"])
spec = w.spec
h_init = np.asarray(spec.init(vw._rng(vw._S_INIT, *seed, 0)), float).reshape(1, -1)
ens = vw.Ensemble(w, h_init, spec.memory_init(h_init), seed, np.arange(1), 0)
H0 = [ens.h0[0].copy()]
M_ens = [ens.m[0].copy()]
mass = [ens.h0[0].reshape(C, -1).sum(1)]
T_AG = 61
for _ in range(spec.burn_in + T_AG):
    ens.step(None)
    H0.append(ens.h0[0].copy())
    M_ens.append(ens.m[0].copy())
    mass.append(ens.h0[0].reshape(C, -1).sum(1))
mass = np.array(mass)
res["mass_law"] = {"ticks": len(mass) - 1, "steps": 20 * (len(mass) - 1),
                   "max_rel_drift_per_channel": float(np.abs(mass / mass[0] - 1).max()),
                   "min_A": float(min(h.min() for h in H0))}
bi = spec.burn_in
yo_mine = [tr.phi(H0[bi + t][None], M_ens[bi + t][None])[0] for t in range(T_AG + 1)]
yc_mine = [my_coarse(H0[bi + t]) for t in range(T_AG + 1)]
res["reproduce_base_000"] = {
    "Yo_max_abs_diff_t0..61": float(np.abs(np.array(yo_mine) - d0["Yo"][:T_AG + 1]).max()),
    "Yc_mine_vs_saved_max_abs_diff": float(np.abs(np.array(yc_mine) - d0["Yc"][:T_AG + 1]).max()),
    "st_h0_t60_max_abs_diff": float(np.abs(H0[bi + 60] - d0["st_h0"][0]).max()),
    "st_m_t60_max_abs_diff": float(np.abs(M_ens[bi + 60] - d0["st_m"][0]).max()),
}
# replay the tracker from the h0 history alone
m = tr.memory_init(H0[0][None])
rep_diff = 0.0
for t in range(1, len(H0)):
    m = tr.memory_update(m, H0[t][None])
    rep_diff = max(rep_diff, float(np.abs(m[0] - M_ens[t]).max()))
res["supervenience"] = {"tracker_replayed_from_h0_history_max_abs_diff_m": rep_diff,
                        "phi_coarse_ignores_m": bool(np.array_equal(parts["phi_coarse"](H0[-1][None], None),
                                                                     parts["phi_coarse"](H0[-1][None], M_ens[-1][None]))),
                        "phi_objects_ignores_h_given_m": bool(np.array_equal(tr.phi(H0[-1][None], M_ens[-1][None]),
                                                                              tr.phi(np.zeros((1, l0.n0)), M_ens[-1][None])))}
# tracker has no hidden state: same inputs -> same output, object dict unchanged
before = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in tr.__dict__.items() if k != "l0"}
a1 = tr.update_one(M_ens[30], H0[31])
a2 = tr.update_one(M_ens[30], H0[31])
same_dict = all((np.array_equal(before[k], tr.__dict__[k]) if isinstance(before[k], np.ndarray) else before[k] == tr.__dict__[k])
                for k in before)
res["supervenience"]["update_one_deterministic"] = bool(np.array_equal(a1, a2))
res["supervenience"]["tracker_state_unchanged"] = bool(same_dict)
# my own components vs present slots
match = []
for t in range(bi, len(H0), 6):
    comps = my_components(H0[t], tr.blur, tr.thr, tr.m_min)
    T = tr.table(M_ens[t][None])[0]
    pres = T[T[:, 0] > 0.5]
    mine = np.sort([c[0] for c in comps])
    theirs = np.sort(pres[:, 1])
    ok = mine.size == theirs.size and np.allclose(mine, theirs, rtol=1e-9, atol=1e-9)
    cen_err = None
    if ok:
        # centroid via the torus embedding in h1 vs mine (match by mass)
        errs = []
        for c in comps:
            k = int(np.argmin(np.abs(pres[:, 1] - c[0])))
            cx = math.atan2(pres[k, 4], pres[k, 3]) * W / (2 * np.pi) % W
            cy = math.atan2(pres[k, 6], pres[k, 5]) * H / (2 * np.pi) % H
            errs.append(max(abs((cx - c[2] + W / 2) % W - W / 2), abs((cy - c[1] + H / 2) % H - H / 2)))
        cen_err = max(errs)
    match.append({"tick": t - bi, "n_mine": int(mine.size), "n_slots": int(theirs.size), "mass_match": bool(ok),
                  "centroid_max_err_px": cen_err})
res["phi_objects_vs_my_components"] = match
# one branch replicate bit for bit
e2 = vw.Ensemble(w, d0["st_h0"][0][None], d0["st_m"][0][None], (77, 202, 0, 0, 1), [0], int(d0["st_tick"][0]))
bd = []
for s in range(8):
    e2.step(None)
    bd.append(max(float(np.abs(e2.h1()[0] - b0["Yo"][0, 0, s]).max()),
                  float(np.abs(my_coarse(e2.h0[0]) - b0["Yc"][0, 0, s]).max())))
res["reproduce_branch_000_state0_rep1_8ticks_max_abs_diff"] = max(bd)
# replicate 0 = base continuation (identical noise)
e3 = vw.Ensemble(w, d0["st_h0"][0][None], d0["st_m"][0][None], seed, [0], int(d0["st_tick"][0]))
e3.step(None)
res["base_continuation_from_saved_state_t61_diff"] = float(np.abs(e3.h1()[0] - d0["Yo"][61]).max())

# ------------------------------------------------------------------ 1b. stress test of reintegration
rng = np.random.default_rng(11)
A = H0[-1].reshape(l0.shape)
m_before = A.reshape(C, -1).sum(1)
A2 = l0.substep(A, rng.standard_normal((2,) + l0.shape) * 200.0)   # flows far beyond the clip
res["mass_stress_flow_std_100"] = {"rel_err": float(np.abs(A2.reshape(C, -1).sum(1) / m_before - 1).max()),
                                   "min_A": float(A2.min())}

# ------------------------------------------------------------------ 2. kick under admissible inputs
Cn = spec.inputs
h = H0[-1][None].copy()
S = h[0].reshape(C, HW).sum(0)
body = np.flatnonzero(S > 0.05)
worst, minA, moved_max, n_ok = 0.0, np.inf, 0.0, 0
for it in range(400):
    if it % 2 == 0:
        a = Cn.sample(rng, w.n_in)                          # random cells
    else:                                                    # body-targeted, random amplitudes
        cells = rng.choice(body, 8, replace=False)
        v = rng.uniform(0.05, 1.0, 8) * np.repeat([-1, 1], 4)
        v[4:] *= -v[:4].sum() / v[4:].sum()
        v *= min(1.0, 4.0 / np.abs(v).sum(), 1.0 / np.abs(v).max())
        a = {int(inv[c]): float(x) for c, x in zip(cells, v)}
    if Cn.violations(a, 0, None, 0.0):
        continue
    n_ok += 1
    u = np.zeros((1, spec.n_u))
    u[0, w.in_map[list(a.keys())]] = list(a.values())
    hk = l0.kick(h, u)
    dm = np.abs(hk[0].reshape(C, HW).sum(1) - h[0].reshape(C, HW).sum(1)).max()
    worst = max(worst, float(dm))
    minA = min(minA, float(hk.min()))
    moved_max = max(moved_max, 0.5 * float(np.abs(hk - h).sum()))
res["kick_admissible"] = {"n_inputs": n_ok, "max_abs_mass_change_per_channel": worst, "min_A": minA,
                          "max_moved_mass": moved_max}

# ------------------------------------------------------------------ 3. constraint violations (agent API)
wa = vw.VectorWorld(specs["objects"], world_seed=0)
wa.reset(seed=5)
dz = wa.designer
bad = {
    "k=9": {i: (0.25 if i < 4 else -0.2) for i in range(9)},
    "value 1.5": {0: 1.5, 1: -1.5},
    "total 4.4": {i: (0.55 if i < 4 else -0.55) for i in range(8)},
    "non-zero sum": {0: 0.5, 1: -0.4},
    "nan": {0: float("nan"), 1: 0.0},
    "index n_in": {wa.n_in: 0.5, 0: -0.5},
    "string key": {"3": 0.5, 0: -0.5},
    "dense wrong shape": np.zeros(wa.n_in + 1),
}
viol = {}
for nm, a in bad.items():
    h_b, t_b, used_b = dz.state()["h0"].copy(), wa.t, wa.ticks_used
    try:
        wa.step(a)
        viol[nm] = "ACCEPTED"
    except vw.InputViolation as e:
        same = np.array_equal(h_b, dz.state()["h0"]) and wa.t == t_b and wa.ticks_used == used_b
        viol[nm] = ("rejected, nothing ran" if same else "rejected BUT STATE CHANGED") + ": " + str(e)[:90]
good = {int(inv[body[0]]): -0.5, int(inv[body[1]]): 0.5}
h_b, t_b, used_b = dz.state()["h0"].copy(), wa.t, wa.ticks_used
try:
    wa.run([(0, good), (1, good), (2, bad["k=9"])], query_times=[3])
    viol["run with bad 3rd entry"] = "ACCEPTED"
except vw.InputViolation as e:
    same = np.array_equal(h_b, dz.state()["h0"]) and wa.t == t_b and wa.ticks_used == used_b
    viol["run with bad 3rd entry"] = ("rejected, nothing ran" if same else "rejected BUT STATE CHANGED") + ": " + str(e)[:80]
res["violations"] = viol

# zero-sum tolerance loophole: check() allows |sum| <= 1e-9*max(1, l1); kick pools only if
# |sum| <= 1e-9*l1. For l1 < 1 the gap sends a near-zero-sum command down the 'designer probe'
# branch, which ADDS the positive part (split equally over channels) while sources on empty
# cells remove nothing.
empty = np.flatnonzero(dz.state()["h0"].reshape(C, HW).sum(0) < 1e-12)
src_c, snk_c = empty[0], empty[len(empty) // 2]
eps_cmd = {int(inv[snk_c]): 0.45, int(inv[src_c]): -0.45 + 9e-10}
v = np.array(list(eps_cmd.values()))
res_loop = {"command_sum": float(v.sum()), "l1": float(np.abs(v).sum()),
            "violations": Cn.violations(eps_cmd, 0, None, 0.0)}
m_b = dz.state()["h0"].reshape(C, HW).sum(1)
n_acc = 0
for _ in range(10):
    try:
        wa.step(eps_cmd)
        n_acc += 1
    except vw.InputViolation as e:
        res_loop["rejected"] = str(e)[:100]
        break
m_a = dz.state()["h0"].reshape(C, HW).sum(1)
res_loop.update({"accepted_ticks": n_acc, "mass_before": m_b.tolist(), "mass_after": m_a.tolist(),
                 "mass_created_total": float((m_a - m_b).sum())})
res["zero_sum_loophole"] = res_loop

# ------------------------------------------------------------------ 4. permutations and card
wb = vw.VectorWorld(specs["objects"], world_seed=1)
wc = vw.VectorWorld(specs["coarse"], world_seed=0)
o = wa.step(None)
h1 = dz.state()["h1"] if "h1" in dz.state() else wa._ep.h1()[0]
q = 1e-3 * np.round(wa._ep.h1()[0][wa.out_map] / 1e-3)
card = json.dumps(wa.card())
words = [x for x in ("slot", "mass", "centroid", "velocity", "present", "block", "channel", "x_cos", "glider",
                     "Flow-Lenia", "grid", "cell") if x.lower() in card.lower()]
res["permutation"] = {
    "obs_equals_quantised_h1_out_map": bool(np.array_equal(o, q)),
    "out_map_fixed_points": int((wa.out_map == np.arange(wa.n_obs)).sum()),
    "in_map_fixed_points": int((wa.in_map == np.arange(wa.n_in)).sum()),
    "seed0_vs_seed1_out_map_equal_frac": float((wa.out_map == wb.out_map).mean()),
    "objects_vs_coarse_in_map_equal_frac": float((wa.in_map == wc.in_map).mean()),
    "card_words_found": words,
    "card_notes": wa.card()["notes"],
}
res["cpu_seconds"] = time.time() - t_start
json.dump(vw.jsonable(res), open(OUT, "w"), indent=1, default=str)
print(json.dumps(vw.jsonable(res), indent=1, default=str)[:6000])
