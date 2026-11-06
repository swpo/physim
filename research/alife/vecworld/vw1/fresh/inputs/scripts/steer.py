"""(b) designer-aimed steering through the VW-1 InputPort, against the no-input twin.

usage: python -B steer.py NT NMAX       -> results/steer.npz, results/steer.json, results/steer_video_frames.npz

Targets: for each saved test state (results/states.npz) the isolated moving glider chosen by
run_steer.pick_target (VW-0 strategy code, read only) from the VW-1 tracker memory. Per target, one
block of 5 members sharing ONE noise key: twin (no input), flank+, flank-, lead+, lead-; plus one
null member (no input, block 0's state and key) for the twin-validity check. All blocks advance
together, one Ensemble.step call per tick (closed loop: each tick the steered member's cells come
from its own privileged state (x, m) via run_steer.program; values +-0.5, k = 8, sum|a| = 4, zero
sum), each command checked by the port (Admissible.normalize/check) and canonicalised.
Analysis: the formulas of integrate/analyze.steer_analysis (lateral offset, heading change over the
last 7 surviving ticks, signed so that + = toward the commanded side +n), on the VW-1 records."""
import json
import math
import sys
import time

import common as CM
import jax.numpy as jnp
import numpy as np

from vw.world import make_key, member_keys
import aworld as AW
import run_steer as RS      # VW-0 steering strategies (pick_target, program), read only

NT = int(sys.argv[1]) if len(sys.argv) > 1 else 40
NMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 16
STRATS = ["none", "flank+", "flank-", "lead+", "lead-"]
UID, CY = CM.NF + 4, CM.NF
t_all = time.time()
w, parts, _ = CM.build_world("both")
d = w.designer
C = w.inport.admissible
inv = AW.inverse_in_map(w)
tr = parts["tracker"]
l0g = tr.l0                      # geometry only (H, W, C, HW) for run_steer.program
st = np.load(f"{CM.RES}/states.npz")
X, M = st["x"], st["m"]
targets = []
for s in range(len(X)):
    _, tab = CM.mem_parts(M[s][None])
    tg = RS.pick_target(tab[0], CM.H, CM.W)
    if tg is not None:
        targets.append((s, int(tg)))
    if len(targets) >= NMAX:
        break
print("targets (state, slot):", targets, flush=True)
nb = len(targets)
B = 5 * nb + 1
kblock = member_keys(make_key(5151, 1), nb)
blk = np.r_[np.repeat(np.arange(nb), 5), 0]
keys = kblock[jnp.asarray(blk)]
sidx = [targets[i][0] for i in blk]
ens = d.from_states(jnp.asarray(X[sidx]), mem=(((), jnp.asarray(M[sidx])),), keys=keys)
tabs = np.zeros((B, NT + 1, CM.K, CM.NS))
L1 = np.zeros((B, NT + 1, 336), np.float32)
cells = -np.ones((B, NT, 8), int)
admissible = np.ones((B, NT), bool)
frames = np.zeros((B, NT + 1, 2, CM.H, CM.W), np.float16)     # in memory only
moved = np.zeros((B, NT))
x = np.asarray(ens.x)
m = CM.tracker_mem(ens)
tabs[:, 0] = CM.mem_parts(m)[1]
L1[:, 0] = ens.level(1)
frames[:, 0] = x
null_x = []
for k in range(NT):
    A = np.zeros((B, w.n_in))
    for b in range(B - 1):
        strat = STRATS[b % 5]
        if strat == "none":
            continue
        s_t = targets[b // 5][1]
        pr = RS.program(strat[:-1], 1 if strat.endswith("+") else -1, x[b].ravel(), m[b], s_t, l0g, tr)
        if pr is None:
            continue
        src, snk = pr
        a = {int(inv[c]): -0.5 for c in src}
        a.update({int(inv[c]): 0.5 for c in snk})
        a = C.normalize(a, w.n_in)
        if C.violations(a):
            admissible[b, k] = False
            continue
        C.check(a)
        for j, v in C.canonical(a).items():
            A[b, j] = v
        cells[b, k] = np.concatenate([src, snk])
        u = np.zeros(CM.HW)
        u[w.in_map] = A[b]
        moved[b, k] = CM.moved_matter(x[b].reshape(2, -1), u)
    ens = ens.step(A)
    x = np.asarray(ens.x)
    m = CM.tracker_mem(ens)
    tabs[:, k + 1] = CM.mem_parts(m)[1]
    L1[:, k + 1] = ens.level(1)
    frames[:, k + 1] = x
    null_x.append(float(np.abs(x[B - 1] - x[0]).max()))
    if (k + 1) % 5 == 0:
        print("tick", k + 1, round(time.time() - t_all, 1), "s", flush=True)
sim_s = time.time() - t_all
null_tab = float(np.abs(tabs[B - 1] - tabs[0]).max())


def unwrap(P, start):
    L = np.array([CM.H, CM.W])
    dd = np.vstack([CM.mi(P[0] - start, L)[None], CM.mi(np.diff(P, axis=0), L)])
    return np.cumsum(dd, 0)


rows = []
for i, (s0, s) in enumerate(targets):
    tb = tabs[5 * i]
    uid0 = tb[0, s, UID]
    v0 = tb[0, s, 10:12]
    u0 = v0 / max(np.linalg.norm(v0), 1e-9)
    n0 = np.array([-u0[1], u0[0]])
    for j, strat in enumerate(STRATS[1:], start=1):
        b = 5 * i + j
        ts = tabs[b]
        sign = 1 if strat.endswith("+") else -1
        al_s = [k for k in range(NT) if ts[k + 1, s, 0] > 0.5 and ts[k + 1, s, UID] == uid0]
        al_b = [k for k in range(NT) if tb[k + 1, s, 0] > 0.5 and tb[k + 1, s, UID] == uid0]
        kend = min(max(al_s) if al_s else -1, max(al_b) if al_b else -1)
        row = {"state": int(s0), "slot": int(s), "block": i, "member": int(b), "strategy": strat, "ticks": NT,
               "survived_ticks": int(kend + 1), "admissible_all": bool(admissible[b].all()),
               "steered_ticks": int((cells[b, :, 0] >= 0).sum()),
               "moved_per_steered_tick_median": float(np.median(moved[b][cells[b, :, 0] >= 0]))
               if (cells[b, :, 0] >= 0).any() else 0.0}
        if kend >= 7:
            start = tb[0, s, CY:CY + 2]
            Us = unwrap(ts[1:kend + 2, s, CY:CY + 2], start)
            Ub = unwrap(tb[1:kend + 2, s, CY:CY + 2], start)
            off = Us[-1] - Ub[-1]
            lat = off[1] * n0[0] + off[0] * n0[1]
            fwd = off[1] * u0[0] + off[0] * u0[1]
            ds, db = Us[-1] - Us[-8], Ub[-1] - Ub[-8]
            ang = math.degrees(math.atan2(ds[0], ds[1]) - math.atan2(db[0], db[1]))
            ang = (ang + 180) % 360 - 180
            row.update({"lateral_offset_px_signed": float(sign * lat), "forward_offset_px": float(fwd),
                        "heading_change_deg_signed": float(sign * ang), "twin_path_px": float(np.hypot(*Ub[-1])),
                        "mass_ratio_end": float(ts[kend + 1, s, 1] / tb[kend + 1, s, 1])})
        rows.append(row)


def summ(rr):
    if not rr:
        return None
    lat = np.array([x["lateral_offset_px_signed"] for x in rr])
    hd = np.array([x["heading_change_deg_signed"] for x in rr])
    mr = np.array([x["mass_ratio_end"] for x in rr])
    n = len(rr)
    fneg = float((hd < 0).mean())
    return {"n": n, "heading_change_median_deg_signed": float(np.median(hd)),
            "abs_heading_change_median_deg": float(np.median(np.abs(hd))),
            "frac_turn_toward_minus_n(source flank for 'flank')": fneg,
            "n_turn_toward_minus_n": int((hd < 0).sum()), "n_turn_toward_plus_n": int((hd > 0).sum()),
            "frac_se_binomial": float(math.sqrt(fneg * (1 - fneg) / n)),
            "lateral_median_px_signed": float(np.median(lat)), "frac_lateral_toward_minus_n": float((lat < 0).mean()),
            "survived_full_frac": float(np.mean([x["survived_ticks"] == x["ticks"] for x in rr])),
            "survived_ticks_median": float(np.median([x["survived_ticks"] for x in rr])),
            "twin_path_px_median": float(np.median([x["twin_path_px"] for x in rr])),
            "mass_within_5pct_frac": float((np.abs(mr - 1) <= 0.05).mean()),
            "mass_within_20pct_frac": float((np.abs(mr - 1) <= 0.2).mean())}


ok = [r for r in rows if "heading_change_deg_signed" in r]
summary = {k: summ([r for r in ok if r["strategy"].startswith(k)]) for k in ("flank+", "flank-", "lead+", "lead-",
                                                                             "flank", "lead")}
summary["all"] = summ(ok)
summary["n_targets"] = nb
summary["n_runs_total"] = len(rows)
summary["n_runs_dropped_identity_lost_within_7_ticks"] = len(rows) - len(ok)
summary["all_commands_admissible"] = bool(admissible.all())
summary["moved_per_steered_tick_median"] = float(np.median([r["moved_per_steered_tick_median"] for r in rows]))
summary["null_check_max_abs_x"] = float(max(null_x))
summary["null_check_max_abs_table"] = null_tab
summary["sim_seconds"] = sim_s
summary["members"] = B
summary["ticks"] = NT
# the video run: majority turning direction, survives >= 20 ticks, no tracker event and stable mass on the
# target in both twins, flank preferred, turn angle nearest the median |angle| of the majority
hd = np.array([r["heading_change_deg_signed"] for r in ok])
maj = -1 if (hd < 0).mean() >= 0.5 else 1
EVC = CM.NF + 3


def clean(r):
    """no tracker event on the target and target mass within 20% of its start, in both twins, while it survives"""
    ke, s_ = r["survived_ticks"], r["slot"]
    for tb_ in (tabs[5 * r["block"]], tabs[r["member"]]):
        if np.any(tb_[1:ke + 1, s_, EVC] != 0) or np.any(np.abs(tb_[1:ke + 1, s_, 1] / tb_[0, s_, 1] - 1) > 0.2):
            return False
    return True


for r in ok:
    r["clean_no_event_mass_within_20pct"] = bool(clean(r))
summary["all_clean_no_event_mass_within_20pct"] = summ([r for r in ok if r["clean_no_event_mass_within_20pct"]])
summary["all_with_event_or_mass_change"] = summ([r for r in ok if not r["clean_no_event_mass_within_20pct"]])
cand = [r for r in ok if np.sign(r["heading_change_deg_signed"]) == maj and r["survived_ticks"] >= 20 and r["clean_no_event_mass_within_20pct"]]
cand = cand or [r for r in ok if np.sign(r["heading_change_deg_signed"]) == maj and r["survived_ticks"] >= 20]
cand = cand or [r for r in ok if np.sign(r["heading_change_deg_signed"]) == maj]
medabs = np.median(np.abs(hd[np.sign(hd) == maj]))
cand.sort(key=lambda r: (not r["strategy"].startswith("flank"), abs(abs(r["heading_change_deg_signed"]) - medabs)))
vid = cand[0]
summary["video_run"] = vid
bt, bs = 5 * vid["block"], vid["member"]
np.savez_compressed(f"{CM.RES}/steer_video_frames.npz", twin=frames[bt].astype(np.float32),
                    steered=frames[bs].astype(np.float32), tab_twin=tabs[bt], tab_steered=tabs[bs],
                    L1_twin=L1[bt], L1_steered=L1[bs], cells=cells[bs], slot=vid["slot"], strategy=vid["strategy"],
                    state=vid["state"])
del frames
np.savez_compressed(f"{CM.RES}/steer.npz", targets=np.array(targets), strats=np.array(STRATS), tabs=tabs.astype(np.float32),
                    L1=L1, cells=cells, admissible=admissible, moved=moved, NT=NT)
json.dump({"summary": summary, "rows": rows}, open(f"{CM.RES}/steer.json", "w"), indent=1)
print(json.dumps(summary, indent=1), flush=True)
